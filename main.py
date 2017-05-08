'''
Created on May 3, 2017

@author: ravishekhar

Blog Application Main module for setting the config and routes  

'''

import webapp2
import os
from config import webapp2_config
from routes import application_routes
import logging


curr_path = os.path.abspath(os.path.dirname(__file__)) 
templet_dir = os.path.join(curr_path, 'templates')


def handle_404(request, response, exception):
    logging.exception(exception)
    response.write('<h1>Oops! I could swear this page was here!</h1><br><h2><a href="/blog">Better Get back to safty</a></h2>')
    response.set_status(404)

def handle_500(request, response, exception):
    logging.exception(exception)
    response.write('<h1>Its our bad. I promiss it will not happen again ;)</h1><br><h2><a href="/blog">Better Get back to safty</a></h2>')
    response.set_status(500)

app = webapp2.WSGIApplication(routes=application_routes, config=webapp2_config, debug=True)

app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500