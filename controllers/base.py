'''
Created on May 3, 2017

@author: ravishekhar

module contains  BaseHandler which inherits from webapp2.RequestHandler
'''
import webapp2
import logging

from webapp2_extras import sessions, jinja2
from models.user import User


class BaseHandler(webapp2.RequestHandler):
    """
        Class for handling jinja2 templates and entry point for the app
    """
    
    # initialize method for overriding the webapp2.RequestHandler.__init__() method.
    # attributes are current request, response and app objects
    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        
        
        uid = self.request.cookies.get('site_token')
        
        self.user = uid and User.by_id(int(uid))

        if not self.request.cookies.get('site_token') == None:
            self.user = User.checkToken(self.request.cookies.get('site_token'))
        else:
            self.user = None
    
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)


    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()
    
    
    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)


    def render_response(self, _template, **context):
        
        # Renders a template and writes the result to the response.
        # set logged in user to the session
        # set flash message
        ctx = {
            'user': self.user,
            'flash': self.session.get_flashes(),
            'session': self.session
        }
        ctx.update(context)
        rv = self.jinja2.render_template(_template, **ctx)
        
        self.response.write(rv)

    # method shows error (e.g. 404) when any of the classes inherited 
    # has error, such as wrong post id number which will pass the url 
    # regex test but will get a document 
    def handle_exception(self, exception, debug):
        # Log the error.
        logging.exception(exception)

        # Set a custom message.
        self.render_response('404.html')

        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
        else:
            self.response.set_status(500)
