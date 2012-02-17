import urllib

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class BasePage(webapp.RequestHandler):

    def get_current_user(self):
        return users.get_current_user()

    def check_user(self):
        user = self.get_current_user()
        if user:
            return True
        else:
            self.redirect(users.create_login_url(self.request.uri))
            return False

    def create_file(self, filename):
        file = File()
        file.author = self.get_current_user()
        file.name = filename
        key = file.put()
        self.redirect('/file?' + urllib.urlencode({'id': key}))
        return key
