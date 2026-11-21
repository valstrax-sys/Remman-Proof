#!/usr/bin/env bash
# Usage: pause-at.sh <HH:MM UTC>  — create state/STOP at that time; controllers stop after their current chunk.
cd /g/rh-verif || exit 1
t=$(date -u -d "today $1" +%s); now=$(date -u +%s); [ $t -le $now ] && t=$((t+86400))
echo "[$(date -u +%FT%TZ)] pause scheduled for $(date -u -d @$t +%FT%TZ)" >> logs/pause.log
sleep $((t-now))
echo "pause demandée par l'utilisateur à 23:00 heure locale ($(date -u +%FT%TZ)) ; reprise prévue demain" > state/STOP
echo "[$(date -u +%FT%TZ)] state/STOP created" >> logs/pause.log
