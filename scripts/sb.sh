#!/usr/bin/env bash
# Windows-side helper (Git Bash): run a command as 'builder' in the rhbuild sandbox,
# after making sure the read-only exchange folder is mounted (root step).
export MSYS_NO_PATHCONV=1
wsl.exe -d rhbuild -u root -- bash -c "mountpoint -q /exchange || mount -t drvfs 'G:\rh-verif\exchange' /exchange -o uid=0,gid=0,umask=022" || exit 90
exec wsl.exe -d rhbuild -- "$@"
