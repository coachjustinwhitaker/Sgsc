"""One-time import of the U12 companion page into records (activities, plan, age, goals, players, framework, skills, club overlay)."""
import yaml, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
def dump(path, obj): path.parent.mkdir(parents=True, exist_ok=True); path.write_text(yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, width=100), encoding='utf-8')
def load(p): return yaml.safe_load(p.read_text(encoding='utf-8'))
ORDER = max(load(f)['order'] for f in (R / 'data' / 'activities').glob('*.yaml') if 'u12' not in load(f)['ages'] or 'u10' in load(f)['ages'] or 'u8' in load(f)['ages'])
def act(i, name, block, skills, lo, hi, space, setup, look_for, question, equipment, pairs):
    global ORDER; ORDER += 1
    return {'id': i, 'order': ORDER, 'name': name, 'block': block, 'skills': skills, 'ages': ['u12'], 'tracks': ['rec'], 'levels': ['intro'],
            'players': {'min': lo, 'max': hi}, 'space': space, 'minutes': 15, 'setup': setup, 'look_for': look_for, 'question': question,
            'pairs_with': pairs, 'equipment': equipment}
NEW = [
 act('half-and-half', 'Half and Half', 'B2', ['Supporting', 'Combination Play'], 6, 16, 'half',
  'Rectangular grid with goals at each end and a midpoint line of cones. 3v3 or 4v4. Normal scrimmage, except a goal only counts if the attacking team has at least one player in both their attacking AND defending halves when the goal is scored. The player who stays back is providing depth and defensive security.',
  'Forces players to spread across the length of the field, not just the width. The player who stays in the defending half might miss the goal celebration. Acknowledge them specifically. US Soccer introduces depth of shape explicitly at U12. This game teaches it without you naming it.',
  'The player who stayed back when your team scored: what were they protecting?', '1 ball · 2 small goals · Disc cones including midpoint line · Pinnies', ['flying-numbers', 'barcelona']),
 act('3v3-plus-1-keep-away', '3v3+1 Keep-Away', 'B2', ['Possession', 'Body Shape'], 7, 14, 'quarter',
  'Square of cones for every 7 players. Two teams of 3 in different colors, one neutral player who plays with whoever has the ball. Attackers rack up passes. When defenders win it, the neutral player switches sides immediately. No delay. After a minute, switch roles.',
  'The neutral player switching sides instantly is the whole point. That instant role switch seeds transition awareness naturally inside a possession game. Also look for players opening their hips to receive before the ball arrives. Works well as Activity B after Flying Numbers.',
  'When the ball turned over, how quickly did you read whose team you were joining or defending against?', '1 ball per grid · 4 cones per square · 3 colors of pinnies', ['flying-numbers']),
 act('2v2v2-keep-away', '2v2v2 Keep-Away', 'B3', ['Pressing', 'Covering'], 6, 18, 'quarter',
  'Square of cones for every 6 players. Three pairs in different colors. Two pairs attack and keep the ball away from the defending pair. When defenders steal or force a mistake, they replace the attacking pair who last touched the ball. Immediately, no stoppages. The new defenders must get into position fast.',
  'The defending pair must communicate constantly: who pressures the ball, who covers behind. Look for the pair who splits those jobs naturally. The team that defends compactly wins the ball most often.',
  'When you were the defending pair, how did you decide who would press the ball and who would cover?', '1 ball per grid · 4 cones per square · 3 colors of pinnies', ['flying-numbers', 'half-court-soccer']),
 act('half-court-soccer', 'Half Court Soccer', 'B3', ['Compact Shape', 'Marking'], 6, 14, 'half',
  'Rectangular grid, wider than it is long. A check line at one end, the goal at the other. Both teams attack the same goal, like half-court basketball. If a team steals the ball, they must clear it by dribbling over the check line before they can attempt to score. Play 3v3 plus an optional rotating goalkeeper.',
  'The check line creates a natural defending moment. Defenders must get compact between the ball and the goal. When the attack clears the line and comes back, defenders must re-organize quickly. Watch for players who position between opponent and goal rather than just chasing the ball.',
  'When the other team was dribbling toward goal, where were you standing? Between the ball and the goal, or somewhere else?', '1 ball · 1 goal · Disc cones including check line · Pinnies', ['2v2v2-keep-away', 'flying-numbers']),
 act('shrinking-field-defending', 'Shrinking Field: Defending Focus', 'B3', ['Compact Shape', 'Pressing'], 6, 16, 'quarter',
  'Rectangular grid with small goals at each end. 3v3 or 4v4. Every minute, move each touchline in by 3 steps. Explicitly frame it as a defending focus before starting: "today we are watching the defending team, not the attacking team." Play 2 to 3 rounds.',
  'As the field shrinks, the compact defending shape becomes more and more important. Watch for the defending team getting tighter: closer together, higher up, forcing play to one side. Are they reacting to the ball or anticipating where it is going? Any moment of anticipation is worth highlighting.',
  'As the field got smaller, did defending get easier or harder? What does that tell you about defending in tight spaces?', '1 ball · 2 small goals · Disc cones', ['half-court-soccer', '2v2v2-keep-away']),
 act('flying-numbers-transition', 'Flying Numbers: Transition Focus', 'B4', ['Decision-Making', 'Communication'], 8, 20, 'half',
  'Same as the opening game anchor, but now explicitly framed around transition. Outgoing players must sprint off the field. Incoming players must sprint on. No walking at any point during rotation. Call the numbers quickly so there is barely any gap between rounds.',
  'The transition moment is the entire point. What happens the instant a goal is scored or the ball goes out? Do players react and sprint in, or shuffle in? Urgency in transition is a habit and habits form through repetition. This is why Flying Numbers appears in both the anchor and focus roles.',
  'What is the difference between a team that sprints into transition and a team that walks? How does that change what the other team can do?', '1 ball · 2 goals · Disc cones · Pinnies', ['crisscross', 'hawaii']),
 act('crisscross', 'Crisscross', 'B4', ['Decision-Making', 'Scanning'], 4, 16, 'quarter',
  'Square grid with a goal on the middle of each side, 4 goals total. One team scores on the two endline goals; the other scores on the two touchline goals. Play 2v2 or 3v3. Score by passing through a goal to a teammate. The cross-axis attack means defenders must constantly re-orient.',
  'Trains the transition instinct directly: the instant you win the ball, find the goal immediately. Players who hesitate give defenders time to recover. Players who look up the moment they win possession and find a goal in one or two actions are showing what the transition block looks like in practice.',
  'How quickly after winning the ball did you find your target? What would have happened if you waited two more seconds?', "1 ball · 4 cone goals (pairs, arm's length apart) · Pinnies", ['flying-numbers-transition', 'hawaii']),
 act('hawaii', 'Hawaii', 'B4', ['Decision-Making', 'Pressing'], 6, 16, 'half',
  'Square grid. Two goals set back about 5 yards from each end, one per team. 3v3 or 4v4. Players can score on either goal on their end line but must shoot from inside the grid. Keep extra balls next to you and feed them in immediately after each score or out-of-bounds. Continuous play, no stoppages.',
  'The continuous play means players are constantly switching between attack and defense. Watch for who reacts instantly versus who celebrates and switches off. Relentless transitions make this the most game-realistic activity in this group.',
  'When a new ball came in while you were still celebrating a goal, how quickly did you switch back to defending?', 'Multiple balls (keep several nearby) · 4 goals in 2 pairs · Disc cones · Pinnies', ['flying-numbers-transition', 'crisscross']),
 act('hotbox', 'Hotbox', 'B2', ['Combination Play', 'Decision-Making'], 6, 16, 'half',
  "Rectangular grid with a small goal at each end and a no-go square (the hotbox) in the center. 3v3 or 4v4. Players cannot enter the hotbox. Only balls can pass through. When the attackers' path is blocked by the hotbox and a defender on one side, the solution is to switch the ball to the other side.",
  'Naturally brings in all four blocks in a single activity: ball mastery under pressure, switching the point of attack, cutting off lanes around the hotbox, and instant reaction on turnover. Best used in week 7 to observe all four without isolating any one.',
  'When your path was blocked, what did you do? And when the ball turned over, what was your first movement?', '1 ball · 2 small goals · Disc cones for outer grid and hotbox square · Pinnies', ['team-handball', 'five-goal-game']),
 act('team-handball', 'Team Handball', 'B2', ['Combination Play', 'Supporting'], 8, 18, 'half',
  'Mark space with 4 cones, goals at each end. Two teams. Players use their hands to pass and catch. They can run with the ball but only for three steps. Score with your feet, but only after a teammate passes you the ball. No dropping to yourself. If the ball hits the ground, goes out, or is intercepted, it is a turnover.',
  "Using their hands makes it easier for players to keep their heads up and see their teammates' positions. Because scoring requires an assist, combination play is mandatory, not optional. The three-step limit creates natural transition moments. Good final-week activity before the closing game.",
  'Because you had to score from a pass, what did you do differently in terms of your positioning than in a normal game?', '1 ball (any type) · 2 goals · Disc cones · Pinnies', ['hotbox', 'five-goal-game']),
]
for a in NEW: dump(R / 'data' / 'activities' / f'{a["id"]}.yaml', a)
# shared with U10: add U12 and give U12 its own wording
SHARED = {
 'flying-numbers': {'setup': 'Mark space with cones, goals on both sides. Two teams along the touchline either side of you. Call a number combo and each side sends in that number to scrimmage. New players rotate in after every goal or ball out. Frame the transition explicitly: outgoing players sprint off, incoming players sprint on. No walking at any point.',
   'look_for': 'The most adaptable game in the toolkit and the best anchor activity at U12. Works as pure anchor (high energy, familiar) or as a transition focus when you emphasize the urgency of sprinting in and out. If one player is dominating, play them 1v2.',
   'question': 'When you had more players than the other team, what did you do with that extra person?'},
 'barcelona': {'setup': 'Rectangular grid with goals at each end. 3v3 or 4v4, no goalkeeper. Score points equal to the number of passes completed before scoring: 8 passes before a goal = 8 points. A missed shot scores nothing. Play short rounds of 3 to 4 minutes.',
   'look_for': 'Watch for players who switch the ball to the far side before going to goal, drawing defenders before finding the opening. Celebrate it when it happens by name. Best as a focus activity, not an anchor.',
   'question': 'Before you scored, was there a moment where you switched the ball to the other side? What did that open up?'},
 'five-goal-game': {'setup': 'Rectangular grid with a cone goal in each corner plus one in the center, 5 goals total. 3v3 or 4v4. Players try to pass the ball through any goal to a teammate to score in any direction. Defenders protect all 5 goals and can only gain possession by intercepting or stealing.',
   'look_for': 'At U12 this game requires players to read the whole picture: all five goals, where teammates are, where defenders are. Watch for players who signal to a teammate where they are switching before the ball arrives. That anticipation is team play at its most sophisticated. Also watch for immediate transition reactions on every turnover.',
   'question': 'When you changed which goal you were going for, did your teammate know before you passed, or after?'}}
for i, texts in SHARED.items():
    p = R / 'data' / 'activities' / f'{i}.yaml'; o = load(p); o['ages'] = sorted(set(o['ages'] + ['u12'])); o.setdefault('for_age', {})['u12'] = texts; dump(p, o)
def sess(a, an, b, bn): return {'a': {'activity': a, 'note': an}, 'b': {'activity': b, 'note': bn}}
W = lambda n, focus, block, s1, s2, **kw: {'week': n, 'focus': focus, 'sessions': [s1, s2], 'block': block, 'level': 'intro', **kw}
weeks = [
 W(1, 'Me & the Ball and Me & My Teammates in a bigger game', 'B2',
   sess('flying-numbers', 'High energy, variable pressure. Settles the group into the new format', 'half-and-half', 'Depth in shape: at least one player in each half for a goal to count'),
   sess('3v3-plus-1-keep-away', 'Neutral player switches instantly on turnover. Seeds transition', 'barcelona', 'Patience and pass counting: points equal the number of passes before scoring')),
 W(2, 'Consolidating combination play before new focuses', 'B2',
   sess('flying-numbers', 'Call uneven numbers (2v1, 3v2) to demand decisions', 'five-goal-game', 'Change target when the path is blocked: combination play under decision pressure'),
   sess('barcelona', 'Revisit: can they beat last week\'s pass count before scoring?', 'team-handball', 'Must score from a pass, so combination play is mandatory')),
 W(3, 'Team defending introduced', 'B3',
   sess('flying-numbers', 'Anchor: familiar, resets energy between the two new concepts', '2v2v2-keep-away', 'Who presses, who covers? The first and second defender chain begins'),
   sess('2v2v2-keep-away', 'Revisit: add a 2-touch limit to increase pressure on defenders', 'half-court-soccer', 'Clear the ball over the check line before scoring: compact defending shape')),
 W(4, 'Team defending deepens: shape and pressure together', 'B3',
   sess('half-court-soccer', 'Revisit: now frame it explicitly as a defending focus', 'shrinking-field-defending', 'Compact shape becomes critical as space disappears'),
   sess('shrinking-field-defending', 'Revisit: ask did defending get easier or harder, and why?', '2v2v2-keep-away', 'Consolidation: can the defending pair now communicate without being reminded?')),
 W(5, 'Transitions introduced: both moments', 'B4',
   sess('flying-numbers-transition', 'Outgoing players sprint off, incoming players sprint on. No walking', 'crisscross', 'Four goals on different axes: find the goal instantly after winning the ball'),
   sess('crisscross', 'Revisit: how quickly after winning the ball do they find a target?', 'hawaii', 'Continuous play, no stoppages: relentless transitions both ways')),
 W(6, 'Transition moments deepen: urgency becoming habit', 'B4',
   sess('hawaii', 'Revisit: feed new balls in even faster. No celebrations mid-session', 'flying-numbers-transition', 'Revisit with emphasis: watch who reacts and who watches when the ball goes out'),
   sess('five-goal-game', 'Win the ball, find the goal immediately: both transitions in one game', 'hotbox', 'Switch the point of attack plus an immediate transition reaction'), also_blocks=['B2']),
 W(7, 'Integration: all four blocks in play together', 'B4',
   sess('hotbox', 'All four blocks in one game. Do not over-coach. Watch', 'team-handball', 'Must assist to score: combination play, positioning and transition'),
   sess('five-goal-game', 'Integration game: observe all four blocks without coaching any one', '3v3-plus-1-keep-away', 'Final consolidation: transition, possession and defending all present'), also_blocks=['B1', 'B2', 'B3']),
 {'week': 8, 'focus': "Coach's choice both days", 'coach_choice': True, 'note': 'What does your group love most? What do they still need most? Run your two best sessions of the season. Both are correct answers.'}]
dump(R / 'data' / 'plans' / 'u12-rec.yaml', {'id': 'u12-rec', 'age': 'u12', 'track': 'rec', 'sessions_per_week': 2, 'weeks': weeks})
dump(R / 'data' / 'ages' / 'u12-rec.yaml', {'id': 'u12-rec', 'age': 'u12', 'track': 'rec', 'label': 'U12',
 'pills': ['controlling', 'protecting', 'driving', 'dribbling', 'passing', 'shooting', 'scanning', 'supporting', 'body-shape', 'covering', 'marking'],
 'pills_note': 'Covering and Marking are the two defending perceptual skills players first met at U10. At U12 they move from individual actions into how the team defends. **Covering** means positioning close enough to the first defender to step in if they are beaten. **Marking** means tracking a specific opponent and denying them the ball in a good position. Together these two skills are how team defending starts to function rather than just individual reactions to the ball.',
 'next_age': 'U14', 'goals': 'u12', 'players': 'u12', 'framework': 'u12'})
goals = [('keeps-ball-pressure', 'Keeps the ball under pressure with confidence', ['B1']), ('passes-and-moves', 'Passes and moves without needing to be reminded', ['B2']),
 ('defends-as-team', 'Defends as part of a team, not just individually', ['B3']), ('reacts-to-turnover', 'Reacts to the moment the ball changes hands', ['B4']),
 ('communicates', 'Communicates with and coaches teammates on the field', ['B2', 'B3']), ('team-identity', 'Competes in 9v9 with real team identity', ['B1', 'B2', 'B3', 'B4']),
 ('wants-to-play', 'Shows up wanting to play again', ['B1', 'B2', 'B3', 'B4'])]
dump(R / 'data' / 'goals' / 'u12.yaml', {'age': 'u12', 'goals': [{'id': i, 'text': t, 'blocks': b} for i, t, b in goals]})
dump(R / 'data' / 'players' / 'u12.yaml', {'id': 'u12', 'age': 'u12',
 'who': [{'label': 'They have been around the game', 'text': 'Most of these players have been playing for several years. They are still developing their understanding that passing creates space and that defending takes real collective effort. They are ready to be coached on how their individual actions connect to what the team is doing.'},
  {'label': 'How you deliver feedback matters', 'text': 'Players at this age are more aware of how they look in front of their peers. When you have something to say to an individual, find something they did right first. Save whole-group feedback for moments of collective success, not individual correction.'},
  {'label': 'Two practices build habits', 'text': 'With two sessions a week, what you introduce on day one has time to settle before day two builds on it. Pay attention to what shows up in the second session without you asking for it. That carry-over is the sign the concept is taking hold.'},
  {'label': 'Ask them why, not just what', 'text': 'Players at this age can answer deeper questions. "Why does switching the ball make the defender\'s job harder?" is a question a U12 player can genuinely engage with. Use that.'}],
 'great_session': [{'title': 'Immediate reaction to transition', 'text': 'When the ball turns over, do players react instantly? Or do they watch it happen? That first-second reaction is the whole introduction to the game-moments block.'},
  {'title': 'Compact defending shape', 'text': 'Are defenders close enough to support each other? The distance between first and second defender tells you everything about their shape.'},
  {'title': 'Combination play happening naturally', 'text': 'Players who are passing and moving without being asked are showing that the habits from U10 are sticking. If it is not happening yet, go back to a simpler passing activity. The habit builds with repetition.'},
  {'title': 'Players coaching each other', 'text': 'US Soccer notes this explicitly at U12: player-to-player coaching is a development goal, not just a nice thing to see. Step back when it happens.'},
  {'title': 'Practice A concept in Practice B', 'text': 'If a concept introduced in the first session of the week appears in the second session without you asking for it, that is the whole point of two practices a week.'},
  {'title': 'Everyone gets time in goal', 'text': 'Rotate the goalkeeper so every player experiences the position. If someone shows real enthusiasm for it, encourage that too. Positional identity starts forming at this age.'}],
 'prepared': 'Preparation at U12 matters more than at any previous age. You have four active focuses and a season arc that builds deliberately. Know which focus is the priority for this week before you arrive. With two practices per week, Practice A introduces the concept and Practice B deepens it. If the group needs more time on the same concept before moving forward, run the consolidation instead. Both are correct responses. Try to avoid pairing two new concepts in the same session: Activity A works best as something players already know well enough to run without much explanation, and Activity B is where the new concept lives.',
 'parents': {'intro': 'Before the session starts, take 30 seconds to walk over. Something like:',
  'script': 'Today we are working on what happens when the ball changes hands, in the first second after we win it or lose it. The most helpful thing you can do is cheer the team moments: the player who sprints to press the second they lose the ball, the player who finds a teammate the instant they win it.',
  'outro': 'At this age players are more aware of what the sideline is saying than they were at U8 or U10. Positive sideline energy is genuinely useful. Critical sideline energy genuinely disrupts.'},
 'shape': {'title': 'The session', 'note': 'Up to 90 minutes. Arrive 15 minutes early. Opening game, Activity A, Activity B, closing game.',
  'opening': {'label': 'Opening game', 'minutes': '12 min', 'title': '5v5 or 6v6 free small-sided game',
   'setup': 'Same setup every session. Smaller than the closing game, so more touches and cleaner decisions. Small goals or full goals depending on space. Teams of 5 or 6, no goalkeeper. Quick restarts. Let them play the first 8 minutes without saying anything. On Practice B days, watch specifically for whether the concept from Practice A earlier in the week shows up.',
   'job': 'Watch the transition moments specifically. What happens in the first couple of seconds after the ball changes hands? That tells you which focus area to prioritize today. Come in with Activity A already chosen and let the opening game confirm your read.',
   'question': 'When the ball changed hands today, when you won it or lost it, what was your first reaction?', 'kit': '1 ball per team · Small or full goals · Disc cones · Pinnies in 2 colors'},
  'closing': {'label': 'Closing game', 'minutes': '25 min', 'title': 'Full game',
   'setup': 'The biggest game of the session. Proper goals if possible. Include a goalkeeper and rotate it so every player experiences the position across the season. No offside until players are genuinely ready for it. Let the game run without stopping. Watch for the focus you introduced that week showing up without being asked for: a compact defensive shape, or a player who sprints to press the instant possession is lost. On Practice B days, notice whether anything from the first session carried over.',
   'question': 'Was there a moment today where your whole team did something together, attacking or defending, that one player could not have done alone?', 'kit': 'Proper goals if possible · Disc cones · Pinnies in 2 colors'}},
 'cues': [{'when': 'Team defends compactly', 'say': '"That shape right there, everyone close enough to support each other. That is exactly what we are building toward."'},
  {'when': 'Player presses instantly after turnover', 'say': 'Name it in the moment: "Did everyone see that? No hesitation, immediate reaction. That is what we are building toward."'},
  {'when': 'Player switches the point of attack', 'say': '"That pass across the field: what did it do to the defenders? It made them run. That is the whole idea."'},
  {'when': 'Players coaching each other', 'say': 'Step further back. Let it run. Come back and ask: "What did you tell your teammate there?"'},
  {'when': 'Concept from Practice A shows up in Practice B', 'say': '"You did that in the first session this week. Your body remembered. That is exactly what two practices is for."'},
  {'when': 'Players too self-critical', 'say': '"The best players in the world make mistakes in every game. The difference is what they do next."'}]})
def sk(b, area, bullets): return {'id': f'u12-{b.lower()}-{area.lower().replace(" ", "-")}-intro', 'age': 'u12', 'block': b, 'area': area, 'level': 'intro', 'tracks': ['rec'], 'bullets': bullets}
dump(R / 'data' / 'skills' / 'u12.yaml', {'skills': [
 sk('B1', 'Scanning and Body Shape', ['Scan before the ball arrives and again as pressure closes in', 'Open the hips and shoulders toward the attacking goal when receiving', 'Keep the head up while dribbling in a busy space']),
 sk('B1', 'Controlling', ['Control passes that arrive in the air, on the bounce or on the turn', 'Take the first touch away from the nearest opponent', 'Play one touch when the pass is right there']),
 sk('B1', 'Protecting', ['Hold off a closing opponent with the body and the arm out for balance', 'Keep the ball on the far foot from the defender', 'Release the ball at the right moment']),
 sk('B1', 'Driving and Dribbling', ['Drive into open space at speed', 'Accelerate past a defender after a change of direction', 'Choose between taking on a defender and passing']),
 sk('B1', 'Passing', ['Play the pass at the right speed and at the right time', 'Lead a teammate with the pass into space', 'Play a longer pass in the air when the field allows']),
 sk('B1', 'Shooting', ['Read the goalkeeper before shooting', 'Shoot to the far side from an angle', 'Take one touch when an opponent is closing']),
 sk('B2', 'Supporting', ['Create height, width and depth around the ball', 'Offer a vertical or diagonal option to the player on the ball', 'Move off a teammate so two players are not in the same space']),
 sk('B2', 'Switching and Wall Passes', ['Switch the ball to the far side when the near side is closed', 'Play a wall pass (give and go) in a small space', 'Recognize when a teammate on the other side is free']),
 sk('B2', 'Combining in Threes', ['Find the free player between or behind the opposition', 'Make a third-player run when two teammates are combining', 'Engage a defender 1v1 or 2v1 to create the space']),
 sk('B2', 'Decision-Making', ['Choose the quick pass or the dribble based on the pressure', 'Talk to teammates with calls that help', 'Stay involved in the next play after passing']),
 sk('B3', 'Pressure, Cover and Support', ['The nearest player pressures the ball', 'The second player covers behind the presser at a distance that lets them step in', 'The rest of the team supports to cut off space']),
 sk('B3', 'Compact Shape', ['Stay close to teammates so the space between lines is small', 'Move together toward the ball side', 'Close the middle of the field first']),
 sk('B3', 'Marking and Intercepting', ['Stay between the opponent and the goal', 'Mark a specific opponent and deny them the ball in a good position', 'Step in to intercept when the pass is on']),
 sk('B3', 'Recovery and Preventing the Switch', ['Recover goal-side when pressure is broken', 'Cut off the pass to the far side', 'Re-apply pressure as soon as the shape is back']),
 sk('B4', 'Reacting When We Lose It', ['React in the first second after losing the ball', 'Press at once if teammates are close, delay if they are not', 'Sprint back into shape when pressure is broken']),
 sk('B4', 'Reacting When We Win It', ['Look up for the first pass forward on winning the ball', 'Join the attack with speed', 'Play forward when it is on and keep it when it is not']),
 sk('B4', 'Urgency in the Moment', ['Recognize at once that possession has changed', 'Accelerate toward the ball or space', 'Keep the intensity through repeated turnovers'])]})
dump(R / 'data' / 'framework' / 'u12.yaml', {'age': 'u12', 'blocks': {
 'B1': {'tagline': 'Same habits, more pressure.', 'overview': 'Players know the individual skills from U8 and U10. At U12 they deepen them under more pressure, on a bigger field, with more opponents. Scanning, body shape, first touch, passing range and shooting all get tested at a faster speed.', 'problem': 'Players receive, protect and move the ball under real pressure, with their head up and body open.', 'focus': ['Scanning before and during receiving', 'First touch away from pressure', 'Passing at the right speed and time', 'Reading the goalkeeper when shooting']},
 'B2': {'tagline': 'Pass, move, and switch the picture.', 'overview': 'This block goes deeper than U10 as the game gets more complex. Players learn to give the team height, width and depth, to switch the point of attack, to use wall passes in small spaces, and to find the third player.', 'problem': 'Players use teammates to move the defense: spreading out, switching the ball and combining to find free players.', 'focus': ['Height, width and depth', 'Switching the point of attack', 'Wall passes and third-player runs', 'Finding free players between the lines']},
 'B3': {'tagline': 'Defend together.', 'overview': 'Compact team shape and team defending are reinforced and emphasized from U10. One player pressures the ball, one covers behind, and the rest support to cut off space. Defending moves from individual actions to how the team defends.', 'problem': 'Players defend as a team: pressure, cover and support, with a compact shape and a plan for the far side.', 'focus': ['Pressure, cover and support', 'Compact shape and distances', 'Marking and intercepting', 'Recovering and preventing the switch']},
 'B4': {'tagline': 'React in the first second.', 'overview': 'This block is introduced at U12. It covers both transition moments: what we do the instant we lose the ball, and the instant we win it. At this age the aim is the habit of reacting at once, not complex decisions.', 'problem': 'Players recognize the moment possession changes and react at once, pressing or recovering when it is lost and looking forward when it is won.', 'focus': ['Recognizing the turnover instantly', 'Immediate pressure or recovery', 'First pass forward on winning the ball', 'Urgency repeated across the game']}}})
dump(R.parent / 'coachtool' / 'theme' / 'sgsc' / 'overlay' / 'u12.yaml', {'format': '9v9',
 'pathway': ['Some players will show real passion and ability this season', "Sierra Gold's competitive program exists to open more doors for those players when they are ready", 'Talk to your club director about what that pathway looks like'],
 'contact': 'Got a question about an activity? Want to talk through what you are seeing at training? Not sure how to introduce a new concept to your group? Your Age Group Coordinator and the club Technical Director are there for exactly this. Reach out any time.'})
