'''
Created on May 3, 2017

@author: ravishekhar

module for creating application routes

'''

from webapp2_extras.routes import RedirectRoute

__all__ = ['application_routes']

# Empty root list
application_routes = []


# list of all the routes
_route_info = [
  ('main',  'GET',  '/',      'controllers.home.HomeHandler'),
  ('login',   None,  '/blog/login', 'controllers.accountManager.LoginHandler'),
  ('logout',  None,  '/blog/logout', 'controllers.accountManager.LogoutHandler'),
  ('signup',  None,  '/blog/signup', 'controllers.accountManager.SignupHandler'),
  
  ('blog.show',  'GET',   r'/blog/<post_id:\d+>', 'controllers.blog.PostShowHandler'),
  ('blog.list',  'GET',   r'/blog', 'controllers.blog.PostListHandler'),
  ('blog.create',  None,  r'/blog/newpost', 'controllers.blog.PostCreateHandler'),
  ('blog.edit',  None,    r'/blog/<post_id:\d+>/edit', 'controllers.blog.PostEditHandler'),
  ('blog.delete',  None,  r'/blog/<post_id:\d+>/delete', 'controllers.blog.PostDeleteHandler'),
  
  ('blog.comment.create',  None,   r'/blog/<post_id:\d+>/comment/newcomment', 'controllers.comment.CreateCommentHandler'),
  ('blog.comment.update',  None,   r'/blog/<post_id:\d+>/comment/<comment_id:\d+>/update', 'controllers.comment.EditCommentHandler'),
  ('blog.comment.delete',  None,   r'/blog/<post_id:\d+>/comment/<comment_id:\d+>/delete', 'controllers.comment.DeleteCommentHandler'),
  
  ('blog.like',  None,   r'/blog/<post_id:\d+>/vote/<vote_val:(like|dislike)>', 'controllers.blog.PostLikeHandler')]

# create root object 
# using RedirectRoute Found at: webapp2_extras.routes

for name, methods, pattern, handler_cls in _route_info:
    # Allow a single string, but this has to be changed to a list.
    # None here means any method
    if isinstance(methods, basestring):
        methods = [methods]
    
    # Create the route
    route = RedirectRoute(name=name, 
                          methods=methods,
                          template=pattern,
                          handler=handler_cls,
                          strict_slash=True)

    # Add the route to the public list
    application_routes.append(route)
