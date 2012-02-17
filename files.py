import urllib

from google.appengine.ext import db

from models import File
from base import BasePage

class FilesPage(BasePage):

    def show_files(self):
        files = db.GqlQuery("SELECT * FROM File WHERE author = :1 LIMIT 50", self.get_current_user())
        if files.count() > 0:
            self.redirect('/file?' + urllib.urlencode({'id': files[0].key()}))
        else:
            file_id = self.create_file("New File")
            self.redirect('/file?' + urllib.urlencode({'id': file_id}))

    def get(self):
        if not self.check_user():
            return
        self.show_files()

    def post(self):
        if not self.check_user():
            return
        #self.create_file()
