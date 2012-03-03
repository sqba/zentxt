import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from home import HomePage, SuggestionsPage
from files import FilesPage, CreateNewFilePage, RenameFilePage
from file import FilePage, HtmlPage, LastFile, FileInfoPage
from revisions import RevisionsPage
from revision import RevisionPage


application = webapp.WSGIApplication([
    ('/', HomePage),
    ('/file', FilePage),
    ('/fileinfo', FileInfoPage),
    ('/last', LastFile),
    ('/html', HtmlPage),
    ('/save', FilePage),
    ('/files', FilesPage),
    ('/newfile', CreateNewFilePage),
    ('/rename', RenameFilePage),
    ('/revisions', RevisionsPage),
    ('/rev', RevisionPage),
    ('/revert', RevisionPage),
    ('/suggestions', SuggestionsPage)
], debug=True)


def main():
    run_wsgi_app(application)


if __name__ == '__main__':
    main()
