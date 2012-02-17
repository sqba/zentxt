import urllib

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import File


class FilesPage(webapp.RequestHandler):

    def show_files(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        files = db.GqlQuery("SELECT * FROM File WHERE author = :1 LIMIT 50", user)
        if files.count() > 0:
            self.redirect('/file?' + urllib.urlencode({'file_id': files[0].key()}))
        else:
            file_id = self.create_file("New File")
            self.redirect('/file?' + urllib.urlencode({'file_id': file_id}))

    def create_file(self, filename):
        guestbook_name = self.request.get('guestbook_name')
        file = File()
        file.author = users.get_current_user()
        file.name = filename
        key = file.put()
        self.redirect('/file?' + urllib.urlencode({'file_id': key}))
        return key

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.show_files()

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
