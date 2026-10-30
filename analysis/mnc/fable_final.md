# Triple M Mid North Coast Secret Sound: independent read of the raw evidence

Written 30 Oct 2026 from the audio (`clues/mnc/clue.wav`, `clues/mnc/clue_stacked.wav`), the stack report, the full
transcript package (`harvest/mnc/package/mnc_evidence.md`, 200 segments, 13 May to 29 Oct) and the owner's A/B ear
verdicts. No other analysis files were read. Scripts: `analysis/mnc/fable_final/measure_clue.py`,
`measure_recorder.py`, `events_detail.py` (figure: `clue_stacked_analysis.png`).

## 1. What the clip contains (measured)

All times on the original clip timeline (stacked file = original + 0.050 s). The stack report says the object's sound
occupies 0.05-0.36 s; everything before 0.05 s and after 0.40 s is station bed, not Sarge's recording.

### 1.1 Events

| Event | Onset | Peak | Level (5 ms RMS, rel. loudest) | 10-90 % rise | Character |
|---|---|---|---|---|---|
| A0 (pre-click) | 0.059 | 0.064 | -12 dB | 4.6 ms | tiny, very short (<10 ms), bright: 3-12 kHz, 5.5 kHz and 2.5 kHz lines |
| A (first main hit) | 0.112 | 0.123 | about -5 dB | 11 ms | bright click, energy centred 1.0-1.9 kHz (lines 1.14, 1.34, 1.55, 1.68, 1.84 kHz) plus 3-6 kHz; centroid ~4 kHz |
| A-thud | 0.135 | 0.141-0.151 | -12 dB | - | low thud following A by ~30 ms: ~147 Hz (110-250 Hz band) then 60-90 Hz (40-110 Hz band); gone by 0.20 s |
| gap | 0.19-0.245 | - | -25 to -36 dB | - | faint rattle at 0.21-0.23 s (2.5 kHz), otherwise near-silent |
| B (second, loudest hit) | 0.248 | 0.257 | 0 dB | 8 ms | heavier "clunk": dominant 780 Hz with 430, 550, 650, 908, 1060, 1360 Hz; 500-1000 Hz holds half the energy |
| B-thump | 0.27 | 0.285 | -11 dB | - | 60-80 Hz thump ~30 ms after B (period-measured 67 Hz), decays by 0.33 s |
| B-ring | 0.26-0.34 | - | - | - | ~790 Hz component: drops 13 dB in the first 20 ms, then a slow tail at about -220 dB/s (T60 ~0.27 s) down to the floor at 0.34 s |
| end | 0.37 | - | floor | - | nothing object-related after 0.37 s (stack common ratio 0.07 at 0.375, 0.014 at 0.40) |

Interval A -> B = 0.134 s (0.112 -> 0.248). B is ~5 dB louder than A. Broadband decay after B: -20 dB at +56 ms,
-30 dB at +81 ms. Peak level of the original file -6 dBFS; the stacked median peaks at -1.2 dBFS.

### 1.2 Spectral character

- A and B are different contacts, not two copies of one: log-spectrum correlation 0.54. A puts 4-8 kHz at -6 dB
  relative to its own total, B puts it at -16 dB; B puts 500-1000 Hz at -3 dB, A at -14 dB.
- The 780-800 Hz mode is the signature of the clip. It is excited only by B (band level -24 dB at A, -4 dB at B).
  A ~430 Hz mode is also excited by B only.
- Low-frequency content: both hits are followed, ~30 ms later, by a thump (147 Hz then 60-90 Hz after A; 67 Hz after
  B). That is a housing or bench being set in motion by the mechanism's travel, picked up by a close microphone (Sarge,
  30 Jul: "we get the microphone up nice and close to it").
- Quiet head (-0.05 to 0.05 s): -46.6 dBFS RMS with faint lines at 112 Hz and 5.0-6.3 kHz (5.46 and 5.76 kHz strongest).
  The stack says that region is only 5-10 % common to broadcasts, so this is mostly station bed, not a whine from the
  object. No 50 Hz mains hum of note.
- Centroid falls from ~4 kHz (A) to ~1.1 kHz at 0.30 s: the clip ends on a dull, mid-heavy ring, not a bright one.

### 1.3 Reading of the mechanics

A spring-loaded lever or key of noticeable travel: A is the lever hitting the end of its travel or tripping a catch
(light, bright, hard-on-hard click), 134 ms later B is the catch or mechanism snapping home (heavier, exciting the
housing's ~430 and ~790 Hz modes and a 67 Hz body thump). The short decay (-30 dB in 80 ms) and the single dominant
mid mode say a small, thin-walled housing (pressed steel or hard plastic, roughly toaster- or bin-sized), damped by
whatever it sits on. Nothing sustained follows (no motor, hiss, water, buzz), so either the action makes no continuous
sound or Sarge cut it.

What it is not, acoustically: not boomy (Sarge, 31 May: his ute glove box is "a bit more boomy, bassier"), not a tiny
part (two events with body thumps), not a free-ringing metal part (no long high-Q ring), not a motorised device.

## 2. The recorder key presses (Freesound 641862) versus the clue

File: 16.5 s, 44.1 kHz, 17 presses/releases detected (0.0, 0.97, 1.27, 1.84, 2.91, 4.10, 5.08, 5.92, 7.19, 8.26,
9.48, 10.68, 11.44, 13.11, 13.43, 14.25, 15.17 s), peaks 0 dBFS. The owner's best window (7.04 s) contains the press at
7.19 s.

| Property | Clue (B) | Recorder press at 7.19 s |
|---|---|---|
| Structure | two hits 134 ms apart, 2nd louder | two bursts 40 ms apart (0.18 and 0.22 s in window), then a 150 ms clatter |
| Loud-part band profile (dB rel max: 20-100 / 100-250 / 250-600 / 600-1.5k / 1.5-3k / 3-6k / 6-12k / 12-20k) | -7 / -12 / -8 / 0 / -5 / -10 / -13 / -29 | 0 / -15 / -24 / -32 / -32 / -33 / -39 / -49 |
| Dominant mode | 780 Hz (plus 430) | 40-80 Hz housing boom; 150 Hz; little above 400 Hz in the loud part |
| 1/3-octave difference clue minus recorder | +16 dB at 800 Hz, +10 dB at 1 kHz, +13 dB at 200 Hz | recorder has +9 dB at 50-80 Hz, +6-8 dB at 6-8 kHz |
| Broadband decay after peak | -20 dB at 56 ms, -30 dB at 81 ms | -20 dB at 128 ms, -30 dB at 168 ms |
| Best log-envelope correlation of the clue's 0.03-0.40 s | - | 0.54 at 7.11 s (moderate) |

Other presses in the file vary a lot (the 2.91 s press is bright, 3-6 kHz dominant; the 1.84 s press is 250-1500 Hz
dominant), so "piano-key press" covers a family of sounds. What the recorder shares with the clue is the two-stage
press-then-snap structure and a hard mid click; what it does not share is the heavy 40-80 Hz chassis boom and the
8 kHz brightness. The clue's housing is lighter and smaller than a tape recorder, with a pronounced ~800 Hz mode, and
its lever travels longer (134 ms between stages versus 40 ms for a short key). This agrees with the owner: the button
mechanism is the right kind (spring-loaded latching lever) but the object is not a tape machine.

## 3. Sarge's hints, in date order, and what each implies

"Absolutely not!" (Promo Sally, from early Sep) carries no information. "Good guess" / "we haven't had that one" are
near-worthless: on 16 Sep Sarge admitted "I say that to a lot of people even when it's not a good guess". The list
below keeps only remarks that describe the sound or the answer, or that are visibly stronger than his default patter.

| Date | Guess | Sarge | Implication |
|---|---|---|---|
| 18 May | "a metal flap coming down" | "we'd have to be a bit more specific" | he wants action + object |
| 24 May | "inside the house or around the house?" | "I'm not going to disclose that just yet" | recorded at/around home (he records them himself) |
| 25 May | opening a tin of coffee | "does sound a lot like it" | lid-off-a-tin timbre is in the right family |
| 31 May | closing the glove box in your ute | "in my ute it's got a bit more of a boomy, bassier sound, so no" | the clue is less boomy than a glove box |
| 1 Jun | putting a price tag on something | "sounds like it, but it's not" | a spring-loaded handheld clack is close in timbre |
| 9 Jun | pushing the door-open button on the microwave | "sounds like a very cheap microwave" | cheap-sounding object |
| 10 Jun | "is it something in the kitchen?" | "I'm gonna have to have a more specific guess" (no denial); 19 Aug a caller cites a "close to the kitchen" clue | kitchen plausible, unconfirmed |
| 15 Jun | pushing Ctrl-Alt-Delete on a keyboard | "got me grinning like crazy" | pressing a key/button is the right idea |
| 18 Jun | the button to turn on the studio microphone | "sounds a bit too cheap and tacky to be honest, it's a bit high tech around here" | the object is cheap, low-tech |
| 28 Jun | switch on a powerpoint/power board | "sounds exactly like it, no it's not" | a chunky switch click is the timbre |
| 28 Jun | pushing play on a vinyl player | "you said something in that answer that really excited me" | "pushing [a named button]" wording is right |
| 1 Jul | space bar on the keyboard | "the last three people have been saying the right words, but not completely right" | verb/button words right, object wrong |
| 1 Jul | pushing eject on the tape player | "shudder in my voice ... heart racing ... you could be very close" | pushing a latching transport-style button is close |
| 2 Jul | pressing play on a cassette player | "the past six people have been saying really good things" | as above |
| 6 Jul | pushing the freshness button on a preserving jar lid | "a lot of really good things in there" | "pushing ... down on top of" words |
| 13 Jul | pushing the buttons on an old-school tape deck | "really good words in there that could lead to the actual secret sound" | "pushing", "button(s)", maybe "old school" |
| 14 Jul | push button on a power board, "plasticky" | "yeah, you're right, Lorraine. No it's not" | he agrees the sound is plasticky |
| 15 Jul | closing the door on your cassette deck | "I own one but it's in storage back home in Bathurst, I didn't get access to record it this time" | NOT any cassette deck of his; he had to use what was at home |
| 15 Jul | pushing a plug into a socket | "that's pretty well what the last secret sound was, the charger" | previous sound: plugging in a charger; this one is a different everyday action |
| 19 Jul | pushing the power button on the computer | "a lot of intrigue ... we're sort of hovering around the right area" | pushing an on/off-type button is the right area |
| 26 Jul | mouse click | "bloody sounds like it, but it's not" | - |
| 29 Jul | pushing down the button on the toaster | "my sphincter tightened ... it was very close" | pushing a lever/button DOWN is very close |
| 30 Jul | car window button | "we get the microphone up nice and close to it" | close-miked small object |
| 20 Aug | putting the portafilter in/out of the coffee machine | "the action you are speaking of is similar to what the actual secret sound is" | the action is putting/pushing something in and locking it |
| 25 Aug | putting toast in a toaster and pushing the toast down | "heart race ... what you said is probably what the actual answer is ... had words that would be in the actual correct answer" | answer contains "pushing ... down" and probably "in"; object not quite the toaster |
| 27 Aug | pushing the button to open a microwave door | "the first half of that answer is almost correct, that's what I've been saying for a fair few of the guesses" | answer starts "pushing the button..." |
| 31 Aug | lid on your kettle | "your guesses are usually really good ... I can't really say too much more" | evasive; lid-closing action not far |
| 9 Sep | pushing the lock down on a briefcase | "when you started saying your answer..." (cut off) | "pushing the ... down" start is right |
| 15 Sep | battery pack into a charging station | "what kind of battery pack into what kind of charging station? specify" | he asks for detail only when something is right |
| 15 Sep | "is it just when the toast pops up?" | "you can move away from [the toaster], give it up" | explicit steer off the toaster |
| 16 Sep | CD player lid/button | "we are getting close, by the way" | general |
| 21 Sep | popping batteries into a compartment, like a mouse | "you're hot. Like, you're hot. Close" | putting something into a compartment that clicks |
| 23 Sep | pushing the air-fryer drawer closed | "thought you had it for a second ... yeah, it is pushing something" | confirms "pushing" |
| 27 Sep | pushing a button on your torch | "it really does sound like that" | timbre of a plastic latching button; a light |
| 12 Oct | Ken (guesses: pen click, mouse, play on cassette player, remote cover) | "one of them was remarkably close" | one of those four |
| 13 Oct | closing the back of a remote after changing the battery | "a remarkable guess" | compartment cover click is close |
| 19 Oct | pushing the switch to turn the wireless mouse back on after changing batteries | "it's around that area ... judging by my reaction, yes"; the Mayor: "very very close" | pushing a switch to turn something on, after putting something in |
| 26 Oct | pushing in the cabinet door, the little magnetic button | "my heart skipped a beat when you started saying your answer" | answer starts "pushing in the ..." or "pushing the ..." |

Summary of what the hints pin down:

1. Wording: "pushing [in/down] the [button/lever/switch] ..." is the confirmed first half. "Down" and "in" both drew
   physical reactions; "play/eject/power/on" buttons all drew reactions, so the button is one that engages something.
2. Object: cheap, tacky, plasticky, low-tech, close-miked, at home, probably kitchen; not boomy. Explicitly ruled out
   by Sarge: toaster (steered off, four toaster actions refused), any cassette deck (in storage in Bathurst), microwave
   (6 refusals), kettle (8), seatbelt (8), stapler, hole punch, pen, mouse, keyboard keys, CD player, torch, remote
   cover, mouse battery cover, drill battery/chargers, coffee pod/portafilter, latches and cupboard catches, power
   board/powerpoint switches, air fryer drawer, briefcase, bin pedal.
3. Action: something is put in or down and pushed until it latches (toast-down, pod-in, batteries-in, remote-back,
   mouse switch-on all "hot"), and the pushed part is an on/power-type control (computer power button "right area",
   mouse "switch to turn it back on" "very very close").

## 4. Decision

### Best guess (say it exactly like this)

**"Pushing the lever down on a rice cooker."** (If asked to be more specific: "putting the pot in and pushing the cook
lever down to turn it on.")

Why this one:

- Mechanism: the cheap mechanical rice cooker's cook lever is a spring-loaded lever with 2-3 cm of travel that snaps
  home against a magnet with a loud click-CLUNK, and pops up when done. It is exactly the piano-key-with-latch class
  the owner's ear picked out (tape recorder key: close mechanism, wrong machine) and the two-stage, 134 ms-apart,
  second-louder signature in the clip. The thin pressed-steel/plastic body gives a single strong mid mode (the clue's
  780 Hz) and a short decay, and the pot/base on the bench gives the 67 Hz thump.
- Hints: "pushing ... down" (toaster very close, 29 Jul); the toaster is the same lever-to-latch action, which is why
  it was "very close" and "probably what the answer is ... words in the correct answer" (25 Aug) yet steered off
  (15 Sep); "putting X in and pushing down" words; "the action is similar" to locking a portafilter in (20 Aug);
  "pushing the power button ... hovering around the right area" (19 Jul) and "pushing the switch to turn it back on ...
  very very close" (19 Oct), because the lever is the cooker's on switch; "cheap and tacky", "plasticky", "cheap
  microwave" all fit a $20 rice cooker; kitchen.
- Owner verdicts: nothing in the rejected list is a rice cooker or toaster-type lever; the one close recording is a
  latching lever.
- Guessed before? Only "opening a rice cooker" (15 Jun, Jesse): "Uh, no, it's not" - a different action, in the
  pre-hint period. The lever has never been guessed on air.

### Ranked alternatives

| # | Guess (as a caller should say it) | Why it fits the sound | Why it fits the hints | Owner's ear | Already guessed? |
|---|---|---|---|---|---|
| 2 | "Pushing the lever down on the toaster" | Same latching-lever mechanics; thin steel body ring ~800 Hz; bench thump. Acoustically the closest household lever to the clip. | Strongest single reactions of the whole run (29 Jul "very close", 25 Aug "probably what the actual answer is"). Only survives if the station is holding out for exact wording ("lever", not "button"/"toast"), and Sarge's 15 Sep "move away from it, give it up" was banter. | Not tested; no toaster in the rejected list. | Yes: toaster button down 29 Jul (very close); toast in + push down 25 Aug (words right); cancel button 7 Sep, crumb tray 3 Sep, pops up 15 Sep and 21 Sep, eject/cancel 27 Oct (all Absolutely not). |
| 3 | "Pushing the bottle into the SodaStream" (or "pushing the button on a SodaStream") | Bottle snaps into the collar with a plastic click-clunk; hard plastic body mode in the 700-900 Hz range; machine rocks on the bench (thump). | "Putting ... in and pushing down" words, portafilter "action similar", batteries-into-compartment "hot" (CO2 cylinder in the back), "pushing the button" first half, cheap plastic, kitchen. | Not tested. | Never guessed. |
| 4 | "Pushing the button on the kitchen bin to open the lid" (touch-top / push-button bin) | Push-release latch: press click (A), latch lets go and the sprung lid/thin steel body rings (B) with a body thump. | "Pushing the button to open ..." (27 Aug first half almost correct), "pushing in the ..." heart-skip (26 Oct), tinny/cheap, kitchen, home. | Caution: "sprung lids and cases" were judged way off, though a push-button bin may not have been among them. | Only the pedal bin (17 May, Cassie: "No, it's not"). The button lid has not been guessed. |
| 5 | "Pushing the push light on" (battery stick-on LED push light; dome is the button) | Push-push latch with a plastic dome: press click then latch clack; small hollow plastic body. | Cheap and tacky, plasticky, battery-powered (batteries-in guesses "hot", remote back "remarkable"), "switch to turn it back on" "very close", torch button "really does sound like that", power button "right area", "pushing in the cabinet ..." heart-skip (push lights live in cabinets). | Not tested. Light switches rejected, but a push light is a different mechanism. | Never guessed. |
| 6 | "Pressing play on the VCR" (or "pushing eject on the video player") | Old VCR transport keys are mechanical latching keys; mechanism engages ~100 ms after the key. | Explains the mid-year cluster: "pushing play" excited him (28 Jun), "pushing eject on the tape player" very close (1 Jul), "pressing play on a cassette player" among Ken's "remarkably close" (12 Oct), "old-school tape deck buttons" good words; VCR itself never named. Weak on "down/in", batteries, kitchen, cheap. | Tape-recorder key is the one close recording. | Never guessed as VCR; every cassette-machine guess refused (26 May, 23 Jun, 1-2 Jul, 13 Jul, 15 Jul, 28 Jul, 9 Sep, 27 Sep, 28 Oct). |
| 7 | "Pushing the button on the rangehood" (light or fan push-push button) | Latching piano-key buttons in a large tinny steel box: click then clack, sheet-metal ring, box boom. | Kitchen, tinny/echoey, "pushing the button" first half, "turn it on" area, old-school. | Caution: desk/pedestal fan push buttons were judged way off, and these are the same switch family. | Never guessed. |
| 8 | "Pushing the eject button on the hand mixer" (or "clicking the stick-blender attachment in") | Spring-loaded plastic release: press then beaters/arm snap; small plastic housing. | "Pushing eject" very close (1 Jul), "KitchenAid stick mixer" battery guess "wonderful" (16 Sep), kitchen, cheap plastic, "pushing in". | Not tested. | Not guessed (stick mixer only as a battery-pack guess, 16 Sep, Absolutely not). |
| 9 | "Pressing play on a Walkman" (portable cassette player / boombox) | Genuine piano-key transport, plastic housing (lighter than the Freesound recorder, so less boom, more mid). | Fits every "play/eject/old-school" reaction and "cheap and tacky"; the cassette deck in storage is a different object. | Closest family on the owner's ear. | Not guessed as Walkman; "tape recorder" (28 Oct) and "cassette player" (2 Jul) refused, which is the main problem. |
| 10 | "Pushing the pop-up plug down in the sink" | Push-push clicker latch in a basin: click, latch clack, basin ring. | "Pushing ... down", home, plasticky, never guessed. | Not tested. | Never guessed. |
| 11 | "Pushing the pump down on the soap dispenser" | Pump bottoms out (click), spring returns (clack) ~150 ms later; bottle on bench thump. | "Pushing down", kitchen/bathroom, cheap plastic, never guessed. Weak on the hard latching timbre. | Not tested. | Never guessed. |

Not worth more air time: stapler/staple remover/hole punch (14+ refusals), seatbelt (8), microwave door/button (6),
kettle switch/lid (8), pen click (6), mouse click (7), keyboard keys/space bar (5), cassette deck/player/recorder (9),
CD player (2), coffee pod/portafilter (6), batteries into drill/charger/vacuum (7), remote/mouse battery cover (4),
cupboard/magnetic catches (5), power board/powerpoint (4), torch, tape measure, toolbox, briefcase, suitcase handle,
air fryer, sandwich/toastie maker (2), self-inking stamp (3), price gun (3), tin opener/can (6), camera shutter.

## 5. What a library recording would need, for the top three

Common requirements (from section 1): one action lasting about 0.35 s; two distinct impacts 0.10-0.18 s apart with
the second 3-8 dB louder; first impact bright (1-2 kHz plus 3-6 kHz), second dull with a single dominant housing mode
between 600 and 900 Hz and a 60-150 Hz thump 20-40 ms after it; everything down 30 dB within 80 ms of the second
impact; no motor, hiss, buzz or water afterwards; no long bright ring. Check with `measure_clue.py`-style band
profiles: loud part should read roughly -7 / -12 / -8 / 0 / -5 / -10 / -13 (20 Hz to 12 kHz bands).

1. Rice cooker cook lever: a close-miked recording of a cheap mechanical rice cooker (Kmart/Tiger/National style)
   with the pot in, lever pushed down to "cook" until it latches. Expect click (lever hits stop) then CLUNK (magnet
   latch) with a hollow metal body note; the pop-up ("keep warm" click-off) would be a single clack and is the wrong
   action. Search: "rice cooker switch", "rice cooker lever", "cooker click".
2. Toaster lever: push the carriage lever down on a cheap two-slice toaster until the latch catches (no toast
   needed). Expect slide, click at the bottom, latch clunk, tinny shell ring. The pop-up is the wrong action. Search:
   "toaster lever", "toaster push down", "toaster handle".
3. SodaStream bottle/button: push an empty bottle up into the collar until it clicks and locks, then (separately) press
   the carbonating button without gas. Expect a plastic snap with a hard-plastic body note and a rock of the machine on
   the bench; any hiss means gas was in the line and is the wrong take. Search: "sodastream", "soda maker bottle",
   "bottle lock click".

Useful alternates for 4-6: "bin lid button" / "touch top bin"; "push light" / "tap light"; "VCR play" / "VHS eject".

Web notes used only for mechanism and for naming: rice cooker cook switch = spring-loaded lever held by a magnet that
releases at its Curie temperature ([kottke.org](https://kottke.org/24/01/the-clever-engineering-trick-that-allows-simple-rice-cookers-to-perfectly-cook-rice),
[US4431906A](https://patents.google.com/patent/US4431906A/esLanguage), [metafilter](https://metafilter.com/185671/How-A-Rice-Cooker-Works));
commercial libraries list toaster lever takes as "Toaster Push And Release", "Toaster Start Pull Down Lever"
([Soundstripe](https://www.soundstripe.com/library/sound-effects/26727)), an "electric cooker switch click"
([Artlist](https://artlist.io/sfx/track/our-kitchen-vol-2---electric-cooker-switch-click/87469)) and a CC0 "stove switch"
lever ([OpenGameArt](https://opengameart.org/content/stove-switch)); no Freesound hits surfaced for "rice cooker switch",
so the Freesound search should be done directly with the terms above.

## 6. Caveats

- The 790 Hz "ring" is mostly a fast decay (13 dB in 20 ms) with a low-level tail; it is a damped housing mode, not a
  bell. Do not over-weight long-ringing candidates.
- The transcripts are auto-generated; the 1 Jul "pushing a jack in on the tape player" is read here as "pushing
  eject", and 14 Oct Beno's garbled guess as a ring-pull. Neither changes the conclusion.
- Sarge's reactions are the only evidence that separates objects; they are consistent with "pushing a lever/button
  down or in until it latches, on a cheap plastic/tin kitchen appliance", and the rice cooker is the only unguessed
  appliance that matches both that and the measured mechanics. If the owner's A/B of a rice cooker lever is a miss, the
  SodaStream and the push-button bin are the next cheapest to test, and the toaster lever should be re-guessed on air
  with the word "lever" before anything else, because its wording may be the whole reason it was refused.
