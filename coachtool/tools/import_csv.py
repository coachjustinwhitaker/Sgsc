"""Imports activities from a CSV (data/templates/activities-template.csv) or from a batch file
downloaded from the Activity Builder page (.json).
Usage: python3 tools/import_csv.py <file.csv|file.json> [--update]
CSV lists (skills, ages, tracks, levels, pairs_with) are separated by semicolons. A new activity is
skipped if its id exists, unless --update (a builder batch marks its own edits). Everything is checked,
and nothing is kept if the check fails."""
import csv, re, sys, json, base64, pathlib, yaml
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
from check import check
def slug(n): return re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')
def lst(v): return v if isinstance(v, list) else [x.strip() for x in str(v or '').split(';') if x.strip()]
def rows_from(src):
    if src.suffix.lower() == '.json':
        return [dict(r) for r in json.loads(src.read_text(encoding='utf-8'))['activities']]
    out = []
    for row in csv.DictReader(src.open(encoding='utf-8-sig')):
        row = {k.strip(): (v or '').strip() for k, v in row.items() if k}
        if row.get('name') and not row['name'].startswith('Example'): out.append(row)
    return out
def main():
    src = pathlib.Path(sys.argv[1]); update_all = '--update' in sys.argv
    adir = ROOT / 'data' / 'activities'; ddir = ROOT / 'data' / 'diagrams'; ddir.mkdir(exist_ok=True)
    existing = {f.stem: yaml.safe_load(f.read_text(encoding='utf-8')) for f in adir.glob('*.yaml')}
    order = max([a['order'] for a in existing.values()] + [0])
    backup = {}; written = []; skipped = []; newfiles = []
    for row in rows_from(src):
        i = row.get('id') or slug(row['name'])
        if i in existing and not (update_all or row.get('update')): skipped.append(i); continue
        old = existing.get(i)
        if old: order_n = old['order']; backup[i] = (adir / f'{i}.yaml').read_text(encoding='utf-8')
        else: order += 1; order_n = order
        new = {'id': i, 'order': order_n, 'name': row['name'], 'block': str(row['block']).upper(), 'skills': lst(row['skills']),
             'ages': lst(row['ages']), 'tracks': lst(row['tracks']), 'levels': lst(row['levels']),
             'players': {'min': int(row['players_min']), 'max': int(row['players_max'])}, 'space': str(row['space']).lower(),
             'minutes': int(row.get('minutes') or 15), 'setup': row['setup'], 'look_for': row['look_for'], 'question': row['question'],
             'pairs_with': lst(row.get('pairs_with')), 'equipment': row['equipment']}
        a = dict(old) if old else {}; a.update(new)
        if row.get('diagram'): a['diagram'] = row['diagram']
        if (row.get('source') or '').strip(): a['source'] = row['source'].strip()
        if (row.get('type') or '').strip(): a['type'] = row['type'].strip().lower()
        for _k in ('scoring', 'objective', 'rules', 'progression'):
            if (row.get(_k) or '').strip(): a[_k] = row[_k].strip()
        if row.get('diagram_data') and a.get('diagram'):
            f = ddir / a['diagram']
            if not f.exists(): newfiles.append(f)
            f.write_bytes(base64.b64decode(row['diagram_data'].split(',', 1)[1]))
        (adir / f'{i}.yaml').write_text(yaml.safe_dump(a, sort_keys=False, allow_unicode=True, width=100), encoding='utf-8'); written.append(i)
    errs, _ = check()
    if errs:
        for i in written:
            f = adir / f'{i}.yaml'
            if i in backup: f.write_text(backup[i], encoding='utf-8')
            else: f.unlink()
        for f in newfiles: f.unlink(missing_ok=True)
        sys.exit('Nothing imported. Fix these:\n' + '\n'.join(errs))
    print(f'imported {len(written)}: {", ".join(written) or "none"}')
    if skipped: print(f'skipped (already exist, use --update): {", ".join(skipped)}')
main()
