export PATH="$HOME/.elan/bin:$PATH" ELAN_HOME=/work/vol/elan XDG_CACHE_HOME=/work/vol/cache
cd /work/vol/lean
t=$(python3 -c "
import gzip,json
print(' '.join('+'+json.loads(l)['module']+':olean' for l in gzip.open('/work/repo/tracker/modules.jsonl.gz','rt') if json.loads(l)['packet'] in ('$1')))")
elan run leanprover/lean4:v4.33.1 lake build --no-build $t 2>&1 | tail -2; echo "NOBUILD_RC=${PIPESTATUS[0]}"
