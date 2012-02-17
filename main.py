import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from files import FilesPage, HomePage, SuggestionsPage
from file import FilePage
from revision import RevisionPage


application = webapp.WSGIApplication([
    ('/', FilesPage),
    ('/home', HomePage),
    ('/file', FilePage),
    ('/save', FilePage),
    ('/rev', RevisionPage),
    ('/revert', RevisionPage),
    ('/suggestions', SuggestionsPage)
], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
