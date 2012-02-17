import os
import urllib

from google.appengine.ext import db
from google.appengine.api import users

from models import File
from base import BasePage
import base

from google.appengine.ext.webapp import template

class FilesPage(BasePage):

    def show_files(self):
        self.response.out.write("show_files")
        files = db.GqlQuery("SELECT * FROM File WHERE author = :1 LIMIT 50", self.get_current_user())
        if files.count() > 0:
            self.redirect('/file?' + urllib.urlencode({'id': files[0].key()}))
        else:
            if self.check_user():
                file_id = self.create_file("New File")
            else:
                self.redirect('/home')

    def get(self):
#        if not self.check_user():
#            return
        self.show_files()

#    def post(self):
#        if not self.check_user():
#            return
        #self.create_file()

class HomePage(BasePage):
    def get(self):
        if self.check_user(False):
            self.redirect('/')
            return
        template_values = {
            'user'      : self.get_current_user(),
            'login_url' : users.create_login_url(self.request.uri)
        }
        path = os.path.join(os.path.dirname(__file__), 'home.html')
        self.response.out.write(template.render(path, template_values))

class SuggestionsPage(BasePage):
    def get(self):
        user = users.User(base.SUGGESTIONS_USER)
        files = db.GqlQuery("SELECT * FROM File WHERE author = :1 LIMIT 50", user)
        if files.count() > 0:
            file_id = files[0].key()
        else:
            file_id = self.create_file("Suggestions", user)
            #self.redirect('/file?' + urllib.urlencode({'id': file_id}))
        self.redirect('/file?' + urllib.urlencode({'id': file_id}))
