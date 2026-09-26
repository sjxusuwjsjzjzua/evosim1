#!/bin/bash
# Local batch: tools/batch.sh <label> "<k=v,k=v>" <ticks> <seed>...
# Freezes a copy of evosim.html into runs/<label>/ (so editing the build
# mid-batch is safe), then runs the seeds, 4 at a time, in the background.
# Each seed writes runs/<label>/s<seed>.json, -genomes.json and .txt.
#   tools/batch.sh curve3 "dietCurve=3" 400000 401 402 403 404
#   python3 tools/v1score.py runs/curve3/s???.json
set -e
cd "$(dirname "$0")/.."
L=$1; X=$2; T=$3; shift 3
D=runs/$L; mkdir -p "$D"; cp evosim.html "$D/build.html"
(
for s in "$@"; do
  while [ "$(pgrep -x node | wc -l)" -ge "${JOBS:-4}" ]; do sleep 5; done
  node run.js --build "$D/build.html" --seed "$s" --ticks "$T" --every 20000 --set "gridN=64${X:+,$X}" \
    --out "$D/s$s.json" --dump "$D/s$s-genomes.json" > "$D/s$s.txt" 2>&1 &
  sleep 2
done
wait
) > /dev/null 2>&1 &
echo "batch $L: ${#@} seeds, logs in $D/"
