from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from private.accounts import service_account, view_id
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
                    help='Name of app to import data related to')
    )
    help = 'Imports analytics data'

    def handle(self, **options):
        start_year = int(options["year"])
        start_month = int(options["start_month"])
        start_day = int(options["start_day"])
        num_days = int(options["num_days"])
        app = options['app']

        base_start_date = datetime.date(year=start_year, month=start_month, day=start_day)

        app_module = importlib.import_module(app)
        if not 'analytics_import_models'  in app_module.__dict__:
            raise CommandError("Module must contain list 'analytics_import_models' defining the analytics data models.")

        for i in range(0, num_days):
            start_date = base_start_date + datetime.timedelta(days=i)

            for model in app_module.analytics_import_models:
                self._load_data(model, start_date=start_date)

    @staticmethod
    def _load_data(data_model, start_date):
        f = file('private/privatekey.pem', 'rb')
        key = f.read()
        f.close()
        credentials = SignedJwtAssertionCredentials(service_account,
                                                    key,
                                                    scope='https://www.googleapis.com/auth/analytics.readonly')
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build('analytics', 'v3', http=http)
        data_query = service.data().ga().get(ids='ga:%s' % view_id,
                                             metrics=data_model.get_metrics(),
                                             start_date=start_date.strftime("%Y-%m-%d"),
                                             end_date=start_date.strftime("%Y-%m-%d"),
                                             dimensions=data_model.get_dimensions(),
                                             sort=data_model.get_sort(),
                                             segment='gaid::-1',
                                             filters=data_model.get_filters(),
                                             max_results=10000)
        feed = data_query.execute()

        if 'rows' in feed:
            data_model.process_data(feed, start_date)
            print "%s - %s - Processed data" % (start_date, data_model.__name__)
        else:
            print "%s - %s - No data available" % (start_date, data_model.__name__)