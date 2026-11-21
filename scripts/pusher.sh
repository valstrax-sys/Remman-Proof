#!/usr/bin/env bash
# Windows side (Git Bash): every 10 min, push local commits to GitHub under the git lock.
# Stops when state/STOP exists and no controller is running.
cd /g/rh-verif || exit 1
export MSYS_NO_PATHCONV=1
while true; do
  if [ -n "$(git log origin/main..main --oneline 2>/dev/null | head -1)" ]; then
    until mkdir state/.gitlock 2>/dev/null; do sleep 2; done
    wsl.exe -d Kali -- bash /mnt/g/rh-verif/scripts/kali-push.sh </dev/null; rc=$?
    rmdir state/.gitlock
    echo "[$(date -u +%FT%TZ)] push rc=$rc head=$(git rev-parse --short HEAD)" >> logs/pusher.log
  fi
  [ -e state/STOP ] && ! ps -ef | grep -q '[c]ontroller.sh' && { git log origin/main..main --oneline | grep -q . || exit 0; }
  sleep 600
done
