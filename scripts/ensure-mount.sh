mountpoint -q /exchange || { mkdir -p /exchange; mount -t drvfs 'G:\rh-verif\exchange' /exchange -o uid=0,gid=0,umask=022; }
mountpoint /exchange
