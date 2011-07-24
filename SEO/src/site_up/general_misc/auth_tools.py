'''Defines various auth-related tools.'''

import django.utils.decorators
import django.contrib.auth.decorators
from django.contrib import auth


def login_required(decorated=None,
                   redirect_field_name=auth.REDIRECT_FIELD_NAME,
                   login_url=None):
    '''
    View-decorator that ensures that the user is logged in.
    
    If the user is not logged it, he will get redirected to the login page, and
    only after he's logged in he'll get redirected back to the original page.
    '''
    def actual_decorator(decorated):
        function_decorator = django.contrib.auth.decorators.user_passes_test(
            lambda u: u.is_authenticated(),
            login_url=login_url,
            redirect_field_name=redirect_field_name
        )
        if issubclass(decorated, django.views.generic.View):
            
            decorated.dispatch = \
                django.utils.decorators.method_decorator(function_decorator)\
                                                        (decorated.dispatch)
            return decorated
        else:
            return function_decorator(decorated)
            
    if decorated:
        return actual_decorator(decorated)
    return actual_decorator
