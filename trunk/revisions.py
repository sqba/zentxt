import os
import urllib

from google.appengine.ext import db
from google.appengine.api import users

from models import File, Revision
from base import BasePage
import base

from google.appengine.ext.webapp import template


class RevisionsPage(BasePage):

    def get_revisions(self, file):
        try:
            query = Revision.gql("WHERE file = :1 ORDER BY date DESC", file)
            #.filter('__key__ != :1', file.head.key())
            return query.fetch(100)
        except: #BadKeyError:
            return None

    def get(self):
        file_id = self.request.get("file")
        file = self.get_file(file_id)
        if file is None:
            self.response.out.write("File not found")
            return
        if self.get_file_permission(file) < base.ACCESS_READ:
            self.redirect('/')
            return

        head = file.head
        if head is None:
            revisions = []
        else:
            revisions = self.get_revisions(file)

        template_values = {
            'user'      : self.get_current_user(),
            'file_id'   : file_id,
            'revisions' : revisions,
            'login_url' : users.create_login_url(self.request.uri)
        }

        path = self.get_template_path( 'revisions.html' )
        self.response.out.write(template.render(path, template_values))

