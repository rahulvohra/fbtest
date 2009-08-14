from django.conf.urls.defaults import *

urlpatterns = patterns('fbsample.fbapp.views',
    (r'^$', 'index'),
    (r'^ideas/$', 'index'),
    url(r'^ideas/new/$', 'new_idea', name='new_idea'),
    # Define other pages you want to create here
)

