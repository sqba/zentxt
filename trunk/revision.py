from google.appengine.ext import db

from models import File, Revision
from base import BasePage

import diff_match_patch as dmp_module


dmp = dmp_module.diff_match_patch()
dmp.Diff_Timeout = 0.1  # Don't spend more than 0.1 seconds on a diff.


def distance (sx, sy):
    diffs = dmp.diff_main(sx, sy)
    dmp.diff_cleanupSemantic(diffs)
    return dmp.diff_prettyHtml(diffs)


class RevisionPage(BasePage):

    def get_revision_by_id(self, id):
        rev_key = db.Key(id)
        query = Revision.gql("WHERE __key__ = :1", rev_key)
        entities = query.fetch(1)
        if len(entities) == 0:
            return None
        return entities[0]

    def get_previous_revision(self, rev):
        q = Revision.all().filter('date >', rev.date)
        prev = q.get()
        return prev

    def get(self):
        if not self.check_user():
            return

        rev = self.get_revision_by_id( self.request.get("id") )
        if rev is None:
            return

        prev = self.get_previous_revision( rev )
        if prev is None:
            return

        diff = distance(rev.content, prev.content).replace("&para;", "")
        self.response.out.write(diff)
