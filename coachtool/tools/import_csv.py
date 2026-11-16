"""Imports activities from a CSV (see data/templates/activities-template.csv).
Usage: python3 tools/import_csv.py <file.csv> [--update]
Lists (skills, ages, tracks, levels, pairs_with) are separated by semicolons. A new activity is
skipped if its id exists, unless --update. Everything is checked, and nothing is kept if the check fails."""
import csv, re, sys, pathlib, shutil, yaml
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from check import check
def slug(n): return re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')
def lst(v): return [x.strip() for x in v.split(';') if x.strip()]
def main():
    src = pathlib.Path(sys.argv[1]); update = '--update' in sys.argv
    adir = ROOT / 'data' / 'activities'
    existing = {f.stem: yaml.safe_load(f.read_text(encoding='utf-8')) for f in adir.glob('*.yaml')}
    order = max([a['order'] for a in existing.values()] + [0])
    backup = {}; written = []; skipped = []
    for row in csv.DictReader(src.open(encoding='utf-8-sig')):
        row = {k.strip(): (v or '').strip() for k, v in row.items() if k}
        if not row.get('name') or row['name'].startswith('Example'): continue
        i = row.get('id') or slug(row['name'])
        if i in existing and not update: skipped.append(i); continue
        old = existing.get(i)
        if old: order_n = old['order']; backup[i] = (adir / f'{i}.yaml').read_text(encoding='utf-8')
        else: order += 1; order_n = order
        a = {'id': i, 'order': order_n, 'name': row['name'], 'block': row['block'].upper(), 'skills': lst(row['skills']),
             'ages': lst(row['ages']), 'tracks': lst(row['tracks']), 'levels': lst(row['levels']),
             'players': {'min': int(row['players_min']), 'max': int(row['players_max'])}, 'space': row['space'].lower(),
             'minutes': int(row['minutes'] or 15), 'setup': row['setup'], 'look_for': row['look_for'], 'question': row['question'],
             'pairs_with': lst(row.get('pairs_with', '')), 'equipment': row['equipment']}
        if row.get('diagram'): a['diagram'] = row['diagram']
        if old and old.get('aliases'): a['aliases'] = old['aliases']
        (adir / f'{i}.yaml').write_text(yaml.safe_dump(a, sort_keys=False, allow_unicode=True, width=100), encoding='utf-8'); written.append(i)
    errs, _ = check()
    if errs:
        for i in written:
            f = adir / f'{i}.yaml'
            if i in backup: f.write_text(backup[i], encoding='utf-8')
            else: f.unlink()
        sys.exit('Nothing imported. Fix these:\n' + '\n'.join(errs))
    print(f'imported {len(written)}: {", ".join(written) or "none"}'); 
    if skipped: print(f'skipped (already exist, use --update): {", ".join(skipped)}')
main()
