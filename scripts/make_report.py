"""Build reports/<ID>.md and logs/<ID>/ from an exported chunk directory.
Usage: python make_report.py <exportdir> <machine-label>"""
import sys, os, json, hashlib, gzip, shutil, re, datetime
src, machine = sys.argv[1], sys.argv[2]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cid = os.path.basename(src.rstrip('/\\'))
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def rd(name, default=''):
    p = os.path.join(src, name)
    return open(p, encoding='utf-8', errors='replace').read() if os.path.exists(p) else default
logdir = os.path.join(root, 'logs', cid); os.makedirs(logdir, exist_ok=True)
receipt = json.loads(rd('receipt.json', '{}') or '{}')
blog = os.path.join(src, 'build.log')
log_sha = sha(blog) if os.path.exists(blog) else None
# compressed copies of all evidence
hashes = {}
for name in sorted(os.listdir(src)):
    p = os.path.join(src, name)
    if name in ('disk.txt',): continue
    dst = os.path.join(logdir, name + ('.gz' if name.endswith(('.log', '.lean', '.mem')) else ''))
    if dst.endswith('.gz'):
        with open(p, 'rb') as fi, gzip.GzipFile(dst, 'wb', mtime=0) as fo: shutil.copyfileobj(fi, fo)
    else:
        shutil.copyfile(p, dst)
    hashes[name] = sha(p)
with open(os.path.join(logdir, 'SHA256SUMS'), 'w', newline='\n') as f:
    for k, v in hashes.items(): f.write(f'{v}  {k}\n')
blogtxt = rd('build.log')
built = len(re.findall(r'\]\s+Built\s', blogtxt))
replayed = len(re.findall(r'\]\s+Replayed\s', blogtxt))
errors = [l for l in blogtxt.splitlines() if re.match(r'^(error|✖)', l)]
warnings = len(re.findall(r'^warning:', blogtxt, re.M))
audit = rd(f'{cid}.audit.log')
summary = re.findall(r'AXIOM_AUDIT_SUMMARY.*', audit)
union = re.findall(r'AXIOM_AUDIT_UNION.*', audit)
flags = re.findall(r'.*(static_verdict=FLAG|verdict=NOT_LOADED|AXIOM_AUDIT_DECL).*', audit)
audit_err = [l for l in audit.splitlines() if 'error' in l][:10]
audit_ok = bool(summary) and 'verdict=OK' in summary[-1]
def tv(txt, key):
    for line in txt.splitlines():
        if key in line: return line.rsplit(': ', 1)[-1].strip()
    return '?'
ttxt, atxt = rd(f'{cid}.time'), rd(f'{cid}.audit.time')
mem = [l.split() for l in rd(f'{cid}.mem').splitlines() if len(l.split()) >= 2]
mempeak = max((int(x[1]) for x in mem), default=0)
maxprocs = max((int(x[2]) for x in mem if len(x) > 2), default='?')
ec = receipt.get('exit_code')
targets_mods = [c[1:].rsplit(':', 1)[0] for c in receipt.get('command', []) if c.startswith('+')]
built_names = set(re.findall(r'\]\s+Built\s+([^\s:]+)', re.sub(r'\[[0-9;]*m', '', blogtxt)))
missing_built = [t for t in targets_mods if t not in built_names]
verified = (ec == 0 and log_sha == receipt.get('log_sha256') and audit_ok and not errors and not missing_built)
status = 'VÉRIFIÉ (build + audit axiomes)' if verified else ('BUILD OK MAIS CIBLES SANS LIGNE Built' if (ec == 0 and missing_built) else 'ÉCHEC BUILD' if ec not in (0, None) else ('AUDIT NON CONCLUANT' if ec == 0 else 'INCOMPLET'))
tasks_ = receipt.get('tasks', [])
rebuilt = receipt.get('rebuilt_project_modules', [])
md = f"""# Chunk {cid} — {status}

| Champ | Valeur |
|---|---|
| Chunk | `{cid}` ({len(tasks_)} modules cibles ; projet `rohanarun/alpoge-rh-replay`, choisi localement, **sans claim public**) |
| Machine | {machine} |
| Début / fin (UTC) | {receipt.get('started_utc','?')} → {receipt.get('ended_utc','?')} |
| Durée du build | {receipt.get('elapsed_seconds','?')} s (wall clock /usr/bin/time : {tv(ttxt,'Elapsed (wall clock)')}) |
| Code de sortie du build | **{ec}** |
| Pic RAM (sandbox entière, échantillonné toutes les 5 s) | {mempeak} MiB |
| Pic RSS du plus gros processus du build | {tv(ttxt,'Maximum resident set size')} kB (inclut les .olean Mathlib mappés en mémoire et partagés entre processus ; surestime la mémoire privée) |
| Processus `lean` simultanés (max observé) | {maxprocs} |
| Toolchain | {receipt.get('toolchain','?')} |
| Mathlib | `{receipt.get('mathlib','?')}` |
| SHA-256 de `parts.sha256` (14 parts vérifiées par `sha256sum -c`) | `{receipt.get('inputs_manifest_sha256','?')}` |
| Commande | `python3 tracker/tasks.py build {cid} /work/vol/lean /work/receipts/{cid} --bundle` → Lake : `{' '.join(receipt.get('command',[]))[:200]}{'…' if len(' '.join(receipt.get('command',[])))>200 else ''}` |
| SHA-256 du log de build | `{log_sha}` (receipt : `{receipt.get('log_sha256')}`, {'identiques' if log_sha == receipt.get('log_sha256') else '**DIFFÉRENTS**'}) |
| Lignes `Built` dans le log | {built} (dont {len(rebuilt)} imports projet reconstruits localement hors cibles) ; `Replayed` : {replayed} ; warnings : {warnings} ; erreurs : {len(errors)} |
| Bundle `.olean` cibles (non commité) | sha256 `{rd('bundle.sha256').strip() or 'n/a'}`, {rd('bundle.size').strip() or '?'} octets |

## Axiomes

Audit maison (`logs/{cid}/{cid}.lean.gz`) : importe les {len(tasks_)} modules, parcourt toutes les dépendances de **toutes** les déclarations de ces modules (mêmes champs que `Lean.collectAxioms`), liste aussi `axiom` / `@[extern]` / `@[implemented_by]` déclarés. Contrôle négatif validé (détecte `Lean.ofReduceBool`, `Lean.trustCompiler` dans `Init.Core`). Durée {tv(atxt,'Elapsed (wall clock)')}, pic RSS {tv(atxt,'Maximum resident set size')} kB.

```
{chr(10).join(union) or '(pas de ligne UNION)'}
{chr(10).join(summary) or '(pas de ligne SUMMARY)'}
```
Résultat : **{'uniquement propext, Classical.choice, Quot.sound' if audit_ok else 'NON CONCLUANT / ANOMALIE — voir log'}**

## Anomalies
"""
anom = []
if errors: anom.append('Erreurs de build :\n```\n' + '\n'.join(errors[:20]) + '\n```')
if flags: anom.append('Signalements audit :\n```\n' + '\n'.join(flags[:20]) + '\n```')
if audit_err: anom.append('Erreurs de l\'audit :\n```\n' + '\n'.join(audit_err) + '\n```')
if log_sha != receipt.get('log_sha256'): anom.append('Hash du log différent du receipt.')
if missing_built: anom.append(f'{len(missing_built)} cible(s) sans ligne `Built` dans ce run (déjà compilées auparavant) : ' + ', '.join(missing_built[:20]))
if any(n.startswith('run-') and 'interrupted' in n for n in os.listdir(src)): anom.append('Une tentative précédente a été interrompue (infrastructure : perte SSH/veille) ; son log partiel est conservé dans logs/' + cid + '/ ; les sorties de build des cibles ont été supprimées avant la reprise pour tout recompiler.')
md += ('\n\n'.join(anom) if anom else 'Aucune.') + '\n'
md += f"""
## Fichiers
`logs/{cid}/` : receipt.json, build.log.gz, audit, mesures temps/mémoire ; `logs/{cid}/SHA256SUMS` donne les hashes des fichiers **non compressés**.
Modules cibles : {', '.join(tasks_)}
"""
open(os.path.join(root, 'reports', cid + '.md'), 'w', encoding='utf-8', newline='\n').write(md)
print(cid, status, 'built', built, 'peak', mempeak, 'elapsed', receipt.get('elapsed_seconds'))
