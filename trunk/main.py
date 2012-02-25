import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from home import HomePage, SuggestionsPage
from files import FilesPage, NewFilePage
from file import FilePage
from revisions import RevisionsPage
from revision import RevisionPage


application = webapp.WSGIApplication([
    ('/', HomePage),
    ('/file', FilePage),
    ('/save', FilePage),
    ('/files', FilesPage),
    ('/newfile', NewFilePage),
    ('/revisions', RevisionsPage),
    ('/rev', RevisionPage),
    ('/revert', RevisionPage),
    ('/suggestions', SuggestionsPage)
], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
