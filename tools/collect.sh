#!/usr/bin/env bash
# Pull every per-seed result branch into runs/ as local JSON logs.
#
# Actions pushes each seed's log to a scratch branch runs/<label>/seed-<N>,
# with the file at the branch ROOT as `seed-<N>.json` -- NOT under out/.
# Getting that path wrong collected nothing for a full cycle on
# 2026-08-24, which is why it is spelled out here.
#
# runs/ is gitignored and does NOT survive a container restart; the branches
# do, so this script is the recovery path as well as the daily collector.
# Idempotent: files already present are skipped.
set -u
cd "$(dirname "$0")/.."
mkdir -p runs/rot-collect runs/v53-collect
n=0
for br in $(git branch -r | grep -oP 'origin/runs/standing/seed-\S+'); do
  s=${br##*seed-}; f=runs/rot-collect/$s.json
  [ -f "$f" ] && continue
  timeout 6 git show "$br:seed-$s.json" > "$f" 2>/dev/null && n=$((n+1)) || rm -f "$f"
done
echo "standing new: $n"
m=0
for br in $(git branch -r | grep -oP 'origin/runs/h[0-9][^ ]*/seed-\S+'); do
  s=${br##*seed-}; lab=$(echo "$br" | sed 's|origin/runs/||;s|/seed-.*||')
  f=runs/v53-collect/$lab-$s.json
  [ -f "$f" ] && continue
  timeout 6 git show "$br:seed-$s.json" > "$f" 2>/dev/null && m=$((m+1)) || rm -f "$f"
done
echo "h-arm new: $m"
ls runs/rot-collect | wc -l; ls runs/v53-collect | wc -l
