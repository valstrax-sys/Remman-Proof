#!/usr/bin/env bash
# Run as root inside the rhbuild distro. Creates an unprivileged builder account
# and disables Windows drive automount + interop, so archive code cannot reach
# Windows files, ~/.ssh, tokens, or launch Windows executables.
set -euxo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq curl git python3 build-essential ca-certificates time zstd >/dev/null
id builder 2>/dev/null || useradd -m -s /bin/bash builder
# no sudo for builder
deluser builder sudo 2>/dev/null || true
passwd -l builder
cat > /etc/wsl.conf <<'CONF'
[automount]
enabled = false
mountFsTab = false
[interop]
enabled = false
appendWindowsPath = false
[user]
default = builder
CONF
mkdir -p /work && chown builder:builder /work
df -h /
