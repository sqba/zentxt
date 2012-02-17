import cgi
import os
import urllib

from google.appengine.ext.webapp import template

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import File, Revision

import diff_match_patch as dmp_module


dmp = dmp_module.diff_match_patch()
dmp.Diff_Timeout = 0.1  # Don't spend more than 0.1 seconds on a diff.


def distance (sx, sy):
    diffs = dmp.diff_main(sx, sy)
    dmp.diff_cleanupSemantic(diffs)
    return dmp.diff_prettyHtml(diffs)


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
        text = revision.content

        q = Revision.all().filter('date >', revision.date)
        tmp = q.get()
        if tmp is None:
			return
        prev = tmp.content
            
        diff = distance(text, prev)
        diff = diff.replace("&para;", "")
        self.response.out.write(diff)

    def get(self):
        self.get_revision()
        
    def post(self):
        self.get_revision()
