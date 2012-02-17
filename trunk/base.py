import urllib

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import File, Revision


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

    def get_file(self, id):
        query = File.gql("WHERE __key__ = :1 AND author = :2", db.Key(id), self.get_current_user())
        entities = query.fetch(1)
        if len(entities) > 0:
            return entities[0]
        else:
            return None

    def get_revision_by_id(self, id):
        rev_key = db.Key(id)
        query = Revision.gql("WHERE __key__ = :1 AND author = :2", db.Key(id), self.get_current_user())
        entities = query.fetch(1)
        if len(entities) == 0:
            return None
        return entities[0]
