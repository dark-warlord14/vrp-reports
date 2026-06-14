#!/usr/bin/env bash
# Safely publish reports to the `data` branch via OVERLAY + explicit purge list.
#
# The production data branch holds the authoritative multi-year history (correct
# metadata-reward captures). We must NOT regress it, so:
#   1. Overlay our locally-scraped report.json/report.md (add/update only).
#   2. Remove ONLY issue dirs in an explicit purge list (re-confirmed denials /
#      no-bounty), never by the no_bounty checkpoint (which can be contaminated
#      by capture failures) and never the whole "award_text + no amount" class
#      (which also contains genuine amount-extraction misses).
#   3. Rebuild index.json/stats.json from the MERGED worktree so the site reflects
#      everything on the branch.
#
# Purge list: /tmp/fp_result.json {"remove":[ids...]} if present, else none.
#
# Usage: scripts/push_data.sh "<commit scope>" [--push]
set -euo pipefail

REPO=/root/shantanu/vrp-reports
SRC="$REPO/data"
WT=/tmp/vrp-data-wt
PURGE_JSON=/tmp/fp_result.json
SCOPE="${1:-refresh}"
DO_PUSH="${2:-}"

cd "$REPO"
[ -f "$SRC/index.json" ] || { echo "ERROR: $SRC/index.json missing" >&2; exit 1; }

git fetch origin data --quiet
git worktree remove --force "$WT" 2>/dev/null || true
rm -rf "$WT"
git worktree add --detach "$WT" origin/data --quiet
before=$(find "$WT/issues" -name report.json | wc -l)

# 1) Overlay local reports (NO --delete)
mkdir -p "$WT/issues"
rsync -a --include='*/' --include='report.json' --include='report.md' --exclude='*' \
  "$SRC/issues/" "$WT/issues/"

# 2) Remove ONLY the explicit purge list (re-confirmed denials)
removed=0
if [ -f "$PURGE_JSON" ]; then
  while IFS= read -r id; do
    [ -n "$id" ] || continue
    if [ -d "$WT/issues/$id" ]; then rm -rf "$WT/issues/$id"; removed=$((removed+1)); echo "  purged denial: $id"; fi
  done < <(.venv/bin/python -c "import json;print('\n'.join(json.load(open('$PURGE_JSON')).get('remove',[])))")
fi

# 3) Union-merge CI state (no_bounty + discovery checkpoints) — site-irrelevant but keeps CI sane
.venv/bin/python - "$SRC" "$WT" <<'PY'
import json, sys, glob, os
src, wt = sys.argv[1], sys.argv[2]
def load(p):
    try: return json.load(open(p))
    except Exception: return None
def u(a,b): return sorted({str(x) for x in (a or [])} | {str(x) for x in (b or [])})
json.dump(u(load(f"{src}/no_bounty.json"), load(f"{wt}/no_bounty.json")), open(f"{wt}/no_bounty.json","w"), indent=2)
for p in glob.glob(f"{src}/discovery_*.json"):
    n=os.path.basename(p); json.dump(u(load(p), load(f"{wt}/{n}")), open(f"{wt}/{n}","w"), indent=2)
print("merged CI state")
PY

# 4) Rebuild index + stats from merged worktree
.venv/bin/python - "$WT" <<'PY'
import sys, pathlib
wt=pathlib.Path(sys.argv[1])
import vrp.config as c
c.ISSUES_DIR=wt/"issues"; c.INDEX_FILE=wt/"index.json"; c.STATS_FILE=wt/"stats.json"
import vrp.index_builder as ib
ib.ISSUES_DIR=c.ISSUES_DIR; ib.INDEX_FILE=c.INDEX_FILE; ib.STATS_FILE=c.STATS_FILE
n=ib.rebuild_index(); ib.build_stats(); print(f"merged index: {n} reports")
PY

after=$(find "$WT/issues" -name report.json | wc -l)
cd "$WT"; git add -A
dels=$(git diff --cached --name-status | grep -E '^D' | grep -c 'report\.json$' || true)
echo "=== VERIFY ==="
echo "reports before: $before   after overlay+purge: $after   (purged denials: $removed)"
echo "index entries: $(grep -c '"id"' index.json)"
echo "report.json deletions staged: $dels  (expect = $removed)"
if [ "$dels" != "$removed" ]; then
  echo "ABORT: unexpected deletion count ($dels != $removed) — not pushing." >&2
  cd "$REPO"; git worktree remove --force "$WT" 2>/dev/null || true; exit 1
fi

if [ "$DO_PUSH" = "--push" ]; then
  if git diff --cached --quiet; then echo "No data changes."; else
    git -c user.name="Claude Code" -c user.email="noreply@anthropic.com" \
      commit -q -m "data: refresh VRP reports (${SCOPE})

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
    git push origin HEAD:data && echo "PUSHED to data branch."
  fi
fi
cd "$REPO"; git worktree remove --force "$WT" 2>/dev/null || true
