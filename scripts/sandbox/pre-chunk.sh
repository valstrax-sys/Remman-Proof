#!/usr/bin/env bash
# Usage: pre-chunk.sh <TASK_ID>   (builder, in the sandbox)
# If a previous attempt for this task was interrupted (receipt dir exists), keep its
# evidence under /work/receipts/aborted/ and delete the *target* modules' build outputs
# (never sources), so the retry recompiles every target and logs a "Built" line for it.
set -uo pipefail
id="$1"; R=/work/receipts/$id
[ -e "$R" ] || { echo "PRE_CHUNK $id fresh"; exit 0; }
ts=$(date -u +%Y%m%dT%H%M%SZ)
mkdir -p /work/receipts/aborted
mv "$R" "/work/receipts/aborted/$id-$ts"
for f in /work/audit/$id.audit.log /work/logs/$id.time /work/logs/$id.mem; do [ -f "$f" ] && mv "$f" "$f.aborted-$ts"; done
n=0
while read -r mod; do
  stem="/work/vol/lean/.lake/build/lib/lean/${mod//.//}"
  irs="/work/vol/lean/.lake/build/ir/${mod//.//}"
  for f in "$stem".* "$irs".*; do [ -f "$f" ] && rm -f "$f" && n=$((n+1)); done
done < <(python3 - "$id" <<'EOF'
import sys, gzip, json
t = sys.argv[1]
with gzip.open('/work/repo/tracker/modules.jsonl.gz', 'rt') as f:
    for line in f:
        r = json.loads(line)
        if t in (r['id'], r['packet'], r['module']): print(r['module'])
EOF
)
echo "PRE_CHUNK $id retry: previous attempt moved to /work/receipts/aborted/$id-$ts, removed $n target build files"
