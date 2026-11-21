cd /g/rh-verif
for m in main laptop; do echo "$m: done=$(wc -l < state/done-$m.txt) last: $(grep -a ' done ' logs/controller-$m.log | tail -1 | cut -c1-110)"; grep -a ' start ' logs/controller-$m.log | tail -1 | cut -c1-140; done
grep -l "ÉCHEC\|NON CONCLUANT\|INCOMPLET" reports/P*.md 2>/dev/null | head
cat state/disk.txt 2>/dev/null
