#!/usr/bin/env python3
"""Import skill areas by level from a comp methodology site folder (comp/u13u14, comp/u11u12).
Usage: import_site_skills.py <site_dir> <age>   (writes comp rows into data/skills/<age>.yaml, replacing earlier comp rows)"""
import sys, re, yaml
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parent.parent
LV = {'intro': 'intro', 'dev': 'dev', 'app': 'app'}
slug = lambda s: re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def clean(t): return re.sub(r'\s+', ' ', t.replace('’', "'")).strip()
def rows_for(site, age):
    out = []
    for f in sorted(Path(site).glob('SGSC_B[1-5]_*.html')):
        block = re.search(r'SGSC_(B\d)_', f.name).group(1)
        soup = BeautifulSoup(f.read_text(), 'html.parser')
        for area in soup.select('.skill-area'):
            name = clean(area.select_one('.skill-area-title').get_text())
            nodes = area.select('.level-row') or area.select('.level-card')
            for n in nodes:
                cls = ' '.join(n.get('class', []))
                lv = next((v for k, v in LV.items() if re.search(r'\b(level-)?' + k + r'\b', cls)), None)
                if not lv: raise SystemExit(f'{f.name} {name}: no level in {cls}')
                bullets = [clean(li.get_text()) for li in n.select('li')]
                for g in n.select('.app-group'):
                    tag = clean(g.select_one('.app-group-tag').get_text()); p = clean(g.select_one('p').get_text())
                    bullets.append(f'{tag}: {p}')
                if not bullets: raise SystemExit(f'{f.name} {name} {lv}: no bullets')
                out.append({'id': f'{age}-{block.lower()}-{slug(name)}-{lv}-comp', 'age': age, 'block': block, 'area': name, 'level': lv, 'tracks': ['comp'], 'bullets': bullets})
    return out
def merge(existing, new):
    """Identical intro rows already in rec become shared (rec + comp). Other levels reuse that row's area name."""
    alias = {}
    def sig(r): return (r['block'], r['level'], tuple(r['bullets']))
    ex = {sig(r): r for r in existing if 'comp' not in r['tracks'] or 'rec' in r['tracks']}
    for r in new:
        m = ex.get(sig(r))
        if m: alias[(r['block'], r['area'])] = m['area']
    shared, added = 0, []
    for r in new:
        m = ex.get(sig(r))
        if m:
            if 'comp' not in m['tracks']: m['tracks'].append('comp')
            shared += 1; continue
        r['area'] = alias.get((r['block'], r['area']), r['area'])
        r['id'] = f"{r['age']}-{r['block'].lower()}-{slug(r['area'])}-{r['level']}-comp"
        added.append(r)
    return added, shared
if __name__ == '__main__':
    site, age = sys.argv[1], sys.argv[2]
    path = ROOT / 'data' / 'skills' / f'{age}.yaml'
    d = yaml.safe_load(path.read_text()) if path.exists() else {'skills': []}
    d['skills'] = [r for r in d['skills'] if not (r['id'].endswith('-comp') and r['tracks'] == ['comp'])]
    added, shared = merge(d['skills'], rows_for(site, age))
    d['skills'] += added
    path.write_text(yaml.safe_dump(d, sort_keys=False, allow_unicode=True, width=100))
    print(f'{age}: {shared} intro rows shared with rec, {len(added)} comp rows added')
