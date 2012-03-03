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

        max_results = int(self.request.get("max"))
        if max_results is None:
            max_results = 10

        query = File.gql("WHERE author = :1", self.get_current_user())
        files = query.fetch(max_results);

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

class CreateNewFilePage(BasePage):
    def post(self):
        file_name = self.request.get('name')
        self.log_info("NewFilePage " + file_name)
        file_id = self.create_file(file_name)
        self.response.out.write(file_id)

class RenameFilePage(BasePage):
    def post(self):
        file_name = self.request.get('name')
        self.log_info("RenameFilePage " + file_name)
        file_id = self.request.get("id")
        file = self.get_file(file_id)
        if file is None:
            self.response.out.write("File not found")
            return
        file.name = file_name
        file.put()
        self.response.out.write(file_id)
