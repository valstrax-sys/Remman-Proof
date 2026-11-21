"""Regenerate state/STATE.md from reports, queues and done files."""
import os, re, glob, json, datetime, subprocess
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
rows = []
for p in sorted(glob.glob(os.path.join(root, 'reports', 'P*.md')) + glob.glob(os.path.join(root, 'reports', 'M*.md'))):
    cid = os.path.basename(p)[:-3]
    head = open(p, encoding='utf-8').readline().strip()
    status = head.split('—', 1)[-1].strip()
    rec = os.path.join(root, 'logs', cid, 'receipt.json')
    r = json.load(open(rec)) if os.path.exists(rec) else {}
    txt = open(p, encoding='utf-8').read()
    mach = 'portable' if '| Machine | portable' in txt else 'principale'
    rows.append((cid, mach, status, len(r.get('tasks', [])), r.get('elapsed_seconds', 0), len(r.get('rebuilt_project_modules', [])), r.get('ended_utc', '')[:19]))
ok = [x for x in rows if x[2].startswith('VÉRIFIÉ')]
bad = [x for x in rows if not x[2].startswith('VÉRIFIÉ')]
def rate(m):
    xs = [x for x in ok if x[1] == m]
    mods = sum(x[3] + x[5] for x in xs); secs = sum(x[4] for x in xs)
    return mods, secs, (mods / secs * 3600 if secs else 0)
def readf(p):
    return open(p, encoding='utf-8').read() if os.path.exists(p) else ''
running = readf(os.path.join(root, 'state', 'running.txt')).strip()
disk = readf(os.path.join(root, 'state', 'disk.txt')).strip()
blockers = readf(os.path.join(root, 'state', 'blockers.md')).strip()
def qinfo(m):
    q = [l.split('\t')[0] for l in readf(os.path.join(root, 'state', f'queue-{m}.txt')).splitlines()[1:] if l]
    d = set(readf(os.path.join(root, 'state', f'done-{m}.txt')).split())
    nxt = [x for x in q if x not in d][:5]
    return len(q), len(d), nxt
md = [f'# STATE — vérification distribuée de l\'archive Lean d\'Alpöge\n', f'Mis à jour : {now}\n']
md.append('## Résumé\n')
md.append(f'- Chunks vérifiés (build exit 0 + audit axiomes OK) : **{len(ok)}** ({sum(x[3] for x in ok)} modules cibles, {sum(x[5] for x in ok)} imports reconstruits en plus)')
md.append(f'- Chunks en échec / non concluants : **{len(bad)}** ' + (', '.join(f'{x[0]} ({x[2]})' for x in bad) if bad else ''))
md.append(f'- En cours : {running or "rien"}')
for m, lab in (('principale', 'main'), ('portable', 'laptop')):
    mods, secs, rt = rate(m); n, d, nxt = qinfo(lab)
    md.append(f'- Débit {m} : {rt:.0f} modules/heure ({mods} modules en {secs/3600:.2f} h de build) ; file `state/queue-{lab}.txt` : {d}/{n} faits ; prochains : {", ".join(nxt)}')
md.append(f'- Disque : {disk or "?"}')
md.append('\n## Bloquants / décisions utilisateur\n')
md.append(blockers or 'Aucun.')
md.append('\n## Chunks\n')
md.append('| Chunk | Machine | Statut | Modules cibles | Imports reconstruits | Durée build (s) | Fin (UTC) |')
md.append('|---|---|---|---:|---:|---:|---|')
for x in rows:
    md.append(f'| [{x[0]}](../reports/{x[0]}.md) | {x[1]} | {x[2]} | {x[3]} | {x[5]} | {x[4]} | {x[6]} |')
md.append('\n## Reprise\n')
md.append('Relancer le contrôleur : `bash scripts/controller.sh main` (Git Bash, depuis `G:\rh-verif`) et `bash scripts/controller.sh laptop`. '
          'Chaque contrôleur reprend la file `state/queue-<machine>.txt` en sautant ce qui est dans `state/done-<machine>.txt`. '
          'Un chunk interrompu laisse `/work/receipts/<ID>` dans la sandbox : le supprimer (en tant que builder) avant de relancer. '
          'Créer `state/STOP` pour arrêter proprement après le chunk courant.')
open(os.path.join(root, 'state', 'STATE.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(md) + '\n')
print('STATE.md updated', len(ok), len(bad))
