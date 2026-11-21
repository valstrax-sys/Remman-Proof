"""Greedy two-machine schedule of packets in depth order, minimising duplicated
prerequisite builds. Output: state/queue-main.txt, state/queue-laptop.txt"""
import sys, collections, json
sys.path.insert(0, '/mnt/g/rh-verif/tools/alpoge-rh-replay/tracker')
import tasks
rows = tasks.load()
byid = {r['id']: r for r in rows}
packets = collections.OrderedDict()
for r in sorted(rows, key=lambda r: (r['depth'], r['packet'])):
    packets.setdefault(r['packet'], []).append(r)
print('packets', len(packets))
depthcount = collections.Counter(r['depth'] for r in rows)
cum=0
for d in range(0, 12):
    cum += depthcount[d]; print('depth', d, depthcount[d], 'cum', cum, 'packets', sum(1 for p,m in packets.items() if m[0]['depth']==d))
built = {'main': set(), 'laptop': set()}
speed = {'main': 1.0, 'laptop': 0.8}
load = {'main': 0.0, 'laptop': 0.0}
queues = {'main': [], 'laptop': []}
def closure(ids):
    seen=set(); st=list(ids)
    while st:
        x=st.pop()
        if x in seen: continue
        seen.add(x); st.extend(byid[x]['imports'])
    return seen
LIMIT = int(sys.argv[1]) if len(sys.argv)>1 else 400
for i,(p,mem) in enumerate(packets.items()):
    if i >= LIMIT: break
    need = closure(r['id'] for r in mem)
    best=None
    for m in built:
        cost = len(need - built[m])
        score = (load[m] + cost)/speed[m]
        if best is None or score < best[0]: best=(score,m,cost)
    _,m,cost = best
    built[m] |= need; load[m] += cost
    nopen = sum(1 for r in mem if r['state']=='open')
    queues[m].append(f"{p}\t{mem[0]['depth']}\t{len(mem)}\t{nopen}\t{cost}")
for m in queues:
    open(f'/mnt/g/rh-verif/state/queue-{m}.txt','w').write('packet\tdepth\tmodules\topen_in_snapshot\test_new_builds\n'+'\n'.join(queues[m])+'\n')
    print(m, 'packets', len(queues[m]), 'module builds', int(load[m]))
dup = len(built['main'] & built['laptop'])
print('duplicated modules', dup)
