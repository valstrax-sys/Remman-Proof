import sys, json, gzip, collections
sys.path.insert(0, '/mnt/g/rh-verif/tools/alpoge-rh-replay/tracker')
import tasks
rows = tasks.load()
byid = {r['id']: r for r in rows}
print('rows', len(rows), 'keys', list(rows[0].keys()))
print('states', collections.Counter(r['state'] for r in rows).most_common())
print('depth max', max(r['depth'] for r in rows))
# closure sizes (memo via topological order by depth)
order = sorted(rows, key=lambda r: r['depth'])
clos = {}
import functools
sizes = {}
# closure sets are big; compute sizes for open modules only via BFS with cache of sets for depth<=40
def closure(mid):
    seen = set(); st = [mid]
    while st:
        x = st.pop()
        for d in byid[x]['imports']:
            if d not in seen: seen.add(d); st.append(d)
    return seen
open_rows = [r for r in rows if r['state'] == 'open']
print('open', len(open_rows))
dd = collections.Counter(r['depth'] for r in open_rows)
print('open by depth (lowest 15):', sorted(dd.items())[:15])
res = []
for r in sorted(open_rows, key=lambda r: r['depth'])[:3000]:
    res.append((len(closure(r['id'])), r['depth'], r['id'], r['packet'], r['module']))
res.sort()
for x in res[:25]: print(x)
