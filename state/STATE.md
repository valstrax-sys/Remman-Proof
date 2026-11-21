# STATE — vérification distribuée de l'archive Lean d'Alpöge

Mis à jour : 2026-11-21 17:22 UTC

## Résumé

- Chunks vérifiés (build exit 0 + audit axiomes OK) : **239** (15236 modules cibles, 1052 imports reconstruits en plus)
- Chunks en échec / non concluants : **0** 
- En cours : rien
- Débit principale : 3100 modules/heure (14624 modules en 4.72 h de build) ; file `state/queue-main.txt` : 213/228 faits ; prochains : P0240, P0241, P0243, P0245, P0247
- Débit portable : 1820 modules/heure (1664 modules en 0.91 h de build) ; file `state/queue-laptop.txt` : 26/172 faits ; prochains : P0060, P0063, P0065, P0067, P0069
- File partagée `state/queue-shared.txt` (depuis 14:12 UTC, portable injoignable) : 121/282 faits ; prochains : P0240, P0241, P0242, P0243, P0244
- Disque : laptop :  Go libres sur le disque hôte (13:04:09 UTC)
main : 31 Go libres sur le disque hôte (17:22:03 UTC)

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
| [P0060](../reports/P0060.md) | principale | VÉRIFIÉ (build + audit axiomes ; 27 cibles compilées par un chunk antérieur) | 64 | 0 | 41.7 | 2026-11-21T14:13:12 |
| [P0061](../reports/P0061.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 60.8 | 2026-11-21T12:39:55 |
| [P0062](../reports/P0062.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 62.9 | 2026-11-21T12:41:10 |
| [P0063](../reports/P0063.md) | principale | VÉRIFIÉ (build + audit axiomes ; 18 cibles compilées par un chunk antérieur) | 64 | 0 | 47.1 | 2026-11-21T14:14:14 |
| [P0064](../reports/P0064.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 62.5 | 2026-11-21T12:42:26 |
| [P0065](../reports/P0065.md) | principale | VÉRIFIÉ (build + audit axiomes ; 4 cibles compilées par un chunk antérieur) | 64 | 0 | 65.5 | 2026-11-21T14:15:34 |
| [P0066](../reports/P0066.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 66.4 | 2026-11-21T12:43:46 |
| [P0067](../reports/P0067.md) | principale | VÉRIFIÉ (build + audit axiomes ; 15 cibles compilées par un chunk antérieur) | 64 | 0 | 57.8 | 2026-11-21T14:16:49 |
| [P0068](../reports/P0068.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 73.9 | 2026-11-21T12:45:13 |
| [P0069](../reports/P0069.md) | principale | VÉRIFIÉ (build + audit axiomes ; 10 cibles compilées par un chunk antérieur) | 64 | 0 | 57.7 | 2026-11-21T14:18:03 |
| [P0070](../reports/P0070.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 62.9 | 2026-11-21T12:46:32 |
| [P0071](../reports/P0071.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 68.7 | 2026-11-21T12:47:54 |
| [P0072](../reports/P0072.md) | principale | VÉRIFIÉ (build + audit axiomes ; 44 cibles compilées par un chunk antérieur) | 64 | 0 | 24.8 | 2026-11-21T14:18:44 |
| [P0073](../reports/P0073.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 50.4 | 2026-11-21T12:49:00 |
| [P0074](../reports/P0074.md) | principale | VÉRIFIÉ (build + audit axiomes ; 20 cibles compilées par un chunk antérieur) | 64 | 0 | 44.3 | 2026-11-21T14:19:42 |
| [P0075](../reports/P0075.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 95.2 | 2026-11-21T12:50:41 |
| [P0076](../reports/P0076.md) | principale | VÉRIFIÉ (build + audit axiomes ; 15 cibles compilées par un chunk antérieur) | 64 | 0 | 57.7 | 2026-11-21T14:20:51 |
| [P0077](../reports/P0077.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 64.0 | 2026-11-21T12:51:57 |
| [P0078](../reports/P0078.md) | principale | VÉRIFIÉ (build + audit axiomes ; 16 cibles compilées par un chunk antérieur) | 64 | 0 | 52.3 | 2026-11-21T14:21:57 |
| [P0079](../reports/P0079.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 59.0 | 2026-11-21T12:53:09 |
| [P0080](../reports/P0080.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 132.7 | 2026-11-21T12:55:28 |
| [P0081](../reports/P0081.md) | principale | VÉRIFIÉ (build + audit axiomes ; 15 cibles compilées par un chunk antérieur) | 64 | 0 | 75.6 | 2026-11-21T14:23:28 |
| [P0082](../reports/P0082.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 54.1 | 2026-11-21T12:56:42 |
| [P0083](../reports/P0083.md) | principale | VÉRIFIÉ (build + audit axiomes ; 29 cibles compilées par un chunk antérieur) | 64 | 0 | 33.0 | 2026-11-21T14:24:22 |
| [P0084](../reports/P0084.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 55.4 | 2026-11-21T12:57:49 |
| [P0085](../reports/P0085.md) | principale | VÉRIFIÉ (build + audit axiomes ; 4 cibles compilées par un chunk antérieur) | 64 | 0 | 56.8 | 2026-11-21T14:25:29 |
| [P0086](../reports/P0086.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 70.8 | 2026-11-21T12:59:09 |
| [P0087](../reports/P0087.md) | principale | VÉRIFIÉ (build + audit axiomes ; 5 cibles compilées par un chunk antérieur) | 64 | 0 | 55.7 | 2026-11-21T14:26:38 |
| [P0088](../reports/P0088.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 55.9 | 2026-11-21T13:00:21 |
| [P0089](../reports/P0089.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 65.0 | 2026-11-21T13:01:34 |
| [P0090](../reports/P0090.md) | principale | VÉRIFIÉ (build + audit axiomes ; 12 cibles compilées par un chunk antérieur) | 64 | 0 | 58.7 | 2026-11-21T14:27:48 |
| [P0091](../reports/P0091.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 91.1 | 2026-11-21T13:03:15 |
| [P0092](../reports/P0092.md) | principale | VÉRIFIÉ (build + audit axiomes ; 6 cibles compilées par un chunk antérieur) | 64 | 0 | 64.9 | 2026-11-21T14:29:09 |
| [P0093](../reports/P0093.md) | principale | VÉRIFIÉ (build + audit axiomes) | 39 | 0 | 43.8 | 2026-11-21T13:04:16 |
| [P0094](../reports/P0094.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 8 | 75.3 | 2026-11-21T13:05:42 |
| [P0095](../reports/P0095.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 6 | 138.9 | 2026-11-21T14:31:37 |
| [P0096](../reports/P0096.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 21 | 143.0 | 2026-11-21T13:08:16 |
| [P0097](../reports/P0097.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 3 | 68.0 | 2026-11-21T14:33:07 |
| [P0098](../reports/P0098.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 13 | 195.9 | 2026-11-21T13:11:46 |
| [P0099](../reports/P0099.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 22 | 110.7 | 2026-11-21T14:35:06 |
| [P0100](../reports/P0100.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 13 | 127.3 | 2026-11-21T13:14:27 |
| [P0101](../reports/P0101.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 11 | 74.1 | 2026-11-21T13:15:54 |
| [P0102](../reports/P0102.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 37 | 97.9 | 2026-11-21T14:36:58 |
| [P0103](../reports/P0103.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 10 | 62.1 | 2026-11-21T13:17:09 |
| [P0104](../reports/P0104.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 42 | 96.8 | 2026-11-21T14:38:44 |
| [P0105](../reports/P0105.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 9 | 63.7 | 2026-11-21T13:18:23 |
| [P0106](../reports/P0106.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 52 | 105.2 | 2026-11-21T14:40:37 |
| [P0107](../reports/P0107.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 7 | 62.5 | 2026-11-21T13:19:37 |
| [P0108](../reports/P0108.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 25 | 86.6 | 2026-11-21T14:42:12 |
| [P0109](../reports/P0109.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 4 | 59.6 | 2026-11-21T13:20:48 |
| [P0110](../reports/P0110.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 8 | 78.4 | 2026-11-21T13:22:17 |
| [P0111](../reports/P0111.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 35 | 91.6 | 2026-11-21T14:43:53 |
| [P0112](../reports/P0112.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 20 | 106.7 | 2026-11-21T13:24:10 |
| [P0113](../reports/P0113.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 34 | 95.9 | 2026-11-21T14:45:38 |
| [P0114](../reports/P0114.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 14 | 71.5 | 2026-11-21T13:25:30 |
| [P0115](../reports/P0115.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 23 | 82.9 | 2026-11-21T14:47:11 |
| [P0116](../reports/P0116.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 15 | 72.7 | 2026-11-21T13:26:54 |
| [P0117](../reports/P0117.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 8 | 68.5 | 2026-11-21T13:28:14 |
| [P0118](../reports/P0118.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 76.1 | 2026-11-21T14:48:37 |
| [P0119](../reports/P0119.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 21 | 86.3 | 2026-11-21T13:29:54 |
| [P0120](../reports/P0120.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 25 | 174.3 | 2026-11-21T14:51:36 |
| [P0121](../reports/P0121.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 12 | 71.7 | 2026-11-21T13:31:19 |
| [P0122](../reports/P0122.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 34 | 83.6 | 2026-11-21T13:32:52 |
| [P0123](../reports/P0123.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 27 | 86.6 | 2026-11-21T14:53:35 |
| [P0124](../reports/P0124.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 11 | 69.9 | 2026-11-21T13:34:12 |
| [P0125](../reports/P0125.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 13 | 72.9 | 2026-11-21T14:54:58 |
| [P0126](../reports/P0126.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 32 | 89.5 | 2026-11-21T13:35:49 |
| [P0127](../reports/P0127.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 28 | 94.1 | 2026-11-21T14:56:41 |
| [P0128](../reports/P0128.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 11 | 100.3 | 2026-11-21T13:37:38 |
| [P0129](../reports/P0129.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 21 | 79.4 | 2026-11-21T13:39:13 |
| [P0130](../reports/P0130.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 23 | 97.7 | 2026-11-21T14:58:30 |
| [P0131](../reports/P0131.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 5 | 85.8 | 2026-11-21T13:40:47 |
| [P0132](../reports/P0132.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 64.0 | 2026-11-21T14:59:48 |
| [P0133](../reports/P0133.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 10 | 87.4 | 2026-11-21T13:42:24 |
| [P0134](../reports/P0134.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 13 | 78.7 | 2026-11-21T15:01:18 |
| [P0135](../reports/P0135.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 9 | 72.6 | 2026-11-21T13:43:50 |
| [P0136](../reports/P0136.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 19 | 89.8 | 2026-11-21T13:45:32 |
| [P0137](../reports/P0137.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 4 | 72.0 | 2026-11-21T15:02:44 |
| [P0138](../reports/P0138.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 27 | 108.2 | 2026-11-21T13:47:30 |
| [P0139](../reports/P0139.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 62.6 | 2026-11-21T15:04:00 |
| [P0140](../reports/P0140.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 3 | 64.8 | 2026-11-21T13:48:46 |
| [P0141](../reports/P0141.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 3 | 64.0 | 2026-11-21T13:50:01 |
| [P0142](../reports/P0142.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 2 | 64.4 | 2026-11-21T15:05:16 |
| [P0143](../reports/P0143.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 22 | 76.5 | 2026-11-21T13:51:29 |
| [P0144](../reports/P0144.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 79.9 | 2026-11-21T15:06:45 |
| [P0145](../reports/P0145.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 20 | 93.5 | 2026-11-21T13:53:12 |
| [P0146](../reports/P0146.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 5 | 81.2 | 2026-11-21T13:54:48 |
| [P0147](../reports/P0147.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 81.7 | 2026-11-21T15:08:22 |
| [P0148](../reports/P0148.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 111.2 | 2026-11-21T15:10:26 |
| [P0149](../reports/P0149.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 9 | 79.1 | 2026-11-21T13:56:22 |
| [P0150](../reports/P0150.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 29 | 93.0 | 2026-11-21T13:58:08 |
| [P0151](../reports/P0151.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 64.9 | 2026-11-21T15:11:54 |
| [P0152](../reports/P0152.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 16 | 109.5 | 2026-11-21T14:00:09 |
| [P0153](../reports/P0153.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 71.8 | 2026-11-21T15:13:15 |
| [P0154](../reports/P0154.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 34 | 89.7 | 2026-11-21T14:01:57 |
| [P0155](../reports/P0155.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 74.8 | 2026-11-21T15:14:43 |
| [P0156](../reports/P0156.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 73.5 | 2026-11-21T14:03:22 |
| [P0157](../reports/P0157.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 20 | 88.7 | 2026-11-21T14:05:04 |
| [P0158](../reports/P0158.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 86.4 | 2026-11-21T15:16:21 |
| [P0159](../reports/P0159.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 143.3 | 2026-11-21T14:07:36 |
| [P0160](../reports/P0160.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 2 | 93.8 | 2026-11-21T15:18:10 |
| [P0161](../reports/P0161.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 11 | 76.8 | 2026-11-21T14:09:13 |
| [P0162](../reports/P0162.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 22 | 73.9 | 2026-11-21T14:10:39 |
| [P0163](../reports/P0163.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 68.3 | 2026-11-21T15:19:38 |
| [P0164](../reports/P0164.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 11 | 79.6 | 2026-11-21T14:12:07 |
| [P0165](../reports/P0165.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 121.8 | 2026-11-21T15:21:47 |
| [P0166](../reports/P0166.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 91.7 | 2026-11-21T15:23:32 |
| [P0167](../reports/P0167.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 88.7 | 2026-11-21T15:25:18 |
| [P0168](../reports/P0168.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 91.1 | 2026-11-21T15:27:04 |
| [P0169](../reports/P0169.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 76.0 | 2026-11-21T15:28:38 |
| [P0170](../reports/P0170.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 70.6 | 2026-11-21T15:30:04 |
| [P0171](../reports/P0171.md) | principale | VÉRIFIÉ (build + audit axiomes) | 51 | 0 | 60.8 | 2026-11-21T15:31:20 |
| [P0172](../reports/P0172.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 65.9 | 2026-11-21T15:32:40 |
| [P0173](../reports/P0173.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 292.6 | 2026-11-21T15:37:24 |
| [P0174](../reports/P0174.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 117.1 | 2026-11-21T15:39:38 |
| [P0175](../reports/P0175.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 59.0 | 2026-11-21T15:40:58 |
| [P0176](../reports/P0176.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 5 | 234.2 | 2026-11-21T15:44:48 |
| [P0177](../reports/P0177.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 2 | 84.1 | 2026-11-21T15:46:21 |
| [P0178](../reports/P0178.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 66.6 | 2026-11-21T15:47:44 |
| [P0179](../reports/P0179.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 62.7 | 2026-11-21T15:49:00 |
| [P0180](../reports/P0180.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 70.0 | 2026-11-21T15:50:23 |
| [P0181](../reports/P0181.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 71.6 | 2026-11-21T15:51:47 |
| [P0182](../reports/P0182.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 65.8 | 2026-11-21T15:53:07 |
| [P0183](../reports/P0183.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 64.4 | 2026-11-21T15:54:26 |
| [P0184](../reports/P0184.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 64.5 | 2026-11-21T15:55:44 |
| [P0185](../reports/P0185.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 76.1 | 2026-11-21T15:57:12 |
| [P0186](../reports/P0186.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 68.1 | 2026-11-21T15:58:33 |
| [P0187](../reports/P0187.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 67.1 | 2026-11-21T15:59:54 |
| [P0188](../reports/P0188.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 2 | 72.4 | 2026-11-21T16:01:19 |
| [P0189](../reports/P0189.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 73.9 | 2026-11-21T16:02:45 |
| [P0190](../reports/P0190.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 98.2 | 2026-11-21T16:04:35 |
| [P0191](../reports/P0191.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 73.5 | 2026-11-21T16:06:12 |
| [P0192](../reports/P0192.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 73.7 | 2026-11-21T16:07:40 |
| [P0193](../reports/P0193.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 70.4 | 2026-11-21T16:09:02 |
| [P0194](../reports/P0194.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 2 | 81.0 | 2026-11-21T16:10:35 |
| [P0195](../reports/P0195.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 11 | 82.8 | 2026-11-21T16:12:14 |
| [P0196](../reports/P0196.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 2 | 91.5 | 2026-11-21T16:13:58 |
| [P0197](../reports/P0197.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 75.0 | 2026-11-21T16:15:28 |
| [P0198](../reports/P0198.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 78.8 | 2026-11-21T16:17:03 |
| [P0199](../reports/P0199.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 74.4 | 2026-11-21T16:18:31 |
| [P0200](../reports/P0200.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 69.8 | 2026-11-21T16:19:54 |
| [P0201](../reports/P0201.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 88.0 | 2026-11-21T16:21:33 |
| [P0202](../reports/P0202.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 2 | 69.7 | 2026-11-21T16:23:02 |
| [P0203](../reports/P0203.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 3 | 81.9 | 2026-11-21T16:24:36 |
| [P0204](../reports/P0204.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 67.8 | 2026-11-21T16:26:00 |
| [P0205](../reports/P0205.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 64.4 | 2026-11-21T16:27:17 |
| [P0206](../reports/P0206.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 65.1 | 2026-11-21T16:28:35 |
| [P0207](../reports/P0207.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 65.9 | 2026-11-21T16:29:52 |
| [P0208](../reports/P0208.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 72.6 | 2026-11-21T16:31:17 |
| [P0209](../reports/P0209.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 75.4 | 2026-11-21T16:32:45 |
| [P0210](../reports/P0210.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 75.0 | 2026-11-21T16:34:16 |
| [P0211](../reports/P0211.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 94.9 | 2026-11-21T16:36:06 |
| [P0212](../reports/P0212.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 102.7 | 2026-11-21T16:38:08 |
| [P0213](../reports/P0213.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 100.1 | 2026-11-21T16:40:07 |
| [P0214](../reports/P0214.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 91.3 | 2026-11-21T16:41:59 |
| [P0215](../reports/P0215.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 80.2 | 2026-11-21T16:43:32 |
| [P0216](../reports/P0216.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 63.9 | 2026-11-21T16:44:53 |
| [P0217](../reports/P0217.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 73.9 | 2026-11-21T16:46:18 |
| [P0218](../reports/P0218.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 2 | 74.2 | 2026-11-21T16:47:47 |
| [P0219](../reports/P0219.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 72.6 | 2026-11-21T16:49:12 |
| [P0220](../reports/P0220.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 69.8 | 2026-11-21T16:50:35 |
| [P0221](../reports/P0221.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 97.6 | 2026-11-21T16:52:27 |
| [P0222](../reports/P0222.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 77.9 | 2026-11-21T16:54:02 |
| [P0223](../reports/P0223.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 84.6 | 2026-11-21T16:55:43 |
| [P0224](../reports/P0224.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 101.0 | 2026-11-21T16:57:40 |
| [P0225](../reports/P0225.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 87.2 | 2026-11-21T16:59:30 |
| [P0226](../reports/P0226.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 73.7 | 2026-11-21T17:01:01 |
| [P0227](../reports/P0227.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 59.3 | 2026-11-21T17:02:12 |
| [P0228](../reports/P0228.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 73.0 | 2026-11-21T17:03:32 |
| [P0229](../reports/P0229.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 74.6 | 2026-11-21T17:05:00 |
| [P0230](../reports/P0230.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 70.7 | 2026-11-21T17:06:22 |
| [P0231](../reports/P0231.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 95.8 | 2026-11-21T17:08:09 |
| [P0232](../reports/P0232.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 85.3 | 2026-11-21T17:09:50 |
| [P0233](../reports/P0233.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 80.2 | 2026-11-21T17:11:30 |
| [P0234](../reports/P0234.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 1 | 87.7 | 2026-11-21T17:13:10 |
| [P0235](../reports/P0235.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 81.7 | 2026-11-21T17:14:49 |
| [P0236](../reports/P0236.md) | principale | VÉRIFIÉ (build + audit axiomes) | 42 | 0 | 59.6 | 2026-11-21T17:16:03 |
| [P0237](../reports/P0237.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 80.1 | 2026-11-21T17:17:35 |
| [P0238](../reports/P0238.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 2 | 98.9 | 2026-11-21T17:19:28 |
| [P0239](../reports/P0239.md) | principale | VÉRIFIÉ (build + audit axiomes) | 64 | 0 | 107.4 | 2026-11-21T17:21:32 |

## Reprise

Relancer les contrôleurs (Git Bash, depuis `G:\rh-verif`) : `QUEUE=state/queue-shared.txt bash scripts/controller.sh main` et `QUEUE=state/queue-shared.txt bash scripts/controller.sh laptop`. File partagée : chaque machine saute ce qui figure dans `state/done-main.txt` / `state/done-laptop.txt` ou est en cours sur l'autre (`state/running-*.txt`). Un chunk interrompu est repris proprement (`pre-chunk.sh` : ancienne tentative déplacée dans `/work/receipts/aborted/`, sorties des cibles supprimées puis recompilées). Créer `state/STOP` (ou `state/STOP-<machine>`) pour arrêter proprement après le chunk courant ; `state/jobs-<machine>.txt` règle le parallélisme.
