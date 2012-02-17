import datetime
import urllib
import wsgiref.handlers

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from files import FilesPage
from file import FilePage
from revision import RevisionPage


application = webapp.WSGIApplication([
  ('/', FilesPage),
  ('/file', FilePage),
  ('/save', FilePage),
  ('/rev', RevisionPage)
], debug=True)


def main():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()
