import diff_match_patch as dmp_module
dmp = dmp_module.diff_match_patch()
dmp.Diff_Timeout = 0.1  # Don't spend more than 0.1 seconds on a diff.

def distance (sx, sy):
  diffs = dmp.diff_main(sx, sy)
  dmp.diff_cleanupSemantic(diffs)
  return dmp.diff_prettyHtml(diffs)
