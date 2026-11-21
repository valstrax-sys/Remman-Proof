"""Aggregate verified chunks into reports/SUMMARY.md (runs in Kali: needs the tracker index)."""
import os, sys, json, glob, collections
sys.path.insert(0, '/mnt/g/rh-verif/tools/alpoge-rh-replay/tracker')
import tasks
root = '/mnt/g/rh-verif'
rows = {r['id']: r for r in tasks.load()}
ok, bad = [], []
targets, rebuilt = set(), set()
mach = collections.Counter(); secs = collections.Counter()
for rp in sorted(glob.glob(f'{root}/reports/P*.md')):
    cid = os.path.basename(rp)[:-3]; head = open(rp, encoding='utf-8').readline()
    r = json.load(open(f'{root}/logs/{cid}/receipt.json'))
    m = 'portable' if '| Machine | portable' in open(rp, encoding='utf-8').read() else 'principale'
    (ok if 'VÉRIFIÉ' in head else bad).append(cid)
    if 'VÉRIFIÉ' in head:
        targets.update(r['tasks']); mach[m] += 1; secs[m] += r['elapsed_seconds']
byname = {r['module']: r for r in rows.values()}
for rp in glob.glob(f'{root}/logs/P*/receipt.json'):
    for mod in json.load(open(rp)).get('rebuilt_project_modules', []):
        if mod in byname: rebuilt.add(byname[mod]['id'])
allmods = targets | rebuilt
st = collections.Counter(rows[t]['state'] for t in targets)
st_all = collections.Counter(rows[t]['state'] for t in allmods)
depths = collections.Counter(rows[t]['depth'] for t in targets)
md = f"""# Synthèse — vérification de l'archive Lean d'Alpöge (RH/GRH)

Généré automatiquement (`scripts/summary.py`). Détails par chunk : `reports/P*.md`, état : `state/STATE.md`.

## Résultat

- Chunks (packets de ≤ 64 modules) **vérifiés** : **{len(ok)}** — principale {mach['principale']} ({secs['principale']/3600:.1f} h de build), portable {mach['portable']} ({secs['portable']/3600:.1f} h).
- Chunks en échec / non concluants : **{len(bad)}** {', '.join(bad)}
- Modules **cibles** distincts vérifiés (compilés exit 0 avec ligne `Built`, + audit d'axiomes) : **{len(targets)}** / 175 187.
- Modules distincts compilés au total (cibles + imports reconstruits) : **{len(allmods)}**.
- Profondeurs couvertes (cibles) : {dict(sorted(depths.items()))}
- Axiomes : pour **chaque** chunk vérifié, l'union des axiomes atteints depuis toutes les déclarations des modules cibles est exactement `propext`, `Classical.choice`, `Quot.sound`. Aucun `sorryAx`, `Lean.ofReduceBool`/`ofReduceNat` (native_decide), `Lean.trustCompiler`, aucun `axiom` déclaré, aucun `@[extern]` / `@[implemented_by]` dans ces modules.
- Scan statique de toute l'archive (175 187 fichiers) : aucune occurrence de `native_decide`, `implemented_by`, `@[extern`, `axiom `, `unsafe `, `sorry`/`admit` ; seuls `run_cmd` : `BuildAid/D1..D5.lean` (ajout de noms à la deny-list de `LibrarySuggestions`, sans effet logique).

## Ce que cela établit — et ce que cela n'établit pas

- Établi : ces {len(targets)} modules de l'archive épinglée (hash `9631b4f0…`, Lean 4.33.1, Mathlib `0df444a3`) compilent sans erreur avec la toolchain officielle vérifiée par hash, et leurs déclarations ne dépendent que des trois axiomes standard.
- **Non établi** : le théorème final (`Main.riemannHypothesis`) — il exige les ~175 000 modules ; pas de rejeu `leanchecker --fresh` (noyau frais) ni de vérification des énoncés. Le verdict global appartient à l'audit final (README du projet distribué, page MIT).
- Les modules dépendent du cache Mathlib officiel téléchargé (`lake exe cache get`), non recompilé.

## Statut de ces modules dans l'instantané du projet distribué (tracker `0ca43af`)

Cibles : {dict(st)}
Toutes compilées : {dict(st_all)}

Les modules `open` étaient sans preuve enregistrée dans l'instantané : ce sont des contributions nouvelles potentielles ; les autres sont des **réplications indépendantes**. Aucun n'a été soumis (pas de claim possible : voir bloquants dans `state/STATE.md`).
"""
open(f'{root}/reports/SUMMARY.md', 'w', encoding='utf-8', newline='\n').write(md)
print(len(ok), len(bad), len(targets), len(allmods), dict(st))
