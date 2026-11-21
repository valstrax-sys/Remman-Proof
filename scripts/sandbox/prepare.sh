#!/usr/bin/env bash
# Runs as unprivileged 'builder' inside the rhbuild sandbox.
set -euo pipefail
mkdir -p /work/logs
exec > >(tee -a /work/logs/prepare-outer.log) 2>&1
echo "== prepare start $(date -u +%FT%TZ)"
if ! command -v elan >/dev/null && [ ! -x "$HOME/.elan/bin/elan" ]; then
  curl -sSfL https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -o /tmp/elan-init.sh
  sha256sum /tmp/elan-init.sh
  sh /tmp/elan-init.sh -y --default-toolchain none
fi
export PATH="$HOME/.elan/bin:$PATH"
elan --version
if [ ! -d /work/repo ]; then git clone https://github.com/rohanarun/alpoge-rh-replay /work/repo; fi
cd /work/repo && echo "tracker commit: $(git rev-parse HEAD)"
/usr/bin/time -v ./verify.sh /work/vol --prepare-only
echo "== prepare end $(date -u +%FT%TZ) rc=$?"
