#!/usr/bin/env bash
echo "== host: $(hostname) user: $(whoami) date: $(date -u +%FT%TZ)"
uname -a
echo "== CPU"; lscpu | grep -E 'Model name|^CPU\(s\)|Thread|Core|Socket'
echo "nproc=$(nproc)"
echo "== RAM"; free -g
echo "== Disk"; df -hT / /mnt/g 2>/dev/null
echo "== GPU"; (command -v nvidia-smi >/dev/null && nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv) || echo "nvidia-smi: absent"
echo "== Tools"
for t in gcc g++ clang make cmake python3 pip3 git curl elan lean lake sage docker zstd gh /usr/bin/time tar sha256sum; do
  p=$(command -v "$t" 2>/dev/null); if [ -n "$p" ]; then v=$("$t" --version 2>&1 | head -1); echo "$t: $p | $v"; else echo "$t: MISSING"; fi
done
