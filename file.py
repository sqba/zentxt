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


class FilePage(webapp.RequestHandler):
  def show_revisions(self):
#    guestbook_name=self.request.get('guestbook_name')
    file_id = self.request.get("file_id")
    user = users.get_current_user()

    last_text = ""
    revisions2 = []

    key_object = db.Key(file_id)
    query = File.gql("WHERE __key__ = :1", key_object)
    entities = query.fetch(1)
    if len(entities) > 0:
        file = entities[0]
    else:
        file = File()
        file.put()

    #revisions = db.GqlQuery("SELECT * FROM Revision WHERE ANCESTOR IS :1 AND author = :2 ORDER BY date DESC LIMIT 50", guestbook_key(guestbook_name), user)
    #revisions = db.GqlQuery("SELECT * FROM Revision WHERE file = :1 ORDER BY date DESC LIMIT 50", file)

    query = Revision.gql("WHERE file = :1 ORDER BY date DESC", file)
    revisions = query.fetch(1)
    if len(revisions) > 0:
        last_text = cgi.escape(revisions[0].content)
        last_date = revisions[0].date

        query = Revision.gql("WHERE file = :1 and date < :2 ORDER BY date DESC", file, last_date)
        revisions = query.fetch(100)
    else:
        last_text = "Welcome to ZenTxt!"
        revisions = []

    template_values = {
      'user' : user,
      'file_id' : file_id,
      'revisions' : revisions,
      'last_text' : last_text,
      'file_id' : file_id,
    }

    path = os.path.join(os.path.dirname(__file__), 'file.html')
    self.response.out.write(template.render(path, template_values))

  def get(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
    else:
      self.show_revisions()

  def post(self):
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      return
    # We set the same parent key on the 'Revision' to ensure each revision is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.
#    guestbook_name = self.request.get('guestbook_name')
    revision = Revision()

    #revision.author = users.get_current_user()
    revision.content = self.request.get('content')
    file_id = self.request.get("file_id")
    key_object = db.Key(file_id)
    query = File.gql("WHERE __key__ = :1", key_object)
    entities = query.fetch(1)
    revision.file = entities[0]
    revision.put()
    self.redirect('/file?' + urllib.urlencode({'file_id': file_id}))
