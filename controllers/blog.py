"""
Created on Apr 22, 2017

@author: ravishekhar

=====================
Blog classes for udacity blog project.
"""
from controllers.base import BaseHandler
from models.user import User
from models.post import Post
from models.comment import Comment

from controllers.accountManager import login_required
from google.appengine.ext import ndb
from models.vote import Vote


class BlogHandler(BaseHandler):
    
    def get(self):
        self.render_response('layout.html')


class PostCreateHandler(BaseHandler):
    """
    handler for creating new post
    """
    
    @login_required
    def get(self):
        self.render_response('post_form.html')
    

    def post(self):
        
        # additional check for user login
        if not self.user:
            self.redirect("/blog/login")
        else:
            # get the title and body from form
            title = self.request.get('subject')
            body = self.request.get('content')
            
            # create a dict variable for sending back the title 
            # and body in case there is an error            
            params = dict(title=title, body=body)
            
            # form validation
            if not title:
                params['error_title'] = "That's not a valid title."
                self.render_response('post_form.html', **params)
            elif not body:
                params['error_body'] = "That's not a valid body."
                self.render_response('post_form.html', **params)
            else:
                # Get user key
                u_key = ndb.Key(User, self.user.key.id())
                
                # create post object
                p = Post(title=title, body=body, author_id=u_key)
                
                # put returns a key
                post_key = p.put()
                
                post_id = post_key.id()
                
                self.redirect('/blog/%s' % post_id, str(post_id))


class PostEditHandler(BaseHandler):
    """
    handler for edting a post
    """

    def get(self, post_id):
        
        # initialize user object
        user = None
        if self.request.cookies.get('site_token'):
            # call checktoken method to get the user object
            user = User.checkToken(self.request.cookies.get('site_token'))
        
        # get post object
        post = Post.get_by_id(int(post_id))
        
        # get post author id
        post_user_id = post.author_id.get().key.id()
        
        # if user logged in
        if not user:
            self.redirect("/blog/login")
        
        # check if logged in user is same as post author 
        # and render edit form
        elif post_user_id == self.user.key.id():
            post = Post.query_post(post_id)
            self.render_response('post_edit.html', post=post)
        else:
            # show flash msg that user can only edit own post.
            self.session.add_flash('You can not edit others post.', 'alert')
            self.redirect("/blog/%s" % post_id)
    
    def post(self, post_id):
        
        # get the title and body from form
        title = self.request.get('title')
        body = self.request.get('body')
        
        # create a dict variable for sending back the title 
        # and body in case there is an error
        params = dict(title=title, body=body)
        
        # form validation
        if not title:
            params['error_title'] = "That's not a valid title."
            self.render_response('post_form.html', **params)
        elif not body:
            params['error_body'] = "That's not a valid body."
            self.render_response('post_form.html', **params)
        else:
            
            # update the post object and put
            post_to_edit = Post.get_by_id(int(post_id))  # or ndb.Key(Job, job_id).get()
            post_to_edit.title = title
            post_to_edit.body = body
            post_to_edit.put()
            self.session.add_flash('Your post has been updated.', 'success')
            self.redirect('/blog/%s' % post_id, str(post_id))


class PostDeleteHandler(BaseHandler):
    """
        handler for deleting a post
    """
    # @ndb.transactional(xg=True)    
    def get(self, post_id):
        
        post = Post.get_by_id(int(post_id))
        post_user_id = post.author_id.get().key.id()
        
        if not self.user:
            self.redirect("/blog/login")
        elif post_user_id == self.user.key.id():
            # if the logged in user is same as post author then 
            # continue to delete the post
            post.key.delete()
            self.session.add_flash('Your post has been deleted.', 'success')
            self.redirect('/blog')
        else:
            self.session.add_flash('You can not delete others post.', 'alert')
            self.redirect("/blog/%s" % post_id)


class PostShowHandler(BaseHandler):
    """
        handler for showing individual post page
    """    
    def get(self, post_id, **params):
        post = Post.query_post(post_id)        
        self.render_response('post_show.html', post = post, **params)          

class PostListHandler(BaseHandler):
    """
        handler for showing post list page
    """
    def get(self):
        # posts = Post.all()
        posts = Post.query().fetch(10)
        self.render_response('post_list.html', posts=posts)          


class PostCommentHandler(BaseHandler):
    """
        handler for adding comment on post
    """
    def post(self, post_id):
        
        u_key = None
        
        if not self.user:
            self.redirect('/blog/login')
            return
        else:
            # Get the logged in user reference key
            u_key = ndb.Key(User, self.user.key.id())
        
        body = self.request.get('body')
        
        # Retrive the post object 
        post = Post.query_post(post_id)
        
        params = dict()
        if not body:
            # if body empty then respond with error msg
            params['error'] = "Comment can not be empty."
            self.render_response('post_show.html', post=post, **params)
        else:
            # create a comment object
            new_comment = Comment(body=body, author_id=u_key)
            
            # add comment abject to the database
            comment_key = new_comment.put()
            
            # append comment key to the post object
            post.comments.append(comment_key)
            
            # put the post abject to the databse
            post.put()            
            self.redirect('/blog/%s' % post_id)   


class PostLikeHandler(BaseHandler):
    """
        handler for post like and dislike
    """

    def get(self, post_id, vote_val):
        
        if not self.user:
            self.redirect('/blog/login')
            return
        # Get the logged in user reference key
        u_key = ndb.Key(User, self.user.key.id())
        
        # Retrive the post object 
        post = Post.query_post(post_id)
        
        # Get post user ID
        post_user_id = post.author_id.get().key.id()
        
        # Post author can not vote for its own post
        if self.user.key.id() == post_user_id:            
            self.session.add_flash('You can not vote your own post.', 'warning')
            self.redirect(self.request.referer)
            return
        else:
            # check if the user is already voted
            for voter in post.voters:
                if voter.voter_id.get().key.id() == self.user.key.id():
                    # if found then msg the user that multiple vote not allowed
                    self.session.add_flash('You have already voted!!!!', 'warning')
                    self.redirect('/blog/%s' % post_id)
                    return
            if vote_val == 'like':
                # for like add 1 to the vote count
                post.likes += 1
                post.voters.append(Vote(type = 'like', voter_id=u_key))
                post.put()
                
            elif vote_val == 'dislike' and post.likes > 0:
                # for dislike substract 1 from the vote count
                post.likes -= 1
                post.voters.append(Vote(type = 'dislike', voter_id=u_key))
                post.put()
            else: 
                post.likes += 0

        # params = dict(error="can not do it")
        self.redirect('/blog/%s' % post_id)   
