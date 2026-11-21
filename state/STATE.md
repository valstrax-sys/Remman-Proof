# STATE — vérification distribuée de l'archive Lean d'Alpöge

Mis à jour : 2026-11-21 12:19 UTC

## Résumé

- Chunks vérifiés (build exit 0 + audit axiomes OK) : **25** (1600 modules cibles, 0 imports reconstruits en plus)
- Chunks en échec / non concluants : **0** 
- En cours : laptop: P0020 (depth 0) since 12:17:22 UTC
- Débit principale : 2774 modules/heure (1088 modules en 0.39 h de build) ; file `state/queue-main.txt` : 17/228 faits ; prochains : P0032, P0034, P0035, P0037, P0039
- Débit portable : 1530 modules/heure (512 modules en 0.33 h de build) ; file `state/queue-laptop.txt` : 8/172 faits ; prochains : P0020, P0022, P0024, P0027, P0029
- Disque : laptop : 125 Go libres sur le disque hôte (12:17:20 UTC)
main : 107 Go libres sur le disque hôte (12:19:23 UTC)

## Bloquants / décisions utilisateur

1. **Push GitHub impossible** vers `valstrax-sys/Remman-Proof` : la clé SSH de Kali est une *deploy key en lecture seule* ; la clé Windows (`Hesia-Unit`) n'a pas accès. → Cocher « Allow write access » sur la deploy key (Settings → Deploy keys) **ou** ajouter `Hesia-Unit` comme collaborateur. Ensuite : `cd G:\rh-verif; git push -u origin main` (depuis Kali : `cd /mnt/g/rh-verif && git push -u origin main`). Tous les commits sont locaux en attendant.
2. **Claims impossibles** sur `rohanarun/alpoge-rh-replay` : aucun `gh` authentifié (`gh` 2.23 installé dans Kali par l'agent mais non connecté ; l'API anonyme est en rate-limit). Je ne saisis pas de token. → `gh auth login` par l'utilisateur. Les chunks sont donc choisis **localement** (vérification indépendante, peut recouper des volontaires) ; aucune soumission publique n'a été faite (une soumission exige un claim accordé *avant* le build).
3. **Non bloquant** : `wsl --manage rhbuild --resize 115GB` a échoué (il exige `wsl --shutdown`, que je n'ai pas fait car une session Kali de l'utilisateur est ouverte). Garde-fou appliqué à la place : le contrôleur s'arrête si G: a moins de 20 Go libres. Le VHDX ne rétrécit pas tout seul quand on supprime des fichiers.

## Chunks

| Chunk | Machine | Statut | Modules cibles | Imports reconstruits | Durée build (s) | Fin (UTC) |
|---|---|---|---:|---:|---:|---|
| [P0001](../reports/P0001.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 122.4 | 2026-11-21T11:34:41 |
| [P0002](../reports/P0002.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 356.4 | 2026-11-21T11:58:23 |
| [P0003](../reports/P0003.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 193.0 | 2026-11-21T11:55:22 |
| [P0004](../reports/P0004.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 205.5 | 2026-11-21T12:03:04 |
| [P0005](../reports/P0005.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 104.8 | 2026-11-21T11:57:34 |
| [P0006](../reports/P0006.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 114.7 | 2026-11-21T12:05:35 |
| [P0007](../reports/P0007.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 111.2 | 2026-11-21T12:01:23 |
| [P0008](../reports/P0008.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 69.4 | 2026-11-21T12:02:49 |
| [P0009](../reports/P0009.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 106.9 | 2026-11-21T12:07:54 |
| [P0010](../reports/P0010.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 69.2 | 2026-11-21T12:04:11 |
| [P0011](../reports/P0011.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 107.6 | 2026-11-21T12:10:10 |
| [P0012](../reports/P0012.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 70.0 | 2026-11-21T12:05:35 |
| [P0013](../reports/P0013.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 107.1 | 2026-11-21T12:12:26 |
| [P0014](../reports/P0014.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 59.9 | 2026-11-21T12:06:48 |
| [P0015](../reports/P0015.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 98.4 | 2026-11-21T12:14:33 |
| [P0016](../reports/P0016.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 61.2 | 2026-11-21T12:08:02 |
| [P0017](../reports/P0017.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 82.6 | 2026-11-21T12:09:35 |
| [P0018](../reports/P0018.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 108.2 | 2026-11-21T12:16:49 |
| [P0019](../reports/P0019.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 60.2 | 2026-11-21T12:10:48 |
| [P0021](../reports/P0021.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 71.5 | 2026-11-21T12:12:11 |
| [P0023](../reports/P0023.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 66.1 | 2026-11-21T12:13:32 |
| [P0025](../reports/P0025.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 70.3 | 2026-11-21T12:14:56 |
| [P0026](../reports/P0026.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 75.9 | 2026-11-21T12:16:25 |
| [P0028](../reports/P0028.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 65.0 | 2026-11-21T12:17:47 |
| [P0030](../reports/P0030.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 59.2 | 2026-11-21T12:19:01 |

## Reprise

Relancer le contrôleur : `bash scripts/controller.sh main` (Git Bash, depuis `G:h-verif`) et `bash scripts/controller.sh laptop`. Chaque contrôleur reprend la file `state/queue-<machine>.txt` en sautant ce qui est dans `state/done-<machine>.txt`. Un chunk interrompu laisse `/work/receipts/<ID>` dans la sandbox : le supprimer (en tant que builder) avant de relancer. Créer `state/STOP` pour arrêter proprement après le chunk courant.
