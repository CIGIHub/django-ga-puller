from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from django.conf import settings
import datetime
import httplib2
import importlib


class Command(BaseCommand):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    option_list = BaseCommand.option_list + (
        make_option('--year', '-y', dest='year',
                    default=yesterday.year,
                    help='Year of analytics data to pull'),
        make_option('--month', '-m', dest='start_month',
                    default=yesterday.month,
                    help='Month to start pulling analytics data for'),
        make_option('--day', '-d', dest='start_day',
                    default=yesterday.day,
                    help='Day to start pulling analytics data for'),
        make_option('--num_days', '-n', dest='num_days',
                    default=1,
                    help='Number of days to pull'),
        make_option('--app', '-a', dest='app',
                    help='Name of app to import data related to'),
        make_option('--key', '-k', dest='key',
                    default='private/privatekey.pem',
                    help='Location of the private key file'),
    )
    help = 'Imports analytics data'

    def handle(self, **options):
        start_year = int(options["year"])
        start_month = int(options["start_month"])
        start_day = int(options["start_day"])
        num_days = int(options["num_days"])
        app = options["app"]
        key_file_name = options["key"]
        verbosity = int(options["verbosity"])

        base_start_date = datetime.date(year=start_year, month=start_month, day=start_day)

        app_module = importlib.import_module(app)
        view_id = settings.VIEW_IDS[app]

        if 'analytics_import_models' not in app_module.__dict__:
            raise CommandError("Module must contain list 'analytics_import_models' defining the analytics data models.")

        for i in range(0, num_days):
            start_date = base_start_date + datetime.timedelta(days=i)

            for model in app_module.analytics_import_models:
                self._load_data(view_id, model, start_date=start_date,
                                key_file_name=key_file_name, verbosity=verbosity)

    @staticmethod
    def _load_data(view_id, data_model, start_date, key_file_name, verbosity=1):
        credentials = ServiceAccountCredentials.from_p12_keyfile(
            settings.SERVICE_ACCOUNT,
            key_file_name,
            scopes=['https://www.googleapis.com/auth/analytics.readonly']
        )
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build('analytics', 'v3', http=http)

        filters = data_model.get_filters()

        if filters:
            data_query = service.data().ga().get(
                ids='ga:%s' % view_id,
                metrics=data_model.get_metrics(),
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=start_date.strftime("%Y-%m-%d"),
                dimensions=data_model.get_dimensions(),
                sort=data_model.get_sort(),
                segment='gaid::-1',
                filters=filters,
                max_results=10000
            )
        else:
            data_query = service.data().ga().get(
                ids='ga:%s' % view_id,
                metrics=data_model.get_metrics(),
                start_date=start_date.strftime("%Y-%m-%d"),
                end_date=start_date.strftime("%Y-%m-%d"),
                dimensions=data_model.get_dimensions(),
                sort=data_model.get_sort(),
                segment='gaid::-1',
                max_results=10000
            )

        feed = data_query.execute()

        if 'rows' in feed:
            data_model.process_data(feed, start_date)
            if verbosity > 1: print("{} - {} - Processed data".format(start_date,
                                                                data_model.__name__))
        else:
            if verbosity > 1: print("{} - {} - No data available".format(start_date,
                                                                   data_model.__name__))
