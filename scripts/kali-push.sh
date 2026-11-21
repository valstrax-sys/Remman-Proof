#!/usr/bin/env bash
# Runs in Kali (principal user): push the reports repo with the ark2 deploy key (read/write).
cd /mnt/g/rh-verif || exit 1
GIT_SSH_COMMAND="ssh -i /root/.ssh/id_ed25519 -o IdentitiesOnly=yes -o BatchMode=yes -o ConnectTimeout=20" git push -q origin main 2>&1 | grep -v -E 'post-quantum|store now|pq.html'
exit "${PIPESTATUS[0]}"
