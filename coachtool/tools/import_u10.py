"""One-time import: reads the existing U10 companion page and writes activity and plan records.
Kept for provenance. After import, the records are the source of truth."""
import re, html, sys, yaml, pathlib
SRC = pathlib.Path(sys.argv[1]); OUT = pathlib.Path(sys.argv[2])
s = SRC.read_text(encoding='utf-8')
def txt(x): return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', x))).strip()
def slug(n): return re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')
# Names the old page used for the same activity. The checker found these mismatches.
ALIASES = {'4v2 Keep-Away': 'rondo', '1v1 to Goals': '1v1-to-endlines-goals', '1v1 to Endlines': '1v1-to-endlines-goals',
           '2v2 to Endlines': '2v2-to-endlines-attacking', '2v2 to Endlines — Attacking': '2v2-to-endlines-attacking',
           'Triangle Goal Game': 'gates-passing#triangle-goal-game'}
# Draft metadata. Players are group sizes the setup supports. Space is a size class. Review before use.
META = {'flying-numbers': (6, 16, 'medium'), 'shrinking-field': (6, 16, 'medium'), '1v1-to-endlines-goals': (2, 14, 'small'),
        'rondo': (5, 15, 'small'), 'gates-passing': (2, 16, 'medium'), 'end-zone-passing': (6, 16, 'medium'),
        'numbers-passing': (4, 8, 'small'), '2v2-to-endlines-attacking': (4, 12, 'small'), '3v2-to-goal': (5, 15, 'medium'),
        'five-goal-game': (6, 16, 'medium'), 'barcelona': (6, 16, 'medium'), 'rondo-5v2': (7, 14, 'small'),
        'approach-delay': (2, 12, 'small'), 'pressure-cover-3v3': (6, 12, 'medium'), 'shadow-marking': (8, 16, 'medium'),
        'squeeze-the-space': (9, 18, 'half')}
bars = [(m.start(), txt(m.group(1))) for m in re.finditer(r'<span class="skill-group-label">(.*?)</span>', s)]
def block_for(pos):
    b = [g for p, g in bars if p < pos][-1]
    return 'B1' if 'BALL' in b else 'B2' if 'TEAMMATES' in b else 'B3'
acts = []
for m in re.finditer(r'<div class="act-card">.*?</div></div>\n', s, re.S):
    c = m.group(0)
    g = lambda cls: re.search(r'<div class="%s">(.*?)</div>' % cls, c, re.S)
    d = {txt(k): txt(v) for k, v in re.findall(r'<div class="a-label">(.*?)</div>\s*<div class="a-text"[^>]*>(.*?)</div>', c, re.S)}
    pairs = txt(re.search(r'pairs-tag">(.*?)</span>', c, re.S).group(1)).replace('→ Pairs well with:', '').strip()
    acts.append(dict(order=int(txt(g('act-num').group(1)).split()[-1]), name=txt(g('act-name').group(1)),
        skills=[x.strip() for x in txt(g('act-focus').group(1)).split('·')], block=block_for(m.start()),
        setup=d['Setup'], look_for=d['What to Look For'], question=txt(g('a-question').group(1)).strip('“”"'),
        pairs_raw=[x.strip() for x in re.split(r',\s*(?:or\s+)?|\s+or\s+', pairs) if x.strip()],
        equipment=txt(re.search(r'<span class="e-tag">(.*?)</span>', c, re.S).group(1))))
ids = {a['name']: slug(a['name']) for a in acts}
ids['Approach & Delay'] = 'approach-delay'
def resolve(n):
    n = n.strip().rstrip('.')
    if n in ids: return ids[n]
    return ALIASES.get(n)
unresolved = []
(OUT / 'activities').mkdir(parents=True, exist_ok=True)
for a in acts:
    a['id'] = ids[a['name']]
    pw = []
    for n in a['pairs_raw']:
        r = resolve(n)
        if r: pw.append(r)
        else: unresolved.append((a['id'], n))
    lo, hi, space = META[a['id']]
    rec = {'id': a['id'], 'order': a['order'], 'name': a['name'], 'block': a['block'], 'skills': a['skills'],
           'ages': ['u10'], 'tracks': ['rec'], 'levels': ['intro'], 'players': {'min': lo, 'max': hi},
           'space': space, 'minutes': 15, 'setup': a['setup'], 'look_for': a['look_for'], 'question': a['question'],
           'pairs_with': pw, 'equipment': a['equipment']}
    if a['id'] == 'rondo': rec['aliases'] = ['4v2 Keep-Away']
    if a['id'] == 'gates-passing':
        rec['variants'] = [{'id': 'triangle-goal-game', 'name': 'Triangle Goal Game',
                            'note': 'Progression: replace the gates with cone triangles. Players score by passing through a triangle to their partner.'}]
    (OUT / 'activities' / f"{a['id']}.yaml").write_text(yaml.safe_dump(rec, sort_keys=False, allow_unicode=True, width=100), encoding='utf-8')
print(len(acts), 'activities; unresolved pairs:', unresolved)
# plan
tb = s[s.index('rotation-table'):]; tb = tb[:tb.index('</table>')]
weeks = []
for m in re.finditer(r'<tr class="week-a">(.*?)</tr>\s*<tr class="week-b">(.*?)</tr>', tb, re.S):
    ra, rb = m.group(1), m.group(2)
    num = int(txt(re.search(r'class="week-num"[^>]*>(.*?)</td>', ra).group(1)))
    focus = txt(re.findall(r'<td rowspan="2"[^>]*>(.*?)</td>', ra, re.S)[1])
    def slot(row, first):
        tds = re.findall(r'<td>(.*?)</td>', row, re.S)
        out = []
        for td in tds:
            nm = txt(re.sub(r'<span class="prac-label[^"]*">.*?</span><br>', '', re.sub(r'<div class="pair-tag">.*?</div>', '', td, flags=re.S)))
            note = txt(re.search(r'pair-tag">(.*?)</div>', td, re.S).group(1))
            r = resolve(nm) or unresolved.append(('plan wk%d' % num, nm)) or nm
            out.append({'activity': r, 'note': note})
        return out
    sa, sb = slot(ra, True), slot(rb, False)
    weeks.append({'week': num, 'focus': focus, 'sessions': [{'a': sa[0], 'b': sa[1]}, {'a': sb[0], 'b': sb[1]}]})
w8 = re.search(r'<td class="week-num"[^>]*>8</td>\s*<td[^>]*>(.*?)</td>\s*<td colspan="2"[^>]*>(.*?)</td>', tb, re.S)
weeks.append({'week': 8, 'focus': txt(w8.group(1)), 'coach_choice': True, 'note': txt(w8.group(2))})
BLOCK = {1: 'B1', 2: 'B1', 3: 'B2', 4: 'B2', 5: 'B2', 6: 'B3', 7: 'B3'}
for w in weeks:
    if w['week'] in BLOCK: w['block'] = BLOCK[w['week']]; w['level'] = 'intro'
plan = {'id': 'u10-rec', 'age': 'u10', 'track': 'rec', 'sessions_per_week': 2, 'weeks': weeks}
(OUT / 'plans').mkdir(parents=True, exist_ok=True)
(OUT / 'plans' / 'u10-rec.yaml').write_text(yaml.safe_dump(plan, sort_keys=False, allow_unicode=True, width=100), encoding='utf-8')
print('plan weeks:', len(weeks), 'unresolved total:', unresolved)
