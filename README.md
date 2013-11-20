django-ga-puller
================

Django app used to pull daily Google Analytics data into your django database. It provides abstract models which you should
inherit from in your app.

To Use
------

In your app,

Create models that inherit from the abstract classes provided.  Here is a sample of a basic implementation:

    from ga_puller.models import AnalyticsPage, DailyEventTrackingBase, DailyPageTrackingBase

    class Page(AnalyticsPage):

        def __unicode__(self):
            return "%s" % self.page_path


    class DailyEventData(DailyEventTrackingBase):
    
        page = models.ForeignKey('Page')
        
        @classmethod
        def get_page_class(cls):
            return Page


    class DailyPageTrackingData(DailyPageTrackingBase):
    
        page = models.ForeignKey('Page')
        
        @classmethod
        def get_page_class(cls):
            return Page


Add a list named analytics_import_models defining the data models to the __init__.py of your app module:

    from models import DailyPageTrackingData, DailyEventData
    analytics_import_models = [DailyPageTrackingData, DailyEventData]
