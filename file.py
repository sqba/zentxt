import cgi
import os
import urllib

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template

from models import File, Revision
from base import BasePage
import base

class FilePage(BasePage):

    def get_revisions(self, file):
        query = Revision.gql("WHERE file = :1 ORDER BY date DESC", file)
        #.filter('__key__ != :1', file.head.key())
        return query.fetch(100)

    def has_text_changed(self, file, text):
        head = file.head
        if not head is None:
            return (text != head.content)
        else:
            return True

    def get(self):
#        if not self.check_user():
#            return

        file_id = self.request.get("id")
        file = self.get_file(file_id)
        if file is None:
            file = File()
            file.put()
        else:
            if self.get_file_permission(file) < base.ACCESS_READ:
                return

        head = file.head
        if head is None:
            file_text = "Welcome to ZenTxt!"
            revisions = []
        else:
            file_text = cgi.escape(head.content)
            revisions = self.get_revisions(file)

        template_values = {
            'user'      : self.get_current_user(),
            'file_id'   : file_id,
            'revisions' : revisions,
            'file_text' : file_text,
            'login_url' : users.create_login_url(self.request.uri)
        }

        path = os.path.join(os.path.dirname(__file__), 'file.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
#        if not self.check_user():
#            return

        file_id = self.request.get("id")
        file = self.get_file( file_id )
        if file is None:
            self.response.out.write(file_id + " not found")
            return

        if self.get_file_permission(file) < base.ACCESS_WRITE:
            self.response.out.write("permission denied")
            return

        new_text = self.request.get('content')

        if self.has_text_changed(file, new_text):
            revision = Revision()
            revision.author     = self.get_current_user()
            revision.content    = new_text
            revision.file       = file
            revision.prev       = file.head
            revision.put()
            
            file.head = revision
            file.put()

        self.redirect('/file?' + urllib.urlencode({'id': file_id}))
