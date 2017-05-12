'''
Created on May 3, 2017

@author: ravishekhar

module contains  BaseHandler which inherits from webapp2.RequestHandler
'''

import webapp2
import logging
from utils.udhash import hash_str, check_hash_strg

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

        uid = self.read_secure_cookie('site_token')

        self.user = uid and User.by_id(int(uid))

        #======================================================================
        # if not self.request.cookies.get('site_token') == None:
        #     self.user = User.checkToken(self.request.cookies.get('site_token'))
        # else:
        #     self.user = None
        #======================================================================

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

    # sets a cookie whose name is name and value is val
    def set_secure_cookie(self, name, val):
        cookie_val = hash_str(val)
        # expire time not set so it expires when
        # when you close the browser.
        # set the cookie on Path / so we can delete on same path
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        # find the cookie in the request
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_hash_strg(cookie_val)

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
