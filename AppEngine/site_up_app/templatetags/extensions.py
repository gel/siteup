'''
Created on Jun 13, 2011

@author: GEL
'''

from django import template
register = template.Library()

def makeGoogleLink(query):
    query = query.replace(" ", "+",)
    return "http://www.google.com/search?q=" + query

@register.filter
def link(object):
    return '%s' % (makeGoogleLink(object))

@register.filter
def length(object):
    return len(object)
