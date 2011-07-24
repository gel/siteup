'''Defines various exceptions.'''

class OutOfPurchasedSearches(Exception):
    '''
    The user tried to make a new search but he doesn't have enough credit.
    
    He could buy more if he wants to search..
    '''
