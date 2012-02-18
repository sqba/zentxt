import urllib

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import File, Revision, FilePermissions

ACCESS_NONE     = 0
ACCESS_READ     = 1
ACCESS_WRITE    = 2
SUGGESTIONS_USER = "SUGGESTIONS"

class BasePage(webapp.RequestHandler):

    def get_current_user(self):
        return users.get_current_user()

    def check_user(self, redirect=True):
        user = self.get_current_user()
        if user:
            return True
        else:
            if redirect:
                self.redirect(users.create_login_url(self.request.uri))
            return False

    def create_permission(self, file, user, access):
        perm = FilePermissions()
        perm._file = file
        perm.user = user
        perm.access = access
        perm.put();

    def get_file_permission(self, file):
        query = FilePermissions.gql("WHERE _file = :1 AND user = :2", file, self.get_current_user())
        entities = query.fetch(1)
        if len(entities) > 0:
            return entities[0].access
        else:
            user = users.User(SUGGESTIONS_USER)
            query = FilePermissions.gql("WHERE _file = :1 AND user = :2", file, user)
            entities = query.fetch(1)
            if len(entities) > 0:
                return entities[0].access
            else:
                self.response.out.write("file permission denied")
                return ACCESS_NONE

    def create_file(self, filename, user=None):
        file = File()
        if user is None:
            user = self.get_current_user()
        file.author = user
        file.name = filename
        key = file.put()
        self.create_permission(file, file.author, ACCESS_WRITE)
        self.redirect('/file?' + urllib.urlencode({'id': key}))
        return key

    def get_file(self, id):
        query = File.gql("WHERE __key__ = :1", db.Key(id))
        entities = query.fetch(1)
        if len(entities) > 0:
            file = entities[0]
            #if self.get_file_permission(file):
            return file
        return None

    def get_revision_by_id(self, id):
        rev_key = db.Key(id)
        query = Revision.gql("WHERE __key__ = :1", db.Key(id))
        entities = query.fetch(1)
        if len(entities) > 0:
            rev = entities[0]
            return rev
        return None