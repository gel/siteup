from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('site_up_app.urls')),
)