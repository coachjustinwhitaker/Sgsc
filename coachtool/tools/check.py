"""Checks the records. Exit code 1 if anything is wrong."""
import sys, pathlib, yaml, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
BLOCKS = {'B1', 'B2', 'B3', 'B4', 'B5'}
def load(p): return yaml.safe_load(p.read_text(encoding='utf-8'))
def check(root=ROOT):
    errs = []
    ladder = load(root / 'rules' / 'ladder.yaml')
    acts = {}
    for f in sorted((root / 'data' / 'activities').glob('*.yaml')):
        a = load(f)
        for k in ['id', 'name', 'block', 'skills', 'ages', 'tracks', 'levels', 'players', 'space', 'setup', 'look_for', 'question', 'equipment']:
            if a.get(k) in (None, '', []): errs.append(f'{f.name}: missing {k}')
        if a.get('id') != f.stem: errs.append(f'{f.name}: id {a.get("id")} does not match file name')
        if a.get('space') not in ('quarter', 'half', 'full'): errs.append(f'{f.name}: space must be quarter, half or full, not {a.get("space")}')
        if a.get('block') not in BLOCKS: errs.append(f'{f.name}: bad block {a.get("block")}')
        d = a.get('diagram')
        if d and not (root / 'data' / 'diagrams' / d).is_file(): errs.append(f'{f.name}: diagram file {d} not found in data/diagrams')
        if d and d.rsplit('.', 1)[-1].lower() not in ('png', 'jpg', 'jpeg', 'webp', 'svg'): errs.append(f'{f.name}: diagram must be png, jpg, webp or svg')
        tags = load(root / 'data' / 'vocab' / 'activity-tags.yaml'); okt = set(tags['actions'] + tags['concepts'])
        for t in a.get('skills', []):
            if t not in okt: errs.append(f'{f.name}: skill tag "{t}" is not in data/vocab/activity-tags.yaml')
        acts[a['id']] = a
        for age in a.get('ages', []):
            for tr in a.get('tracks', []):
                if age in ladder[tr] and a['block'] not in ladder[tr][age]:
                    errs.append(f'{a["id"]}: block {a["block"]} is not part of {tr} {age}')
                for lv in a.get('levels', []):
                    if lv not in ladder['levels'][tr]: errs.append(f'{a["id"]}: level {lv} is not used in {tr}')
    seen = {}
    for a in acts.values():
        for k in ('setup', 'look_for', 'question'):
            key = re.sub(r'\W+', ' ', a[k].lower()).strip()
            if key in seen: errs.append(f'{a["id"]}: {k} repeats {seen[key]}')
            seen[key] = f'{a["id"]}.{k}'
    def ref_ok(r):
        base, _, var = r.partition('#')
        if base not in acts: return False
        return not var or var in [v['id'] for v in acts[base].get('variants', [])]
    for a in acts.values():
        for r in a.get('pairs_with', []):
            if not ref_ok(r): errs.append(f'{a["id"]}: pairs_with {r} does not exist')
            if r == a['id']: errs.append(f'{a["id"]}: pairs with itself')
    for f in sorted((root / 'data' / 'plans').glob('*.yaml')):
        p = load(f); allowed = ladder[p['track']].get(p['age'], [])
        nums = [w['week'] for w in p['weeks']]
        if nums != list(range(1, len(nums) + 1)): errs.append(f'{f.name}: weeks are not numbered 1 to {len(nums)}')
        for w in p['weeks']:
            if w.get('coach_choice'): continue
            if w['block'] not in allowed: errs.append(f'{f.name} wk{w["week"]}: block {w["block"]} not allowed for {p["track"]} {p["age"]}')
            if w['level'] not in ladder['levels'][p['track']]: errs.append(f'{f.name} wk{w["week"]}: level {w["level"]} not used in {p["track"]}')
            for i, ses in enumerate(w['sessions'], 1):
                ids = []; full = []
                for slot in ('a', 'b'):
                    r = ses[slot]['activity']
                    if not ref_ok(r): errs.append(f'{f.name} wk{w["week"]} session {i} {slot}: unknown activity {r}'); continue
                    ids.append(r.split('#')[0]); full.append(r)
                if len(full) == 2 and full[0] == full[1]: errs.append(f'{f.name} wk{w["week"]} session {i}: A and B are the same activity')
                if ids and not any(acts[x]['block'] == w['block'] for x in ids):
                    errs.append(f'{f.name} wk{w["week"]} session {i}: neither activity is a {w["block"]} activity')

    # skills, goals and age configs
    vocab = load(root / 'data' / 'vocab' / 'skills.yaml')
    seen_b = {}
    for f in sorted((root / 'data' / 'skills').glob('*.yaml')):
        recs = load(f)['skills']; areas = {}
        for r in recs:
            if r['block'] not in BLOCKS: errs.append(f'{r["id"]}: bad block {r["block"]}')
            if not r.get('bullets'): errs.append(f'{r["id"]}: no bullets')
            for tr in r['tracks']:
                if r['level'] not in ladder['levels'][tr]: errs.append(f'{r["id"]}: level {r["level"]} not used in {tr}')
                if r['age'] in ladder[tr] and r['block'] not in ladder[tr][r['age']]: errs.append(f'{r["id"]}: block {r["block"]} not part of {tr} {r["age"]}')
            areas.setdefault((r['block'], r['area']), set()).add(r['level'])
            for b in r['bullets']:
                key = (r['age'], re.sub(r'\W+', ' ', b.lower()).strip())
                if key in seen_b: errs.append(f'{r["id"]}: bullet repeats {seen_b[key]}: "{b[:50]}"')
                seen_b[key] = r['id']
        for (b, a), lv in areas.items():
            if 'intro' not in lv: errs.append(f'{f.name}: {b} {a} has no intro level')
    for f in sorted((root / 'data' / 'goals').glob('*.yaml')):
        g = load(f)
        for x in g['goals']:
            for b in x['blocks']:
                if b not in BLOCKS: errs.append(f'goal {x["id"]}: bad block {b}')
    for f in sorted((root / 'data' / 'ages').glob('*.yaml')):
        a = load(f)
        for pid in a['pills']:
            if pid not in vocab: errs.append(f'{f.name}: pill {pid} is not in the skill vocabulary')
        if not (root / 'data' / 'goals' / (a['goals'] + '.yaml')).exists(): errs.append(f'{f.name}: goals file {a["goals"]} missing')
    return errs, acts
if __name__ == '__main__':
    errs, acts = check()
    for e in errs: print('ERROR', e)
    print(f'{len(acts)} activities checked, {len(errs)} problems')
    sys.exit(1 if errs else 0)
