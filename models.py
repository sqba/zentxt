from google.appengine.ext import db

class Revision(db.Model):
    author = db.UserProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    content = db.TextProperty()
#    diff = db.TextProperty()
#    file = db.ReferenceProperty(File)
    file = db.ReferenceProperty(collection_name='file')
    prev = db.SelfReferenceProperty()

class File(db.Model):
    author = db.UserProperty()
    name = db.StringProperty()
    head = db.ReferenceProperty(Revision)
