import os
import urllib

from google.appengine.ext import db
from google.appengine.api import users

from models import File
from base import BasePage
import base

from google.appengine.ext.webapp import template


class HomePage(BasePage):

    def logged_user_home(self):
        files = db.GqlQuery("SELECT * FROM File WHERE author = :1 LIMIT 50", self.get_current_user())
        if files.count() > 0:
            file_id = files[0].key()
        else:
            file_id = self.create_file("New File")
        self.redirect('/file?' + urllib.urlencode({'id': files[0].key()}))

    def anon_user_page(self):
        template_values = {
            'user'      : self.get_current_user(),
            'login_url' : users.create_login_url(self.request.uri)
        }
        path = os.path.join(os.path.dirname(__file__), 'home.html')
        self.response.out.write(template.render(path, template_values))

    def get(self):
        if self.check_user(False):
            self.logged_user_home()
        else:
            self.anon_user_page()

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
