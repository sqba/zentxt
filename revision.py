import cgi
import os
import urllib

from google.appengine.ext.webapp import template

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import File, Revision

from diff import distance


class RevisionPage(webapp.RequestHandler):

    def get_revision(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
            return

        rev_id = self.request.get("rev_id")
        key_object = db.Key(rev_id)
        query = Revision.gql("WHERE __key__ = :1", key_object)
        entities = query.fetch(1)
        revision = entities[0]
        text = cgi.escape(revision.content)
        
        #self.response.out.write(text)
        #return

        q = Revision.all().filter('date >', revision.date)
        tmp = q.get()
        if tmp is None:
			return
        prev = cgi.escape(tmp.content)
            
        if len(text) > 0:
            diff = distance(text, prev)
            #diff = diff.replace("\n", "<br>")
            diff = diff.replace("&para;", "")
            #diff = diff.replace("<br>", "\n")
            self.response.out.write(diff)

    def get(self):
        self.get_revision()
        
    def post(self):
        self.get_revision()
