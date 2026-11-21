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
- **Nettoyage** : les `.olean` produits sont tous des prérequis potentiels des chunks plus profonds de la même machine, donc on les garde tant que la place le permet. On ne supprime rien.
