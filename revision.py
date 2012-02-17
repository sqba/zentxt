from google.appengine.ext import db

from models import File, Revision
from base import BasePage

import diff_match_patch as dmp_module

dmp = dmp_module.diff_match_patch()
dmp.Diff_Timeout = 0.1  # Don't spend more than 0.1 seconds on a diff.


class RevisionPage(BasePage):

    def distance(self, sx, sy):
        diffs = dmp.diff_main(sx, sy)
        dmp.diff_cleanupSemantic(diffs)
        return dmp.diff_prettyHtml(diffs)

    def get(self):
        if not self.check_user():
            return

        rev = self.get_revision_by_id( self.request.get("id") )
        if rev is None:
            self.response.out.write("rev not found")
            return

        prev = rev.prev
        if prev is None:
            self.response.out.write("prev not found")
            return

        diff = self.distance(prev.content, rev.content).replace("&para;", "")
        self.response.out.write(diff)
