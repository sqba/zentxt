import os
import urllib

from google.appengine.ext import db
from google.appengine.api import users

from models import File, Revision
from base import BasePage
import base

from google.appengine.ext.webapp import template


class FilesPage(BasePage):

    def get(self):
        if not self.check_user(False):
            #self.logged_user_home()
            self.redirect('/')
            return

        query = File.gql("WHERE author = :1", self.get_current_user())
        files = query.fetch(50);

        if len(files) > 0:
            head = files[0].head
        else:
            head = Revision()

        user = users.User(base.SUGGESTIONS_USER)
        query = File.gql("WHERE author = :1", user)
        public_files = query.fetch(50);
        files = files + public_files

        template_values = {
            'user'      : self.get_current_user(),
            'files'   	: files,
            'head'      : head,
            'login_url' : users.create_login_url(self.request.uri)
        }

        path = self.get_template_path( 'files.html' )
        self.response.out.write(template.render(path, template_values))

class NewFilePage(BasePage):
    def post(self):
        file_name = self.request.get('name')
        self.create_file(file_name);

