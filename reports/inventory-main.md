# Inventaire — machine principale (Arkveld)

Relevé le 2026-11-21 (≈11:20–11:40 UTC) par l'agent. Logs bruts : `logs/inventory/main-windows.txt`, `logs/inventory/main-kali.txt`, `logs/inventory/main-rhbuild.txt`.

## Matériel

| Élément | Valeur |
|---|---|
| CPU | AMD Ryzen 7 5800X, 8 cœurs physiques / 16 threads logiques (`Win32_Processor`) |
| CPU visibles par WSL | 12 (`nproc`, limité par `processors=12` dans `.wslconfig`) |
| RAM physique | 23,9 Go (Windows) |
| RAM visible par WSL | 19 GiB total, 12 GiB de swap (`free -g`), conforme à `memory=20GB`, `swap=12GB` |
| GPU | NVIDIA GeForce RTX 3080 10 Go, pilote 580.88 (visible sous Windows et WSL) |
| Disque de travail | G: = SSD NVMe 256 Go, NTFS, 134,6 Go libres au départ |
| Autres disques | C: 8,5 Go libres (critique : ne rien y écrire), D: 20 Go, E: 297 Go, F: 313 Go |

**GPU** : Lean n'utilise pas le GPU pour compiler ni pour vérifier dans le noyau. La RTX 3080 n'est pas utilisée pour la vérification.

## `.wslconfig` (`%UserProfile%\.wslconfig`)

```
[wsl2]
memory=20GB
processors=12
swap=12GB
nestedVirtualization=false
```

Réglage proposé pour une machine de 24 Go : `memory=20GB` (on le garde, cela laisse environ 4 Go à Windows), `processors=15` (au lieu de 12, pour un job Lean de plus) et `swap=16GB`.
**Non appliqué** : il faudrait un `wsl --shutdown`, et la distro Kali a une session de login ouverte depuis plus de 1 h 30 (le shell `-bash` de l'utilisateur). Je ne la coupe pas sans accord. Le gain attendu est faible, environ +25 % de CPU, et la limite réelle est la RAM.

## Logiciels

- WSL 2.6.3.0, noyau 6.6.87.2-1, Windows 10.0.26200.9457.
- Distros au départ : `Kali` (Running, WSL2, Kali Rolling 2025.3, utilisateur root) et `docker-desktop` (Stopped).
  - Remarque : le prompt parle de `kali-linux`, mais sur cette machine la distro s'appelle `Kali`. Sur le portable, elle s'appelle bien `kali-linux`.
- Outils dans Kali :

  | Outil | Version / état |
  |---|---|
  | gcc / g++ | 15.2.0 |
  | clang | 21.1.8 |
  | make | 4.4.1 |
  | cmake | 3.31.6 |
  | python3 | 3.13.12 |
  | pip | 26.1.1 |
  | git | 2.53.0 |
  | curl | 8.20.0 |
  | zstd | 1.5.7 |
  | sage | 10.9 |
  | docker | client Windows dans le PATH |
  | elan / lean / lake | **absents** (installés seulement dans la sandbox de build) |
  | gh | **absent** |
  | /usr/bin/time | absent |

- Côté Windows : git 2.53.0, pas de `gh`.

## Accès

| Test | Résultat |
|---|---|
| `ssh matis@192.168.1.143` (portable) | Échec avec les clés par défaut. **OK** avec `-i ~/.ssh/id_ed25519_remote` (côté Windows). Le portable tourne sous Windows (shell `cmd`), pas sous Linux. |
| `ssh -T git@github.com` depuis Kali | Authentifié comme **deploy key de `valstrax-sys/Remman-Proof`** |
| `ssh -T git@github.com` depuis Windows | Authentifié comme l'utilisateur **`Hesia-Unit`** (clé `id_ed25519_hesia`) |
| Clone de `valstrax-sys/Remman-Proof` | OK (dépôt vide) |
| Push de la branche `agent-healthcheck` (deploy key Kali) | **ÉCHEC** : `The key you are authenticating with has been marked as read only` |
| Push de la branche `agent-healthcheck` (Hesia-Unit) | **ÉCHEC** : `Permission to valstrax-sys/Remman-Proof.git denied to Hesia-Unit` |
| `gh` (claims du projet distribué) | **ABSENT / non authentifié**. Les claims ne peuvent pas être ouverts. |

### Bloquants (décision de l'utilisateur requise)

1. **Push impossible** vers le dépôt de rapports. Corrections possibles, au choix :
   - cocher « Allow write access » sur la deploy key de Kali, dans *Settings → Deploy keys* de `valstrax-sys/Remman-Proof` ;
   - ajouter `Hesia-Unit` comme collaborateur.

   En attendant, tout est commité **localement** dans `G:\rh-verif` (branche `main`), prêt à être poussé.
2. **Claims sur `rohanarun/alpoge-rh-replay` impossibles** : pas de `gh` authentifié. Il faut lancer `gh auth login` (installation de `gh` dans Kali puis connexion interactive, à faire par l'utilisateur ; je ne saisis jamais de token).
   - En attendant, les chunks sont choisis **localement** (§5.1 du prompt), sans réservation publique. Ce sont donc des vérifications indépendantes qui peuvent recouper le travail d'autres volontaires.
   - Aucune issue n'a été ouverte et aucun résultat n'a été publié.
