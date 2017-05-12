'''
Created on May 9, 2017

@author: ravishekhar
'''

from controllers.base import BaseHandler
from models.user import User
from models.post import Post
from models.comment import Comment

from google.appengine.ext import ndb
import logging


class CreateCommentHandler(BaseHandler):
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


class EditCommentHandler(BaseHandler):
    """
        handler for editing comment on post
    """

    def get(self, post_id, comment_id):
        # get post object
        post = Post.get_by_id(int(post_id))

        if not self.user:
            self.redirect('/blog/login')
            return
        
        # get comment object
        comment = Comment.get_by_id(int(comment_id))

        if comment:
            # comment author
            comment_user_id = comment.author_id.get().key.id()

            if comment_user_id == self.user.key.id():
                self.render_response('post_comment_edit.html',
                                 post=post, comment=comment)
            else:            
                # show flash msg that user can only edit own comment.
                self.session.add_flash('You can not edit others comment.', 'alert')
                self.redirect("/blog/%s" % post_id)
        else:
            self.session.add_flash('This comment can not be edited.', 'alert')
            self.redirect("/blog/%s" % post_id)

    def post(self, post_id, comment_id):

        # User login check
        if not self.user:
            self.redirect('/blog/login')
            return

        # get post object
        post = Post.get_by_id(int(post_id))

        # get comment object
        comment_to_edit = Comment.get_by_id(int(comment_id))

        # form validation
        # if not body: not working therefore isalnum() func used.
        # Needs to be checked in follow-up

        if post and comment_to_edit:
            
            # get the title and body from form
            body = self.request.get('body')

            # create a dict variable for sending back the body in case
            # there is an error
            params = dict(body=body)
        
            comment_user_id = comment_to_edit.author_id.get().key.id()

            if comment_user_id != self.user.key.id():
                self.session.add_flash('You can not edit others comment.', 'alert')
                self.redirect("/blog/%s" % post_id)

            elif not body or body.isspace():
                params['error_body'] = "That's not a valid comment."
                self.render_response('post_comment_edit.html',
                                 post=post, comment=comment_to_edit, **params)
            else:
                comment_to_edit.body = body
                comment_to_edit.put()
                self.session.add_flash(
                    'Your comment has been updated.', 'success')
                self.redirect('/blog/%s' % post_id, str(post_id))
                return
        else:
            self.session.add_flash('This comment can not be edited.', 'alert')
            self.redirect("/blog/%s" % post_id)

class DeleteCommentHandler(BaseHandler):
    """
        handler for deleting comment on post
    """

    def get(self, post_id, comment_id):
        
        if not self.user:
            self.redirect('/blog/login')
            return

        # get post object
        post = Post.get_by_id(int(post_id))

        # get comment object
        comment = Comment.get_by_id(int(comment_id))

        if post and comment:
            # comment author
            comment_user_id = comment.author_id.get().key.id()

            if comment_user_id == self.user.key.id():
                # if the logged in user is same as post author then
                # continue to delete the post

                # get comment position
                pos = post.comments.index(ndb.Key('Comment', int(comment_id)))
    
                # remove comment from comments list
                post.comments.pop(pos)  # Remove comment from comments list
    
                # update post on db
                post.put()

                # delete comment from db
                comment.key.delete()
                self.session.add_flash(
                    'Your comment has been deleted.', 'success')
                self.redirect("/blog/%s" % post_id)
            else:
                self.session.add_flash(
                    'You can not delete others comment.', 'warning')
                self.redirect("/blog/%s" % post_id)
        else:
            # show flash msg that user can only edit own comment.
            self.session.add_flash(
                'Can not delete comment at this time.', 'alert')
            self.redirect("/blog/%s" % post_id)
