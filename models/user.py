'''
Created on April 28, 2017

@author: ravishekhar
'''

from google.appengine.ext import ndb
import hashlib      


class User(ndb.Model):

    """
        Model for representing an user.
    """
    username = ndb.StringProperty(required=True)
    password = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

    @staticmethod
    def checkToken(token):
        return User.get_by_id(long(token))

    
    # Password hashing
    def setPassword(self, password):
        return hashlib.md5(password).hexdigest()

    
    # checks the user entered password vs database hashed password
    @staticmethod
    def checkPassword(password, form_password):
        if not form_password:
            return False        
        return password == hashlib.md5(form_password).hexdigest()

        return False


    @classmethod
    # cls refers to self, which here is Class User
    def by_id(cls, uid):
        # get_by_id is a Datastore fxn
        return cls.get_by_id(uid)
