"""One-time import of the U10 framework draft (claude/U10-framework-content.md in the Methodology project) into skill records."""
import yaml, re, pathlib, sys
OUT = pathlib.Path(sys.argv[1])
A = [
('B1','Scanning and Body Shape',
 ['Look for the ball, teammates and the goal before receiving','Open the body so the field is in view when the ball arrives','Keep the head up while driving and dribbling'],
 ['Scan more than once before receiving under light pressure','Receive on the half-turn when there is space','Recognize when there is time to take a touch and when to play first time']),
('B1','Controlling',
 ['Receive passes from up to 20 yards with a soft first touch','Move toward the ball when an opponent is close','Take the first touch toward goal when the way is open'],
 ['Use the first touch to move the ball away from pressure','Receive with the inside or outside of either foot as needed','Control without looking down at the ball']),
('B1','Protecting',
 ['Shield the ball with the body between the ball and the opponent',"Keep the ball away from the opponent's feet",'Hold the ball until a teammate is open'],
 ['Shield under contact and keep control','Decide when to hold the ball and when to release it','Turn out of pressure with the ball protected']),
('B1','Driving and Dribbling',
 ['Push the ball a few steps ahead and keep it within reach','Take on an opponent with a change of pace or direction','Dribble when it creates danger on goal'],
 ['Change pace and direction to create real separation','Choose between driving into space and taking on a defender','Keep the head up to see the next decision while dribbling']),
('B1','Passing',
 ["Pass to a teammate's feet or into space from 5 to 20 yards",'Look at the teammate while passing','Pass so the receiver can continue forward'],
 ["Match the weight of the pass to the teammate's movement",'Use different surfaces of the foot to play the pass','Pass first time when the picture calls for it']),
('B1','Shooting',
 ['Shoot on goal from short and medium range','Use the laces for power and the inside of the foot for placement','Follow the ball after the shot'],
 ['Choose placement or power depending on the goalkeeper','Shoot after a dribble, pass or cross','Shoot with an opponent closing']),
('B2','Supporting',
 ['Find open space and show the player with the ball you are available','Spread out to make the field big','Move to a new spot after passing'],
 ['Choose a support position that gives the passer a forward option','Adjust the angle and distance as the ball moves','Call or signal for the ball with a word or a hand']),
('B2','Give and Go',
 ['Pass to a teammate and run into space for the return','Pass into feet so the teammate can play it back','Keep moving after the pass'],
 ['Time the run so the return pass arrives in space','Use a first-time return pass when the defender is close','Look for the give and go when the dribble is blocked']),
('B2','2v1 and Combination',
 ['Notice when a teammate is free and a 2v1 is possible','Drive at one defender, then pass to the free teammate','Celebrate passes that beat a defender'],
 ['Commit the defender by driving at them, then release at the right time','Support at an angle that the defender cannot cover both options','Finish the 2v1 with a shot or a final pass']),
('B2','Decision-Making',
 ['Choose between dribbling and passing in the game','Pass to a free teammate when the dribble is closed','Talk to teammates with simple calls'],
 ['Make the choice faster as the picture changes','Choose the forward pass when it is there, the safe pass when it is not','Stay connected to the next play after the pass']),
('B3','Pressing and Challenging',
 ['Run to the player with the ball to stop them from scanning and passing forward','Slow down as you arrive so you do not get dribbled past','Go in to win the ball when the moment is right'],
 ['Choose when to press, when to delay and when to go in','Show the ball carrier one way and cut off the other','Press again straight away if the first press is beaten']),
('B3','Delaying',
 ['Slow the ball carrier down when a teammate is not ready to help','Stay between the ball and the goal','Stand with the body at an angle to the goal you are protecting'],
 ['Delay until cover arrives, then step in','Force the ball carrier toward the sideline','Keep a balanced stance to react to a change of direction']),
('B3','Covering',
 ['Stand behind the pressing teammate at a good distance','Be ready to press if they are beaten','Block the passing option nearest to the ball'],
 ['Adjust distance and angle as the press changes','Call out "I\'ve got cover" so the presser commits','Slide across when the first defender steps in']),
('B3','Marking',
 ['Stay close to the opponent in your area','Keep your body between the opponent and the goal','Stay close enough to stop an easy pass to them'],
 ['Stay goal-side and ball-side as the ball moves','Anticipate the pass and step in to intercept','Switch the mark with a teammate when needed']),
('B3','Compact Shape and Recovery',
 ['Stay close to your teammates when the other team has the ball','Run back goal-side when the ball is lost','Close the middle of the field first'],
 ['Shift together toward the ball','Recognize when the team is too spread out and close the gaps','Re-apply pressure as soon as a teammate is beaten']),
('B3','Denying the Finish',
 ['Get narrow and close the center near goal','Stop the cross and block the shot','Stay on your feet until the shot is taken'],
 ['Choose between blocking the shot and staying goal-side','Step in to challenge when the opponent has a chance on goal','Cover the near post area when the ball is wide']),
]
slug = lambda n: re.sub(r'[^a-z0-9]+','-',n.lower()).strip('-')
recs = []
for b, area, intro, dev in A:
    for lvl, bl, tr in (('intro', intro, ['rec','comp']), ('dev', dev, ['comp'])):
        recs.append({'id': f'u10-{b.lower()}-{slug(area)}-{lvl}', 'age': 'u10', 'block': b, 'area': area, 'level': lvl, 'tracks': tr, 'bullets': bl})
(OUT/'skills').mkdir(parents=True, exist_ok=True)
(OUT/'skills'/'u10.yaml').write_text(yaml.safe_dump({'skills': recs}, sort_keys=False, allow_unicode=True, width=110), encoding='utf-8')
print(len(recs), 'skill records')
