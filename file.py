import cgi
import os
import urllib

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template

from models import File, Revision
from base import BasePage
import base

import HTMLParser

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

    def GetOutput(self):
#        if not self.check_user():
#            return

        file_id = self.request.get("id")
        file = self.get_file(file_id)
        if file is None:
            file = File()
            file.put()
        else:
            if self.get_file_permission(file) < base.ACCESS_READ:
                self.redirect('/')
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

        path = self.get_template_path( 'file.html' )
        return template.render(path, template_values)

    def get(self):
        self.response.out.write( self.GetOutput() )

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

        self.log_info("new_text = " + new_text)

        if self.has_text_changed(file, new_text):
            revision = Revision()
            revision.author     = self.get_current_user()
            revision.content    = new_text
            revision.file       = file
            revision.prev       = file.head
            revision.put()
            
            file.head = revision
            file.put()

        #self.redirect('/file?' + urllib.urlencode({'id': file_id}))
        #self.response.out.write(file_id)


class HtmlPage(FilePage):
    def get(self):
        self.response.headers['Content-Type'] = "text/html; charset=utf-8"
        h = HTMLParser.HTMLParser()
        val = h.unescape( self.GetOutput() )
        self.response.out.write(val)

class LastFile(FilePage):
    def get_public_file_id(self):
        return "not_defined"

    def get(self):
        if self.check_user(False):
            query = Revision.gql("WHERE author = :1 ORDER BY date DESC", self.get_current_user())
            revs = query.fetch(1)
            if len(revs) > 0:
                file_id = revs[0].file.key()
            else:
                file_id = self.create_file("New File")
        else:
                file_id = self.get_public_file_id()
        self.response.out.write(file_id)

class FileInfoPage(BasePage):
    def get(self):
        file_id = self.request.get("id")
        file = self.get_file(file_id)
        if file is None:
            file = File()
        else:
            if self.get_file_permission(file) < base.ACCESS_READ:
                file = File()
        template_values = {
            'file'   	: file
        }
        path = self.get_template_path( 'fileinfo.html' )
        self.response.out.write(template.render(path, template_values))
