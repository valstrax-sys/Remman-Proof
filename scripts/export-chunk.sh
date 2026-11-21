#!/usr/bin/env bash
# Run as root in a sandbox: copy one chunk's evidence (no .olean) to the exchange folder.
# Usage: export-chunk.sh <ID> <machine>
set -eu
id="$1"; m="$2"; o="/exchange/out/$m/$id"; rm -rf "$o"; mkdir -p "$o"
R=/work/receipts/$id
for f in receipt.json build.log; do [ -f "$R/$f" ] && cp "$R/$f" "$o/"; done
[ -f "$R/targets.tar.gz" ] && sha256sum "$R/targets.tar.gz" | awk '{print $1}' > "$o/bundle.sha256" && stat -c %s "$R/targets.tar.gz" > "$o/bundle.size"
for f in /work/audit/$id.lean /work/audit/$id.audit.log /work/logs/$id.time /work/logs/$id.audit.time /work/logs/$id.mem /work/logs/run-$id.log; do [ -f "$f" ] && cp "$f" "$o/"; done
df -B1 --output=used,avail / | tail -1 > "$o/disk.txt"
ls "$o"
