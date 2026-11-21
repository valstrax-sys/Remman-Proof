#!/usr/bin/env bash
# Usage: audit-chunk.sh <TASK_ID>  — axiom audit of every declaration in the task's modules.
# Runs as unprivileged builder in the rhbuild sandbox. Uses the pinned toolchain binary
# and the LEAN_PATH prepared by Lake (same approach as verify.sh's final checks).
set -uo pipefail
id="$1"; A=/work/audit; mkdir -p "$A" /work/logs
export PATH="$HOME/.elan/bin:$PATH" ELAN_HOME=/work/vol/elan XDG_CACHE_HOME=/work/vol/cache
cd /work/vol/lean
TC=$ELAN_HOME/toolchains/leanprover--lean4---v4.33.1/bin
LP="$(elan run leanprover/lean4:v4.33.1 lake env printenv LEAN_PATH)"
python3 /exchange/in/gen_audit.py "$id" "$A/$id.lean"
/usr/bin/time -v -o "/work/logs/$id.audit.time" env LEAN_PATH="$LP" "$TC/lean" "$A/$id.lean" > "$A/$id.audit.log" 2>&1
arc=$?
echo "AUDIT_EXIT $id $arc $(date -u +%FT%TZ)"
echo "AUDIT_STATIC_OK_COUNT $(grep -c 'static_verdict=OK' "$A/$id.audit.log")"
grep -E "AXIOM_AUDIT_UNION|AXIOM_AUDIT_SUMMARY|AXIOM_AUDIT_DECL|static_verdict=FLAG|verdict=NOT_LOADED|error" "$A/$id.audit.log" | cut -c1-600 | head -30
exit $arc
