#!/usr/bin/env bash
# Safely publish locally-scraped reports to the `data` branch via OVERLAY.
#
# The production data branch holds the full multi-year history (more reports
# than any single local partial scrape). So we MUST NOT blanket-delete: we
# overlay our local report.json/report.md onto the branch (add/update), then
# surgically remove only issues now known to be no-bounty (e.g. self-healed
# false positives), then rebuild index.json/stats.json from the MERGED set so
# the site reflects everything on the branch. discovery_*.json and no_bounty.json
# are union-merged to preserve CI state.
#
# Usage: scripts/push_data.sh "<commit scope>" [--push]
#   Without --push: stages + prints verification only (no commit/push).
set -euo pipefail

REPO=/root/shantanu/vrp-reports
SRC="$REPO/data"
WT=/tmp/vrp-data-wt
SCOPE="${1:-refresh}"
DO_PUSH="${2:-}"

cd "$REPO"
[ -f "$SRC/index.json" ] || { echo "ERROR: $SRC/index.json missing" >&2; exit 1; }

git fetch origin data --quiet
git worktree remove --force "$WT" 2>/dev/null || true
rm -rf "$WT"
git worktree add --detach "$WT" origin/data --quiet

before=$(find "$WT/issues" -name report.json | wc -l)

# 1) Overlay local reports (NO --delete: never drop branch-only reports)
mkdir -p "$WT/issues"
rsync -a \
  --include='*/' --include='report.json' --include='report.md' --exclude='*' \
  "$SRC/issues/" "$WT/issues/"

# 2) Remove issues now known no-bounty (self-healed false positives etc.)
removed=0
if [ -f "$SRC/no_bounty.json" ]; then
  while IFS= read -r id; do
    [ -n "$id" ] || continue
    if [ -d "$WT/issues/$id" ]; then
      rm -rf "$WT/issues/$id"; removed=$((removed+1)); echo "  purged no-bounty dir: $id"
    fi
  done < <(.venv/bin/python -c "import json;print('\n'.join(map(str,json.load(open('$SRC/no_bounty.json')))))")
fi

# 3) Union-merge CI state files (no_bounty + per-year discovery checkpoints)
.venv/bin/python - "$SRC" "$WT" <<'PY'
import json, sys, glob, os
src, wt = sys.argv[1], sys.argv[2]
def load(p):
    try: return json.load(open(p))
    except Exception: return None
def union_list(a, b):
    return sorted({str(x) for x in (a or [])} | {str(x) for x in (b or [])})
# no_bounty.json
nb = union_list(load(f"{src}/no_bounty.json"), load(f"{wt}/no_bounty.json"))
json.dump(nb, open(f"{wt}/no_bounty.json","w"), indent=2)
# per-year discovery checkpoints + queue
for p in glob.glob(f"{src}/discovery_*.json"):
    name = os.path.basename(p)
    merged = union_list(load(p), load(f"{wt}/{name}"))
    json.dump(merged, open(f"{wt}/{name}","w"), indent=2)
print("merged CI state (no_bounty + discovery checkpoints)")
PY

# 4) Rebuild index.json + stats.json from the MERGED worktree issues/
.venv/bin/python - "$WT" <<'PY'
import sys, pathlib
wt = pathlib.Path(sys.argv[1])
import vrp.config as c
c.ISSUES_DIR = wt/"issues"; c.INDEX_FILE = wt/"index.json"; c.STATS_FILE = wt/"stats.json"
import vrp.index_builder as ib
ib.ISSUES_DIR = c.ISSUES_DIR; ib.INDEX_FILE = c.INDEX_FILE; ib.STATS_FILE = c.STATS_FILE
n = ib.rebuild_index(); ib.build_stats()
print(f"rebuilt merged index: {n} reports")
PY

after=$(find "$WT/issues" -name report.json | wc -l)
cd "$WT"
git add -A
echo "=== VERIFY ==="
echo "reports on branch before: $before   after overlay+purge: $after   (purged FP dirs: $removed)"
echo "index.json entries: $(grep -c '\"id\"' index.json)"
echo "staged file count: $(git diff --cached --name-only | wc -l)"
echo "deletions of report.json (should equal purged FP count = $removed):"
git diff --cached --name-status | awk '$1=="D" && /report\.json$/' | wc -l

if [ "$DO_PUSH" = "--push" ]; then
  if git diff --cached --quiet; then
    echo "No data changes."
  else
    git -c user.name="Claude Code" -c user.email="noreply@anthropic.com" \
      commit -q -m "data: refresh VRP reports (${SCOPE})

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
    git push origin HEAD:data
    echo "PUSHED to data branch."
  fi
fi

cd "$REPO"
git worktree remove --force "$WT" 2>/dev/null || true
