"""One-time import of the U6 companion page into records. U6 has a Discovery area (D) instead of B1-B5 blocks, and borrows four B1 games."""
import yaml, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
def dump(path, obj): path.parent.mkdir(parents=True, exist_ok=True); path.write_text(yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, width=100), encoding='utf-8')
def load(p): return yaml.safe_load(p.read_text(encoding='utf-8'))
# ladder and blocks
lp = R / 'rules' / 'ladder.yaml'; t = lp.read_text(encoding='utf-8')
if 'u6: [D, B1]' not in t:
    t = t.replace('  u6: []', '  u6: [D, B1]   # Discovery area, plus a few B1 games borrowed from U8'); lp.write_text(t, encoding='utf-8')
bp = R / 'data' / 'blocks.yaml'; b = bp.read_text(encoding='utf-8')
if '\nD:' not in b:
    bp.write_text(b.rstrip('\n') + '\nD: {name: Discovery, group_label: "Movement, ball comfort and joy", css: ""}\n', encoding='utf-8')
ORDER = max(load(f)['order'] for f in (R / 'data' / 'activities').glob('*.yaml') if 'u6' not in load(f)['ages'] or len(load(f)['ages']) > 1)
def act(i, name, skills, lo, hi, setup, look_for, question, equipment, pairs):
    global ORDER; ORDER += 1
    return {'id': i, 'order': ORDER, 'name': name, 'block': 'D', 'skills': skills, 'ages': ['u6'], 'tracks': ['rec'], 'levels': ['intro'],
            'players': {'min': lo, 'max': hi}, 'space': 'quarter', 'minutes': 10, 'setup': setup, 'look_for': look_for, 'question': question,
            'pairs_with': pairs, 'equipment': equipment}
NEW = [
 act('sharks-and-minnows', 'Sharks and Minnows', ['Dribbling', 'Scanning'], 4, 14,
  'Mark a rectangle and call it the ocean. Every player is a minnow with their own ball. You are the shark. Minnows line up along one end and on your signal they all dribble to the other side without getting their ball knocked away by you. Any minnow whose ball is knocked out becomes a shark and joins you for the next crossing. Minnows who make it safely line up and go again. Play until everyone has become a shark, then start fresh with a new volunteer as the first shark.',
  'Encourage minnows to keep their heads up to find gaps, small touches to get around the sharks, and bigger touches to escape when they have space. The game is self-regulating as more sharks appear. Go after your more confident players first.',
  'How did you get past the shark? Did you go fast or did you go around?', '1 ball per player · Disc cones for rectangle', ['octopus', 'kangaroo-jacks']),
 act('octopus', 'Octopus', ['Dribbling', 'Driving'], 4, 14,
  'Mark a square grid and call it the ocean. Every player has a ball and dribbles freely anywhere in the grid. You are the octopus, roaming the grid trying to tag players. If tagged, it is 10 toe taps to get back in. Hold two pool noodles as tentacles if you have them. They make no practical difference and players will absolutely love it. Unlike Sharks and Minnows, there is no crossing from side to side: players move freely in all directions and must dodge you wherever they go.',
  'Look for players using small touches to dodge around you and bigger touches to escape when they have space. Slow down for players who need more success, speed up for players who need more challenge. The free-roaming format means every player is always active, which keeps energy high.',
  'When I came toward you, how did you decide which way to go?', '1 ball per player · Disc cones for grid · 2 pool noodles as tentacles (optional but highly recommended)', ['sharks-and-minnows']),
 act('kangaroo-jacks', 'Kangaroo Jacks', ['Dribbling', 'Controlling'], 4, 14,
  'Rectangle about 20 by 15 yards. One or two volunteers are the Kangaroo Jacks. Everyone else has a ball. Kangaroo Jacks must hop everywhere they go. Players dribble from one side of the grid to the other without getting tagged by a hopping Kangaroo Jack. If tagged, that player becomes a Kangaroo too. After a minute or so, call time, catch your breath, and play again.',
  'The hopping is the whole point. Two-footed hopping is genuinely difficult for many 5 and 6 year olds and they will fall over and think it is hilarious. That is fine. Let them. The coordination work happening in this game is foundational to athletic development and they will never know they are training.',
  'When more kangaroos appeared, how did you find space to dribble?', '1 ball per player (except kangaroos) · Disc cones for rectangle', ['bunny-trail', 'snake']),
 act('snake', 'Snake', ['Communication', 'Scanning'], 6, 16,
  "Grid about 20 by 20 yards. One player is the head of the snake, the only player without a ball. Everyone else dribbles freely. The snake runs around trying to tag other players. When tagged, a player grabs the back of the snake's shirt and joins the snake. The snake grows with every tag. They must stay connected for a tag to count. The game ends when everyone has become part of the snake. Start again with a new volunteer as the head.",
  'The snake will fall apart constantly. That is the fun. Encourage the snake to communicate and call out who they are going after. Remind non-snakes to keep their heads up to find snake-free space. Watch for moments of genuine teamwork as the snake gets longer. Hissing is encouraged and should be modeled by the coach.',
  'When you were in the snake, how did you decide which direction to go?', '1 ball per player (except the snake head) · Disc cones for grid', ['kangaroo-jacks']),
 act('bunny-trail', 'Bunny Trail', ['Dribbling', 'Controlling'], 4, 16,
  'Create a circle of cones spaced about 6 feet apart. Each player starts at a cone with their own ball. On your call, players either dribble to the next cone or hop while carrying their ball. Alternate between dribbling and hopping segments on your command. Tell players to imagine a force field the size of their arms and to keep the ball inside it while they dribble.',
  'The dribbling and hopping alternate creates a natural rhythm, and the coordination challenge of switching between the two is the whole point. Some players will struggle with two-footed hopping. Demonstrate it and encourage the attempt. Do not run more than three hopping segments in a row or energy will drop.',
  'Which was harder, dribbling or hopping? Why?', '1 ball per player · 1 cone per player arranged in a circle', ['kangaroo-jacks']),
 act('mosquitoes', 'Mosquitoes', ['Dribbling', 'Shooting', 'Scanning'], 6, 16,
  'Small grid about 15 by 15 yards. Divide players into two groups: mosquitoes (each with a ball) and campers (no ball). Mosquitoes dribble their ball and try to hit campers below the knee. When a mosquito lands a hit, that player switches roles. Play until you call time. Keep the grid small so players have to dribble close before striking rather than shooting from distance.',
  'The game is controlled chaos and that is the point. It combines dribbling, shooting and spatial awareness in a genuinely silly format that 6-year-olds love. Watch for players who dribble close before shooting rather than kicking from far away. If balls are consistently going high, narrow the space further or switch to a different game.',
  'How did you sneak up on your camper without them getting away?', '1 ball per mosquito · Disc cones for grid', ['octopus']),
]
for a in NEW: dump(R / 'data' / 'activities' / f'{a["id"]}.yaml', a)
SHARED = {
 'red-light-green-light': {'setup': 'Grid about 25 by 20 yards. Every player has a ball. Green light: dribble fast. Yellow light: slow down with small touches. Red light: stop with one foot on the ball. Call lights at random. After a minute, ask players to suggest a new color and assign it a new action: orange means spin around, purple means jump. Add each new color a few times before introducing the next one.',
   'look_for': "This game is simple, familiar, and brilliant at this age. Most players already know the concept from the road. The player-generated colors keep it fresh and give them ownership. Look for players keeping the ball within arm's reach at yellow and actually stopping on red rather than letting the ball roll away.",
   'question': 'What was the hardest color to remember? What action did you pick?'},
 '101-dalmatians': {'setup': "Grid about 25 by 20 yards with cone triangles scattered throughout, one per player. Every player has a ball. Players score by dribbling through a triangle with the ball within arm's reach of their body. Players count their own score out loud and shout it each time they score. Set a group target before the game starts and count up together. Try 20 to start. If they get there quickly, raise it next round. Your job is to roam the grid and knock balls away. Go after your strongest players first.",
   'look_for': 'Count up loudly with the group as the number climbs. The shared team goal creates genuine collective excitement when they hit the target. Raise the number each round to keep it challenging. Encourage small touches and heads up. Do not worry about perfect technique. Just getting the ball to the triangles is a win at this age.',
   'question': 'How many did we get? Should we try for more next round?'},
 'wreck-it-ralph': {'setup': 'Grid about 20 by 20 yards with a cone goal in each corner, opening inward. Every player has a ball. Players dribble around the grid and score by dribbling their ball through any corner goal. You are Wreck-It Ralph, roaming the grid and trying to knock balls away. Ball knocked out: 10 toe taps to re-enter. Play short rounds of about a minute. Encourage players to beat their own score.',
   'look_for': 'Players who look up to find an open goal before driving toward it are already doing something sophisticated. Most will just head for the nearest goal, and that is completely fine at U6. Celebrate every goal loudly. The game introduces goal-scoring instinct without any coaching required.',
   'question': 'How many goals did you score? Which goal was easiest to get to?'},
 'dinosaur-tag': {'setup': 'Each pair sets up a triangle of three cones with sides about 5 yards long. One player is the dinosaur, one is the park ranger. Both dribble around their triangle. The dinosaur tries to tag the park ranger. The park ranger can go any direction around the triangle but cannot leave the ball behind. Switch roles after every tag or after one minute. Hissing by the dinosaur is strongly encouraged.',
   'look_for': 'Some players will struggle to turn the ball around the triangle corners. That is fine. The skill develops with time on the ball. Focus on the competition and the fun, not the technique. The pairs format means everyone is active simultaneously and no one is waiting. Watch for players using both feet.',
   'question': 'What did you do when the dinosaur was catching up to you?'}}
for i, texts in SHARED.items():
    p = R / 'data' / 'activities' / f'{i}.yaml'; o = load(p); o['ages'] = sorted(set(o['ages'] + ['u6']), key=lambda x: int(x[1:])); o.setdefault('for_age', {})['u6'] = texts; dump(p, o)
def sess(a, an, b, bn): return {'a': {'activity': a, 'note': an}, 'b': {'activity': b, 'note': bn}}
W = lambda n, focus, a, an, b, bn: {'week': n, 'focus': focus, 'sessions': [sess(a, an, b, bn)], 'block': 'D', 'level': 'intro', 'also_blocks': ['B1']}
weeks = [
 W(1, 'Moving with the ball', 'red-light-green-light', 'Ball close at yellow, a real stop at red', 'octopus', 'Small touches to dodge, bigger touches to escape'),
 W(2, 'Dodging and changing direction', 'sharks-and-minnows', 'Heads up to find the gaps', 'kangaroo-jacks', 'Let the hopping be silly. The coordination work is real'),
 W(3, 'Counting, scoring and heads up', '101-dalmatians', 'Count together and raise the target each round', 'snake', 'Players calling out who they are chasing'),
 W(4, 'Both feet, turns and hops', 'dinosaur-tag', 'Watch for both feet on the turns', 'bunny-trail', 'Keep hopping segments to three in a row at most'),
 W(5, 'Finding the goal', 'wreck-it-ralph', 'Celebrate every goal loudly', 'sharks-and-minnows', 'Revisit: can they find the gaps faster?'),
 W(6, 'Silly games, real skills', 'mosquitoes', 'Dribble close before striking. Keep the grid small', 'octopus', 'Revisit: dodging with a smile'),
 W(7, 'Favorites', '101-dalmatians', 'Revisit: beat last time\'s group total', 'mosquitoes', 'Revisit: keep shots below the knee'),
 {'week': 8, 'focus': "Coach's choice", 'coach_choice': True, 'note': 'Run what your group loves most. If they are begging for more, you picked right.'}]
dump(R / 'data' / 'plans' / 'u6-rec.yaml', {'id': 'u6-rec', 'age': 'u6', 'track': 'rec', 'sessions_per_week': 1, 'slot_labels': {'a': 'First activity', 'b': 'Second activity'}, 'weeks': weeks})
dump(R / 'data' / 'ages' / 'u6-rec.yaml', {'id': 'u6-rec', 'age': 'u6', 'track': 'rec', 'label': 'U6', 'pills': [], 'pills_note': '', 'next_age': 'U8', 'goals': 'u6', 'players': 'u6', 'framework': 'u6'})
goals = [('runs-to-ball', 'Runs toward the ball instead of away from it', ['D']), ('moves-with-ball', 'Moves with the ball rather than kicking it away', ['D']),
 ('finds-goal', 'Knows where the goal is and tries to shoot at it', ['D']), ('wants-to-return', 'Shows up to the next session excited to play again', ['D'])]
dump(R / 'data' / 'goals' / 'u6.yaml', {'age': 'u6', 'goals': [{'id': i, 'text': t, 'blocks': b} for i, t, b in goals]})
dump(R / 'data' / 'players' / 'u6.yaml', {'id': 'u6', 'age': 'u6',
 'who': [{'label': 'They are just starting', 'text': 'For many of these players, this is their first experience on a team. Some have never kicked a ball. Start with zero assumptions about what they know. Everything is new and that is a gift. You get to be the person who introduces them to the game.'},
  {'label': 'Fun is the curriculum', 'text': 'At this age, fun is not a means to an end. It is the end. A player who loves being on the field at age 6 is a player who is still playing at 16. A player who has a bad experience now may never come back. That is the real stakes here.'},
  {'label': 'Movement matters more than you think', 'text': 'The hopping, the turning, the chasing, the changing direction. These are not just games. They are building the coordination, balance and agility that underpin every athletic skill your players will ever develop. The animal games are doing real work, even when it looks like pure chaos. You do not need to tell the players any of that. Just run the game and let them be ridiculous.'},
  {'label': 'Short attention spans are normal', 'text': 'A six-year-old has about 6 to 8 minutes of focused attention before they need a reset. This is not misbehavior, it is how kids this age work. Keep activities short. Switch often. If something is not working, just move on. You do not need to fix it.'}],
 'great_session': [{'title': 'Constant movement', 'text': 'Players are running, chasing, dribbling, hopping or laughing for almost every minute of the session. If players are standing still waiting, the game needs to change.'},
  {'title': 'Noise and joy', 'text': 'The louder and more chaotic it sounds, the better. Squealing, giggling, shouting animal names. This is exactly what success sounds like at U6.'},
  {'title': 'Every player has a ball', 'text': 'During practice activities, every player should have their own ball at their feet as much as possible. Waiting in line or sharing kills engagement at this age.'},
  {'title': 'Lots of goals', 'text': 'Set up games where players score frequently. Nothing builds confidence and excitement faster than scoring a goal. Celebrate every single one.'},
  {'title': 'The coach is playing too', 'text': 'At U6, you are not standing on the sideline with a clipboard. You are the shark. You are Wreck-It Ralph. Get in there. Your energy sets the tone for the whole session.'},
  {'title': 'It ends too soon', 'text': 'If players are asking "can we play more?" when the session ends, you have done your job perfectly. End while they still want more, every single week.'}],
 'prepared': 'Preparation at U6 is simple. Know which two activities you are going to run. Have your cones laid out before the first player arrives. Put a ball at every player\'s starting spot. That is it. You do not need a session plan with timing breakdowns. You need to show up with energy and an idea of what game you are playing first. The rest follows.',
 'parents': {'intro': 'U6 parents are more anxious than any other age group, and more likely to intervene. Before the session, walk over and say something like:',
  'script': 'These sessions are going to look like organized chaos, and that is completely intentional. The games are silly on purpose. Every one of them is building coordination, confidence, and a love of the ball. The best thing you can do is cheer loudly and let them figure things out for themselves. If they run to you mid-game, just point them back to the field with a smile.',
  'outro': 'At this age, a crying player who came to the field is still a win. Stay warm, stay calm, and keep things moving. Most players warm up within a few sessions.'},
 'shape': {'title': 'The session', 'note': 'About 45 to 50 minutes. Arrive 15 minutes early. Opening game, two activities of about 10 minutes, closing game.',
  'opening': {'label': 'Opening game', 'minutes': '8 to 10 min', 'title': 'Small-sided game, free play',
   'setup': 'Same setup every week. Mini or pop-up goals at each end if you have them, cone goals otherwise. Pop-up goals give players the satisfaction of the ball going into a net, which matters at this age. Split however many players you have into two roughly equal teams. No goalkeeper, no offside, no rules beyond kick-in restarts. Keep the field small enough that every player is near the action most of the time. When in doubt, go smaller. Mark the space, put the ball down, and step back. Restart quickly after every goal and celebrate each one.',
   'job': 'Get in there a little. Encourage. High-five. React to goals like they are the greatest thing you have ever seen. At U6, your energy is contagious in both directions. Do not coach. Do not correct. Just play.',
   'question': 'What was your favorite part of today?', 'kit': '1 ball per team · Mini or pop-up goals (cone goals as fallback) · Disc cones for boundaries · Pinnies in 2 colors'},
  'closing': {'label': 'Closing game', 'minutes': '10 min', 'title': 'Back to play',
   'setup': 'Same small-sided game as the opening. Same teams or mix them up, either works. Let it run without interruption. Your job is to restart quickly after goals and keep the energy up. Bring everyone in at the end. High-fives all around, then one very simple question to close the loop. End while they still want more.',
   'question': 'What was your favorite part of today?', 'kit': '1 ball per team · Mini or pop-up goals (cone goals as fallback) · Disc cones for boundaries · Pinnies in 2 colors'}},
 'cues': [{'when': 'Player is standing still or disengaged', 'say': 'Go to them. Get a ball at their feet. Get them moving. Do not ask what is wrong in front of the group. Just play alongside them for a minute.'},
  {'when': 'Player is upset or crying', 'say': 'Kneel down, speak quietly, and give them a moment. Do not rush them back in. Most players come back on their own when they are ready. Keep the game going so they have something to come back to.'},
  {'when': 'Player runs to their parents mid-game', 'say': 'Normal. Let the parent redirect them back. If it happens every session, have a quiet word with the parent about how to respond.'},
  {'when': 'Player scores a goal', 'say': 'React like it is the greatest thing you have ever seen. Name the player. Make the celebration visible. At U6, that moment of recognition is more valuable than any coaching point.'},
  {'when': 'Game is getting too chaotic', 'say': 'That is usually fine. If it genuinely breaks down, call a quick freeze, give one simple instruction, and restart. Do not stop the game for more than 30 seconds.'},
  {'when': 'Players are not listening to instructions', 'say': 'Keep instructions to one sentence. Demonstrate rather than explain. If they are not listening, start the game and they will figure it out.'}]})
dump(R / 'data' / 'skills' / 'u6.yaml', {'skills': [
 {'id': 'u6-d-move-with-the-ball-intro', 'age': 'u6', 'block': 'D', 'area': 'Move with the ball', 'level': 'intro', 'tracks': ['rec'], 'bullets': ['Keep the ball close', 'Use your feet to take it with you', 'Run toward the ball instead of away from it']},
 {'id': 'u6-d-heads-up-intro', 'age': 'u6', 'block': 'D', 'area': 'Heads up', 'level': 'intro', 'tracks': ['rec'], 'bullets': ['See what is around you', 'Find space', 'See your teammates']},
 {'id': 'u6-d-have-fun-intro', 'age': 'u6', 'block': 'D', 'area': 'Have fun', 'level': 'intro', 'tracks': ['rec'], 'bullets': ['Smile, laugh and make noise while playing', 'Celebrate every goal', 'Show up excited for the next session']}]})
dump(R / 'data' / 'framework' / 'u6.yaml', {'age': 'u6', 'blocks': {'D': {'tagline': 'Move with the ball. Heads up. Have fun.', 'overview': 'There are no player action frameworks, no tactical concepts and no positional requirements at this age. Just three things, said plainly, that you can come back to in any game at any moment. Fun is the most important one, and the one coaches forget most often.', 'problem': 'Players fall in love with the game: moving with the ball, looking up, and wanting to come back next week.', 'focus': ['Move with the ball: keep it close, use your feet, take it with you', 'Heads up: see what is around you, find space, see your teammates', 'Have fun']}}})
dump(R / 'theme' / 'sgsc' / 'overlay' / 'u6.yaml', {'format': '5v5'})
