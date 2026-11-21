# STATE — vérification distribuée de l'archive Lean d'Alpöge

Mis à jour : 2026-11-21 14:17 UTC

## Résumé

- Chunks vérifiés (build exit 0 + audit axiomes OK) : **119** (7591 modules cibles, 580 imports reconstruits en plus)
- Chunks en échec / non concluants : **4** P0060 (BUILD OK MAIS CIBLES SANS LIGNE Built), P0063 (BUILD OK MAIS CIBLES SANS LIGNE Built), P0065 (BUILD OK MAIS CIBLES SANS LIGNE Built), P0067 (BUILD OK MAIS CIBLES SANS LIGNE Built)
- En cours : rien
- Débit principale : 3223 modules/heure (6507 modules en 2.02 h de build) ; file `state/queue-main.txt` : 97/228 faits ; prochains : P0166, P0168, P0170, P0172, P0174
- Débit portable : 1820 modules/heure (1664 modules en 0.91 h de build) ; file `state/queue-laptop.txt` : 26/172 faits ; prochains : P0060, P0063, P0065, P0067, P0069
- File partagée `state/queue-shared.txt` (depuis 14:12 UTC, portable injoignable) : 5/282 faits ; prochains : P0069, P0072, P0074, P0076, P0078
- Disque : laptop :  Go libres sur le disque hôte (13:04:09 UTC)
main : 75 Go libres sur le disque hôte (14:17:14 UTC)

## Bloquants / décisions utilisateur

1. **Push GitHub impossible** vers `valstrax-sys/Remman-Proof` : la clé SSH de Kali est une *deploy key en lecture seule* ; la clé Windows (`Hesia-Unit`) n'a pas accès. → Cocher « Allow write access » sur la deploy key (Settings → Deploy keys) **ou** ajouter `Hesia-Unit` comme collaborateur. Ensuite : `cd G:\rh-verif; git push -u origin main` (depuis Kali : `cd /mnt/g/rh-verif && git push -u origin main`). Tous les commits sont locaux en attendant.
2. **Claims impossibles** sur `rohanarun/alpoge-rh-replay` : aucun `gh` authentifié (`gh` 2.23 installé dans Kali par l'agent mais non connecté ; l'API anonyme est en rate-limit). Je ne saisis pas de token. → `gh auth login` par l'utilisateur. Les chunks sont donc choisis **localement** (vérification indépendante, peut recouper des volontaires) ; aucune soumission publique n'a été faite (une soumission exige un claim accordé *avant* le build).
3. **Non bloquant** : `wsl --manage rhbuild --resize 115GB` a échoué (il exige `wsl --shutdown`, que je n'ai pas fait car une session Kali de l'utilisateur est ouverte). Garde-fou appliqué à la place : le contrôleur s'arrête si G: a moins de 20 Go libres. Le VHDX ne rétrécit pas tout seul quand on supprime des fichiers.
- [laptop] arrêt : espace libre hôte ? Go < 20 Go avant P0063 (2026-11-21T13:04:31Z)
4. **Portable injoignable depuis ~13:01 UTC** (SSH timeout, hôte injoignable au ping) — probablement mise en veille Windows. Le chunk P0060 en cours a été perdu (sera relancé proprement : sorties des cibles supprimées puis recompilées). Je ne modifie pas les réglages d'alimentation du portable (réglage système). → Désactiver la veille sur secteur (`powercfg /change standby-timeout-ac 0`) si vous voulez qu'il travaille la nuit. Le contrôleur v2 l'attend jusqu'à 6 h et reprend automatiquement.

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
| [P0060](../reports/P0060.md) | principale | BUILD OK MAIS CIBLES SANS LIGNE Built | 64 | 0 | 41.7 | 2026-11-21T14:13:12 |
| [P0061](../reports/P0061.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 60.8 | 2026-11-21T12:39:55 |
| [P0062](../reports/P0062.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 62.9 | 2026-11-21T12:41:10 |
| [P0063](../reports/P0063.md) | principale | BUILD OK MAIS CIBLES SANS LIGNE Built | 64 | 0 | 47.1 | 2026-11-21T14:14:14 |
| [P0064](../reports/P0064.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 62.5 | 2026-11-21T12:42:26 |
| [P0065](../reports/P0065.md) | principale | BUILD OK MAIS CIBLES SANS LIGNE Built | 64 | 0 | 65.5 | 2026-11-21T14:15:34 |
| [P0066](../reports/P0066.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 66.4 | 2026-11-21T12:43:46 |
| [P0067](../reports/P0067.md) | principale | BUILD OK MAIS CIBLES SANS LIGNE Built | 64 | 0 | 57.8 | 2026-11-21T14:16:49 |
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
| [P0093](../reports/P0093.md) | principale | VÉRIFIÉ (build + audit axiomes) | 39 | 0 | 43.8 | 2026-11-21T13:04:16 |
| [P0094](../reports/P0094.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 8 | 75.3 | 2026-11-21T13:05:42 |
| [P0096](../reports/P0096.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 21 | 143.0 | 2026-11-21T13:08:16 |
| [P0098](../reports/P0098.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 13 | 195.9 | 2026-11-21T13:11:46 |
| [P0100](../reports/P0100.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 13 | 127.3 | 2026-11-21T13:14:27 |
| [P0101](../reports/P0101.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 11 | 74.1 | 2026-11-21T13:15:54 |
| [P0103](../reports/P0103.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 10 | 62.1 | 2026-11-21T13:17:09 |
| [P0105](../reports/P0105.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 9 | 63.7 | 2026-11-21T13:18:23 |
| [P0107](../reports/P0107.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 7 | 62.5 | 2026-11-21T13:19:37 |
| [P0109](../reports/P0109.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 4 | 59.6 | 2026-11-21T13:20:48 |
| [P0110](../reports/P0110.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 8 | 78.4 | 2026-11-21T13:22:17 |
| [P0112](../reports/P0112.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 20 | 106.7 | 2026-11-21T13:24:10 |
| [P0114](../reports/P0114.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 14 | 71.5 | 2026-11-21T13:25:30 |
| [P0116](../reports/P0116.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 15 | 72.7 | 2026-11-21T13:26:54 |
| [P0117](../reports/P0117.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 8 | 68.5 | 2026-11-21T13:28:14 |
| [P0119](../reports/P0119.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 21 | 86.3 | 2026-11-21T13:29:54 |
| [P0121](../reports/P0121.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 12 | 71.7 | 2026-11-21T13:31:19 |
| [P0122](../reports/P0122.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 34 | 83.6 | 2026-11-21T13:32:52 |
| [P0124](../reports/P0124.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 11 | 69.9 | 2026-11-21T13:34:12 |
| [P0126](../reports/P0126.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 32 | 89.5 | 2026-11-21T13:35:49 |
| [P0128](../reports/P0128.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 11 | 100.3 | 2026-11-21T13:37:38 |
| [P0129](../reports/P0129.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 21 | 79.4 | 2026-11-21T13:39:13 |
| [P0131](../reports/P0131.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 5 | 85.8 | 2026-11-21T13:40:47 |
| [P0133](../reports/P0133.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 10 | 87.4 | 2026-11-21T13:42:24 |
| [P0135](../reports/P0135.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 9 | 72.6 | 2026-11-21T13:43:50 |
| [P0136](../reports/P0136.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 19 | 89.8 | 2026-11-21T13:45:32 |
| [P0138](../reports/P0138.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 27 | 108.2 | 2026-11-21T13:47:30 |
| [P0140](../reports/P0140.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 3 | 64.8 | 2026-11-21T13:48:46 |
| [P0141](../reports/P0141.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 3 | 64.0 | 2026-11-21T13:50:01 |
| [P0143](../reports/P0143.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 22 | 76.5 | 2026-11-21T13:51:29 |
| [P0145](../reports/P0145.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 20 | 93.5 | 2026-11-21T13:53:12 |
| [P0146](../reports/P0146.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 5 | 81.2 | 2026-11-21T13:54:48 |
| [P0149](../reports/P0149.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 9 | 79.1 | 2026-11-21T13:56:22 |
| [P0150](../reports/P0150.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 29 | 93.0 | 2026-11-21T13:58:08 |
| [P0152](../reports/P0152.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 16 | 109.5 | 2026-11-21T14:00:09 |
| [P0154](../reports/P0154.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 34 | 89.7 | 2026-11-21T14:01:57 |
| [P0156](../reports/P0156.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 73.5 | 2026-11-21T14:03:22 |
| [P0157](../reports/P0157.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 20 | 88.7 | 2026-11-21T14:05:04 |
| [P0159](../reports/P0159.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 143.3 | 2026-11-21T14:07:36 |
| [P0161](../reports/P0161.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 11 | 76.8 | 2026-11-21T14:09:13 |
| [P0162](../reports/P0162.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 22 | 73.9 | 2026-11-21T14:10:39 |
| [P0164](../reports/P0164.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 11 | 79.6 | 2026-11-21T14:12:07 |

## Reprise

Relancer les contrôleurs (Git Bash, depuis `G:\rh-verif`) : `QUEUE=state/queue-shared.txt bash scripts/controller.sh main` et `QUEUE=state/queue-shared.txt bash scripts/controller.sh laptop`. File partagée : chaque machine saute ce qui figure dans `state/done-main.txt` / `state/done-laptop.txt` ou est en cours sur l'autre (`state/running-*.txt`). Un chunk interrompu est repris proprement (`pre-chunk.sh` : ancienne tentative déplacée dans `/work/receipts/aborted/`, sorties des cibles supprimées puis recompilées). Créer `state/STOP` (ou `state/STOP-<machine>`) pour arrêter proprement après le chunk courant ; `state/jobs-<machine>.txt` règle le parallélisme.
