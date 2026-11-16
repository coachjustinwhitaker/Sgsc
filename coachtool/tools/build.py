"""Builds pages from the records. Usage: python3 tools/build.py <plan id> <brand id>"""
import sys, re, html, base64, pathlib, yaml
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from check import check, load, ROOT
def esc(t):
    t = html.escape(t, quote=False)
    for ch, ent in {'’': '&rsquo;', '‘': '&lsquo;', '“': '&ldquo;', '”': '&rdquo;', '—': '&mdash;', '–': '&ndash;'}.items():
        t = t.replace(ch, ent)
    return t
def names_list(refs, acts):
    ns = []
    for r in refs:
        base, _, var = r.partition('#')
        ns.append(next(v['name'] for v in acts[base].get('variants', []) if v['id'] == var) if var else acts[base]['name'])
    return ns[0] if len(ns) == 1 else ' or '.join(ns) if len(ns) == 2 else ', '.join(ns[:-1]) + ', or ' + ns[-1]
def card(a, acts):
    equip = esc(a['equipment'])
    return f'''    <div class="act-card">
      <div class="act-header">
        <div class="act-num">Activity {a["order"]:02d}</div>
        <div class="act-name">{esc(a["name"])}</div>
        <div class="act-focus">{esc(" · ".join(a["skills"]))}</div>
      </div>
      <div class="act-body">
        <div class="a-label">Setup</div><div class="a-text">{esc(a["setup"])}</div>
        <div class="a-label">What to Look For</div><div class="a-text">{esc(a["look_for"])}</div>
        <div class="a-question">&ldquo;{esc(a["question"])}&rdquo;</div>
        <span class="pairs-tag">&#8594; Pairs well with: {esc(names_list(a["pairs_with"], acts))}</span>
        <div class="e-tags" style="margin-top:10px;"><span class="e-tag">{equip}</span></div>
      </div></div>
'''
def activities_html(plan, acts, blocks):
    out = ''
    for b in ['B1', 'B2', 'B3', 'B4', 'B5']:
        group = sorted([a for a in acts.values() if a['block'] == b and plan['age'] in a['ages'] and plan['track'] in a['tracks']], key=lambda a: a['order'])
        if not group: continue
        bl = blocks[b]
        out += f'''  <div class="skill-group-bar {bl["css"]}"><span class="skill-group-label">{esc(bl["name"].upper())} &nbsp;&mdash;&nbsp; {esc(bl["group_label"])}</span></div>
  <div class="activity-grid" style="margin-top:14px;">
''' + ''.join(card(a, acts) for a in group) + '  </div>\n\n'
    return out.rstrip('\n') + '\n'
def rotation_html(plan, acts):
    cell = 'style="vertical-align:middle;border-right:2px solid #e0e5f0;"'
    out = ''
    def nm(r):
        base, _, var = r.partition('#')
        return next(v['name'] for v in acts[base]['variants'] if v['id'] == var) if var else acts[base]['name']
    for w in plan['weeks']:
        if w.get('coach_choice'):
            out += f'''      <tr>
        <td class="week-num" style="border-right:2px solid #e0e5f0;">{w["week"]}</td>
        <td style="font-style:italic;color:var(--gray-mid);font-size:11.5px;border-right:1px solid #eee;">{esc(w["focus"])}</td>
        <td colspan="2" style="font-style:italic;color:var(--gray-mid);">{esc(w["note"])}</td>
      </tr>
'''
            continue
        s1, s2 = w['sessions']
        out += f'''
      <tr class="week-a">
        <td rowspan="2" class="week-num" {cell}>{w["week"]}</td>
        <td rowspan="2" style="vertical-align:middle;border-right:1px solid #eee;font-size:11.5px;font-style:italic;color:var(--gray-mid);">{esc(w["focus"])}</td>
        <td><span class="prac-label prac-a">Practice A</span><br>{esc(nm(s1["a"]["activity"]))}<div class="pair-tag">{esc(s1["a"]["note"])}</div></td>
        <td>{esc(nm(s1["b"]["activity"]))}<div class="pair-tag">{esc(s1["b"]["note"])}</div></td>
      </tr>
      <tr class="week-b">
        <td><span class="prac-label prac-b">Practice B</span><br>{esc(nm(s2["a"]["activity"]))}<div class="pair-tag">{esc(s2["a"]["note"])}</div></td>
        <td>{esc(nm(s2["b"]["activity"]))}<div class="pair-tag">{esc(s2["b"]["note"])}</div></td>
      </tr>'''
    return out
def build(plan_id, brand_id, out=None):
    errs, acts = check()
    if errs: sys.exit('Fix these first:\n' + '\n'.join(errs))
    plan = load(ROOT / 'data' / 'plans' / f'{plan_id}.yaml'); blocks = load(ROOT / 'data' / 'blocks.yaml')
    brand = load(ROOT / 'theme' / brand_id / 'brand.yaml')
    logo = 'data:image/png;base64,' + base64.b64encode((ROOT / 'theme' / brand_id / brand['logo_file']).read_bytes()).decode()
    age = load(ROOT / 'data' / 'ages' / f'{plan_id}.yaml'); vocab = load(ROOT / 'data' / 'vocab' / 'skills.yaml')
    goals = load(ROOT / 'data' / 'goals' / f"{age['goals']}.yaml")['goals']
    pills = '\n    '.join(f'<span class="pill {vocab[p]["kind"]}">{esc(vocab[p]["label"])}</span>' for p in age['pills'])
    note = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', esc(age['pills_note']))
    gl = '\n'.join(f'      <div class="profile-item">{esc(g["text"])}</div>' for g in goals)
    page = (ROOT / 'templates' / 'companion-rec.html').read_text(encoding='utf-8')
    page = page.replace('{{PILLS}}', pills).replace('{{PILLS_NOTE}}', note).replace('{{NEXT_AGE}}', age['next_age']).replace('{{GOALS}}', gl)
    page = page.replace('{{ACTIVITIES}}', activities_html(plan, acts, blocks)).replace('{{ROTATION}}', rotation_html(plan, acts))
    for k, v in brand.items(): page = page.replace('{{brand.%s}}' % k, v)
    page = page.replace('{{brand.logo_src}}', logo)
    left = [t for t in re.findall(r'\{\{[^}]+\}\}', page)]
    if left: sys.exit(f'Unfilled tokens: {left}')
    out = pathlib.Path(out or ROOT / 'build' / f'{plan_id}.{brand_id}.html'); out.write_text(page, encoding='utf-8'); return out
def build_app(plan_id, brand_id):
    import json
    errs, acts = check()
    if errs: sys.exit('Fix these first:\n' + '\n'.join(errs))
    import io, mimetypes
    from PIL import Image
    for a in acts.values():
        d = a.get('diagram')
        if not d: continue
        f = ROOT / 'data' / 'diagrams' / d
        if f.suffix.lower() == '.svg': raw, mime = f.read_bytes(), 'image/svg+xml'
        else:
            im = Image.open(f); im.thumbnail((720, 720)); buf = io.BytesIO()
            if im.mode in ('RGBA', 'LA', 'P'): im.save(buf, 'PNG', optimize=True); mime = 'image/png'
            else: im.convert('RGB').save(buf, 'JPEG', quality=82, optimize=True); mime = 'image/jpeg'
            raw = buf.getvalue()
        a['diagram_src'] = f'data:{mime};base64,' + base64.b64encode(raw).decode()
    blocks = load(ROOT / 'data' / 'blocks.yaml'); brand = load(ROOT / 'theme' / brand_id / 'brand.yaml'); ladder = load(ROOT / 'rules' / 'ladder.yaml')
    teams = []
    for pf in sorted((ROOT / 'data' / 'plans').glob('*.yaml'), key=lambda f: load(f)['age']):
        plan = load(pf); age = load(ROOT / 'data' / 'ages' / f"{plan['id']}.yaml"); fid = age['goals']
        skills = [r for f in (ROOT / 'data' / 'skills').glob(f"{plan['age']}.yaml") for r in load(f)['skills']]
        teams.append({'id': plan['id'], 'age': plan['age'], 'track': plan['track'], 'label': age.get('label', plan['age'].upper()), 'plan': plan,
                      'goals': load(ROOT / 'data' / 'goals' / f"{fid}.yaml")['goals'], 'players': load(ROOT / 'data' / 'players' / f"{age['players']}.yaml"),
                      'framework': load(ROOT / 'data' / 'framework' / f"{age['framework']}.yaml"), 'skills': skills, 'club': (load(ROOT / 'theme' / brand_id / 'overlay' / f"{plan['age']}.yaml") if (ROOT / 'theme' / brand_id / 'overlay' / f"{plan['age']}.yaml").exists() else {}), 'ladder': ladder[plan['track']][plan['age']]})
    data = {'activities': sorted(acts.values(), key=lambda a: a['order']), 'teams': teams, 'blocks': blocks, 'ladder': ladder}
    (ROOT / 'build' / 'data.json').write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
    logo = 'data:image/png;base64,' + base64.b64encode((ROOT / 'theme' / brand_id / brand.get('logo_small_file', brand['logo_file'])).read_bytes()).decode()
    page = (ROOT / 'app' / 'index.html').read_text(encoding='utf-8').replace('/*DATA*/', json.dumps(data, ensure_ascii=False))
    for k, v in brand.items(): page = page.replace('{{brand.%s}}' % k, v)
    page = page.replace('{{brand.logo_src}}', logo)
    left = re.findall(r'\{\{[^}]+\}\}', page)
    if left: sys.exit(f'Unfilled tokens: {left}')
    out = ROOT / 'build' / f'planner.{brand_id}.html'; out.write_text(page, encoding='utf-8'); return out
def build_author():
    import json
    errs, acts = check()
    if errs: sys.exit('Fix these first:\n' + '\n'.join(errs))
    build_app('u10-rec', 'sgsc')  # fills diagram_src on the activity records
    data = {'activities': sorted(acts.values(), key=lambda a: a['order']), 'blocks': load(ROOT / 'data' / 'blocks.yaml'),
            'tags': load(ROOT / 'data' / 'vocab' / 'activity-tags.yaml'), 'ladder': load(ROOT / 'rules' / 'ladder.yaml')}
    page = (ROOT / 'app' / 'author.html').read_text(encoding='utf-8').replace('/*DATA*/', json.dumps(data, ensure_ascii=False))
    out = ROOT / 'build' / 'activity-builder.html'; out.write_text(page, encoding='utf-8')
    (ROOT / 'build' / 'index.html').write_text('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Coach tool</title><style>body{font:18px/1.6 -apple-system,Segoe UI,Arial,sans-serif;max-width:560px;margin:40px auto;padding:0 16px}a{display:block;margin:12px 0}</style></head><body><h1>Coach tool</h1><a href="planner.sgsc.html">Season planner (rec: U8, U10, U12)</a><a href="activity-builder.html">Activity builder</a></body></html>', encoding='utf-8')
    return out
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'author': print('wrote', build_author()); sys.exit()
    if len(sys.argv) > 3 and sys.argv[3] == 'app': print('wrote', build_app(sys.argv[1], sys.argv[2])); sys.exit()
    print('wrote', build(sys.argv[1], sys.argv[2]))
