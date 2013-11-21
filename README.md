django-ga-puller
================

Django app used to pull daily Google Analytics data into your django database. It provides abstract models which you should
inherit from in your app.

To Use
------

Add the app to your settings.py file:

    INSTALLED_APPS = [...
                      'ga_puller',
                      ...]
                      
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
    

Create a 'private' python package at the root level of your django project (at the same level as the manage.py file).

The application requires a service account for authentication with Google.  These can be configured by logging into your account at https://cloud.google.com.

Copy your Google API private key file to the private directory (name it privatekey.pem). 

Create a python file named 'accounts.py' in the private directory with the following code (update with your account data):
 
    service_account = 'xxxxxx@developer.gserviceaccount.com'
    view_ids = {'app_name': '#########', ...}


This package uses [Google APIs Client Library for Python](https://developers.google.com/api-client-library/python/) which should automatically be installed through setup.


Release Notes:

0.1.0: Initial Release
0.1.1: Updated to support importing from separate views in google analytics.
