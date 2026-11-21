# Test: does deleting .setup.json of already-built modules force Lake to rebuild them?
export PATH="$HOME/.elan/bin:$PATH" ELAN_HOME=/work/vol/elan XDG_CACHE_HOME=/work/vol/cache
cd /work/vol/lean
mods="BuildAid.D1 CompanionTheory.HarishChandraModules.NonemptyRepresentations.ExpEntry"
for m in $mods; do ls -la .lake/build/ir/${m//.//}.setup.json 2>&1 | awk '{print $5, $9}'; done
echo "== before deletion (--no-build)"; elan run leanprover/lean4:v4.33.1 lake build --no-build $(for m in $mods; do printf '+%s:olean ' $m; done) 2>&1 | tail -2; echo "rc=${PIPESTATUS[0]}"
for m in $mods; do rm -f .lake/build/ir/${m//.//}.setup.json; done
echo "== after deletion (--no-build)"; elan run leanprover/lean4:v4.33.1 lake build --no-build $(for m in $mods; do printf '+%s:olean ' $m; done) 2>&1 | tail -3; echo "rc=${PIPESTATUS[0]}"
echo "== downstream depth-1 module (--no-build)"; d=$(python3 -c "
import gzip,json
for l in gzip.open('/work/repo/tracker/modules.jsonl.gz','rt'):
    r=json.loads(l)
    if r['packet']=='P0096': print(r['module']); break")
elan run leanprover/lean4:v4.33.1 lake build --no-build +$d:olean 2>&1 | tail -2; echo "rc=${PIPESTATUS[0]} ($d)"
