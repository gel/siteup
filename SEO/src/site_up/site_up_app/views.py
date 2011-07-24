import django.views.generic

from general_misc import auth_tools

from . import models
from .algorithm import algorithm
from django import http
from django.core.urlresolvers import reverse

@auth_tools.login_required
class SearchView(django.views.generic.TemplateView):
    template_name = 'search.html'
    
    def post(self, request, **kwargs):
        """ run the search algorithm """
        
        profile = request.user.get_profile()
        if profile.n_purchased_searches <= 0:
            return http.HttpResponseRedirect(reverse('not-enough-searches'))        
        profile.n_purchased_searches -= 1
        profile.save()
        
        query = request.POST['query']
        search_quality = request.POST['SearchQuality']
        search_iterations = int(request.POST['SearchIterations'])
        '''
        switch statement in python
        '''
        search_time = {
          'Very Fast': lambda : 30,
          'Fast'     : lambda : 90,
          'Normal'   : lambda : 300,
          'Good'     : lambda : 900,
          'Very Good': lambda : 1800
        }[search_quality]()
        
        result = algorithm(query, search_time, search_iterations)
        search = models.Search(user=request.user, query=query, result=result, type=search_quality, iterations=search_iterations)
        search.save()

        context = self.get_context_data(**kwargs)
        context['remaining_searches'] = profile.n_purchased_searches
        context['search'] = search
        return self.render_to_response(context)
        
    def get_context_data(self, **kwargs):
        """ got remaining searches counter for the user """
        
        context_data = super(SearchView, self).get_context_data(**kwargs)

        profile = self.request.user.get_profile()
        context_data['remaining_searches'] = profile.n_purchased_searches
        
        return context_data
 
  
@auth_tools.login_required
class HomeView(django.views.generic.TemplateView):
    template_name = 'home.html'
 
    def get_context_data(self, **kwargs):
        """ show all past searches """
        context_data = super(HomeView, self).get_context_data(**kwargs)
        
        existing_searches = \
            models.Search.objects.filter(user=self.request.user).order_by('-datetime_created')
        context_data['existing_searches'] = existing_searches
        context_data['index_searches'] = range(1,1+len(existing_searches))
        return context_data


@auth_tools.login_required
class BuyView(django.views.generic.TemplateView):
    template_name = 'account-Buy_searches.html'
    
    def post(self, request, **kwargs):
        """ "buy" new searches  """
        searches_num = request.POST['searches_num']
        
        profile = request.user.get_profile()        
        profile.n_purchased_searches += int(searches_num)
        profile.save()

        context = self.get_context_data(**kwargs)
        context['action_results'] = searches_num
        return self.render_to_response(context)

@auth_tools.login_required
class PaymentSettingsView(django.views.generic.TemplateView):
    template_name = 'account-Payment_setting.html'
    
    def post(self, request, **kwargs):
        print "Hello!"
        payment_method = request.POST['payment_method']
        
        print payment_method
        profile = request.user.get_profile()
        profile.preferred_payment_method = payment_method
        print profile
        profile.save()
        

        context = self.get_context_data(**kwargs)
        context['action_results'] = payment_method
        return self.render_to_response(context)
    
@auth_tools.login_required
class UpdateDetailsView(django.views.generic.TemplateView):
    template_name = 'account-Account_details.html'
    
    def post(self, request, **kwargs):
        """ update user's account details  """
        context = self.get_context_data(**kwargs)
        
        new_email = request.POST['new_email']
        if new_email:
            if not django.contrib.auth.models.User.objects.filter(email=new_email):
                request.user.email = new_email
                context['email_results_str'] = 'Your updated email has saved!'
                context['user_email'] = new_email
            else:
                context['email_results_str'] = 'This email is already exists!'
        
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']
        if old_password or new_password1 or new_password2:
            if not old_password or not new_password1 or not new_password2:
                context['password_results_str'] = 'Missing fields!'
            elif new_password1 != new_password2:
                context['password_results_str'] = 'New password fields don\'t match!'
            elif not request.user.check_password(old_password):
                context['password_results_str'] = ''
            else:
                request.user.set_password(new_password1)
                context['password_results_str'] = 'Your updated password has saved!'
        
        request.user.save()
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        """ show user's account details """
        context_data = super(UpdateDetailsView, self).get_context_data(**kwargs)
        profile = self.request.user.get_profile()
        
        context_data['user_name'] = self.request.user.username
        context_data['user_email'] = self.request.user.email
        context_data['user_preferred_payment_method'] = profile.preferred_payment_method
        return context_data

