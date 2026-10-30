# MNC Secret Sound: the "Key_Old_Recorder" near-miss (Freesound 641862) and what it tells us

Analyst: Fable 5.1. Inputs: `listening/full/641862_Key-Old-Recorder.mp3` (16.5 s, 44.1 kHz, resampled to 48 kHz),
`clues/mnc/clue_stacked.wav`, step-1 measurements (`fable_fresh_step1.md`), step-2 hints (`fable_fresh_step2.md`),
`analysis/mnc/onair_guesses.json` (196 guesses: 146 wrong, 37 warm, 13 unclear), and the owner's A/B verdicts.
Script: `analysis/mnc/fable_fresh/08_recorder.py`; figures `recorder_overview.png`, `recorder_events.png`,
`recorder_vs_clue.png`, `recorder_spectro.png`; the best 0.7 s window is saved as
`analysis/mnc/fable_fresh/recorder_best_window_48k.wav`. Levels are dB re full scale after peak normalisation;
times inside a window are seconds from the window start (window = matcher offset, 0.70 s long like the stacked clue).

## 0. Short version

The recorder file is twelve presses of a sprung piano-key transport key. Each press is: a sharp initial click, a
crunch as the key bottoms/locks 20 to 30 ms later, a big slow body thump, then 100 to 170 ms later a single sharp
clack as the key springs back to its top stop, followed by long metallic ringing. The clue has the **same grammar in
the same order and at the same tempo** (press-crunch, delayed thump, release-clack 133 ms later, ring), which is why
the owner hears it as close. It differs in four consistent ways: the clue's clicks are duller and crunchier (energy
1 to 4 kHz, not 4 to 8 kHz), its thump is higher and tighter (62 Hz, T60 0.15 s, not ~45 Hz, T60 0.4 s), its release
has 13 ms of plastic chatter instead of one clean metal snap, and its ring is stronger but shorter (791 Hz, T60 0.33 s,
not 814 Hz, T60 0.9 s) with a whole comb of 1 to 3 kHz plastic-housing modes behind it. So: the same kind of
sprung push key, but smaller, in a hard-plastic housing with a thin metal part, on or in a smaller/stiffer body, and
pressed by a softer touch.

## 1. The recorder presses, measured like the clue

### 1.1 Whole file

* 16.49 s; noise floor -53 dB (clue: -47 dB). The recording carries steady background tones near 230, 470 and
  1500 Hz (motor/room; absent in the clue) and a long low rumble under each press.
* Twelve press groups (1 ms-envelope peaks over -10 dB at 1.87, 2.95, 4.14/4.23, 5.11/5.22, 5.97, 7.22/7.36, 8.46,
  9.54/9.88, 11.06, 11.63/11.98, 13.13/13.31, 14.35 s). Most are a *pair*: press (crunch) then release (clack)
  100 to 170 ms later; some are two presses of different keys.
* Dryness: 4 to 8 kHz falls 20 dB within 4 to 14 ms of each click (clue 4 to 7 ms). Both are close-miked.

### 1.2 The best window (7.04 s; matcher score 0.883)

| Event | t in window | abs t | Level (>2 kHz 0.5 ms env) | Width (-15 dB) | Shape |
|---|---|---|---|---|---|
| pre-click | 0.148 | 7.188 | -40 dB | 2.6 ms | abrupt, tiny |
| initial click | 0.157 | 7.197 | -11 dB | 3.5 ms | abrupt, sharp (key starts to move / contact) |
| lock crunch | 0.168 to 0.180 | 7.208 to 7.220 | -28 rising to -9 dB | 10 ms | crescendo ending on its loudest grain |
| thump | peaks 0.220 | 7.260 | <250 Hz -8 dB | | starts ~0.185, builds over 35 ms, instantaneous frequency 44 to 48 Hz, decays with T60 ~0.4 s (73 Hz component T60 430 ms, 34 Hz component T60 660 ms) |
| release clack | 0.317 | 7.357 | -6 dB (loudest) | 4.1 ms | abrupt; 42 dB jump in 3 ms; one clean snap, little chatter |
| ring | 0.33 onward | | 814 Hz 13 dB above neighbours, T60 ~0.9 s; 1640 Hz T60 0.4 s; 450/490 Hz T60 0.15 to 0.17 s; 150 Hz T60 0.18 s | | |

Intervals: initial click to lock 23 ms; lock to release **137 ms**; thump peaks 40 ms after the lock grain and
63 ms after the initial click. Loudest-click spectral centroid 5.6 kHz; 4 to 8 kHz peak -10 dB; 16 to 20 kHz -25 dB.

### 1.3 The other matcher windows

| Window | Structure | Press-to-release | Thump f / level | Notes |
|---|---|---|---|---|
| 13.02 s | small tick 0.033; press (abrupt -15 dB at 0.095, -6 dB at 0.113, crescendo 0.122); second *press* at 0.284 to 0.298 (crescendo, -12 dB) | 170 ms, but the second event is another press, not a release | 61 to 64 Hz, -12 dB; 73 Hz T60 0.57 s | thump frequency here is the closest to the clue; ring weak (546 Hz T60 0.57 s, 2.4 kHz) |
| 3.92 s | press 0.186 (abrupt -20) / 0.203 (-15) / crescendo 0.212; release 0.309 (abrupt -11 dB, 12 ms) | 100 ms | 54 Hz, -8.5 dB | 508 Hz T60 0.7 s, 1517 Hz steady tone |
| 1.72 s | press 0.132 (-12) / 0.148 (-6, abrupt); tiny release tick 0.247 (-14 dB, 1.6 ms) | 100 ms | 72 to 78 Hz then 46 Hz, -15 dB | release very weak |
| 8.32 s | press 0.144 (abrupt -5 dB, 3.6 ms, very sharp); second press 0.292 (crescendo -14 dB) | 148 ms | 56 to 76 Hz, -25 dB | thump weak; room rumble before |

Across windows the recorder's press-to-release spacing is 100 to 170 ms (the clue: 133 ms), its thump sits at 45 to
65 Hz with T60 0.4 to 0.6 s, and its rings (450 to 550, 814, 1640 Hz) last 0.4 to 0.9 s.

### 1.4 Feature-by-feature comparison

| Feature | Clue (stacked) | Recorder (best window) | Verdict |
|---|---|---|---|
| Overall grammar | tick (A) 54 ms before; crunch press (B); delayed thump; release clack (C); ring; settle tick (D) | tick 9 ms before; sharp click then crunch press; delayed thump; release clack; ring; (no settle tick) | **same order** |
| Press-to-release | 133 ms | 137 ms (100 to 170 across presses) | **match** |
| Press (B) | 13 ms crescendo ending on loudest grain, -5 dB, no clean spike; centroid 3 to 4 kHz; flat 250 Hz to 6 kHz | 3.5 ms sharp click (-11 dB) then 10 ms crescendo to -9 dB; centroid >5 kHz | same crunch, but the recorder adds a loud metallic initial click the clue lacks |
| Pre-click (A) | -15 dB (10 dB under B), 54 ms before B, centroid 5 to 6 kHz | -11 dB (2 dB under the lock), 23 ms before the lock | clue's first contact is softer and earlier: a finger landing gently, not a contact leaf snapping |
| Thump | starts 15 ms after click, peaks +24 ms; 62 Hz (first cycle 86 Hz); Q 4 to 7, T60 0.12 to 0.2 s; peak -15 dB; 15 to 28 % of event energy | starts ~5 ms after lock, peaks +40 ms; 44 to 48 Hz (some presses 55 to 64 Hz); T60 0.4 to 0.6 s; peak -8 dB; dominant | clue thump is **higher, shorter, quieter**: a smaller, stiffer, more damped body (or bench) than the recorder's large case |
| Release (C) | abrupt 2 ms onset to -2 dB, then **13 ms of chatter**; centroid 2.5 kHz falling to 0.9 kHz in 6 ms; strongest 1 to 4 kHz | abrupt 3 ms, -6 dB, **4 ms wide, one clean snap**; centroid 5.6 kHz; strongest 4 to 8 kHz | clue release is duller and rattly (plastic part hitting a plastic stop and bouncing); recorder is a steel lever snapping on a metal stop |
| Main ring | 791 Hz, 28 dB above neighbours, Q ~120, T60 0.33 s; re-excited by the thump; 20 dB weaker after B | 814 Hz, 13 dB above neighbours, T60 ~0.9 s; also 1640 Hz T60 0.4 s | same pitch region, but the clue's is **stronger, cleaner and shorter**: a thinner/smaller metal part that is better coupled to the release and more damped (held, clamped, or touching plastic) |
| Other modes | 472 Hz (T60 0.14 s); comb 1125, 1300, 1700, 1850, 2035, 2570, 3190 Hz all T60 0.11 to 0.19 s, after both B and C | 450/490 Hz (T60 0.15 s); 150 Hz; little between 1 and 3 kHz except 1640 Hz | the clue has a **hard-plastic housing full of 1 to 3 kHz modes**; the recorder's case is deader with a few long metal rings |
| Brightness | 4 to 8 kHz peaks -17/-14/-18 dB (A/B/C); 16 to 24 kHz -27 dB rel | 4 to 8 kHz -10 dB; 16 to 20 kHz -25 dB | recorder is brighter/clickier; clue is crunchier |
| Dryness, noise | 20 dB in 4 to 7 ms; floor -47 dB; no tones | 20 dB in 4 to 14 ms; floor -53 dB; steady tones ~230/470/1500 Hz and rumble | both close-miked; the clue has no machine/room tone |
| After-event | settle tick D at +95 ms; sound gone by 0.38 s | no settle tick; ring and rumble last >0.5 s | clue object settles fast |

**What the owner most likely hears as "close but not it":** the rhythm and the two-part "crunch ... clack" with a
thump under the first and a ring after the second are the same; but the recorder is clickier and more metallic
(sharper, higher clicks), its thump is deeper and lingers, and its ring is thinner and longer, whereas the clue is
"plastickier": duller clicks, a short tight thump, a rattle on the release, and a fuller, shorter ring. In words:
*the recorder is a steel mechanism in a big box; the clue is a plastic mechanism with one metal part in a small box.*

## 2. Mechanism, and the physical difference that would give the clue

### 2.1 What the recorder key is

A classic transport "piano key": a long plastic key lever pivoting at the rear, driving a steel slide against a
return spring. Pressing it: (1) the key leaves its rest position and a contact leaf or detent snaps (the sharp
initial click), (2) the slide travels and its locking bar drops into the notch or the key hits the bottom stop
(the crunch: several steel-on-steel grains in 10 ms), (3) the hand's force goes on into the chassis and the thin
case breathes at 35 to 50 Hz (the thump), then (4) on release (here the key did not latch, or the operator let go)
the spring throws the slide/key back against its upper stop: one hard metal clack, and the slide, spring and head
plate ring (814, 1640 Hz for 0.4 to 0.9 s).

### 2.2 What must differ to produce the clue

| Clue feature | Physical difference from the recorder |
|---|---|
| No loud initial click; a soft tick 54 ms early | No contact leaf or detent at the start of travel; the first thing heard is the finger/nail landing on a plastic key or the key leaving a soft rest. Longer travel at a slower start (54 ms from first touch to bottoming). |
| Crunch of 1 to 2 ms plastic grains, centroid 3 to 4 kHz | The key bottoms or latches in **plastic guides** (plastic ratchet/stop, moulded button in a moulded housing), not steel slides; lighter parts. |
| Thump 62 Hz, Q 5, peak 10 dB lower, delayed 24 ms | A smaller, stiffer, more damped body than a tape-recorder case: a hard-plastic housing 15 to 30 cm across, or a small appliance pressed into a bench/desk, with a softer finger follow-through. The first cycle at 86 Hz suggests the push itself (12 ms force pulse) shapes the thump. |
| Release with 13 ms rattle, duller (1 to 4 kHz) | The returning key/button hits a **plastic stop** and bounces (chatter), rather than a steel lever on a metal stop; spring weaker or part lighter. |
| 791 Hz ring, Q 120, T60 0.33 s, excited by the release and re-excited by the thump; weak after the press | One **thin metal part** struck or released by the return stroke: a return spring, a steel contact strip or plate, a lid hinge, a thin lid or shade (sizes that ring near 790 Hz: 1 mm steel strip 8 cm, 0.3 mm tin lid 7 cm, 3 mm steel bar 14 cm, 2 mm aluminium 11 cm), coupled to the housing so it decays in 0.3 s rather than 0.9 s. |
| Comb of 1.1 to 3.2 kHz modes, Q 60 to 110, after both stages | A hard-plastic (ABS/polycarbonate) housing of modest size, thin-walled: "cheap and tacky", "plasticky", "tinny", slightly "echo-y", exactly Sarge's words. |
| Everything over by 0.38 s | Light parts, damped body; no big case rumble. |

So the clue is: **a sprung push key or button, with plastic travel and stops and one thin metal part, in a small
hard-plastic housing, pressed and let go in about 130 ms**, recorded with the microphone very close.

## 3. Objects with the same (or closely related) mechanism, ranked

Score M = fit to measurements (1 to 5: sprung button in a hard-plastic body with a metal part, press-release 100 to
200 ms, bench/body thump, plastic rattle on return, ~800 Hz ring). Score H = fit to Sarge's hints (step 2: answer
starts "pushing the [button/switch/lock] [down/in]...", cheap/plasticky/tinny, kitchen-ish, warm words: toaster
lever, tape-player button, power button, switch after batteries, batteries into a compartment). "On air" cites the
JSON verdicts; a warm earlier guess is kept, not dropped.

1. **"Pushing the lever down on the rice cooker" (the cook lever that clicks down and pops up).** M5 H4. Sprung
   lever in a plastic/thin-steel body, latches with a crunch, springs back with a clack and tinny ring; kitchen;
   kin of the "very close" toaster lever. On air: only "opening a rice cooker" (15 Jun, wrong).
2. **"Pushing the lever down on the toaster" (without it catching, so it springs back).** M5 H5. Press crunch, body
   thump, carriage springs up and clacks, steel frame rings. On air: "pushing down the button on the toaster"
   (29 Jul, **warm, "very close"**), "putting toast in and pushing it down" (25 Aug, **warm, words in the answer**);
   cancel button (07 Sep), pop-up (15 Sep), crumb tray (03 Sep), eject (27 Oct) all wrong. Re-ask only with a new
   twist (empty toaster / not plugged in / the lever rather than the button).
3. **"Pushing a key on the electric keyboard / piano" (unplugged electronic keyboard key).** M5 H4. Plastic key
   bottoms on a plastic/felt stop (crunch), hollow plastic case thumps, key springs back and rattles on its top stop
   ~130 ms later, metal keybed strip rings; cheap and tinny. Sarge grinned at "keyboard" guesses (15 Jun; 01 Jul
   "right words") while refusing every *computer* keyboard guess (28 May, 11 Jun, 16 Jun, 18 Jun wrong). Never
   guessed as a musical keyboard.
4. **"Pushing the push-button switch on the desk lamp / bedside lamp."** M4 H5. Push-push latching switch (press
   click, release clack), lamp base on the table (thump), thin metal shade or arm rings; "switch", "pushing the
   button", cheap. On air: power-board switch (28 Jun, warm "sounds exactly like it"), push-button on a power board
   (14 Jul, wrong but "plasticky, you're right"), hot-plate switch (28 Jul, wrong, "my sounds are up that alley");
   lamp never guessed.
5. **"Pushing the button on the range hood / exhaust fan" (piano-key buttons, light or fan).** M4 H4. Same
   piano-key mechanism as the recorder, mounted in a thin sheet-steel hood (tinny, echo-y, 60 Hz panel), kitchen,
   cheap. On air: never. (Owner's own fan-button recordings were "way off", but those were pedestal/desk fans in
   plastic heads; the hood's sheet metal is a different body.)
6. **"Pushing the power button on the stereo / boombox / mini hi-fi."** M4 H4. Big push-push latching button in a
   plastic front panel over a steel chassis: clunk, clack, chassis ring; the tape-deck family is warm (13 Jul
   "really good words", 01 Jul "very close", 02 Jul "really good things") while the tape keys themselves are
   refused and the deck is in storage. On air: "clicking in the buttons on an old radio" (16 Jul, wrong), "pushing
   play on a vinyl player" (28 Jun, warm); power button of a stereo never guessed.
7. **"Pushing the start / power button on the washing machine or dryer."** M4 H3. Push-push button in a thin
   enamelled-steel body: cheap/tinny, bench-like thump. On air: never (dishwasher tablet door 06 Sep, unclear).
8. **"Pushing the button on the kettle to open the lid."** M5 H4 (step-2 candidate; a release button that frees a
   sprung lid rather than a sprung key, but the press-then-pop timing is identical). On air: kettle lid open/close
   (31 Aug, warm "can't say more"), kettle lid closed (27 Oct, wrong), kettle switch (06 Jul, 24 Aug, 06 Sep, wrong).
9. **"Pushing the button on the kitchen bin to open the lid."** M5 H4 (step-2 top candidate; same reasoning as 8:
   plastic latch press, hollow bin thump, thin lid clacks and rings). On air: pedal bin (17 May, wrong); never as a
   push-button lid.
10. **"Pushing the button on the thermos / flask to open the spout" or "pushing the flip-lid button on a drink
    bottle".** M4 H3. Plastic button, sprung lid snaps on a stainless body. On air: takeaway coffee lid (01 Sep,
    wrong); never.
11. **"Pushing a key on an old typewriter."** M4 H2. Sprung key lever, type bar strikes (clack with a metal ring),
    key returns; dry close-miked clicks. Misfit: not cheap/plasticky, body is a heavy frame. On air: never.
12. **"Pushing the button on the kitchen timer / stopwatch."** M3 H4. Plastic button in a small hollow case;
    "pushing the button", kitchen, cheap; weak thump unless on the bench. On air: never (alarm-clock snooze 20 Oct
    wrong).
13. **"Pushing the foot switch on the lamp cord / Christmas lights."** M4 H3. Round plastic push-push switch on the
    floor: click-clack, floor thump, cheap. On air: never.
14. **"Pushing the on/off switch on the wireless keyboard."** M3 H5. Slide/push switch on a battery gadget lying on
    the desk; the mouse version was "very very close" (19 Oct, warm). Misfit: a slide switch is shorter and quieter
    than the measured 13 to 16 ms crunches. On air: never as keyboard.
15. **"Pushing the lock down on the car door" (old pull-up knob) / "pushing the lock button".** M3 H4. Sprung knob in
    a hollow door (60 Hz panel), tinny; "pushing the lock down" started Sarge's heart (09 Sep, unclear). On air: door
    latch into the jamb (26 May, wrong), deadbolt (20 Aug, wrong).
16. **"Pushing the lever down on a lever-arch file."** M3 H2. Sprung lever with a catch, steel mechanism on a
    cardboard board (thump); office. On air: ring binder (18 May, warm "good guess, not exactly").
17. **"Pushing the button on the stand mixer / blender (old piano-key buttons)."** M4 H3. Piano-key switches in a
    plastic base; kitchen. Misfit: motor would start. On air: never (stick-mixer battery 16 Sep warm "right track").
18. **"Pushing the button on the old push-button telephone."** M3 H2. Sprung keys in a hollow plastic body, tinny.
    On air: never.
19. **"Pushing the handbrake / boot-release / fuel-flap button in the car."** M3 H3. Sprung release buttons that
    free a catch with a pop; "crap car" tinny remark (29 Jun). On air: sunglass holder (29 Jun, 07 Sep, wrong),
    glove box (31 May, wrong, "boomier"), window button (30 Jul, warm).
20. **"Pushing the ignition button on the BBQ / gas stove igniter."** M3 H2. Sprung piezo button: press crunch and
    release clack; hollow steel body. On air: gas lighter (10 Jun, wrong), gas plate (23 Aug, wrong).
21. **"Pushing the button on the torch / bike light."** M3 H3. Push-push switch in a plastic tube. On air: torch
    (27 Sep, **warm**, "it really does sound like that"); bike light never.
22. **"Pushing the button on the doorbell / intercom / lift."** M3 H2. Sprung wall button in a hollow plastic
    housing. On air: crossing button (26 Jun, unclear), sliding-door button (22 Oct, wrong).
23. **"Pushing an arcade / pinball button."** M4 H1. Big sprung plastic button with a microswitch: clunk-clack and
    cabinet thump. Not domestic. On air: never.
24. **"Pushing the lock button on the bathroom door knob" (privacy push-lock).** M3 H3. Sprung button in a
    hollow knob; pops out when the handle turns. On air: toilet-door latch (13 May, unclear).
25. **"Pushing the button down on the pump-pot / air-pot flask."** M4 H3 (step-2 candidate). On air: never.
26. **"Pushing the tare / on button on the kitchen scales."** M3 H4. Battery device on the bench, "pushing the
    button", kitchen, cheap. Misfit: usually a soft tactile dome. On air: never.
27. **"Pushing the pedal / button on the sewing machine" or "pushing the key on the cash register / calculator".**
    M3 H1. Sprung mechanical keys. On air: never.
28. **"Pushing a key on the old recorder / pushing play on the tape deck."** M4 H4 by words, but Sarge cannot have
    recorded his deck (15 Jul) and the family has been refused on 26 May, 23 Jun, 15 Jul, 28 Jul, 09 Sep, 27 Sep,
    28 Oct; keep only as the acoustic reference (this file).

## 4. Library search terms for the top 15

| # | Candidate | Search terms |
|---|---|---|
| 1 | rice cooker lever | `rice cooker`, `cooker lever` |
| 2 | toaster lever (empty / unplugged) | `toaster lever`, `toaster push` |
| 3 | electronic keyboard key (unplugged) | `piano key`, `keyboard key click`, `synth key` |
| 4 | desk/bedside lamp push switch | `lamp switch`, `lamp button` |
| 5 | range hood buttons | `range hood`, `rangehood button`, `cooker hood` |
| 6 | stereo/boombox power button | `stereo power`, `boombox button`, `hifi button` |
| 7 | washing machine / dryer button | `washer button`, `dryer button` |
| 8 | kettle lid button | `kettle lid`, `lid release` |
| 9 | push-button bin lid | `bin lid`, `trash button` |
| 10 | flask / bottle spout button | `thermos button`, `flask lid`, `bottle lid` |
| 11 | typewriter key | `typewriter key` |
| 12 | kitchen timer / stopwatch button | `kitchen timer`, `stopwatch click` |
| 13 | lamp foot switch | `foot switch`, `cord switch` |
| 14 | wireless keyboard switch | `keyboard switch`, `slide switch` |
| 15 | car door lock knob / lock button | `door lock knob`, `car lock button` |

A library hit must reproduce, on the step-1 scripts: two events 100 to 200 ms apart with the second 2 to 5 dB louder;
first event a 10 to 15 ms crescendo with energy 1 to 4 kHz (not a 3 ms spike at 5 kHz); a 55 to 70 Hz thump peaking
20 to 30 ms after the first event with T60 under 0.25 s; the second event abrupt but with 10 to 15 ms of chatter;
a single 750 to 850 Hz ring 25 to 30 dB above its neighbours with T60 0.25 to 0.45 s only after the second event;
and a 1 to 3 kHz mode comb after both. The recorder file fails on the thump (too low, too long), the click
brightness, the release chatter and the ring strength/length, which is exactly the "close but not it" the owner
reports.
