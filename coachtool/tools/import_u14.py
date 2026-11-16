"""One-time import of the U14 companion page into records. Skill areas (Introduction column) and block text come from the B1-B5 content docs."""
import yaml, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
def dump(path, obj): path.parent.mkdir(parents=True, exist_ok=True); path.write_text(yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, width=100), encoding='utf-8')
def load(p): return yaml.safe_load(p.read_text(encoding='utf-8'))
vp = R / 'data' / 'vocab' / 'skills.yaml'; v = vp.read_text(encoding='utf-8')
if 'finishing:' not in v: vp.write_text(v.rstrip('\n') + '\nfinishing: {label: Finishing, kind: tech}\ntiming-runs: {label: Timing Runs, kind: perc}\n', encoding='utf-8')
ORDER = max(load(f)['order'] for f in (R / 'data' / 'activities').glob('*.yaml'))
def act(i, name, block, skills, lo, hi, space, setup, look_for, question, equipment, pairs):
    global ORDER; ORDER += 1
    return {'id': i, 'order': ORDER, 'name': name, 'block': block, 'skills': skills, 'ages': ['u14'], 'tracks': ['rec'], 'levels': ['intro'],
            'players': {'min': lo, 'max': hi}, 'space': space, 'minutes': 15, 'setup': setup, 'look_for': look_for, 'question': question,
            'pairs_with': pairs, 'equipment': equipment}
NEW = [
 act('duels-to-goal', 'Duels to Goal', 'B5', ['Shooting', 'Decision-Making'], 6, 20, 'half',
  'Two lines of players about 25 yards from a full-size goal with a goalkeeper (rotate keepers often). The coach plays a ball in. The first attacker and first defender race to it and play 1v1 to goal. Shot, save, miss or ball out ends the duel. Next pair goes. Keep the pace quick: three or four duels per player, then swap roles.',
  'The moment of decision: does the attacker commit, or hesitate and give the defender time? Look for the attacker who takes one decisive touch toward goal, and for the player who shoots early instead of dribbling one extra time. For defenders, look for patience: delay, do not dive in.',
  'When you had the ball facing the goalkeeper, what did you decide first: shoot, dribble, or pass? What told you that?', 'Balls in a bag · 1 full-size goal · Disc cones · Pinnies', ['flying-numbers', 'waves']),
 act('waves', 'Waves', 'B5', ['Numerical Advantage', 'Passing', 'Shooting'], 8, 20, 'full',
  "Full-size goal with a goalkeeper. Three attackers start from the halfway line against two defenders and attack in waves. When the wave finishes (goal, save, or ball out), the three attackers become the next wave's defenders, and the two defenders go to the back of the attacking line. Coach feeds a new ball in right away so play is continuous.",
  'Numbers-up decisions are the heart of this one. Watch for the attacker who carries the ball until a defender commits, then passes. Watch for the third attacker arriving late into the box. Celebrate a good final pass as loudly as the goal.',
  'With three against two, who decided when to pass and when to shoot? How did you know?', 'Balls in a bag · 1 full-size goal · Disc cones · Pinnies in 2 colors', ['duels-to-goal', 'wide-service-finishing']),
 act('wide-service-finishing', 'Wide Service Finishing', 'B5', ['Shooting', 'Supporting'], 8, 18, 'half',
  'Full-size goal with a goalkeeper. Wide players on each flank serve balls into the box while two or three attackers arrive to finish. Start with serves along the ground or driven low, finish with feet. Once the group is confident, add a defender in the box. Rotate servers, finishers and the goalkeeper every few turns. Heading is optional: if you include it, use a lighter ball, toss to the head from short range, and keep the total number of headers very low.',
  'Do the attackers time their runs so they arrive as the ball does, rather than standing in the box waiting? Do they attack the near post and far post with different players? Watch for the serve itself: low and hard, away from the goalkeeper, is hard to defend.',
  'When the cross came in, how did you decide where to run? What did your teammate do differently from you?', 'Balls in a bag · 1 full-size goal · Disc cones for the wide channels · Pinnies', ['waves', 'flying-numbers'])]
for a in NEW: dump(R / 'data' / 'activities' / f'{a["id"]}.yaml', a)
SHARED = {
 'flying-numbers': {'setup': 'Mark a space with cones, goals on both sides. Two teams along the touchline either side of you. Call a number combination and each side sends in that many players to scrimmage. New players rotate in after every goal or ball out. Outgoing players sprint off, incoming players sprint on. No walking at any point.',
   'look_for': 'Your anchor activity every week. Players know it from U12, so it needs almost no explanation and it settles the group fast. At U14, call uneven numbers (3v2, 4v3) and watch what the extra player does. If one player is dominating, play them 1v2.',
   'question': 'When your team had the extra player, what did you do with that advantage?'},
 'barcelona': {'setup': 'Rectangular grid with goals at each end. 4v4, no goalkeeper. Score points equal to the number of passes completed before scoring: 8 passes before a goal is 8 points. A missed shot scores nothing. Play short rounds of 3 to 4 minutes.',
   'look_for': 'Watch for players who switch the ball to the far side before going to goal, drawing defenders across before finding the opening. Name it when it happens. Best as a focus activity, not an anchor.',
   'question': 'Before you scored, was there a moment you switched the ball to the other side? What did that open up?'},
 'shrinking-field-defending': {'setup': 'Rectangular grid with small goals at each end. 4v4 or 5v5. Every minute, move each touchline in by 3 steps. Tell them before you start: "today we are watching the defending team." Play 2 to 3 rounds.',
   'look_for': 'As the field shrinks, compact shape matters more and more. Watch for the defending team getting tighter: closer together, higher up, forcing play to one side. Are they reacting to the ball or anticipating where it is going? Anticipation is worth naming.',
   'question': 'As the field got smaller, did defending get easier or harder? What does that tell you about defending in tight spaces?'},
 'crisscross': {'setup': 'Square grid with a goal in the middle of each side, 4 goals total. One team scores on the two endline goals, the other on the two touchline goals. Play 3v3 or 4v4. Score by passing through a goal to a teammate. The cross-axis attack forces defenders to re-orient constantly.',
   'look_for': 'The instant a team wins the ball, do they look up and find a target within one or two actions? Players who hesitate give defenders time to recover. That first-second decision is the whole transition idea.',
   'question': 'How quickly after winning the ball did you find your target? What would have happened if you waited two more seconds?'},
 'hotbox': {'setup': "Rectangular grid with a small goal at each end and a no-go square (the hotbox) in the center. 4v4 or 5v5. Players cannot enter the hotbox. Only the ball can pass through it. When the attackers' path is blocked by the hotbox and a defender, the solution is to switch the ball to the other side.",
   'look_for': 'Generates all five blocks in a single game: ball skills under pressure, switching with teammates, cutting off lanes around the box, instant reaction on turnovers, and a decisive finish when the opening appears. Best used in week 7 to observe without isolating any one block. Do not over-coach. Watch.',
   'question': 'When your path was blocked, what did you do? And when the ball turned over, what was your first movement?'}}
for i, texts in SHARED.items():
    p = R / 'data' / 'activities' / f'{i}.yaml'; o = load(p); o['ages'] = sorted(set(o['ages'] + ['u14']), key=lambda x: int(x[1:])); o.setdefault('for_age', {})['u14'] = texts; dump(p, o)
def sess(a, an, b, bn): return {'a': {'activity': a, 'note': an}, 'b': {'activity': b, 'note': bn}}
W = lambda n, focus, block, s1, s2, **kw: {'week': n, 'focus': focus, 'sessions': [s1, s2], 'block': block, 'level': 'intro', **kw}
weeks = [
 W(1, 'Ball skills and combination play on the bigger field', 'B2',
   sess('flying-numbers', 'Anchor. Familiar, settles the group into the new format', 'barcelona', 'Pass counting. Patience before scoring'),
   sess('flying-numbers', 'Call uneven numbers: 3v2, 4v3', 'barcelona', "Revisit. Can they beat last session's pass count?")),
 W(2, 'Team defending with more players and more space', 'B3',
   sess('flying-numbers', 'Anchor', 'shrinking-field-defending', 'Compact shape as space disappears'),
   sess('shrinking-field-defending', 'Revisit. Did defending get easier or harder? Why?', 'barcelona', 'Can the team that just defended now keep the ball against pressure?')),
 W(3, 'Both transition moments revisited', 'B4',
   sess('flying-numbers', 'Sprint on, sprint off. No walking', 'crisscross', 'Find a target the instant the ball is won'),
   sess('crisscross', 'Revisit. How fast after winning the ball do they find a target?', 'shrinking-field-defending', 'Win it, then what? Defend, win, go')),
 W(4, 'Finishing introduced: the decisive action in front of goal', 'B5',
   sess('flying-numbers', 'Anchor. Add a bonus for the first shot after a turnover', 'duels-to-goal', '1v1 to a full-size goal. First decision, first touch, shoot'),
   sess('duels-to-goal', 'Revisit. Reward the early shot and the composed finish', 'waves', '3v2 in waves. When to pass, when to shoot')),
 W(5, 'Finishing deepens: numbers-up decisions and arriving in the box', 'B5',
   sess('duels-to-goal', 'Warm up the finishing with quick duels', 'waves', 'Revisit. Celebrate the final pass'),
   sess('waves', 'Revisit with a second defender recovering late', 'wide-service-finishing', 'Serve low and hard. Attack near and far post')),
 W(6, 'Finishing in context: after transition and combination play', 'B5',
   sess('flying-numbers', 'Anchor. Finish at speed after sprints', 'wide-service-finishing', 'Revisit. Add a defender in the box'),
   sess('wide-service-finishing', 'Revisit. Better timing than last session?', 'crisscross', 'Win the ball, find a target, finish')),
 W(7, 'Integration: all five blocks in play together', 'B5',
   sess('hotbox', 'All five blocks in one game. Observe, do not over-coach', 'waves', 'Final consolidation of finishing under numbers'),
   sess('crisscross', 'Transition urgency', 'hotbox', 'Revisit. What is different from earlier today?'), also_blocks=['B1', 'B2', 'B3', 'B4']),
 {'week': 8, 'focus': "Coach's choice both days", 'coach_choice': True, 'note': 'What does your group love most? What do they still need most? Run your two best sessions of the season. Both are correct answers.'}]
dump(R / 'data' / 'plans' / 'u14-rec.yaml', {'id': 'u14-rec', 'age': 'u14', 'track': 'rec', 'sessions_per_week': 2, 'weeks': weeks})
dump(R / 'data' / 'ages' / 'u14-rec.yaml', {'id': 'u14-rec', 'age': 'u14', 'track': 'rec', 'label': 'U14',
 'pills': ['controlling', 'protecting', 'driving', 'dribbling', 'passing', 'shooting', 'finishing', 'scanning', 'supporting', 'body-shape', 'covering', 'marking', 'timing-runs'],
 'pills_note': '**Finishing** and **Timing Runs** are the new pieces this season. Finishing is shooting with composure when it matters: choosing the corner, striking cleanly, and following up. Timing a run means arriving in the right place at the right moment, not early and not late. Both are what the finishing block looks like in action.',
 'next_age': 'the next level', 'goals': 'u14', 'players': 'u14', 'framework': 'u14'})
goals = [('keeps-ball-full-field', 'Keeps the ball under pressure on the full field', ['B1']), ('defends-as-eleven', 'Defends as part of an eleven-player team', ['B3']),
 ('first-second', 'Reacts in the first second after the ball changes hands', ['B4']), ('shoots-with-composure', 'Takes shots with composure and makes good final-third decisions', ['B5']),
 ('times-runs', 'Times runs to arrive when the ball does', ['B2', 'B5']), ('communicates', 'Communicates with and coaches teammates on the field', ['B2', 'B3']),
 ('wants-to-play', 'Shows up wanting to play again', ['B1', 'B2', 'B3', 'B4', 'B5'])]
dump(R / 'data' / 'goals' / 'u14.yaml', {'age': 'u14', 'goals': [{'id': i, 'text': t, 'blocks': b} for i, t, b in goals]})
dump(R / 'data' / 'players' / 'u14.yaml', {'id': 'u14', 'age': 'u14',
 'who': [{'label': 'Growth is uneven', 'text': 'In any U14 group you will see players who have already grown a lot and players who have not started. Do not read size as skill. Praise decisions and effort, and watch that your biggest players are not only winning duels with size.'},
  {'label': 'The field got big', 'text': 'The jump from 9v9 to 11v11 is a jump in distance, not just numbers. Players tire faster and shape breaks down. Short rests and water breaks are coaching tools, not weaknesses.'},
  {'label': 'Peers matter more than you', 'text': 'At this age what teammates think carries a lot of weight. Individual feedback works best quietly, one on one. Public praise for team moments and brave decisions builds the culture you want.'},
  {'label': 'Some will be ready for more', 'text': 'A few players in your group may be curious about a more competitive pathway. Notice them, encourage them, and pass it on to your club. Do not promise anything. Just open the door.'}],
 'great_session': [{'title': 'Players take the shot', 'text': 'The ball is in the final third and someone shoots, early, with composure, without a second dribble. Missing is fine. Not shooting is the problem.'},
  {'title': 'Compact, connected shape', 'text': 'Eleven players on a big field can look scattered. Look for lines that stay close enough to support each other: defenders, midfielders and forwards moving as one unit.'},
  {'title': 'Instant reaction on turnovers', 'text': 'When the ball changes hands, do players react in the first second or watch? That reaction is the whole game-moments block.'},
  {'title': 'Players talking to each other', 'text': 'Voices on the field: "Man on," "Turn," "Switch." Player-to-player coaching is a development goal. Step back when it happens.'},
  {'title': 'Practice A concept in Practice B', 'text': 'If something from the first session of the week shows up in the second without you asking, the concept is taking hold.'},
  {'title': 'Everyone gets a turn in goal', 'text': 'Rotate the goalkeeper. Finishing practice is also goalkeeper practice, so nobody should miss out on a turn.'}],
 'prepared': 'Preparation at U14 is simpler than at U12, because the group already knows the language. Pick the week\'s focus before you arrive and choose Activity A as something familiar. Activity B is where the new idea lives. If the group needs more time on a concept, run the revisit instead of moving on. With two practices a week, Practice A introduces and Practice B deepens. Both are correct. Try to avoid pairing two new concepts in the same session.',
 'parents': {'intro': 'Before the session starts, take 30 seconds to walk over. Something like:',
  'script': 'This season we are working on finishing and on the moment the ball changes hands. The most helpful thing you can do is cheer the brave decisions: the player who shoots, the player who sprints back, the player who tries the pass that might not work.',
  'outro': 'At U14 players hear everything. Positive sideline energy is genuinely useful. Criticism of a missed shot makes the next shot less likely.'},
 'shape': {'title': 'The session', 'note': 'Up to 90 minutes. Arrive 15 minutes early. Opening game, Activity A, Activity B, closing game.',
  'opening': {'label': 'Opening game', 'minutes': '12 min', 'title': '6v6 or 7v7 free small-sided game',
   'setup': 'Same setup every session. Smaller than the closing game, so more touches, more shots and cleaner decisions. Half a field, with a full-size or large goal at each end. Teams of 6 or 7. Add a goalkeeper if you have one willing. Quick restarts. Let them play the first 8 minutes without saying anything. On Practice B days, watch for whether the concept from Practice A earlier in the week shows up.',
   'job': 'Watch the moments in front of goal. Do players shoot? Do they pick their moment or force it? Watch the transitions too. Come in with Activity A already chosen and let the opening game confirm your read for Activity B.',
   'question': 'When you had a chance to shoot today, what made you take it or pass it up?', 'kit': '1 ball per team · Full-size or large goals · Disc cones · Pinnies in 2 colors'},
  'closing': {'label': 'Closing game', 'minutes': '25 min', 'title': 'Full game',
   'setup': 'The biggest game of the session. Full field, full-size goals, goalkeepers. Play 11v11 if you have the numbers. Short of players? Play 9v9 or 10v10 on a narrower field rather than leaving gaps. Alternatively, put a full-size goal with a keeper at one end and two small goals at the halfway line for the other team to attack. Offside applies, so introduce it early in the season and be patient with it. Let the game run without stopping. Watch for the focus you introduced that week showing up without being asked: a team that stays compact across three lines, a player who sprints to press the instant possession is lost, a forward who shoots when the chance comes.',
   'question': 'Was there a moment today where your whole team did something together, attacking or defending, that one player could not have done alone?', 'kit': 'Full field · Full-size goals · Disc cones · Pinnies in 2 colors'}},
 'cues': [{'when': 'Player shoots early and misses', 'say': '"Good decision. Great shot to take. Take that one every time." Praise the decision before you talk about the technique.'},
  {'when': 'Player passes up a clear shot', 'say': 'Ask, do not tell: "What were you thinking when you had that space?" Then listen. Often it is confidence, not judgment.'},
  {'when': 'Team defends compactly', 'say': '"That shape right there, everyone close enough to support each other. That is exactly what we are building toward."'},
  {'when': 'Player presses instantly after turnover', 'say': 'Name it in the moment: "Did everyone see that? No hesitation. That is the whole idea."'},
  {'when': 'Players coaching each other', 'say': 'Step further back. Let it run. Come back and ask: "What did you tell your teammate there?"'},
  {'when': 'Players too self-critical', 'say': '"The best players in the world miss shots and lose the ball in every game. The difference is what they do next."'}]})
def sk(b, area, bullets): return {'id': f'u14-{b.lower()}-{area.lower().replace(" ", "-").replace("&", "and").replace("(", "").replace(")", "")}-intro', 'age': 'u14', 'block': b, 'area': area, 'level': 'intro', 'tracks': ['rec'], 'bullets': bullets}
dump(R / 'data' / 'skills' / 'u14.yaml', {'skills': [
 sk('B1', 'Perception and Preparation', ['Scan before receiving to identify pressure and options', 'Begin orienting the body to see the field before the ball arrives', 'Recognize the obvious difference between time and immediate pressure']),
 sk('B1', 'Controlling', ['Treat first touch as a decision, not just control', 'Receive across the body to begin opening up the field', 'Use small, controlled touches to set up the next action']),
 sk('B1', 'Protecting', ['Shield and protect the ball when no forward option exists', 'Use the body between the ball and the defender', 'Hold possession until a forward option opens']),
 sk('B1', 'Driving', ['Attack the ball under pressure, move toward it rather than waiting', 'Push into open space when it is available', 'Begin to play with the head up while moving with the ball']),
 sk('B1', 'Dribbling', ['Use a first action, touch or feint, to create space', 'Begin recognizing obvious 1v1 moments', 'Show basic coordination when changing direction with the ball']),
 sk('B1', 'Passing', ['Play forward when possible, support when not', 'Use one touch when the pass dictates it', 'Begin passing accurately with both feet under light pressure']),
 sk('B1', 'Decision-Making', ['Base the decision on body shape and scan before contact', 'Recognize forced one-touch situations versus time to take a touch', 'Decisions are deliberate and often reactive at this level']),
 sk('B2', 'Perception and Preparation', ['Scan beyond the ball to identify nearby teammates', 'Recognize simple support positions: behind, beside and ahead of the ball', 'Identify when a teammate is under pressure and needs an outlet']),
 sk('B2', 'Supporting', ['Offer a clear passing option when a teammate has the ball', 'Move to avoid standing directly behind a defender', 'Reposition after passing rather than watching what happens next']),
 sk('B2', 'Technique for Combination Play', ['Execute basic wall passes at reduced speed', 'Use a simple supporting movement after passing', 'Adjust passing technique to play to feet rather than space in combination situations']),
 sk('B2', 'Passing and Movement', ['Pass and then move to a new supporting position rather than watching the pass', 'Offer a clear option when a teammate has the ball and understand basic spacing around the ball carrier']),
 sk('B2', 'Decision-Making', ['Recognize the basic choice between combining with a teammate and carrying forward individually', 'Begin choosing between pass-and-move and carry based on where the defender is', 'Make simple combination decisions without waiting to be told']),
 sk('B3', 'Perception and Preparation', ['React to losing the ball with immediate urgency', 'Identify the ball carrier as the first priority', 'Recognize nearby teammates as defensive support']),
 sk('B3', 'Covering', ['Recognize the importance of helping a teammate who is pressing', 'Begin to understand basic cover position behind the ball', 'Stay connected to the nearest teammate rather than isolated']),
 sk('B3', 'Shape and Line Management', ['Understand that the team defends as a connected group, not individuals', 'Begin to recognize when the team is too spread out', 'Recover into a basic defensive shape after losing the ball']),
 sk('B3', 'Defensive Decision-Making', ['Understand the basic choice between pressing and delaying', 'Begin to recover goal-side when beaten', 'Recognize the importance of helping teammates defend rather than defending alone']),
 sk('B4', 'Perception and Awareness', ['Recognize the moment possession has changed', 'Identify the immediate attacking or defensive cue that follows', 'Begin scanning during chaotic, fast-moving moments']),
 sk('B4', 'Reaction and Speed', ['React quickly after losing or winning the ball', 'Accelerate toward the ball or space without hesitation', 'Attempt a forward pass after regaining possession when available']),
 sk('B4', 'Decision-Making', ['Choose between fast attack and holding possession after a regain', 'Recognize when the press has failed and the team must recover', 'Support teammates in transition rather than acting alone']),
 sk('B5', 'Recognizing the Moment', ['Identify when in shooting or final-pass range', 'Notice goal location and basic pressure', 'Recognize simple scoring opportunities']),
 sk('B5', 'Preparation and Body Shape', ['Set the body to face goal when receiving near the box', 'Use a settling touch to prepare for a shot or pass', 'Show basic balance before striking the ball']),
 sk('B5', 'Executing Final Actions', ['Use inside foot or simple laces technique to finish', 'Complete uncontested headers or rebounds', 'Execute basic cutbacks or square passes']),
 sk('B5', 'Composure and Ownership', ['Willing to shoot or play the final pass', 'Accept missed chances without frustration', 'Reset quickly after attempts'])]})
B = lambda tag, ov, prob, foc: {'tagline': tag, 'overview': ov, 'problem': prob, 'focus': foc}
dump(R / 'data' / 'framework' / 'u14.yaml', {'age': 'u14', 'blocks': {
 'B1': B('Prepare the body. Read the picture. Execute with intent.', "Every player's relationship with the ball comes before everything else. This block establishes the perceptual and technical habits that make all combination play, defending and finishing possible: scanning before the ball arrives, shaping the body to play forward, and using first touch to create a decision rather than just react to pressure. When a player stalls in a later block, look back here first.", 'Players scan, position and make first-touch decisions under high pressure in tight spaces.', ['Scanning before, during and after receiving', 'Body shape and movement to play forward', 'Using first touch to create a decision, not just control', 'Technique at full game speed and pressure']),
 'B2': B('Create advantage. Move the ball forward. Solve pressure together.', "Combination play only works if the individual technique from the first block is already in place. This block takes that foundation and asks players to solve pressure together: recognizing a teammate's run, providing the right angle of support, and timing the next action so the advantage compounds rather than stalls.", 'Players use teammates to create time, space and numerical advantages, moving the ball forward under pressure through deliberate combination play.', ['Supporting angle, distance and timing', 'Combination play to break defensive lines', 'Recognizing and exploiting overloads', 'Movement after the pass, not just the pass itself']),
 'B3': B('Compact. Coordinated. Aggressive. Defending is not just for defenders.', 'Defending is not just for defenders. Winning the ball back is a collective action: the nearest player pressures, teammates cover behind, and the team stays connected and compact to protect dangerous space. The standard is no longer just reacting to losing the ball. Teams defend proactively, with a compact block that regains possession as high up the field as possible.', 'Players create and maintain a compact defensive block, applying coordinated pressure, cover and balance to prevent forward play and regain the ball.', ['Coordinated pressure, cover and balance', 'Compact shape, vertically and horizontally', 'High defensive line and line management', 'Immediate reaction after losing the ball']),
 'B4': B('Recognizing moments and acting fast.', 'Transitions are the moments that decide games. This block links attacking and defending: the instant possession changes, players must recognize the moment and respond, either with maximum intensity to win the ball back, or with immediate speed to attack before the opponent can organize. A player who reacts fast in transition is applying technique, combination and defensive shape all at once.', 'Players recognize the moment possession changes and respond immediately: pressing or recovering when it is lost, and playing forward at speed or securing the ball when it is won.', ['Immediate recognition of the transition moment', 'Reaction speed and acceleration', 'Press or recover, play forward or secure', 'Communication and organization under chaos']),
 'B5': B('Can we turn advantage into goals?', 'All of the work in the earlier blocks is preparation for this one. Players who scan early, combine well, defend collectively and transition fast create finishing opportunities. This block is about having the composure and technique to take them. When players struggle to finish, the answer is rarely more finishing drills. Check the quality of preparation touches, the timing of runs, and the decisions made before the shot.', 'Players convert advantage into goals under pressure: separating to receive, combining for the final pass, and finishing with composure and limited touches.', ['Converting advantage into goals through quality final actions', 'Separating and unmarking to receive in the box', 'Finishing with composure and limited touches', 'Managing tempo and stakes as the game state demands'])}})
dump(R / 'theme' / 'sgsc' / 'overlay' / 'u14.yaml', {'format': '11v11',
 'rules_title': 'Game rules at U14',
 'rules_intro': 'What changes from 9v9. Know these before the first game so the players, parents and you are not learning them on the touchline.',
 'rules': [{'label': 'Format', 'text': '11v11 on a full-size field, roughly 100 to 120 yards long and 50 to 80 yards wide. Size 5 ball. Goals are 8 feet by 24 feet.'},
  {'label': 'Heading', 'text': 'Deliberate heading is allowed in games at 11v11. Build up to it gradually in training and keep the number of headers low.'},
  {'label': 'Offside', 'text': 'Offside applies. Teach it early. Club linesmen cannot call offside, so with one referee the referee makes that call.'},
  {'label': 'Build-out line', 'text': 'None at 11v11. The build-out line used at 7v7 and 9v9 goes away. Goalkeepers and defenders now play out of the back under real pressure.'},
  {'label': 'Substitutions', 'text': 'Unlimited, at any stoppage with the referee\'s permission. Substitutes wait at the halfway line until the referee waves them on.'},
  {'label': 'Rosters', 'text': 'Up to 18 on a game-day roster. A team needs at least 7 players to play.'},
  {'label': 'Free kicks and penalties', 'text': 'Opponents stand 10 yards back on free kicks. Penalty kicks are taken from 12 yards.'},
  {'label': 'Officials', 'text': 'Three referees where possible. One referee with two club linesmen is allowed when licensed officials are short.'},
  {'label': 'Head injuries', 'text': 'A player removed for a suspected head injury cannot return that day and needs clearance from a licensed healthcare provider before playing again.'}],
 'rules_source': 'Source: NorCal 2025-2026 Handbook, sections 5.3, 5.4, 5.12 and 5.13. League rules always take precedence. If something here does not match what your referee says, ask your Age Group Coordinator.',
 'pathway': ['Some players will show real passion and ability this season', "Sierra Gold's competitive program exists to open more doors for those players when they are ready", 'Talk to your club director about what that pathway looks like'],
 'contact': 'Got a question about an activity? Want to talk through what you are seeing at training? Not sure how to introduce finishing to your group? Your Age Group Coordinator and the club Technical Director are there for exactly this. Reach out any time.'})
