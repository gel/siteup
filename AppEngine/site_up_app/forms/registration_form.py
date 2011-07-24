'''
Defines the `RegistrationForm` class.

See its documentation for more info.
'''

import django.contrib.auth.models
import registration.forms
import registration.models

import site_up_app.models
#from site_up.settings import SEND_EMAIL_VERIFICATION
SEND_EMAIL_VERIFICATION=False

class ProfileCreator(object):
    '''Callable that creates a profile for a new user.'''
    def __init__(self, preferred_payment_method):
        '''
        Construct the `ProfileCreator`.
        
        `preferred_payment_method` is the user's preferred payment method which
        will be saved in his profile. It is one of the choices in
        `site_up_app.models.UserProfile.PAYMENT_METHOD_CHOICES`.
        '''
        self.preferred_payment_method = preferred_payment_method
        
    def __call__(self, user):
        '''Construct a `UserProfile` for `user`.'''
        assert isinstance(user, django.contrib.auth.models.User)
        user_profile = site_up_app.models.UserProfile(
            user=user,
            preferred_payment_method=self.preferred_payment_method
        )
        user_profile.save()
        return user_profile


class RegistrationForm(registration.forms.RegistrationFormUniqueEmail):
    '''Form for registering a new user to SiteUp.'''

    ### Tweaking fields from original `registration`: #########################
    #                                                                         #
    username = django.forms.RegexField(
        regex=r'^\w+$',
        max_length=30,
        widget=django.forms.TextInput(
            attrs=registration.forms.attrs_dict
        ),
        label=u'Username',
        help_text=u'Insert only alphanumeric characters.'
    )
    email = django.forms.EmailField(
        widget=django.forms.TextInput(
            attrs=dict(registration.forms.attrs_dict, maxlength=75)
        ),
        label=u'Email address',
        help_text=u'Please give us a valid email. A notification email will '
                  u'be sent to this address.'
        
    )
    password1 = django.forms.CharField(
        widget=django.forms.PasswordInput(
            attrs=registration.forms.attrs_dict,
            render_value=False
        ),
        label=u'Password',
        help_text=u'For your protection please choose a strong password. A '
                  u'strong password is at least 16 characters long and '
                  u'contains a mix of letters, numbers, and symbols.'
    )
    password2 = django.forms.CharField(
        widget=django.forms.PasswordInput(
            attrs=registration.forms.attrs_dict,
            render_value=False
        ),
        label=u'Repeat password'
    )
    #                                                                         #
    ### Finished tweaking fields from original `registration`. ################
    
    
    preferred_payment_method = django.forms.ChoiceField(
        choices=site_up_app.models.UserProfile.PAYMENT_METHOD_CHOICES,
    )
        
    
    def save(self, profile_callback=None):
        '''
        Create the new `User` and `RegistrationProfile`, and return the `User`.
        '''
        new_user = registration.models.RegistrationProfile.\
                   objects.create_inactive_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email'],
            profile_callback=ProfileCreator(
                self.cleaned_data['preferred_payment_method']
            ),
            send_email=SEND_EMAIL_VERIFICATION
        )
        '''
        TODO - fix Email issue
        '''
        if not SEND_EMAIL_VERIFICATION:
            new_user.is_active = True
            new_user.save()
        
        return new_user
    