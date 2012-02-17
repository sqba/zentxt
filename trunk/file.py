import cgi
import os
import urllib

from google.appengine.ext.webapp import template

from google.appengine.ext import db

from models import File, Revision
from base import BasePage

class FilePage(BasePage):

    def get_file(self, id):
        key_object = db.Key(id)
        query = File.gql("WHERE __key__ = :1", key_object)
        entities = query.fetch(1)
        if len(entities) > 0:
            return entities[0]
        else:
            return None

    def get_head(self, file):
        query = Revision.gql("WHERE file = :1 ORDER BY date DESC", file)
        revisions = query.fetch(1)
        if len(revisions) > 0:
            return revisions[0]
        else:
            return None

    def get_revisions(self, rev):
        query = Revision.gql("WHERE file = :1 and date < :2 ORDER BY date DESC", rev.file, rev.date)
        return query.fetch(100)

    def show_revisions(self):
        file_id = self.request.get("id")

        file = self.get_file(file_id)
        if file is None:
            file = File()
            file.put()

        head = self.get_head(file)
        if head is None:
            file_text = "Welcome to ZenTxt!"
            revisions = []
        else:
            file_text = cgi.escape(head.content)
            revisions = self.get_revisions(head)

        template_values = {
            'user'      : self.get_current_user(),
            'file_id'   : file_id,
            'revisions' : revisions,
            'file_text' : file_text
        }

        path = os.path.join(os.path.dirname(__file__), 'file.html')
        self.response.out.write(template.render(path, template_values))

    def has_text_changed(self, file, text):
        head = self.get_head( file )
        if not head is None:
            return (text != head.content)
        else:
            return True

    def get(self):
        if not self.check_user():
            return
        self.show_revisions()

    def post(self):
        if not self.check_user():
            return

        file_id = self.request.get("id")
        file = self.get_file( file_id )
        new_text = self.request.get('content')

        if self.has_text_changed(file, new_text):
            revision = Revision()
            revision.author     = self.get_current_user()
            revision.content    = new_text
            revision.file       = file
            revision.put()

        self.redirect('/file?' + urllib.urlencode({'id': file_id}))
