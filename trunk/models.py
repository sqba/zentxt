from google.appengine.ext import db

class File(db.Model):
    author = db.UserProperty()
    name = db.StringProperty()

class Revision(db.Model):
    author = db.UserProperty()
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    diff = db.TextProperty()
    file = db.ReferenceProperty(File)
