"""One-time import of the U8 companion page and U8 framework draft into records (activities, plan, age, goals, players, skills, framework)."""
import yaml, pathlib
R = pathlib.Path(__file__).resolve().parent.parent
def dump(path, obj): path.parent.mkdir(parents=True, exist_ok=True); path.write_text(yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, width=100), encoding='utf-8')
ORDER = 16
def act(i, name, block, skills, lo, hi, setup, look_for, question, equipment, pairs):
    global ORDER; ORDER += 1
    return {'id': i, 'order': ORDER, 'name': name, 'block': block, 'skills': skills, 'ages': ['u8'], 'tracks': ['rec'], 'levels': ['intro'],
            'players': {'min': lo, 'max': hi}, 'space': 'quarter', 'minutes': 20, 'setup': setup, 'look_for': look_for, 'question': question,
            'pairs_with': pairs, 'equipment': equipment}
A = [
 act('red-light-green-light', 'Red Light Green Light', 'B1', ['Driving', 'Controlling'], 4, 16,
  'Grid about 25 by 20 yards. Every player has a ball. Green light: dribble fast. Yellow light: slow down with small touches to keep the ball close. Red light: stop with one foot on the ball. Call lights at random as players move around the grid. After a minute, ask players to suggest a new color and give it a new action (orange means swing your arms, purple means dance) and repeat each new color a few times.',
  "Players keeping the ball within arm's reach at yellow. Heads up to avoid collisions. On red light, emphasize using the sole of the foot to stop rather than letting the ball roll away.",
  'When I called yellow, what did you have to do with your feet to keep the ball close?', '1 ball per player · Disc cones for grid', ['gates-dribbling', '101-dalmatians']),
 act('101-dalmatians', '101 Dalmatians', 'B1', ['Dribbling', 'Scanning'], 4, 16,
  "Grid about 25 by 20 yards with small cone triangles scattered throughout, about one triangle per player. Every player has a ball. Players score by dribbling through a triangle with the ball within arm's reach of their body. Players count their own score out loud and shout it each time they hit a triangle. The group goal is 101 combined. Your job is to roam the grid and knock balls away, going after your stronger players first.",
  'Players using small touches to keep the ball close when you approach. Heads up to spot both the triangles and you coming. The counting keeps players invested in the team total.',
  'How did you keep the ball safe when I came near you?', '1 ball per player · Disc cones for outer grid and inner triangles', ['red-light-green-light', 'knockout']),
 act('wreck-it-ralph', 'Wreck-It Ralph', 'B1', ['Dribbling', 'Scanning', 'Shooting'], 4, 16,
  'Grid about 25 by 20 yards with a cone goal in each corner, opening inward. Every player has a ball. Players dribble around the grid and score by dribbling their ball through any corner goal while you (Wreck-It Ralph) roam and try to knock balls away. Ball knocked out: 10 toe taps to re-enter. Play short rounds of about a minute. Cone goals only, no small goals needed.',
  'Players who look up to find an open goal before driving toward it. That is scanning in action. Encourage players to beat their own score each round.',
  'Before you drove toward a goal, what did you check first?', '1 ball per player · Disc cones for grid and corner goals', ['101-dalmatians', 'shooting-gallery']),
 act('duck-tails', 'Duck Tails', 'B1', ['Dribbling', 'Protecting'], 4, 16,
  "Grid about 20 by 20 yards. Every player has a ball and tucks a pinny in the back of their shorts. Players dribble around the space trying to steal a teammate's tail while protecting their own. Start with no elimination: if a tail falls off, tuck it back in and keep playing. For a final competitive round, switch to elimination: tail stolen means you are out. Last player with their tail wins. Count how many tails each player collects.",
  'Players who face their opponent rather than just running away. That is the beginning of how they will take on a defender. Heads up to see where tails are and where opponents are coming from.',
  'What did you do when someone came to steal your tail?', '1 ball per player · Disc cones for grid · Pinnies as tails', ['knockout', 'dinosaur-tag']),
 act('knockout', 'Knockout', 'B1', ['Protecting', 'Dribbling'], 4, 16,
  "Grid about 20 by 20 yards. Every player has a ball and dribbles freely. Players try to knock other players' balls out of the grid while keeping their own in. Ball knocked out: five toe taps outside the grid, then back in (non-elimination). For a final competitive round, switch to elimination: ball knocked out means you are out. Last player with their ball in the grid wins. Remind players to keep their ball close when an opponent approaches.",
  'Players who shield the ball with their body rather than just running away. Players who look up to track both the ball and the incoming threat.',
  'When someone came to knock your ball out, what did you do to protect it?', '1 ball per player · Disc cones for grid', ['duck-tails', '101-dalmatians']),
 act('dinosaur-tag', 'Dinosaur Tag', 'B1', ['Dribbling', 'Controlling'], 2, 16,
  'No outer boundary needed. Each pair sets up a triangle of three cones, with sides about 5 yards long. One player is the dinosaur, one is the park ranger. Both dribble around their triangle. The dinosaur tries to tag the park ranger. The park ranger can go any direction around the triangle but cannot leave the ball. Switch roles after every tag or after one minute. Hissing by the dinosaur is strongly encouraged.',
  'Players learning to change direction quickly while keeping the ball close. Some players will struggle with the turns, and that is fine. Encourage small touches with both inside and outside of the foot. The competition drives the skill.',
  'What did you do with the ball when you needed to change direction quickly?', '1 ball per pair · 3 cones per pair to form a triangle', ['duck-tails', 'shadow-dribbling']),
 act('gates-dribbling', 'Gates Dribbling', 'B1', ['Driving', 'Scanning'], 4, 16,
  "Grid about 25 by 20 yards with 8 to 10 gates scattered throughout. Each gate is two tall cones placed an arm's length apart. Every player has a ball. Score a point by dribbling through any gate. 60-second challenge: how many gates can you get through? Tell players to imagine a force field the size of their arms, and the ball should stay inside it while they dribble. Progress: call a specific cone color and players must look up to find those gates first.",
  'Players who keep their head up find more gates. The game creates the need for scanning without you naming it. After the question, name it: "That looking up while you dribble is called scanning."',
  'How did you find the gates faster? What were you doing with your eyes?', '1 ball per player · 8 to 10 tall cones in pairs · Disc cones for grid · Timer', ['color-tag-dribble', 'shadow-dribbling']),
 act('shadow-dribbling', 'Shadow Dribbling', 'B1', ['Scanning', 'Dribbling'], 2, 16,
  'Grid about 25 by 20 yards. Players in pairs, each with their own ball. One player is the leader who dribbles however they want: fast, slow, turning, zigzagging. Their partner is the shadow, following close behind and mimicking every move. Switch roles every minute. If a leader tries something fancy, encourage the shadow to try it too even if it is not an exact copy.',
  'The shadow must have their head up to follow the leader. Players who look at their own ball fall behind. The game builds the reflex to look up naturally, without you ever asking for it.',
  'How did you stay close to your leader? What did you have to keep your eyes on?', '1 ball per player · Disc cones for grid', ['gates-dribbling', 'dinosaur-tag']),
 act('color-tag-dribble', 'Color Tag Dribble', 'B1', ['Scanning', 'Driving'], 4, 16,
  'Grid about 25 by 20 yards with colored tall cones placed around the space. Every player has a ball and dribbles freely. Hold up a colored cone and all players must dribble to touch a cone of that color before you count to ten. Vary the colors and the pace. Progress: have two callers with different colors at the same time so players must split their attention.',
  'Players who keep their head up while dribbling reach the color fastest. Let the game teach the lesson. After the question, you can name it: "That is scanning."',
  'Who got to the cone fastest? What were you doing with your head while you were dribbling?', '1 ball per player · Multiple colored tall cones · Disc cones for grid', ['gates-dribbling', 'red-light-green-light']),
 act('shooting-gallery', 'Shooting Gallery', 'B1', ['Shooting', 'Decision-Making'], 4, 16,
  "Grid about 20 by 20 yards with a cone goal on the center of each side, all opening inward, four goals total. Every player has their own ball. Players dribble freely inside the grid and shoot at any goal they choose. After the shot, retrieve the ball and go again. No groups, no queues, everyone active the whole time. Challenge: how many different goals can you score on in 60 seconds?",
  'Players who look up to find an open goal before driving toward it. Volume of attempts is the point: confidence to shoot develops now and accuracy comes with time. Celebrate every goal. A player who scores on all four goals in one round deserves a big reaction.',
  'Before you shot, what did you look at?', "1 ball per player · 8 tall cones for 4 goals (pairs, arm's length apart) · Disc cones for grid · Timer", ['wreck-it-ralph', '2v1-to-goal']),
 act('2v1-to-goal', '2v1 to Goal', 'B2', ['Passing', 'Numerical Advantage', 'Decision-Making'], 3, 15,
  'Groups of 3. Two attackers against one defender, attacking a cone goal about 6 yards wide. Ball starts with one attacker around 10 yards out. Rotate roles every 30 seconds. Run 2 to 3 groups simultaneously depending on how many adults are available to manage them. Do not coach the pass: let players discover the advantage of having a teammate free. Rotate defenders regularly so they do not get discouraged.',
  "Do not coach the combination. If a player passes to a free teammate and they score, celebrate it loudly and specifically: \"Did everyone see that? Two players just solved a problem that one player couldn't.\" That moment is the first seed of Me & My Teammates.",
  'When you had two players against one defender, what options did you have? Did you use both of them?', '1 ball per group · 2 tall cones per goal · Pinnies · Run 2 to 3 groups simultaneously', ['shooting-gallery']),
]
for a in A: dump(R / 'data' / 'activities' / f'{a["id"]}.yaml', a)
# 1v1 is shared with U10: add U8 and give U8 its own wording
p = R / 'data' / 'activities' / '1v1-to-endlines-goals.yaml'; o = yaml.safe_load(p.read_text(encoding='utf-8'))
o['ages'] = ['u8', 'u10']
o['for_age'] = {'u8': {
 'setup': "Pairs working in rectangles about 10 by 15 yards. 1v1 to Endlines: players score by dribbling the ball over their opponent's end line with the ball within arm's reach of their body. No shooting, so more touches and more decisions. Progress to 1v1 to Cone Goals: add a cone goal at each end and players score by kicking through below knee height. Run all pairs simultaneously. Fast rotations keep everyone active.",
 'look_for': 'Players trying to dribble past the defender rather than just kicking and chasing. Reward the attempt regardless of outcome. If players are unevenly matched, play the ball directly to the less skilled player to level the challenge.',
 'question': 'When you had the ball, did you try to go past your opponent or around them? What worked?'}}
dump(p, o)
G = lambda focus, act_, note, **kw: {'focus': focus, 'sessions': [{'a': {'activity': act_, 'note': note}}], 'block': 'B1', 'level': 'intro', **kw}
weeks = [G('Driving the ball', 'red-light-green-light', 'Players keeping the ball close at yellow; heads up at green'),
 G('Dribbling under pressure', '101-dalmatians', 'Players using small touches when you get close; players counting out loud'),
 G('Scanning: looking up', 'gates-dribbling', 'Players who find more gates because their heads are up'),
 G('Scanning in pairs', 'shadow-dribbling', 'Shadows who stay close because they are watching the leader, not their own ball'),
 G('Direction changes and protecting', 'dinosaur-tag', 'Players using both feet to turn. The competitive rounds in Duck Tails can also run here'),
 G('Competing for the ball', 'knockout', 'Players shielding with their body; players keeping heads up to track threats'),
 G('Shooting and attacking', 'shooting-gallery', 'Players looking up before shooting. Swap in 2v1 to Goal to look for any moment of combination play', also_blocks=['B2'])]
for i, w in enumerate(weeks, 1): w['week'] = i
weeks = [{'week': w['week'], **{k: v for k, v in w.items() if k != 'week'}} for w in weeks]
weeks.append({'week': 8, 'focus': "Coach's choice", 'coach_choice': True, 'note': 'Use what your group loves most or needs most. Both are correct answers.'})
dump(R / 'data' / 'plans' / 'u8-rec.yaml', {'id': 'u8-rec', 'age': 'u8', 'track': 'rec', 'sessions_per_week': 1, 'weeks': weeks})
dump(R / 'data' / 'ages' / 'u8-rec.yaml', {'id': 'u8-rec', 'age': 'u8', 'track': 'rec', 'label': 'U8',
 'pills': ['controlling', 'protecting', 'driving', 'dribbling', 'passing', 'shooting', 'scanning', 'supporting', 'body-shape'],
 'pills_note': "Navy pills are technical skills: what the body does with the ball. Gold pills are awareness skills. **Scanning** means looking up to see what is around you before the ball arrives. Every great player in the world does this, and you are starting to teach it at age seven. Pick one focus per session and let the game build the rest.",
 'next_age': 'U10', 'goals': 'u8', 'players': 'u8', 'framework': 'u8'})
goals = [('keeps-ball-close', 'Keeps a moving ball close while running', ['B1']), ('changes-direction', 'Changes direction without losing control', ['B1']),
 ('looks-up', 'Looks up sometimes while dribbling, the habit is forming', ['B1']), ('receives-with-intent', 'Receives a short pass and does something intentional with it', ['B1', 'B2']),
 ('beats-defenders', 'Tries to beat defenders rather than just kicking away', ['B1']), ('notices-teammates', 'Notices teammates and occasionally tries to involve them', ['B2']),
 ('competes-with-joy', 'Competes with genuine joy and wants to come back next season', ['B1', 'B2'])]
dump(R / 'data' / 'goals' / 'u8.yaml', {'age': 'u8', 'goals': [{'id': i, 'text': t, 'blocks': b} for i, t, b in goals]})
dump(R / 'data' / 'players' / 'u8.yaml', {'id': 'u8', 'age': 'u8',
 'who': [{'label': 'How they learn', 'text': 'Through experience and repetition, not explanation. Show them a game and they figure it out. Keep instructions short, one idea at a time, then let them play.'},
  {'label': 'What motivates them', 'text': 'Scoring goals. Being successful. Having fun with friends. Competing. Keep score. They care about it, and it creates genuine intensity without you manufacturing it.'},
  {'label': 'Attention and activity', 'text': 'Their attention span is short but improving. Long lines and waiting kill engagement. Every player should be active for virtually the entire session. If kids are standing still, change the game.'},
  {'label': 'Positions and the game', 'text': 'There are no fixed positions at U8. Every player plays everywhere over the course of the season. In the game, rotate the goalkeeper regularly so everyone gets a turn in goal.'}],
 'great_session': [{'title': 'Players have the ball constantly', 'text': 'We encourage players to have the ball at their feet as frequently as possible. One player, one ball is the target during practice activities. No sharing, no waiting.'},
  {'title': 'Lots of goals scored', 'text': 'US Soccer is explicit: set up games where players can be successful and score lots of goals. Frequent scoring means high engagement and happy players.'},
  {'title': 'Noise and energy', 'text': 'Laughing, celebrating, competing. If it is quiet, something is wrong. This age group should be loud and joyful.'},
  {'title': 'Coach mostly watching', 'text': 'Your best coaching is a single question after something happens. Resist the urge to over-coach. The game is the teacher.'},
  {'title': 'Players making decisions', 'text': 'Even simple ones: which goal to attack, when to dribble, when to pass. Decision-making in the game starts here.'},
  {'title': 'Sessions end too soon', 'text': 'If players leave wanting more, you did your job. That desire to return is what builds a long-term love of the game.'}],
 'prepared': 'The best sessions start before the first player arrives. Coaches who show up knowing their activity and their question spend the whole session watching their players and enjoying it. The setup is the same every week: mark a grid with disc cones, lay a ball out for every player, set up cone goals at each end of the closing game space. By the time players arrive, the only thing left to do is put a ball at their feet.',
 'parents': {'intro': 'Before the session starts, take 30 seconds to walk over and say something like:',
  'script': "Today we are working on keeping the ball close and looking up while dribbling. The most helpful thing you can do is cheer everything: the attempt, the stumble, the scramble. That's the job.",
  'outro': 'Most parents want to know what is happening and how to help. Give them a role and they will take it. If you see a parent who is genuinely enthusiastic and engaged, that conversation is worth having.'},
 'shape': {'title': 'The session', 'note': 'About 55 to 60 minutes. Arrive 15 minutes early.', 'opening': {'label': 'Opening game', 'minutes': '10 to 12 min', 'title': 'Free small-sided game',
   'setup': 'Same setup every week, so players know this game before they arrive. Mini goals or cone goals at each end. No offside. Ball out of play: restart with a kick-in or dribble-in from the sideline. Set up the space, then step back. Let them play. Restart quickly after every goal. Rotate the goalkeeper throughout the season so every player gets time in the position.',
   'job': 'Watch. Look for moments of good scanning, a player who tries to beat someone, a clever pass. Make a mental note of two or three things. One of them will tell you which practice activity to run today. Do not stop the game. Do not instruct. Save your voice for the question.',
   'question': 'Who scored a goal today? How did you do it: did you dribble past someone, or did you find a teammate?', 'kit': '1 ball per team · Mini goals or cone goals at each end · Disc cones for boundaries · Pinnies in 2 colors'},
  'practice': {'label': 'Practice', 'minutes': '25 to 30 min', 'note': 'Pick one activity based on what you saw in the opening game and run it for 20 to 25 minutes. Rotate through the toolkit across the season.'},
  'closing': {'label': 'Closing game', 'minutes': '10 to 12 min', 'title': 'Back to the game',
   'setup': 'Same format as the opening. The space can be slightly larger to give players more room. Let it run without stopping and step all the way back. Alternative: one large goal at one end with two cone goals at the halfway line. One team defends the large goal, the other scores through the halfway cones. It gives players a taste of a more directional game.',
   'question': 'What is one thing you did today that you want to try again next week?', 'kit': '1 ball per team · Mini goals, cone goals, or 1 large goal plus cone goals · Disc cones for boundaries · Pinnies in 2 colors'}},
 'cues': [{'when': 'Player looks up while dribbling', 'say': '"Yes, that is scanning. You are already looking for what is next. That is a big deal at any age."'},
  {'when': 'Player tries to dribble past and fails', 'say': '"I love that you tried it. What would you do differently next time?"'},
  {'when': 'Player passes and teammate scores', 'say': 'Celebrate it loudly. Do not over-explain why it worked. Let the result speak for itself.'},
  {'when': 'Player stands still without the ball', 'say': 'Do not instruct. Ask: "Where could you move to help your team right now?"'},
  {'when': 'Player gets frustrated after a mistake', 'say': '"Every player in the world loses the ball. The best ones go and win it straight back."'},
  {'when': 'Session feels chaotic', 'say': 'That is okay. Controlled chaos at U8 is normal. If everyone has a ball and is moving, you are doing it right.'}]})
def sk(b, area, bullets): return {'id': f'u8-{b.lower()}-{area.lower().replace(" ", "-")}-intro', 'age': 'u8', 'block': b, 'area': area, 'level': 'intro', 'tracks': ['rec'], 'bullets': bullets}
dump(R / 'data' / 'skills' / 'u8.yaml', {'skills': [
 sk('B1', 'Controlling', ['Settle the ball close to the body with small touches', 'Receive short passes from 5 to 10 yards', 'Keep the ball close after receiving so the next touch is easy']),
 sk('B1', 'Protecting', ['Put the body between the ball and the opponent', 'Keep the ball on the far foot from the opponent', 'Keep the ball safe until a good option opens']),
 sk('B1', 'Driving', ['Push the ball a few steps ahead and run with it', 'Keep the ball within a few steps of the body', 'Drive into open space']),
 sk('B1', 'Dribbling', ['Take the ball past an opponent with a change of direction or speed', 'Try a move when an opponent is close', 'Use both feet']),
 sk('B1', 'Passing', ["Play short passes to a teammate's feet or into space", 'Pass with the inside of the foot', 'Pass and keep moving']),
 sk('B1', 'Shooting', ['Strike the ball on goal from short range', 'Shoot when in range instead of passing up the chance', 'Follow the ball after the shot']),
 sk('B1', 'Scanning', ['Look up for the ball and the goal while moving', 'Build the habit once ball comfort is there', 'Look first, then decide']),
 sk('B2', 'Supporting', ['Spread out instead of bunching around the ball', 'Find open space with no opponent and no teammate in it', 'Look at the player with the ball so they can find you']),
 sk('B2', 'Passing to a Free Teammate', ['Look up and find a teammate in open space', "Pass to the teammate's feet or into space with the right pace", 'Move to a new spot after passing']),
 sk('B2', 'Decision-Making', ['Choose between dribbling and passing in the game', 'Pass when a teammate is free and the dribble is blocked', 'Celebrate a pass that leads to a goal'])]})
dump(R / 'data' / 'framework' / 'u8.yaml', {'age': 'u8', 'blocks': {
 'B1': {'tagline': 'Keep it close. Head up. Take it with you.', 'overview': "Every player's relationship with the ball comes first. At U8, this block builds comfort and confidence: close touches, moving with the ball, taking on an opponent, and shooting. Heads come up as comfort grows, not before.",
        'problem': 'Players build the comfort and confidence to move with the ball, take on opponents and shoot, with the ball staying close.', 'focus': ['Close control while moving', 'Taking on an opponent 1v1', 'Shooting from short range', 'Looking up as ball comfort grows']},
 'B2': {'tagline': 'A teammate is an option.', 'overview': 'The first look at team play. Players start to see that a teammate in open space is an option, and that a pass can solve a problem a dribble cannot. At U8 this is low structured: spread out, be available, and pass to a free teammate when it helps.',
        'problem': 'Players start to use teammates as options: moving into open space to be available, and passing to a free teammate.', 'focus': ['Finding open space away from opponents and teammates', 'Showing the player with the ball an option to pass to', 'Passing to a free teammate']}}})
