# Inventaire — portable (Velkhana, `matis@192.168.1.143`)

Relevé le 2026-11-21 (≈11:30–12:10 UTC) par SSH depuis la machine principale avec la clé `~/.ssh/id_ed25519_remote`. Logs bruts : `logs/inventory/laptop-*.txt`.

**Le portable tourne sous Windows**, pas sous Linux : le shell SSH est `cmd.exe`. La commande du prompt `ssh <laptop> 'uname -a; nproc; free -g; df -h'` échoue donc telle quelle. Les mêmes informations ont été relevées avec PowerShell et dans WSL.

## Matériel

| Élément | Valeur |
|---|---|
| CPU | AMD Ryzen 7 4800HS, 8 cœurs physiques / 16 threads logiques. WSL voit 16 vCPU. |
| RAM physique | 31,4 Go |
| RAM visible par WSL | 15,3 GiB (15 699 MiB) et 4 GiB de swap. C'est le défaut de WSL (50 % de la RAM), car il n'y a **pas de `.wslconfig`**. |
| GPU | NVIDIA GeForce RTX 2060 Max-Q, 6 Go. Il n'est pas utilisé : Lean ne se sert pas du GPU. |
| Disque | C: = SSD NVMe Fanxiang S500PRO 1 To (NTFS), 158 Go libres au départ |

## `.wslconfig`

Absent. Réglage proposé, à créer dans `C:\Users\matis\.wslconfig` :

```
[wsl2]
memory=26GB
processors=16
swap=8GB
```

Ce réglage donnerait environ 70 % de RAM en plus aux builds Lean. **Je ne l'ai pas appliqué** : il exige un `wsl --shutdown` sur le portable, où la distro `kali-linux` tourne (elle est peut-être utilisée). Le contrôleur utilise pour l'instant 15 jobs Lean (`LEAN_NUM_THREADS=15`) dans 15,3 GiB.

## Logiciels

- WSL 3.0.5.0, noyau 6.18.58.1-1, Windows 10.0.26200.9974.
- Distros au départ : `kali-linux` (Running, par défaut) et `Ubuntu` (Stopped).
- Outils de `kali-linux` :

  | Outil | Version / état |
  |---|---|
  | gcc / g++ | 15.2.0 |
  | make | 4.4.1 |
  | python3 | 3.14.7 |
  | pip | 26.0.1 |
  | git | 2.53.0 |
  | curl | 8.21.0 |
  | docker | 28.5.2 |
  | zstd | 1.5.7 |
  | tar, sha256sum | présents |
  | clang, cmake, sage, elan / lean / lake, gh, /usr/bin/time | absents |

- Côté Windows : git 2.52.0.
- Depuis Windows, `ssh -T git@github.com` échoue : `Bad owner or permissions on C:\Users\matis/.ssh/config`. Depuis `kali-linux`, la clé s'authentifie comme deploy key de `arkveld-code/Robotnik`, sans rapport avec ce travail. **Aucun push n'est fait depuis le portable**, conformément à la règle « seul l'utilisateur principal pousse ».

## Espace de travail mis en place

- Nouvelle distro dédiée `rhbuild` (Ubuntu 24.04), installée dans `C:\rh-verif\wsl\` avec `wsl --install Ubuntu-24.04 --name rhbuild --location C:\rh-verif\wsl --no-launch`.
- Même isolation que sur la machine principale :
  - utilisateur `builder` sans sudo ;
  - automount des disques Windows et interop désactivés ;
  - seul `C:\rh-verif\exchange` est monté par root, en lecture seule pour `builder`.
- Préparation : `verify.sh /work/vol --prepare-only` a réussi en 4 min 06 s. Les 14 parts sont OK et tous les marqueurs d'intégrité sont passés (`logs/laptop-prepare-outer.log`).
- Le portable reçoit sa propre file de packets (`state/queue-laptop.txt`). Il ne renvoie que les rapports et les logs, rapatriés par `scp` vers G:. Aucun `.olean` n'est transféré.
