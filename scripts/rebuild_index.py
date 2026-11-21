"""Rebuild state/built-index.tsv (module -> first chunk whose log has its Built line) from logs/."""
import os, json, gzip, re, glob
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
items = []
for rp in glob.glob(os.path.join(root, 'logs', 'P*', 'receipt.json')):
    cid = os.path.basename(os.path.dirname(rp)); r = json.load(open(rp))
    rep = os.path.join(root, 'reports', cid + '.md')
    mk = 'laptop' if os.path.exists(rep) and '| Machine | portable' in open(rep, encoding='utf-8').read() else 'main'
    items.append((r.get('ended_utc', ''), cid, mk, r.get('log_sha256', ''), r.get('exit_code')))
items.sort()
with open(os.path.join(root, 'state', 'built-index.tsv'), 'w', encoding='utf-8', newline='\n') as f:
    n = 0
    for _, cid, mk, lsha, ec in items:
        if ec != 0: continue
        txt = gzip.open(os.path.join(root, 'logs', cid, 'build.log.gz'), 'rt', errors='replace').read()
        for mod in sorted(set(re.findall(r'\]\s+Built\s+([^\s:]+)', re.sub(r'\x1b\[[0-9;]*m', '', txt)))):
            f.write(f'{mod}\t{cid}\t{mk}\t{lsha}\n'); n += 1
print('index entries', n, 'chunks', len(items))
