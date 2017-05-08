'''
Created on Apr 30, 2017

@author: ravishekhar
'''

from google.appengine.ext import ndb
from models.user import User

class Vote(ndb.Model):
    
    """Model for voting on a post."""

    # Vating type up or down
    type = ndb.StringProperty()

    # Voting date and time
    votingDate = ndb.DateTimeProperty(auto_now=True)
    
    # Voter ID
    voter_id = ndb.KeyProperty(kind=User)
