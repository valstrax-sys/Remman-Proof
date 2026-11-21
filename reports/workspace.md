# Espace de travail et protocole (ce qui a été fait, et pourquoi)

## Arborescence `G:\rh-verif` (= dépôt git des rapports)

```
rh-verif/
  reports/   rapports par chunk + inventaires (commités)
  logs/      logs compressés, receipts, SHA256SUMS par chunk (commités)
  state/     STATE.md, files de chunks, done-*.txt, bloquants (commités)
  scripts/   scripts de l'agent (commités) ; scripts/sandbox/ = copies de ceux qui tournent dans la sandbox
  toolchain/ src/ build/   (vides : voir ci-dessous, tout vit dans le VHDX ext4)
  wsl/       ext4.vhdx de la distro de build (ignoré par git)
  exchange/  in/ = scripts lus par la sandbox ; out/ = preuves exportées par root (ignoré par git)
  tools/     clone de rohanarun/alpoge-rh-replay côté Windows, utilisé pour planifier (ignoré)
```

`.gitignore` exclut `.olean`, `.lake/`, les VHDX, les parts de l'archive, les toolchains et les sources.

## Système de fichiers ext4 sur G:

Méthode choisie : **une distro WSL dédiée dont le disque ext4 (VHDX) est sur G:**.

```
wsl --install Ubuntu-24.04 --name rhbuild --location G:\rh-verif\wsl --no-launch
```

WSL 2.6.3 accepte `--name` et `--location`, et cette commande ne demande pas les droits administrateur. La méthode `wsl --mount --vhd` les aurait demandés.

Avantages :
- la compilation se fait sur de l'ext4 natif, pas sur `/mnt/g` en 9p (qui est très lent) ;
- l'isolation est plus forte qu'avec un simple utilisateur dans Kali.

Le chemin dans la sandbox est `/work`, comme dans la doc Docker du projet. La toolchain, les sources et le build se trouvent dans `/work/vol` :
- `elan/` : la toolchain ;
- `lean/src` : les sources ;
- `lean/.lake` : le build et Mathlib.

C'est l'organisation imposée par `verify.sh`.

## Isolation (règle 4 du prompt)

La distro `rhbuild` est configurée par `scripts/setup-rhbuild-root.sh` :

- **utilisateur `builder`** (uid 1000), sans sudo, mot de passe verrouillé. Tout ce qui exécute du code de l'archive (`verify.sh`, `lake`, `lean`, l'audit) tourne sous cet utilisateur ;
- `/etc/wsl.conf` : `automount enabled=false`, `interop enabled=false`, `appendWindowsPath=false` :
  - aucun disque Windows n'est visible (donc ni `C:\Users\matis\.ssh` ni les tokens) ;
  - aucun `.exe` Windows ne peut être lancé ;
  - vérifié : `mount` ne montre aucun drvfs, `/root` est illisible, `sudo` demande un mot de passe ;
- l'utilisateur principal agit depuis Windows :
  - root monte uniquement `G:\rh-verif\exchange` sur `/exchange` (`uid=0,umask=022`), donc en **lecture seule** pour `builder`. Vérifié : `touch` refusé ;
  - root copie les preuves vers `/exchange/out`. `builder` ne peut rien écrire hors de son ext4 ;
- **les `git push` ne sont faits que par l'utilisateur principal**, côté Windows ou Kali. La sandbox ne contient aucune clé ni aucun token.
  Le push se fait depuis Kali (utilisateur principal) avec la deploy key `ark2` en lecture/écriture, via `scripts/kali-push.sh`, appelé toutes les 10 min par `scripts/pusher.sh`.

Limite connue : la sandbox a accès au réseau, ce qui est nécessaire pour télécharger l'archive et le cache Mathlib. Comme toutes les distros WSL2, elle partage le noyau de la VM.

## Protocole suivi

On suit le README et `CONTRIBUTING.md` de `rohanarun/alpoge-rh-replay` au commit `0ca43af1f884e306c45b6bfac10885b2bb31315c`.

1. `./verify.sh /work/vol --prepare-only`. Ce script :
   - télécharge les 14 parts depuis `https://alpo.ge/lean.tar.gz.partNN` ;
   - fait `sha256sum -c parts.sha256` ;
   - installe Lean 4.33.1 et vérifie le hash des binaires et des `.so` contre la release officielle ;
   - lance `lake exe cache get` ;
   - vérifie que Mathlib est au commit `0df444a…`, puis vérifie les dépendances et les artefacts.

   Tous les marqueurs `REPLAY_*_PASSED` sont présents (`logs/prepare-outer.log`).
2. Pour chaque chunk : `python3 tracker/tasks.py build <ID> /work/vol/lean /work/receipts/<ID> --bundle`. C'est la commande officielle : Lake, `lake build +Module:olean …`. Elle produit le receipt (hash du log, versions, temps) et le bundle des `.olean` cibles.
3. Audit des axiomes : outil de l'agent (`scripts/sandbox/gen_audit.py`), voir chaque rapport. Le projet ne fournit pas d'audit d'axiomes par module : `Audit.lean` ne couvre que les 5 théorèmes de `Main`.

### Écarts et choix

- **Pas de `lake build` du projet entier** : on construit des packets (≤ 64 modules), conformément au protocole du projet distribué. Les sources ne sont jamais modifiées.
- **Parallélisme** : Lake 4.33.1 n'a pas d'option `-j`. On fixe `LEAN_NUM_THREADS` (pool de threads du runtime Lean) à 11 sur la machine principale et à 15 sur le portable, selon la règle min(vCPU − 1, RAM × 0,8 / pic par job). Le pic réel par job est mesuré à environ 0,7 Go de mémoire privée (9,5 Go au total pour 12 jobs sur P0001). Le RSS d'un processus est d'environ 6,7 Go, mais il inclut les `.olean` Mathlib mappés et partagés. L'effet de `LEAN_NUM_THREADS` est mesuré à chaque chunk : le nombre de processus `lean` simultanés est noté dans les rapports.
- **Choix des chunks** : il est fait **localement**, sans claim, faute de `gh` authentifié (voir `state/STATE.md`). `scripts/plan.py` parcourt les packets par profondeur croissante et les répartit de façon gloutonne entre les deux machines, en minimisant les reconstructions de prérequis en double. Résultat : `state/queue-*.txt`.
- **Disque** : `wsl --manage rhbuild --resize 115GB` a échoué, car il demande un `wsl --shutdown` complet, que je ne fais pas tant qu'une session Kali est ouverte. Le garde-fou est le contrôleur : il s'arrête si le disque hôte a moins de 20 Go libres.
- **Nettoyage (§5.6)** : on garde les `.olean`, `.ilean` et traces, prérequis des chunks plus profonds.
  - Constat à 18:15 UTC : sur 107 Go utilisés dans l'ext4, **89 Go** étaient des `*.setup.json` générés par Lake (environ 5,4 Mo par module : la liste de tous les imports transitifs). Les `.olean` ne pesaient que 6,3 Go.
  - Ces fichiers sont des entrées du compilateur, régénérées à chaque compilation ; `tasks.py` les exclut des bundles pour cette raison.
  - Test : après suppression, `lake build --no-build` sur P0001, sur un module de profondeur 1 et sur le packet P0273 (profondeur 3) répond « All targets up-to-date ». Rien n'est recompilé.
  - Ils sont donc supprimés après chaque chunk (`scripts/sandbox/cleanup-setupjson.sh`) ; le nettoyage initial a libéré 89,2 Go dans l'ext4.
  - Limite : le VHDX est dynamique et non sparse, il **ne rétrécit pas**. L'espace libéré n'est réutilisé que pour les écritures suivantes dans l'ext4. G: est resté à 19 Go libres. Pour vraiment récupérer de l'espace sur G:, il faut compacter le VHDX, ce qui demande les droits admin (`Optimize-VHD` / diskpart) ou `wsl --manage rhbuild --set-sparse true --allow-unsafe` : décision de l'utilisateur.
- **Cibles déjà compilées** : quand une cible a déjà été compilée comme prérequis par un chunk antérieur de la même machine, Lake ne la recompile pas (exit 0 = à jour). Le rapport cite alors le chunk et le hash du log où figure sa ligne `Built` (`state/built-index.tsv`). L'audit des axiomes porte toujours sur toutes les cibles.
- **Portable injoignable à partir de 13:01 UTC** (veille probable). Le contrôleur v2/v3 l'attend. Ses packets restants ont été fusionnés dans une file partagée (`state/queue-shared.txt`, triée par profondeur), que la principale traite. Si le portable revient, il saute ce que la principale a fait ou fait en ce moment.
- **20:39 UTC, contrôleur v2 du portable resté actif par erreur** : au retour du portable, une ancienne instance de `controller2.sh laptop` (lancée à 14:12, sur `queue-laptop.txt`, sans la règle « déjà fait ailleurs ») a relancé P0060 puis P0063, deux packets déjà vérifiés par la principale. P0060 a échoué immédiatement (`pre-chunk.sh` absent sur le portable, receipt existant → exit 3) ; P0063 a été arrêté pendant le build à 20:45 UTC. Aucun rapport n'a été écrit ni écrasé (`reports/P0060.md` et `reports/P0063.md` restent ceux de la principale). Logs conservés dans `logs/stale-laptop-v2/`. Seul le contrôleur v3 sur la file partagée reste actif, et les scripts sandbox du portable ont été resynchronisés.
- **21:55 heure locale, disques E: et F: ouverts par l'utilisateur** (disques durs, 277 et 292 Go libres). Décision : **ne pas y compiler pour l'instant.**
  - **Pas de calcul en plus** : E: et F: sont sur la même machine. Les 12 vCPU sont déjà occupés (11 jobs). Un disque de plus n'ajoute pas de puissance de calcul et ralentirait les lectures de `.olean`.
  - **La place n'est pas encore limitante** : l'ext4 de la sandbox n'utilise que 28 Go dans un VHDX de 110 Go (le VHDX ne grossit pas tant que l'ext4 réutilise l'espace libéré).
    - Détail : Mathlib et dépendances 7,6 Go ; `.olean` 9,4 Go pour 23 071 modules, soit environ 0,41 Mo par module ; `.ilean` 0,5 Go ; IR 0,6 Go.
    - Projection pour les 152 000 modules restants : environ 62 Go de `.olean` à taille moyenne constante, et plus si les modules profonds sont plus gros. Total estimé : 90 à 120 Go.
    - Plafond actuel : 110 Go de VHDX, plus ce que G: peut encore céder avant le garde-fou de 17 Go, soit environ 112 Go.
  - **Plan** : le contrôleur s'arrête de lui-même au garde-fou. Il faudra déplacer de l'espace vers E:/F: quand l'ext4 dépassera environ 90 Go utilisés, vers 60 à 70 % de l'avancement. Deux options :
    - disque ext4 supplémentaire sur E:/F: (`wsl --mount --vhd`, droits admin) pour les modules les moins lus ;
    - ou déplacement d'autres données de G:.
- **Pause demandée à 23:00 heure locale (22:00 UTC)** : `scripts/pause-at.sh 22:00` crée `state/STOP`. Les contrôleurs terminent leur chunk en cours puis s'arrêtent. `scripts/pusher.sh` pousse les derniers commits, puis s'arrête.
  - Reprise : supprimer `state/STOP`, puis relancer `MIN_FREE_GB=17 QUEUE=state/queue-shared.txt bash scripts/controller.sh main`, la même commande avec `laptop`, et `bash scripts/pusher.sh`.

## Changement de programme (21/11/2026, 22:00 heure locale)

À la demande de l'utilisateur, on **arrête la compilation** et on **déplace l'espace de travail de la sandbox** (le VHDX de 118 Go) sur un disque dur. Le travail porte désormais sur la compréhension et l'utilisation de la preuve : voir `comprendre/`.

- **Arrêt.** Création de `state/STOP` à 21:02 UTC. Les deux contrôleurs ont fini leur chunk en cours, puis se sont arrêtés proprement. Bilan final : **378 chunks vérifiés, 0 échec, 24 095 modules distincts sur 175 187 (13,8 %)** ; détail dans `state/STATE.md`.
- **Déplacement.**
  - `wsl --manage rhbuild --move` a échoué avec `ERROR_SHARING_VIOLATION`. Le VHDX restait attaché à la VM WSL partagée avec Kali (`/dev/sde`). Le seul moyen de le libérer, `wsl --shutdown`, aurait fermé la session Kali ouverte (bureau `lightdm` et deux shells), donc on ne l'a pas utilisé.
  - On a donc fait `wsl --export rhbuild F:\rh-verif\rhbuild-export.tar` : 24,4 Go, 589 776 entrées vérifiées par `tar -tf`, dont 34 450 `.olean` et 1 405 entrées de receipts.
  - Puis `wsl --unregister rhbuild`, ce qui a supprimé `G:\rh-verif\wsl\ext4.vhdx` et libéré environ 118 Go sur G:.
  - Enfin `wsl --import rhbuild F:\rh-verif\wsl F:\rh-verif\rhbuild-export.tar`. Le nouveau VHDX ne contient que les données réelles (environ 28 Go).
  - `/etc/wsl.conf` (utilisateur par défaut `builder`, automount et interop désactivés) fait partie de l'archive : l'isolation est conservée.
- **Si la compilation reprend un jour**, elle tournera depuis F: (disque dur), donc plus lentement. Le garde-fou disque des contrôleurs vise G: ; il faudra l'adapter à F: (`host_free_gb`).
- **Après l'import** (21/11, 22:25 heure locale) :
  - le VHDX `F:\rh-verif\wsl\ext4.vhdx` fait 29,6 Go, l'ext4 est occupé à 28 Go ;
  - utilisateur par défaut `builder`, `/root` en 700, un seul montage drvfs (l'échange) ;
  - `lake build --no-build` sur P0001, P0273 et P0378 répond « All targets up-to-date » : rien n'a été perdu ;
  - `F:\rh-verif\rhbuild-export.tar` (24,4 Go) est conservé comme sauvegarde, et peut être supprimé si la place manque.
