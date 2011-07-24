'''Defines database models.'''

import django.db.models
import django.contrib.auth.models


class UserProfile(django.db.models.Model):
    '''Profile for a `SiteUp` user.'''
    
    PAYMENT_METHOD_CHOICES = (
        ('Paypal', 'Paypal'),
        ('Credit card', 'Credit card'),
    )
    preferred_payment_method = django.db.models.CharField(
        choices=PAYMENT_METHOD_CHOICES,
        max_length=30,
        help_text='The method in which the user pays for searches.'
    )
    
    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        related_name='user_profile',
    )
    
    
    n_purchased_searches = django.db.models.PositiveIntegerField(
        default=10,
        help_text='The number of searches that the user has credit to do.'
    )
            
            
class Search(django.db.models.Model):
    '''A search for recommended keywords, carried out by a user.'''
    
    user = django.db.models.ForeignKey(
        django.contrib.auth.models.User,
        help_text='The user that made this search.',
        related_name='searches'
    )
    
    query = django.db.models.TextField(
        help_text="Text that describes what the user's site is about."
    )
    
    result = django.db.models.TextField(
        help_text="Keyword list that the user should use to promote his site."
    )
    
    datetime_created = django.db.models.DateTimeField(
        auto_now_add=True,
        help_text='The datetime in which the search was created.'
    )
    
    type= django.db.models.TextField(
        help_text="Search type of the search selected."
    )

    iterations= django.db.models.TextField(
        help_text="Search iterations of the search selected."
    )

    def getResultList(self):
        return self.result.split('\n')

    def getGoogleOrQuery(self):
        query = ""
        for res in self.result.split('\n'):
            query += res + " | "
        query = query.rstrip(' | ')
        return query
    
    def getGoogleImagesLink(self):
        query = self.getGoogleOrQuery()
        return "http://www.google.co.il/search?q=%s&hl=en&client=firefox-a&hs=P3Z&rls=org.mozilla:en-US:official&prmd=ivns&biw=1440&bih=757&um=1&ie=UTF-8&tbm=isch&source=og&sa=N&tab=wi" % query
    
    def getGoogleVideosLink(self):
        query = self.getGoogleOrQuery()
        return "http://www.google.co.il/search?q=%s&hl=en&client=firefox-a&rls=org.mozilla:en-US:official&prmdo=1&tbm=vid&prmd=ivns&source=lnms&ei=4uX4TdbgGsjRtAa6wdmACQ&sa=X&oi=mode_link&ct=mode&cd=3&ved=0CC0Q_AUoAg&biw=1440&bih=786" % query
    
    def getGoogleBlogsLink(self):
        query = self.getGoogleOrQuery()
        return "http://www.google.co.il/search?q=%s&hl=en&client=firefox-a&rls=org.mozilla:en-US:official&biw=1440&bih=786&tbm=blg&prmd=ivns&source=lnms&ei=7Ob4Tda7C8yKswaa5dCKCQ&sa=X&oi=mode_link&ct=mode&cd=6&ved=0CB4Q_AUoBQ&prmdo=1" % query

    def getGoogleDiscussionsLink(self):
        query = self.getGoogleOrQuery()
        return "http://www.google.co.il/search?q=%s&hl=en&client=firefox-a&rls=org.mozilla:en-US:official&prmdo=1&tbm=dsc&prmd=ivns&source=lnms&ei=f-f4Tby8LYfFtAbs38WKCQ&sa=X&oi=mode_link&ct=mode&ved=0CBgQ_AU&biw=1440&bih=786" % query
        