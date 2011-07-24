from django.conf.urls.defaults import *

handler500 = 'djangotoolbox.errorviews.server_error'
'''
('^$', 'django.views.generic.simple.direct_to_template',
     {'template': 'home.html'}),
'''
urlpatterns = patterns('',
    ('^_ah/warmup$', 'djangoappengine.views.warmup'),
    url(r'^', include('site_up_app.urls')),
	
)
