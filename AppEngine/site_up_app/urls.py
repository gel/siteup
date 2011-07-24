import django.contrib.auth.views
from django.conf.urls.defaults import patterns, url
from django.views.generic import TemplateView as tv

import registration.views

from . import views
from . import forms

urlpatterns = patterns('',
                       
    url(r'^$', django.contrib.auth.views.login,
        {'template_name': 'login.html'}, name='login'),
        
    url(r'^logout/$', 'django.contrib.auth.views.logout', {} , name='logout'),
        
    url(r'^faq/$', tv.as_view(template_name='faq.html'),
    name='faq'),
    
    url(r'^info/$', tv.as_view(template_name='info.html'),
    name='info'),

    ### Defining account-related urls: ########################################
    #                                                                         #
    
    url(r'^account/$', tv.as_view(template_name='account.html'),
        name='account'),
        
    url(r'^home/$', views.HomeView.as_view(),
        name='home'),

    url(r'^search/$', views.SearchView.as_view(),
        name='search'),
    
    url(r'^not-enough-searches/$', tv.as_view(template_name='not-enough-searches.html'),
        name='not-enough-searches'),
    
    url(r'^account-Buy_searches/$', views.BuyView.as_view(),
        name='account-Buy_searches'),
    
    url(r'^account-Payment_setting/$', views.PaymentSettingsView.as_view(),
        name='account-Payment_setting'),
    
    url(r'^account-Account_details/$', views.UpdateDetailsView.as_view(),
        name='account-Account_details'),
    
    url(r'^account-Delete_searches/$', tv.as_view(template_name='account-Delete_searches.html'),
        name='account-Delete_searches'),
        
    #                                                                         #
    ### Finished defining account-related urls. ###############################
    
    ### Defining registration-related urls: ###################################
    #                                                                         #
    url(r'^sign-up/$',
        registration.views.register,
        {'template_name': 'sign-up.html',
         'form_class': forms.RegistrationForm,
         'success_url': '/waiting-for-activation/'},
        name='sign-up'),
    
    url(r'^waiting-for-activation/$', tv.as_view(template_name='waiting-for-activation.html'),
        name='waiting-for-activation'),
    
    url(r'^activate-account/(?P<activation_key>\w+)$', registration.views.activate,
        name='activate-account'),
    #                                                                         #
    ### Finished defining registration-related urls. ##########################
    
)
