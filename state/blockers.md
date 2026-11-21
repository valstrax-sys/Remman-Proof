1. **Push GitHub impossible** vers `valstrax-sys/Remman-Proof` : la clé SSH de Kali est une *deploy key en lecture seule* ; la clé Windows (`Hesia-Unit`) n'a pas accès. → Cocher « Allow write access » sur la deploy key (Settings → Deploy keys) **ou** ajouter `Hesia-Unit` comme collaborateur. Ensuite : `cd G:\rh-verif; git push -u origin main` (depuis Kali : `cd /mnt/g/rh-verif && git push -u origin main`). Tous les commits sont locaux en attendant.
2. **Claims impossibles** sur `rohanarun/alpoge-rh-replay` : aucun `gh` authentifié (`gh` 2.23 installé dans Kali par l'agent mais non connecté ; l'API anonyme est en rate-limit). Je ne saisis pas de token. → `gh auth login` par l'utilisateur. Les chunks sont donc choisis **localement** (vérification indépendante, peut recouper des volontaires) ; aucune soumission publique n'a été faite (une soumission exige un claim accordé *avant* le build).
3. **Non bloquant** : `wsl --manage rhbuild --resize 115GB` a échoué (il exige `wsl --shutdown`, que je n'ai pas fait car une session Kali de l'utilisateur est ouverte). Garde-fou appliqué à la place : le contrôleur s'arrête si G: a moins de 20 Go libres. Le VHDX ne rétrécit pas tout seul quand on supprime des fichiers.
- [laptop] arrêt : espace libre hôte ? Go < 20 Go avant P0063 (2026-11-21T13:04:31Z)
4. **Portable injoignable depuis ~13:01 UTC** (SSH timeout, hôte injoignable au ping) — probablement mise en veille Windows. Le chunk P0060 en cours a été perdu (sera relancé proprement : sorties des cibles supprimées puis recompilées). Je ne modifie pas les réglages d'alimentation du portable (réglage système). → Désactiver la veille sur secteur (`powercfg /change standby-timeout-ac 0`) si vous voulez qu'il travaille la nuit. Le contrôleur v2 l'attend jusqu'à 6 h et reprend automatiquement.
- [main] arrêt : espace libre hôte 19 Go < 20 Go avant P0273 (2026-11-21T18:14:27Z)
- [main] 18:14 UTC : seuil abaissé de 20 à 17 Go (croissance max mesurée par chunk : 0,69 Go → reste ≥ 16 Go ≥ 15 Go exigés).
5. **Disque G: : décision utilisateur pour aller plus loin.**
   - Le VHDX de la sandbox fait 118 Go et ne rétrécit pas tout seul. Après le nettoyage des `*.setup.json` (89 Go libérés dans l'ext4, voir `reports/workspace.md`), l'ext4 n'utilise plus que 25 Go, mais G: n'a que 19 Go libres.
   - L'espace libéré dans l'ext4 est réutilisé par les chunks suivants, donc le VHDX devrait cesser de grossir. Le garde-fou (17 Go) reste actif.
   - Pour rendre l'espace à G:, au choix (droits admin, ou option « unsafe ») :
     - `wsl --terminate rhbuild` puis `Optimize-VHD -Path G:\rh-verif\wsl\ext4.vhdx -Mode Full` (PowerShell admin, module Hyper-V) ;
     - ou diskpart `select vdisk file=G:\rh-verif\wsl\ext4.vhdx` / `compact vdisk` ;
     - ou `wsl --manage rhbuild --set-sparse true --allow-unsafe`.
   - Pour un rejeu complet (≈ 175 000 modules), il faudrait aussi plus de temps : ≈ 2 400 modules/h ici, soit environ 3 jours sur cette machine.

- 20:40 UTC : la clé SSH Windows s'authentifie bien comme `Hesia-Unit` et peut lire le dépôt, mais `git push` est refusé (« Permission to valstrax-sys/Remman-Proof.git denied to Hesia-Unit »). Il faut que `valstrax-sys` invite `Hesia-Unit` en collaborateur avec droit d'écriture (Settings → Collaborators) **et** que `Hesia-Unit` accepte l'invitation (https://github.com/valstrax-sys/Remman-Proof/invitations). Ensuite : `cd G:
h-verif; git push -u origin main`.
- 20:38 UTC : portable de nouveau joignable ; le contrôleur v3 reprend la file partagée.
- 21:00 UTC : **push résolu** — la deploy key `ark2` (= `/root/.ssh/id_ed25519` de Kali) est maintenant en lecture/écriture ; `main` poussé sur `valstrax-sys/Remman-Proof`. `scripts/pusher.sh` pousse les nouveaux commits toutes les 10 min (journal : `logs/pusher.log`).
