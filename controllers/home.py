'''
Created on May 4, 2017

@author: ravishekhar
'''

from controllers.base import BaseHandler

class HomeHandler(BaseHandler):
    """
        Home page handler
    """
    def get(self):
        self.render_response('home.html')

