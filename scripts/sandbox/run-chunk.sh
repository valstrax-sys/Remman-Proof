#!/usr/bin/env bash
# Usage: run-chunk.sh <TASK_ID>   (runs as unprivileged builder in the rhbuild sandbox)
# Builds the task with the project's own tracker command, then runs the axiom audit.
set -uo pipefail
id="$1"; jobs="${2:-}"
# Parallelism: Lake has no -j flag in 4.33.1; the Lean runtime thread pool honours LEAN_NUM_THREADS.
[ -n "$jobs" ] && export LEAN_NUM_THREADS="$jobs"
echo "LEAN_NUM_THREADS=${LEAN_NUM_THREADS:-unset}"
export PATH="$HOME/.elan/bin:$PATH"
R=/work/receipts/$id; mkdir -p /work/receipts /work/logs
[ -e "$R" ] && { echo "receipt dir exists: $R"; exit 3; }
cd /work/repo
echo "CHUNK_START $id $(date -u +%FT%TZ) tracker=$(git rev-parse HEAD)"
echo "DISK_BEFORE $(df -B1 --output=used,avail / | tail -1)"
# memory sampler (whole sandbox, MiB used), every 5 s
( while sleep 5; do echo "$(date -u +%T) $(free -m | awk '/Mem:/{print $3}') $(pgrep -c -x lean)"; done ) > "/work/logs/$id.mem" &
sampler=$!
/usr/bin/time -v -o "/work/logs/$id.time" python3 tracker/tasks.py build "$id" /work/vol/lean "$R" --bundle
brc=$?
kill $sampler 2>/dev/null
echo "BUILD_EXIT $id $brc $(date -u +%FT%TZ)"
echo "MEM_PEAK_MIB $(sort -k2 -n /work/logs/$id.mem | tail -1 | awk '{print $2}') MAX_LEAN_PROCS $(sort -k3 -n /work/logs/$id.mem | tail -1 | awk '{print $3}')"
arc=-1
if [ $brc -eq 0 ]; then
  bash /exchange/in/audit-chunk.sh "$id"; arc=$?
fi
echo "DISK_AFTER $(df -B1 --output=used,avail / | tail -1)"
# §5.6 cleanup: drop regenerable Lake compiler inputs (*.setup.json, ~5 MB/module); keep .olean (needed downstream)
[ -f /exchange/in/cleanup-setupjson.sh ] && bash /exchange/in/cleanup-setupjson.sh | head -1
echo "CHUNK_END $id build=$brc audit=$arc $(date -u +%FT%TZ)"
