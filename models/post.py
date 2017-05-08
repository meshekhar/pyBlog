'''
Created on May 1, 2017

@author: ravishekhar
'''

from google.appengine.ext import ndb
from models.user import User
from models.vote import Vote
from models.comment import Comment


class Post(ndb.Model):
    """
    Models an individual Post entry with title, content and date.
        
    """
    title = ndb.StringProperty(required=True)
    body = ndb.TextProperty(required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)
    
    # ID of post user.    
    author_id = ndb.KeyProperty(kind=User)

    # Post votes.
    likes = ndb.IntegerProperty(default=0)
    
    # Post voter data.
    voters = ndb.StructuredProperty(Vote, repeated=True)

    # Post voter data.
    comments = ndb.KeyProperty(kind=Comment, repeated=True)

    @classmethod
    def query_post(cls, post_id):        
        return cls.get_by_id(int(post_id))
