# STATE — vérification distribuée de l'archive Lean d'Alpöge

Mis à jour : 2026-11-21 13:04 UTC

## Résumé

- Chunks vérifiés (build exit 0 + audit axiomes OK) : **77** (4928 modules cibles, 0 imports reconstruits en plus)
- Chunks en échec / non concluants : **0** 
- En cours : main: P0093 (depth 0) since 13:03:41 UTC
- Débit principale : 3219 modules/heure (3264 modules en 1.01 h de build) ; file `state/queue-main.txt` : 51/228 faits ; prochains : P0093, P0094, P0096, P0098, P0100
- Débit portable : 1820 modules/heure (1664 modules en 0.91 h de build) ; file `state/queue-laptop.txt` : 27/172 faits ; prochains : P0063, P0065, P0067, P0069, P0072
- Disque : laptop :  Go libres sur le disque hôte (13:04:09 UTC)
main : 95 Go libres sur le disque hôte (13:03:40 UTC)

## Bloquants / décisions utilisateur

1. **Push GitHub impossible** vers `valstrax-sys/Remman-Proof` : la clé SSH de Kali est une *deploy key en lecture seule* ; la clé Windows (`Hesia-Unit`) n'a pas accès. → Cocher « Allow write access » sur la deploy key (Settings → Deploy keys) **ou** ajouter `Hesia-Unit` comme collaborateur. Ensuite : `cd G:\rh-verif; git push -u origin main` (depuis Kali : `cd /mnt/g/rh-verif && git push -u origin main`). Tous les commits sont locaux en attendant.
2. **Claims impossibles** sur `rohanarun/alpoge-rh-replay` : aucun `gh` authentifié (`gh` 2.23 installé dans Kali par l'agent mais non connecté ; l'API anonyme est en rate-limit). Je ne saisis pas de token. → `gh auth login` par l'utilisateur. Les chunks sont donc choisis **localement** (vérification indépendante, peut recouper des volontaires) ; aucune soumission publique n'a été faite (une soumission exige un claim accordé *avant* le build).
3. **Non bloquant** : `wsl --manage rhbuild --resize 115GB` a échoué (il exige `wsl --shutdown`, que je n'ai pas fait car une session Kali de l'utilisateur est ouverte). Garde-fou appliqué à la place : le contrôleur s'arrête si G: a moins de 20 Go libres. Le VHDX ne rétrécit pas tout seul quand on supprime des fichiers.
- [laptop] arrêt : espace libre hôte ? Go < 20 Go avant P0063 (2026-11-21T13:04:31Z)

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
| [P0020](../reports/P0020.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 115.1 | 2026-11-21T12:19:13 |
| [P0021](../reports/P0021.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 71.5 | 2026-11-21T12:12:11 |
| [P0022](../reports/P0022.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 121.9 | 2026-11-21T12:21:45 |
| [P0023](../reports/P0023.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 66.1 | 2026-11-21T12:13:32 |
| [P0024](../reports/P0024.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 120.6 | 2026-11-21T12:24:14 |
| [P0025](../reports/P0025.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 70.3 | 2026-11-21T12:14:56 |
| [P0026](../reports/P0026.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 75.9 | 2026-11-21T12:16:25 |
| [P0027](../reports/P0027.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 108.0 | 2026-11-21T12:26:28 |
| [P0028](../reports/P0028.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 65.0 | 2026-11-21T12:17:47 |
| [P0029](../reports/P0029.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 202.2 | 2026-11-21T12:30:22 |
| [P0030](../reports/P0030.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 59.2 | 2026-11-21T12:19:01 |
| [P0031](../reports/P0031.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 101.8 | 2026-11-21T12:33:00 |
| [P0032](../reports/P0032.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 60.3 | 2026-11-21T12:20:13 |
| [P0033](../reports/P0033.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 107.8 | 2026-11-21T12:35:19 |
| [P0034](../reports/P0034.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 58.8 | 2026-11-21T12:21:23 |
| [P0035](../reports/P0035.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 65.0 | 2026-11-21T12:22:39 |
| [P0036](../reports/P0036.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 104.8 | 2026-11-21T12:37:32 |
| [P0037](../reports/P0037.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 62.0 | 2026-11-21T12:23:55 |
| [P0038](../reports/P0038.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 115.3 | 2026-11-21T12:39:54 |
| [P0039](../reports/P0039.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 66.1 | 2026-11-21T12:25:14 |
| [P0040](../reports/P0040.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 113.9 | 2026-11-21T12:42:21 |
| [P0041](../reports/P0041.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 62.3 | 2026-11-21T12:26:30 |
| [P0042](../reports/P0042.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 138.0 | 2026-11-21T12:45:08 |
| [P0043](../reports/P0043.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 61.8 | 2026-11-21T12:27:44 |
| [P0044](../reports/P0044.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 70.1 | 2026-11-21T12:29:07 |
| [P0045](../reports/P0045.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 102.8 | 2026-11-21T12:47:23 |
| [P0046](../reports/P0046.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 68.5 | 2026-11-21T12:30:30 |
| [P0047](../reports/P0047.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 93.0 | 2026-11-21T12:49:28 |
| [P0048](../reports/P0048.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 62.6 | 2026-11-21T12:31:46 |
| [P0049](../reports/P0049.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 93.3 | 2026-11-21T12:51:28 |
| [P0050](../reports/P0050.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 54.7 | 2026-11-21T12:32:52 |
| [P0051](../reports/P0051.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 108.2 | 2026-11-21T12:53:45 |
| [P0052](../reports/P0052.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 54.1 | 2026-11-21T12:33:57 |
| [P0053](../reports/P0053.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 55.6 | 2026-11-21T12:35:02 |
| [P0054](../reports/P0054.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 107.0 | 2026-11-21T12:56:01 |
| [P0055](../reports/P0055.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 66.9 | 2026-11-21T12:36:19 |
| [P0056](../reports/P0056.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 103.1 | 2026-11-21T12:58:09 |
| [P0057](../reports/P0057.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 57.4 | 2026-11-21T12:37:29 |
| [P0058](../reports/P0058.md) | portable | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 129.1 | 2026-11-21T13:00:47 |
| [P0059](../reports/P0059.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 60.6 | 2026-11-21T12:38:41 |
| [P0061](../reports/P0061.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 60.8 | 2026-11-21T12:39:55 |
| [P0062](../reports/P0062.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 62.9 | 2026-11-21T12:41:10 |
| [P0064](../reports/P0064.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 62.5 | 2026-11-21T12:42:26 |
| [P0066](../reports/P0066.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 66.4 | 2026-11-21T12:43:46 |
| [P0068](../reports/P0068.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 73.9 | 2026-11-21T12:45:13 |
| [P0070](../reports/P0070.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 62.9 | 2026-11-21T12:46:32 |
| [P0071](../reports/P0071.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 68.7 | 2026-11-21T12:47:54 |
| [P0073](../reports/P0073.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 50.4 | 2026-11-21T12:49:00 |
| [P0075](../reports/P0075.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 95.2 | 2026-11-21T12:50:41 |
| [P0077](../reports/P0077.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 64.0 | 2026-11-21T12:51:57 |
| [P0079](../reports/P0079.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 59.0 | 2026-11-21T12:53:09 |
| [P0080](../reports/P0080.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 132.7 | 2026-11-21T12:55:28 |
| [P0082](../reports/P0082.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 54.1 | 2026-11-21T12:56:42 |
| [P0084](../reports/P0084.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 55.4 | 2026-11-21T12:57:49 |
| [P0086](../reports/P0086.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 70.8 | 2026-11-21T12:59:09 |
| [P0088](../reports/P0088.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 55.9 | 2026-11-21T13:00:21 |
| [P0089](../reports/P0089.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 65.0 | 2026-11-21T13:01:34 |
| [P0091](../reports/P0091.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 91.1 | 2026-11-21T13:03:15 |

## Reprise

Relancer le contrôleur : `bash scripts/controller.sh main` (Git Bash, depuis `G:h-verif`) et `bash scripts/controller.sh laptop`. Chaque contrôleur reprend la file `state/queue-<machine>.txt` en sautant ce qui est dans `state/done-<machine>.txt`. Un chunk interrompu laisse `/work/receipts/<ID>` dans la sandbox : le supprimer (en tant que builder) avant de relancer. Créer `state/STOP` pour arrêter proprement après le chunk courant.
