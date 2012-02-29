import logging

from google.appengine.ext import db
from google.appengine.api import users

from models import File, FilePermissions

ACCESS_NONE     = 0
ACCESS_READ     = 1
ACCESS_WRITE    = 2
SUGGESTIONS_USER = "SUGGESTIONS"

def create_permission(file, user, access):
    perm = FilePermissions()
    perm._file = file
    perm.user = user
    perm.access = access
    perm.put();

def get_file_permission(file, user):
    query = FilePermissions.gql("WHERE _file = :1 AND user = :2", file, user)
    entities = query.fetch(1)
    if len(entities) > 0:
        return entities[0].access
    else:
        user = users.User(SUGGESTIONS_USER)
        query = FilePermissions.gql("WHERE _file = :1 AND user = :2", file, user)
        entities = query.fetch(1)
        if len(entities) > 0:
            return entities[0].access
        else:
#            self.log_info("file permission denied")
#            self.response.out.write("file permission denied")
            return ACCESS_NONE
