import cgi
import datetime
import urllib
import wsgiref.handlers

import os
from google.appengine.ext.webapp import template

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import diff_match_patch as dmp_module
dmp = dmp_module.diff_match_patch()
dmp.Diff_Timeout = 0.1  # Don't spend more than 0.1 seconds on a diff.


class File(db.Model):
  author = db.UserProperty()
  name = db.StringProperty()

class Revision(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  author = db.UserProperty()
  content = db.TextProperty()
  date = db.DateTimeProperty(auto_now_add=True)
  diff = db.TextProperty()
  file = db.ReferenceProperty(File)


def guestbook_key(guestbook_name=None):
  """Constructs a datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')



def distance (sx, sy):
  diffs = dmp.diff_main(sx, sy)
  dmp.diff_cleanupSemantic(diffs)
  return dmp.diff_prettyHtml(diffs)


class RevisionPage(webapp.RequestHandler):
  def show_revisions(self):
    guestbook_name=self.request.get('guestbook_name')
    file_id = self.request.get("file_id")
    user = users.get_current_user()

    key_object = db.Key(file_id)
    query = File.gql("WHERE __key__ = :1", key_object)
    entities = query.fetch(1)
    file = entities[0]

    #revisions = db.GqlQuery("SELECT * FROM Revision WHERE ANCESTOR IS :1 AND author = :2 ORDER BY date DESC LIMIT 50", guestbook_key(guestbook_name), user)
    revisions = db.GqlQuery("SELECT * FROM Revision WHERE file = :1 ORDER BY date DESC LIMIT 50", file)

    prev = ""
    last_text = ""
    revisions2 = []
    for revision in revisions:
        text = cgi.escape(revision.content)
        if len(prev) > 0:
            dist = distance(text, prev)
            #diff = dist.replace("\n", "<br>")
            diff = dist.replace("&para;", "")
            revision.diff = db.Text(diff)
            revisions2.append(revision)
        else:
            last_text = text
        prev = text

    template_values = {
      'user' : user,
      'file_id' : file_id,
      'revisions' : revisions2,
      'last_text' : last_text,
      'file_id' : file_id,
    }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
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
    guestbook_name = self.request.get('guestbook_name')
    revision = Revision(parent=guestbook_key(guestbook_name))

    #revision.author = users.get_current_user()
    revision.content = self.request.get('content')
    file_id = self.request.get("file_id")
    key_object = db.Key(file_id)
    query = File.gql("WHERE __key__ = :1", key_object)
    entities = query.fetch(1)
    revision.file = entities[0]
    revision.put()
    self.redirect('/file?' + urllib.urlencode({'file_id': file_id}))


class FilesPage(webapp.RequestHandler):
  def show_files(self):
    guestbook_name=self.request.get('guestbook_name')
    user = users.get_current_user()
    if not user:
      self.redirect(users.create_login_url(self.request.uri))
      return
    files = db.GqlQuery("SELECT * FROM File WHERE author = :1 LIMIT 50", user)
    if files.count() > 0:
#      template_values = {
#           'revisions' : files,
#      }
#      path = os.path.join(os.path.dirname(__file__), 'files.html')
#      self.response.out.write(template.render(path, template_values))
      self.redirect('/file?' + urllib.urlencode({'file_id': files[0].key()}))
    else:
      file_id = self.create_file("New File")
      self.redirect('/file?' + urllib.urlencode({'file_id': file_id}))

  def create_file(self, filename):
      guestbook_name = self.request.get('guestbook_name')
      file = File(parent=guestbook_key(guestbook_name))
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


application = webapp.WSGIApplication([
  ('/', FilesPage),
  ('/file', RevisionPage),
  ('/save', RevisionPage)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
