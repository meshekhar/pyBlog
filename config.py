'''
Created on May 3, 2017

@author: ravishekhar

Module for configuring the jinja2 templates and sessions 

'''

import os
from utils.custom_filter import nl2br

__all__ = ['webapp2_config']

# Get current dir 
curr_path = os.path.abspath(os.path.dirname(__file__)) 

# Added template sub directories
blog_dir = os.path.join(curr_path, 'templates', 'blog')
user_dir = os.path.join(curr_path, 'templates', 'user')

# Empty config object
webapp2_config = {}

# jinja2 config settings
webapp2_config['webapp2_extras.jinja2'] = {
    'template_path': [os.path.join(curr_path, 'templates'), blog_dir, user_dir ],
    'environment_args': {'autoescape': True,},
    'filters':{'nl2br': nl2br}}

# sessions secret key
webapp2_config['webapp2_extras.sessions'] = {'secret_key': 'ansjds321n31b32b3k2#',}

