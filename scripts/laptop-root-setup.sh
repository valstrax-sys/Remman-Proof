#!/usr/bin/env bash
# First-time root setup on the laptop sandbox: run once from a temporary C: mount.
set -eux
mkdir -p /tmp/x && mount -t drvfs 'C:\rh-verif\exchange' /tmp/x -o uid=0,gid=0,umask=022
bash /tmp/x/in/setup-rhbuild-root.sh
umount /tmp/x
