'''
Created on May 3, 2017

@author: ravishekhar
'''

from google.appengine.ext import ndb
from models.user import User


class Comment(ndb.Model):
    """
        Models an individual Comment entry.
    """
    body = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    
    # ID of commenting user.    
    author_id = ndb.KeyProperty(kind=User)
