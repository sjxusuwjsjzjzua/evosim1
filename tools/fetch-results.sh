#!/usr/bin/env bash
# Pull every results/<label> branch (written by sim.yml) into runs/<label>/.
# Usage: bash tools/fetch-results.sh [label-prefix]
set -u
cd "$(dirname "$0")/.."
git fetch -q origin "refs/heads/results/${1:-}*:refs/remotes/origin/results/${1:-}*" 2>/dev/null
for br in $(git branch -r | grep -oP "origin/results/${1:-}\S*"); do
  lab=${br#origin/results/}; mkdir -p "runs/$lab"
  for f in $(git ls-tree --name-only "$br"); do
    [ -f "runs/$lab/$f" ] || git show "$br:$f" > "runs/$lab/$f"
  done
  echo "$lab: $(ls runs/$lab/*.json 2>/dev/null | wc -l) logs"
done
