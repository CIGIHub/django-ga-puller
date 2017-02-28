from django.db import models


class DailyEventTrackingBase(models.Model):
    date = models.DateField()
    category = models.CharField(max_length=50)
    action = models.CharField(max_length=20)
    label = models.CharField(max_length=2048)
    total_events = models.PositiveIntegerField(null=True)
    unique_events = models.PositiveIntegerField(null=True)
    data_sampled = models.NullBooleanField(null=True)

    def __unicode__(self):
        return "%s: %s - %s - %s - %s - %s - %s" % (self.date, self.category, self.action, self.label,
                                                    self.total_events, self.unique_events, self.data_sampled)

    class Meta:
        abstract = True

    @staticmethod
    def get_metrics():
        return 'ga:totalEvents,ga:uniqueEvents'

    @staticmethod
    def get_dimensions():
        return 'ga:eventAction,ga:pagePath,ga:eventCategory,ga:eventLabel'

    @staticmethod
    def get_filters():
        return 'ga:pagePath!~^/search/*;ga:pagePath!~^/404.html*;ga:pagePath!@?page=;ga:eventAction==PDF,ga:eventAction==DOC,ga:eventAction==Click'

    @staticmethod
    def get_sort():
        return "-ga:totalEvents"

    @classmethod
    def get_page_class(cls):
        raise NotImplementedError()

    @classmethod
    def process_data(cls, data, date):
        data_sampled = data["containsSampledData"]
        for action, page_path, category, label, total_events, unique_events in data["rows"]:
            page, created = cls.get_page_class().objects.get_or_create(page_path=page_path)
            data, created = cls.objects.get_or_create(date=date, page=page, category=category, action=action,
                                                      label=label)
            data.total_events = total_events
            data.unique_events = unique_events
            data.data_sampled = data_sampled
            data.save()


class DailyPageTrackingBase(models.Model):
    date = models.DateField()
    visit_bounce_rate = models.FloatField(null=True)
    average_time_on_page = models.FloatField(null=True)
    exit_rate = models.FloatField(null=True)
    page_views = models.PositiveIntegerField(null=True)
    exits = models.PositiveIntegerField(null=True)
    time_on_page = models.FloatField(null=True)
    unique_page_views = models.PositiveIntegerField(null=True)
    data_sampled = models.NullBooleanField(null=True)

    def __unicode__(self):
        return "%s: %s - %s - %s - %s - %s - %s" % (self.date, self.visit_bounce_rate, self.average_time_on_page,
                                                    self.exit_rate, self.page_views, self.unique_page_views,
                                                    self.data_sampled)

    class Meta:
        abstract = True

    @staticmethod
    def get_metrics():
        return 'ga:visitBounceRate,ga:pageviews,ga:uniquePageviews,ga:avgTimeOnPage,ga:exitRate,ga:exits,ga:timeOnPage'

    @staticmethod
    def get_dimensions():
        return 'ga:pagePath'

    @staticmethod
    def get_filters():
        return 'ga:pagePath!~^/search/*;ga:pagePath!~^/404.html*;ga:pagePath!@?page='

    @staticmethod
    def get_sort():
        return "-ga:pageviews"

    @classmethod
    def get_page_class(cls):
        raise NotImplementedError()

    @classmethod
    def process_data(cls, data, date):
        data_sampled = data["containsSampledData"]
        for page_path, visit_bounce_rate, page_views, unique_page_views, avg_time_on_page, exit_rate, exits, time_on_page in data["rows"]:
            page, created = cls.get_page_class().objects.get_or_create(page_path=page_path)
            data, created = cls.objects.get_or_create(date=date, page=page)
            data.visit_bounce_rate = visit_bounce_rate
            data.average_time_on_page = avg_time_on_page
            data.exit_rate = exit_rate
            data.page_views = page_views
            data.exits = exits
            data.time_on_page = time_on_page
            data.unique_page_views = unique_page_views
            data.data_sampled = data_sampled
            data.save()


class AnalyticsPage(models.Model):
    page_path = models.CharField(max_length=2048)

    class Meta:
        abstract = True


class DailyVisitorTrackingBase(models.Model):
    date = models.DateField()
    sessions = models.PositiveIntegerField(null=True)
    users = models.PositiveIntegerField(null=True)
    average_session_duration= models.FloatField(null=True)
    bounce_rate = models.FloatField(null=True)
    data_sampled = models.NullBooleanField(null=True)

    def __unicode__(self):
        return "{}: {} - {} - {} - {}".format(
            self.date,
            self.sessions,
            self.users,
            self.average_session_duration,
            self.data_sampled
        )

    class Meta:
        abstract = True

    @staticmethod
    def get_metrics():
        return 'ga:sessions,ga:users,ga:avgSessionDuration,ga:bounceRate'
    @staticmethod
    def get_dimensions():
        return ''

    @staticmethod
    def get_filters():
        return 'ga:pagePath!~^/404.html*'

    @staticmethod
    def get_sort():
        return 'ga:sessions'

    @classmethod
    def get_page_class(cls):
        raise NotImplementedError()

    @classmethod
    def process_data(cls, data, date):
        data_sampled = data["containsSampledData"]
        for sessions, users, average_session_duration, bounce_rate in data['rows']:
            data, created = cls.objects.get_or_create(date=date)
            data.sessions = sessions
            data.users = users
            data.average_session_duration = average_session_duration
            data.bounce_rate = bounce_rate
            data.data_sampled = data_sampled
            data.save()

