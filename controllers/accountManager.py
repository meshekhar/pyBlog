'''
Created on May 3, 2017

@author: ravishekhar

Module handles the login, logout and registration

'''

from controllers.base import BaseHandler
from models.user import User
from models.post import Post
from utils import validate as vl


# login check decorator
def login_required(func):
    
    def decorated(*args, **kwargs):
        if args[0].request.method != 'GET':
            args[0].abort(400,
                        detail='The login_required decorator '
                               'can only be used for GET requests.')
        if not args[0].user:
            args[0].redirect("/blog/login")
        return func(*args, **kwargs)

    return decorated


# post author check decorator
def isAuthor(func):
    
    def decorated(*args, **kwargs):

        post = Post.get_by_id(int(kwargs.get('post_id')))
        post_user_id = post.author_id.get().key.id()
        
        if post_user_id != args[0].user.key.id():
            args[0].redirect("/blog/%s" % kwargs.get('post_id'))
        return func(*args, **kwargs)

    return decorated

class LoginHandler(BaseHandler):
    """
        login handler class
        if user not login then it will render login page
        otherwise redirected to home page 
    """
    def get(self):
        if not self.user:
            self.render_response('login.html')
        else:
            self.redirect('/home')
    
    # login post method
    # user input are validated and checked agained the database
    # 
    def post(self):
        
        if not self.user:
            params = dict(login_error="login error")
        
            username = self.request.get('username')
            password = self.request.get('password')
            
            if not username and not password:
                self.render_response('login.html', **params)
                return
            
            user = User.query(User.username == username).get()
            
            if not user:
                self.render_response('login.html', **params)
                return
            
            
            # check if the username and password match with existing record
            # if not then http 403 forbidden error set and redirect to the login page
            # else user object set, cookie added, and flash msg to on welcome page
            if not User.checkPassword(user.password, password):
                self.error(403)
                self.render_response('login.html', **params)            
            else:
                self.user = user
                self.response.set_cookie('site_token', str(self.user.key.id()))
                self.session.add_flash('Welcome back %s' %username, 'success')                
                self.redirect('/blog')    


class LogoutHandler(BaseHandler):
    """ Logout handler """
    # delete cookie
    # and flash msg that user is loged out
    
    def get(self):
        self.response.delete_cookie('site_token')
        self.session.add_flash('Your are succesfuly logged out!', 'success')
        self.user = None
        self.redirect('/')
        

class SignupHandler(BaseHandler):
    '''
        handles user registration function
    '''

    # show registration page if user not logged in
    # otherwise redirected to the blog page
    def get(self):
        if self.user:
            self.session.add_flash('Your are allready login in!', 'warning')
            self.redirect('/blog')
        else:
            self.render_response('signup.html')
    
    
    def post(self):
        have_error = False
        
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username=username, email=email)
        
        # do form validation 
        if not vl.valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not vl.valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not vl.valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        # if error the render signup form with params
        if have_error:
            self.render_response('signup.html', **params)
        else:
            # check for if username exits
            user = User.query(User.username == username).get()
            
            if user:
                # username exist error
                params['username_exist_error'] = "Username already taken, please choose a different one"
                self.render_response('signup.html', **params)
            else:
                # everything pass
                # proceed with creating user object and insert to NDB
                u = User()
                u.username = username
                u.email = email
                u.password = u.setPassword(password)                
                u.put()
                
                # set site cookie
                self.response.set_cookie('site_token', str(u.key.id()))
                
                # show falsh welcome message
                self.session.add_flash("Thankyou for signup %s" %username, level='success', key='_flash')
                
                # redirect to the blog page
                self.redirect('/blog')