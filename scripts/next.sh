cd /mnt/g/rh-verif/tools/alpoge-rh-replay && git pull -q --ff-only 2>&1 | tail -1; echo "tracker HEAD $(git rev-parse HEAD)"
python3 -c "import json;print(json.load(open('tracker/summary.json')))" | head -c 1500; echo
echo "== next"; python3 tracker/tasks.py next --limit 15
echo "== next --cold"; python3 tracker/tasks.py next --cold --limit 15
