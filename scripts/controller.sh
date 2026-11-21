#!/usr/bin/env bash
# Chunk loop controller v2 (Windows side, Git Bash). Usage: bash scripts/controller2.sh main|laptop
# For each packet in state/queue-<machine>.txt not yet in state/done-<machine>.txt:
#   reachability + free-space guard -> pre-chunk (clean interrupted attempts)
#   -> build + axiom audit in the sandbox (unprivileged 'builder')
#   -> export evidence (root, no .olean) -> report -> STATE.md -> local git commit.
# v3: QUEUE=<file> selects a shared queue; items done or running on the other machine are skipped.
# v2: an unreachable laptop is waited for (not counted as a disk failure); a chunk is
# marked done only when its report exists; interrupted attempts are retried cleanly.
# Stop cleanly with state/STOP (both) or state/STOP-<machine>.
# Parallelism can be changed between chunks in state/jobs-<machine>.txt.
set -u
M="$1"
ROOT=/g/rh-verif; cd "$ROOT" || exit 1
export MSYS_NO_PATHCONV=1
Q=${QUEUE:-state/queue-$M.txt}; DONE=state/done-$M.txt; touch "$DONE"
OTHER=$([ "$M" = main ] && echo laptop || echo main)
K="-i $HOME/.ssh/id_ed25519_remote -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=15 -o ServerAliveInterval=30 -o ServerAliveCountMax=6"
LAPTOP=matis@192.168.1.143
MIN_FREE_GB=${MIN_FREE_GB:-20}   # keep >= 15 GB free on the host disk, plus one chunk of margin (max observed chunk growth: 0.69 GB)
MAX_TRIES=3
if [ "$M" = main ]; then JOBS=11; LABEL="machine principale (Ryzen 7 5800X, sandbox WSL rhbuild sur G:, 12 vCPU / 19 GiB)"
else JOBS=10; LABEL="portable (Ryzen 7 4800HS, sandbox WSL rhbuild sur C:, 16 vCPU / 15,3 GiB)"; fi
log() { echo "[$(date -u +%FT%TZ)] [$M] $*" | tee -a "logs/controller-$M.log"; }
FILTER='post-quantum|store now|pq.html'

reachable() { [ "$M" = main ] && return 0; ssh $K -n $LAPTOP 'echo up' 2>/dev/null | grep -q up; }
wait_reachable() {  # wait up to 6 h for the laptop, checking every 5 min
  local waited=0
  until reachable; do
    [ $waited -eq 0 ] && log "UNREACHABLE: laptop does not answer on SSH, waiting (checks every 5 min)"
    [ -e state/STOP ] || [ -e "state/STOP-$M" ] && return 1
    sleep 300; waited=$((waited+300))
    [ $waited -ge 21600 ] && { log "UNREACHABLE for 6 h, giving up"; return 1; }
  done
  [ $waited -gt 0 ] && log "laptop reachable again after ${waited}s"
  return 0
}
host_free_gb() {
  if [ "$M" = main ]; then powershell.exe -NoProfile -Command "[math]::Floor((Get-PSDrive G).Free/1GB)" | tr -d '\r'
  else ssh $K -n $LAPTOP 'powershell -NoProfile -Command "[math]::Floor((Get-PSDrive C).Free/1GB)"' 2>/dev/null | tr -d '\r' | tail -1; fi
}
ensure_mount() {
  if [ "$M" = main ]; then
    wsl.exe -d rhbuild -u root -- bash -c "mountpoint -q /exchange || mount -t drvfs 'G:\\rh-verif\\exchange' /exchange -o uid=0,gid=0,umask=022" </dev/null
  else
    ssh $K $LAPTOP 'wsl -d rhbuild -u root -- bash -s' < scripts/ensure-mount-laptop.sh >/dev/null 2>&1
  fi
}
sandbox() {  # run as builder; returns the remote status (255 = SSH failure)
  if [ "$M" = main ]; then wsl.exe -d rhbuild -- "$@" </dev/null
  else ssh $K -n $LAPTOP "wsl -d rhbuild -- $*" 2> >(grep -av -E "$FILTER" >&2); fi
}
sandbox_root() {
  if [ "$M" = main ]; then wsl.exe -d rhbuild -u root -- "$@" </dev/null
  else ssh $K -n $LAPTOP "wsl -d rhbuild -u root -- $*" 2> >(grep -av -E "$FILTER" >&2); fi
}
commit() {
  until mkdir state/.gitlock 2>/dev/null; do sleep 2; done
  python scripts/state_update.py >/dev/null
  git add -A reports logs state scripts .gitignore >/dev/null 2>&1
  git commit -q -m "$1" >/dev/null 2>&1 || true
  rmdir state/.gitlock
}
sync_scripts() {
  [ "$M" = laptop ] || return 0
  scp $K -q exchange/in/run-chunk.sh exchange/in/audit-chunk.sh exchange/in/gen_audit.py exchange/in/pre-chunk.sh scripts/export-chunk.sh $LAPTOP:C:/rh-verif/exchange/in/ 2>/dev/null
}

wait_reachable && sync_scripts
declare -A tries
while true; do
  progressed=0
  while IFS=$'\t' read -r -u 3 ID DEPTH N OPEN EST; do
    [ -z "$ID" ] && continue
    grep -qx "$ID" "$DONE" && continue
    grep -qx "$ID" "state/done-$OTHER.txt" 2>/dev/null && continue   # shared queue: done elsewhere
    grep -q "^$OTHER: $ID " "state/running-$OTHER.txt" 2>/dev/null && continue   # running elsewhere
    [ -e state/STOP ] || [ -e "state/STOP-$M" ] && { log "STOP file present, exiting"; break 2; }
    [ -s "state/jobs-$M.txt" ] && JOBS=$(tr -dc 0-9 < "state/jobs-$M.txt")
    wait_reachable || break 2
    FREE=$(host_free_gb)
    if [ -z "$FREE" ]; then log "free-space query failed (connectivity?), retrying"; continue; fi
    if [ "$FREE" -lt "$MIN_FREE_GB" ]; then
      log "BLOCKED: host free space ${FREE} GB < $MIN_FREE_GB GB, stopping before $ID"
      echo "- [$M] arrêt : espace libre hôte ${FREE} Go < $MIN_FREE_GB Go avant $ID ($(date -u +%FT%TZ))" >> state/blockers.md
      commit "state: $M stopped on disk guard"; break 2
    fi
    tries[$ID]=$(( ${tries[$ID]:-0} + 1 ))
    if [ "${tries[$ID]}" -gt "$MAX_TRIES" ]; then
      log "GIVING UP on $ID after $MAX_TRIES attempts (infrastructure), leaving it pending"; continue
    fi
    echo "$M: $ID (depth $DEPTH, try ${tries[$ID]}) since $(date -u +%T) UTC" > "state/running-$M.txt"; cat state/running-*.txt > state/running.txt 2>/dev/null
    log "start $ID depth=$DEPTH modules=$N est_new_builds=$EST host_free=${FREE}GB jobs=$JOBS try=${tries[$ID]}"
    ensure_mount
    sandbox bash /exchange/in/pre-chunk.sh "$ID" > "logs/run-$ID.outer.log" 2>&1
    sandbox bash /exchange/in/run-chunk.sh "$ID" "$JOBS" >> "logs/run-$ID.outer.log" 2>&1
    rc=$?
    if ! grep -aq "CHUNK_END $ID" "logs/run-$ID.outer.log"; then
      log "INTERRUPTED $ID (remote status $rc, no CHUNK_END); will retry"
      mv "logs/run-$ID.outer.log" "logs/run-$ID.interrupted-$(date -u +%H%M%S).log"
      continue
    fi
    log "$(grep -aE 'PRE_CHUNK|BUILD_EXIT|MEM_PEAK|AUDIT_EXIT|CHUNK_END' logs/run-$ID.outer.log | tr '\n' ' ')"
    ensure_mount
    sandbox_root bash /exchange/in/export-chunk.sh "$ID" "$M" > /dev/null
    if [ "$M" = laptop ]; then
      mkdir -p exchange/out/laptop; rm -rf "exchange/out/laptop/$ID"
      scp $K -q -r "$LAPTOP:C:/rh-verif/exchange/out/laptop/$ID" exchange/out/laptop/ 2>/dev/null
    fi
    if [ ! -f "exchange/out/$M/$ID/receipt.json" ] && [ ! -f "exchange/out/$M/$ID/build.log" ]; then
      log "EXPORT FAILED for $ID; will retry export+build later"; continue
    fi
    cp "logs/run-$ID.outer.log" "exchange/out/$M/$ID/run-$ID.log"
    for f in logs/run-$ID.interrupted-*.log; do [ -f "$f" ] && mv "$f" "exchange/out/$M/$ID/"; done
    python scripts/make_report.py "exchange/out/$M/$ID" "$LABEL" >> "logs/controller-$M.log" 2>&1
    if [ ! -f "reports/$ID.md" ]; then log "REPORT FAILED for $ID"; continue; fi
    rm -f "logs/run-$ID.outer.log"
    echo "$ID" >> "$DONE"; progressed=1
    printf '%s : %s Go libres sur le disque hôte (%s)\n' "$M" "$(host_free_gb)" "$(date -u +%T) UTC" > "state/disk-$M.txt"; cat state/disk-*.txt > state/disk.txt
    rm -f "state/running-$M.txt"; cat state/running-*.txt > state/running.txt 2>/dev/null || : > state/running.txt
    commit "chunk $ID ($M): $(head -1 reports/$ID.md | sed 's/^# //')"
    log "done $ID: $(head -1 reports/$ID.md)"
  done 3< <(tail -n +2 "$Q")
  # queue exhausted for now: stop when nothing pending, else loop again for retries
  pending=$(tail -n +2 "$Q" | cut -f1 | grep -vxF -f <(cat state/done-main.txt state/done-laptop.txt) | wc -l)
  [ "$pending" -eq 0 ] && { log "queue $Q complete"; break; }
  [ "$progressed" -eq 0 ] && { log "no progress in a full pass, $pending pending; exiting"; break; }
done
rm -f "state/running-$M.txt"
log "controller exit"
