#!/usr/bin/env bash
# §5.6 cleanup (builder): delete Lake-generated *.setup.json compiler inputs of the project build.
# Lake regenerates them when (re)building a module; they are not artifacts needed downstream
# (tested: `lake build --no-build` stays "All targets up-to-date" after deletion). Never touches sources or .olean.
cd /work/vol/lean/.lake/build || exit 1
read n b < <(find . -name '*.setup.json' -type f -printf '%s\n' | awk '{n++; b+=$1} END{print n+0, b+0}')
find . -name '*.setup.json' -type f -delete
echo "CLEANUP_SETUPJSON files=$n bytes=$b $(date -u +%FT%TZ)"
df -B1 --output=used,avail / | tail -1
