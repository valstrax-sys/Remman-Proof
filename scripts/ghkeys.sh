for k in ~/.ssh/id_ed25519 ~/.ssh/id_ed25519_remote; do echo "== kali $k"; timeout 15 ssh -i "$k" -o IdentitiesOnly=yes -o BatchMode=yes -T git@github.com 2>&1; done
