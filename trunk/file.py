import cgi
import os
import urllib

from google.appengine.ext.webapp import template

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import File, Revision


class FilePage(webapp.RequestHandler):

    def show_revisions(self):
        file_id = self.request.get("id")
        user = users.get_current_user()

        file_text = ""
        revisions2 = []

        key_object = db.Key(file_id)
        query = File.gql("WHERE __key__ = :1", key_object)
        entities = query.fetch(1)
        if len(entities) > 0:
            file = entities[0]
        else:
            file = File()
            file.put()

        query = Revision.gql("WHERE file = :1 ORDER BY date DESC", file)
        revisions = query.fetch(1)
        if len(revisions) > 0:
            file_text = cgi.escape(revisions[0].content)
            last_date = revisions[0].date

            query = Revision.gql("WHERE file = :1 and date < :2 ORDER BY date DESC", file, last_date)
            revisions = query.fetch(100)
        else:
            file_text = "Welcome to ZenTxt!"
            revisions = []

        template_values = {
            'user' : user,
            'file_id' : file_id,
            'revisions' : revisions,
            'file_text' : file_text
        }

        path = os.path.join(os.path.dirname(__file__), 'file.html')
        self.response.out.write(template.render(path, template_values))

    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return
        self.show_revisions()

    def post(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return

        revision = Revision()

        #revision.author = users.get_current_user()
        revision.content = self.request.get('content')
        file_id = self.request.get("id")
        key_object = db.Key(file_id)
        query = File.gql("WHERE __key__ = :1", key_object)
        entities = query.fetch(1)
        revision.file = entities[0]

        # Avoid saving same text
        query = Revision.gql("WHERE file = :1 ORDER BY date DESC", revision.file)
        revisions = query.fetch(1)
        if len(revisions) > 0:
            last_text = revisions[0].content
            if revision.content != last_text:
                revision.put()

        self.redirect('/file?' + urllib.urlencode({'id': file_id}))
