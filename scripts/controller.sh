#!/usr/bin/env bash
# Chunk loop controller (Windows side, Git Bash). Usage: bash scripts/controller.sh main|laptop
# For each packet in state/queue-<machine>.txt not yet in state/done-<machine>.txt:
#   free-space guard -> build + axiom audit in the sandbox (unprivileged 'builder')
#   -> export evidence (root, no .olean) -> report -> STATE.md -> local git commit.
# Stop cleanly by creating state/STOP (both) or state/STOP-<machine>.
# Parallelism per machine can be changed between chunks in state/jobs-<machine>.txt.
set -u
M="$1"
ROOT=/g/rh-verif; cd "$ROOT" || exit 1
export MSYS_NO_PATHCONV=1
Q=state/queue-$M.txt; DONE=state/done-$M.txt; touch "$DONE"
K="-i $HOME/.ssh/id_ed25519_remote -o IdentitiesOnly=yes -o BatchMode=yes -o ServerAliveInterval=30"
LAPTOP=matis@192.168.1.143
MIN_FREE_GB=20   # keep >= 15 GB free on the host disk, plus one chunk of margin
if [ "$M" = main ]; then JOBS=11; LABEL="machine principale (Ryzen 7 5800X, sandbox WSL rhbuild sur G:, 12 vCPU / 19 GiB)"
else JOBS=15; LABEL="portable (Ryzen 7 4800HS, sandbox WSL rhbuild sur C:, 16 vCPU / 15,3 GiB)"; fi
log() { echo "[$(date -u +%FT%TZ)] [$M] $*" | tee -a "logs/controller-$M.log"; }

host_free_gb() {
  if [ "$M" = main ]; then powershell.exe -NoProfile -Command "[math]::Floor((Get-PSDrive G).Free/1GB)" | tr -d '\r'
  else ssh $K $LAPTOP 'powershell -NoProfile -Command "[math]::Floor((Get-PSDrive C).Free/1GB)"' 2>/dev/null | tr -d '\r' | tail -1; fi
}
ensure_mount() {
  if [ "$M" = main ]; then
    wsl.exe -d rhbuild -u root -- bash -c "mountpoint -q /exchange || mount -t drvfs 'G:\\rh-verif\\exchange' /exchange -o uid=0,gid=0,umask=022"
  else
    ssh $K $LAPTOP 'wsl -d rhbuild -u root -- bash -s' < scripts/ensure-mount-laptop.sh >/dev/null 2>&1
  fi
}
sandbox() {  # run as builder
  if [ "$M" = main ]; then wsl.exe -d rhbuild -- "$@"
  else ssh $K $LAPTOP "wsl -d rhbuild -- $*" 2>&1 | grep -av -E 'post-quantum|store now|pq.html'; fi
}
sandbox_root() {
  if [ "$M" = main ]; then wsl.exe -d rhbuild -u root -- "$@"
  else ssh $K $LAPTOP "wsl -d rhbuild -u root -- $*" 2>&1 | grep -av -E 'post-quantum|store now|pq.html'; fi
}
commit() {
  until mkdir state/.gitlock 2>/dev/null; do sleep 2; done
  python scripts/state_update.py >/dev/null
  git add -A reports logs state scripts .gitignore >/dev/null 2>&1
  git commit -q -m "$1" >/dev/null 2>&1 || true
  rmdir state/.gitlock
}

if [ "$M" = laptop ]; then  # sync scripts to the laptop exchange folder
  scp $K -q exchange/in/run-chunk.sh exchange/in/audit-chunk.sh exchange/in/gen_audit.py scripts/export-chunk.sh $LAPTOP:C:/rh-verif/exchange/in/ 2>/dev/null
fi

while IFS=$'\t' read -r -u 3 ID DEPTH N OPEN EST; do
  [ -z "$ID" ] && continue
  grep -qx "$ID" "$DONE" && continue
  [ -e state/STOP ] || [ -e "state/STOP-$M" ] && { log "STOP file present, exiting"; break; }
  [ -s "state/jobs-$M.txt" ] && JOBS=$(tr -dc 0-9 < "state/jobs-$M.txt")
  FREE=$(host_free_gb)
  if [ -z "$FREE" ] || [ "$FREE" -lt "$MIN_FREE_GB" ]; then
    log "BLOCKED: host free space ${FREE:-?} GB < $MIN_FREE_GB GB, stopping before $ID"
    echo "- [$M] arrêt : espace libre hôte ${FREE:-?} Go < $MIN_FREE_GB Go avant $ID ($(date -u +%FT%TZ))" >> state/blockers.md
    commit "state: $M stopped on disk guard"; break
  fi
  echo "$M: $ID (depth $DEPTH) since $(date -u +%T) UTC" > "state/running-$M.txt"; cat state/running-*.txt > state/running.txt 2>/dev/null
  log "start $ID depth=$DEPTH modules=$N est_new_builds=$EST host_free=${FREE}GB jobs=$JOBS"
  ensure_mount
  sandbox bash /exchange/in/run-chunk.sh "$ID" "$JOBS" > "logs/run-$ID.outer.log" 2>&1
  log "$(grep -aE 'BUILD_EXIT|MEM_PEAK|AUDIT_EXIT|CHUNK_END' logs/run-$ID.outer.log | tr '\n' ' ')"
  ensure_mount
  sandbox_root bash /exchange/in/export-chunk.sh "$ID" "$M" > /dev/null
  if [ "$M" = laptop ]; then
    mkdir -p exchange/out/laptop
    scp $K -q -r "$LAPTOP:C:/rh-verif/exchange/out/laptop/$ID" exchange/out/laptop/ 2>/dev/null
  fi
  cp "logs/run-$ID.outer.log" "exchange/out/$M/$ID/run-$ID.log" 2>/dev/null
  python scripts/make_report.py "exchange/out/$M/$ID" "$LABEL" >> "logs/controller-$M.log" 2>&1
  rm -f "logs/run-$ID.outer.log"
  echo "$ID" >> "$DONE"
  printf '%s : %s Go libres sur le disque hôte (%s)\n' "$M" "$(host_free_gb)" "$(date -u +%T) UTC" > "state/disk-$M.txt"; cat state/disk-*.txt > state/disk.txt
  rm -f "state/running-$M.txt"; cat state/running-*.txt > state/running.txt 2>/dev/null || : > state/running.txt
  commit "chunk $ID ($M): $(head -1 reports/$ID.md | sed 's/^# //')"
  log "done $ID: $(head -1 reports/$ID.md)"
done 3< <(tail -n +2 "$Q")
log "controller exit"
