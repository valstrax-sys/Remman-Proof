#!/usr/bin/env bash
set -euo pipefail
cd /mnt/g/rh-verif
git config --global --add safe.directory /mnt/g/rh-verif 2>/dev/null || true
[ -d .git ] || git init -q -b main
git config core.filemode false
git config user.name "rh-verif agent (Claude Code)"
git config user.email "noreply@anthropic.com"
git remote get-url origin >/dev/null 2>&1 || git remote add origin git@github.com:valstrax-sys/Remman-Proof.git
git fetch -q origin 2>&1 || true
git branch -a
# healthcheck branch
git checkout -q -B agent-healthcheck
echo "healthcheck $(date -u +%FT%TZ)" > state/healthcheck.txt
git add state/healthcheck.txt
git commit -q -m "healthcheck: test push access" 
git push -u origin agent-healthcheck 2>&1 | grep -v -E 'post-quantum|store now|pq.html'
git push origin --delete agent-healthcheck 2>&1 | grep -v -E 'post-quantum|store now|pq.html'
git checkout -q --orphan main-tmp && git rm -rq --cached . && rm -f state/healthcheck.txt
git branch -D agent-healthcheck main 2>/dev/null || true
git checkout -q --orphan main 2>/dev/null || git checkout -q main
git branch -D main-tmp 2>/dev/null || true
git ls-remote origin
echo HEALTHCHECK_DONE
