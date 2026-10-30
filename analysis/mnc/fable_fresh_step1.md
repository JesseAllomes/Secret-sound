# MNC Secret Sound: fresh step-1 analysis (audio only)

Analyst: Fable 5.1. Inputs: `clues/mnc/clue.wav` (original, 48 kHz), `clues/mnc/clue_stacked.wav` (median of 289
broadcasts, timeline = original + 0.05 s), `harvest/mnc/stack/report.txt`, and the 295 aligned plays. No transcripts,
no sound libraries. Scripts and figures are in `analysis/mnc/fable_fresh/` (01 envelope, 02 spectrogram, 03 modes,
04 attacks, 05 background/consistency, 06 details, 07 overview; PNGs alongside). All times below are **seconds from
the start of the original clip** (stacked time minus 0.05). Levels are dB re full scale of the stacked file unless
stated.

## 0. Summary in one paragraph

The recording is 0.33 s of actual sound (0.05 to 0.38 s), close-miked and dry. It is four hard, broadband "clicks"
(A, B, C, D) of which B and C are each followed, 20 to 30 ms later, by a soft low-frequency **thud** that rings a
~62 Hz mode. A is a small bright tick 53 ms before B; B and C are the main events, 133 ms apart, each a 13 to 16 ms
"crunchy" multi-contact click rather than a single clean impact; D is a tiny tick 95 ms after C. C also sets off a
clean 791 Hz ring (Q ~ 120, T60 ~ 0.33 s) that B barely excites. Everything after 0.38 s and before 0.05 s is
station background. The gestalt is "tick ... crunch-THUD ... CLACK-THUD ... tick", i.e. a two-stage mechanical
action or a two-bounce landing on a resonant surface, with a ringing hard part that only the second event hits.

## 1. What the measurements say

### 1.1 Extent of the recording (confidence: high)

* Common ratio in `report.txt` goes from 0.10 at +0.025 to 0.80 at +0.050 and stays 0.6 to 0.95 until +0.35, then
  0.36 (+0.350), 0.06 (+0.375), 0.01 (+0.400). My own 5 ms recomputation from the plays: 0.14 at 0.050, 0.40 at
  0.055, 0.84 at 0.060; 0.21 at 0.370, 0.05 at 0.375, 0.03 at 0.385. **The object sound occupies 0.055 to 0.375 s.**
* The ratio is weakly above floor (0.03 to 0.10) from -0.03 to +0.05: the clip file carries about 50 ms of its own
  quiet pre-roll (room tone at about -47 dB), not station noise. Nothing of the object is in it.
* The stacked file was gated after 0.38 s (level drops to -100 dB); the original's 791 Hz band keeps decaying
  smoothly through 0.38 to 0.42 s at the expected slope, so nothing was cut off mid-event: the sound simply ends.

### 1.2 Event list (confidence: high for timing and level, medium for internal structure)

| Event | Onset (>bg+10 dB) | Peak | Peak level (1 ms RMS) | Duration of click | Character |
|---|---|---|---|---|---|
| A | 0.058 | 0.0635 | -15 dB | ~4 ms (10-90 % rise 4.4 ms) | small, very bright tick; spectral centroid 5 to 6 kHz; strongest in 4 to 8 kHz (-17 dB), content to >16 kHz; faint 5.5 kHz ring (Q ~ 80) and 1.36 to 1.41 kHz components, all weak |
| B | 0.108 | 0.1175 and 0.1220 (two sub-peaks) | -5 dB | 13 ms (0.111 to 0.124) | broadband "crunch": a crescendo of 1 to 2 ms grains that gets louder towards its end (-39, -29, -22, -14, -11, ... -8 dB per ms) and stops abruptly at 0.1235; centroid 3 to 4 kHz; flat 250 Hz to 6 kHz |
| B-thud | 0.125 (small ripples), big swing 0.133 to 0.16 | 0.145 to 0.152 | <200 Hz peak -16 dB | force pulse ~12 ms wide, peaks 24 ms after B | low thump, see 1.3 |
| C | 0.2445 (precursor), main 0.2495 | 0.2507 | -2 dB (loudest) | 16 ms (0.247 to 0.263) | abrupt start (from -45 to -9 dB in 2 ms) then chattering decay; centroid 2.5 kHz falling to ~0.9 kHz within 6 ms as the 791 Hz ring takes over; strongest in 1 to 4 kHz |
| C-thud | 0.255 ripples, big swing 0.267 to 0.31 | 0.285 | <200 Hz peak -15 dB | force pulse ~12 ms wide, peaks 22 ms after C | same as B-thud, slightly faster decay |
| D | 0.343 | 0.3455 | -42 dB (>2 kHz band) | ~3 ms | tiny bright tick, 4 to 8 kHz; visible in both original and stacked |

Intervals: A→B 54 ms, B→C 133 ms, C→D 95 ms. Click-to-thud-peak delay: B 24 to 30 ms, C 22 to 34 ms (same within
error). The thud is never before the click.

Asymmetry worth noting: **B ramps up and ends on its loudest grain** (like something sliding/ratcheting into a
seat, "crrrk-CLACK"), whereas **C starts at full level and decays with chatter** (like an impact with rattle).
Attack spectra (first 8 ms, 1/3-octave) correlate B-C 0.79, A-B 0.54, A-C 0.39: B and C are the same materials in
contact; A is a smaller/harder contact.

### 1.3 The low-frequency thud (confidence: high that it exists and is delayed; medium on the force-pulse model)

* Below 200 Hz the signal is flat until the click; the first ripples (160 to 200 Hz) start 5 ms after the click, and
  the large swing begins 15 ms after it, peaks at +24 ms (B) / +22 to +34 ms (C), then decays.
* Dominant mode **62 Hz** (instantaneous frequency 60 to 64 Hz, both events; original and stacked agree):
  T60 = 205 ms after B, 118 ms after C (envelope slope, stacked; original 220/121 ms). Matrix-pencil fit gives
  61.4 Hz, T60 235 ms (B) and 62.9 Hz, T60 135 ms (C). **Q ≈ 4 to 7: heavily damped.** The first full cycle in both
  events is shorter (11.6 ms, ~86 Hz) before settling to 62 Hz; the lowpassed waveform grows over 1.5 cycles before
  decaying, so it is a resonator being *driven by a ~10 to 15 ms force pulse*, not an impulse response. Inverse
  filtering the 62 Hz resonator puts the drive peak at 0.141 s (B) and 0.266 to 0.275 s (C).
* Secondary low modes: ~170 Hz (T60 ~100 ms, both events), ~205 to 210 Hz (T60 160 to 175 ms), ~330 Hz (T60 120 to
  165 ms). These start at the click and are not delayed.
* Energy below 200 Hz is 28 % (B) and 15 % (C) of the event energy. Peak amplitude below 200 Hz is only 13 dB under
  the click peak. For a typical phone/handheld recorder (which rolls off below ~100 Hz) this is a *strong* LF event.
* It is not mains hum (Australia is 50 Hz; this is 62 Hz, decays, and is absent before the clip).

### 1.4 Ringing (tonal) components (confidence: high for 791 Hz; medium for the rest)

| Mode | Where | T60 / Q | Notes |
|---|---|---|---|
| **791 Hz** (789 to 792) | after C: -25 dB; after B: -45 dB | T60 330 ms (orig 380), Q ≈ 120 | the only long clean ring. Starts at C's precursor contact (0.2445, already -25 dB by 0.246), dips to -45 dB at 0.272 and comes back to -28 dB by 0.280: it is **re-excited by the thud event** at ~0.272, so the ringing part is mechanically coupled to whatever thuds. Twenty dB weaker after B: B did not hit it (or hit it elsewhere). Still visible (-50 dB) at 0.37 in the original. |
| 472 to 484 Hz | after C (-31 dB flat 0.252 to 0.27, then decays) | T60 ~140 ms | weak after B (-49 dB) |
| 1125 Hz, 1300 Hz, 1700 Hz, 1850 Hz, 2035 Hz, 2570 Hz, 3190 Hz | after both B and C at -28 to -42 dB | T60 110 to 190 ms (Q ~ 60 to 110) | a dense comb of modest-Q body modes, same set after both events: the object struck in B and C is the same stiff but damped body |
| 5.5 kHz, 6.4 kHz, 1.36 to 1.41 kHz | after A only, very weak | T60 30 to 120 ms | A touches a small, hard part |
| 164 to 172, 205 to 210, 330 Hz | after both, with the thud | T60 100 to 175 ms | see 1.3 |

### 1.5 Fine texture of the clicks (confidence: medium)

The >2 kHz envelope within B and C is granular: B has sub-bursts at 0.1104, 0.1122, 0.1153, 0.1163, 0.1175, 0.1193,
0.1205, 0.1220, 0.1232 (spacings 0.8 to 3 ms, autocorrelation peak at 1.1 ms, r = 0.5); C has 0.2454, 0.2479, 0.2491,
0.2508, 0.2535, 0.2555, 0.2578, 0.2608 (spacings 1.2 to 3 ms, autocorrelation 1.7 ms, r = 0.44). Either several parts
making contact in quick succession, a rough/ratcheting contact, or micro-bounces (chatter) of a hard part. A single
clean impact between two hard bodies would be 1 to 3 ms long; these are 13 to 16 ms.

### 1.6 Recording conditions (confidence: high)

* Very dry: 4 to 8 kHz energy falls 20 dB within 3.6 to 6.5 ms of each click peak and 30 dB within 10 to 17 ms.
  Either the mic is within ~0.5 m of the source, or the space is small and dead. No audible room tail.
* Bandwidth of the recording extends beyond 16 kHz (A has content to 20 kHz in the stacked file); the original clip
  was lowpassed at 16 kHz by the broadcast chain.
* No whine/tonal lines belong to the recording: the 11.2, 12.1, 13.3 and 15.75 kHz lines present in individual
  broadcasts are 20 to 30 dB *below* floor in the stacked pre-roll, so they are the station's. No 50 Hz hum either.
* Noise floor of the recording ~ -47 dB re peak (quiet room / phone recorder).
* Plays are consistent: correlation of each play with the median over 0.10 to 0.37 s is 0.95 (median), 0.92 (10th
  percentile), min 0.70. Nothing in the clip varies between broadcasts.

## 2. What the physics allows

### 2.1 The 62 Hz, Q 4 to 7 thud

A 62 Hz mode with T60 ~ 0.15 s and a 12 ms soft drive pulse means a **large, flexible, well-damped surface being
loaded by something compliant**, not a small object. Candidates for the surface: a desk/table top or kitchen bench
(particleboard/laminate tops ring at 50 to 100 Hz with Q ~ 5), a hollow-core door, a cabinet or drawer front, a
plasterboard wall, a plastic bin or large container, a fridge or car door panel, a cardboard carton, a drum-like hollow
body. The delay (20 to 30 ms after the hard click) and the softness of the drive mean the thud is **the second stage of
the same action**: something hard contacts first, then a broader, slower, heavier load arrives, e.g.

* a hand/finger pad following through after a mechanism snaps (press on a stapler/punch/switch/lid: the snap
  happens before the hand's force peaks on the table),
* a flat object landing on a corner/edge first and then slapping down flat (air-cushioned face landing),
* a lid/door that clicks its latch and then seats against a compliant stop/seal,
* a spring-driven part that snaps (click) and then the whole device rocks/lands on its feet.

Because the thud is this strong relative to the clicks, the recorder was very probably **on or near the same surface**
(structure-borne path) or the surface itself is the main radiator. This is a key test (section 4).

### 2.2 The 791 Hz ring, Q ≈ 120

T60 of 0.33 s at 791 Hz rules out free glass or free solid metal (Q 1000+, T60 > 1 s) and rules out soft plastic or
foam-backed parts (Q < 30). It fits: **steel or aluminium that is bolted, riveted, held, or sitting on something**
(spring steel strip, a stapler top arm, a steel plate or lid, a bracket, a binder ring, a lever), **hardwood** (Q 80
to 150: a board, slat, drawer), **hard engineering plastic** (polycarbonate/acrylic/nylon, Q 50 to 120), or **glass or
ceramic damped by hand contact** (held tumbler/jar: T60 drops to 0.1 to 0.4 s). Size examples that put a first
bending mode near 800 Hz: a 1 mm steel strip ~8 cm long; a 3 mm steel bar ~14 cm; a 2 mm aluminium bar ~11 cm; a 3 mm
hard-plastic bar ~7 cm; a 10 mm hardwood slat ~20 cm; a 7 cm tin lid 0.3 mm thick; a 2 cm thick 30 cm wooden board
(2nd mode). Not a coin, key or cutlery (those sit at 2 to 15 kHz), not a bell, bowl or wine glass (longer, purer ring).

The 791 Hz ring is excited by C's first contact (precursor at 0.2445) and again by the thud ~25 ms later, and hardly at
all by B. So the ringing part is **a component of the thing that thuds**, struck or released in C but not in B.

### 2.3 The comb of 1.1 to 3.2 kHz modes with Q ~ 60 to 110, excited by both B and C

A stiff but internally damped body with many modes in the 1 to 3 kHz range: a hard-plastic housing, a wooden object,
a thin-walled metal box with contents, or a laminated/composite slab. The same comb after B and C means B and C
strike the same body. T60 ~ 0.12 s for all of them is typical of ABS/polycarbonate housings and of wood, and of
assembled sheet metal (not of free solid metal).

### 2.4 The clicks themselves

* A: tiny, bright (centroid 5 to 6 kHz), 4 ms: a small hard tip (plastic or metal) touching a hard surface lightly, or
  a small latch/pawl/switch contact; its own ringing is weak and high (5.5 kHz: a small part a few cm long).
* B: 13 ms crescendo chatter ending in the loudest grain: sliding/ratcheting/rolling contact that terminates in a
  hard seat; or an edge landing that rolls onto a face; or a stack of parts engaging in turn.
* C: hard abrupt impact (2 ms rise) with 13 ms of chatter after: a spring-driven snap, a flat slap, or a hard
  bounce with rattle of loose parts.
* Both have energy to 16 kHz+: hard materials (plastic, metal, wood, glass, ceramic), not fabric, paper or soft food.

### 2.5 Timing

B→C = 133 ms. Human press-then-release of a lever or button is typically 80 to 250 ms. A bounce with coefficient of
restitution ~0.7 on a hard surface gives successive intervals shrinking by ~0.7 (133 → 95 ms fits C→D exactly, but A→B
= 54 ms does not fit a bounce chain before B, so A would have to be a separate contact). C being 3 dB louder than B
with a 20 dB stronger 791 Hz ring argues against a passive bounce of the same part and for **a different part or a
spring-driven second stage** (release stroke, snap-back, second corner/face).

### 2.6 What is ruled out or disfavoured by the data

* Anything with a sustained noise (water, pouring, tearing, zipping, scraping, spraying, frying): absent.
* Keys, coins, cutlery, jewellery, chains: no sustained high-frequency jingle, no 3 to 15 kHz long rings.
* Glassware or ceramics rung freely (wine glass, bowl, plate, mug clink): rings would be higher-Q and often >1.5 kHz.
* Speech, footsteps, animals, engines, doors slamming in a big room: wrong structure and far too dry.
* Single-event actions (one switch, one seat belt, one can opening): there are two matched click+thud stages.
* Small handheld objects operated in the air with the recorder held separately: the 62 Hz thud needs a large
  surface and a load path.

## 3. Ranked candidates (phrased as a caller would)

Ranking weighs: two matched click+thud stages 133 ms apart; a soft force pulse 20 to 30 ms after each click; a hard
part ringing at 791 Hz excited only by the second stage; crunchy 13 to 16 ms clicks; a large damped surface at 62 Hz;
very close, dry recording. Nothing is excluded; "misfit" lists what each must explain away.

1. **"Using a stapler" (pressing a stapler on a desk).** Fit: press stroke = crunch of the staple being driven and
   folded (B's 13 ms crescendo ending in the clack as the arm bottoms), hand follow-through thumps the desk 25 ms
   later; release = spring-driven arm snapping up against its stop (C, abrupt, louder) with the steel arm/magazine
   ringing at ~800 Hz, desk rebounding; A = the arm's first contact with the paper/base; D = pusher settling.
   Misfit: the 791 Hz ring should then also appear (weaker) at the press stroke; many staplers release slower than
   133 ms.
2. **"Punching holes with a hole punch."** Fit: same press/release logic, bigger steel body (791 Hz plausible), loud
   release clack, desk thud. Misfit: punch strokes usually produce a duller "chunk" with less high-frequency chatter;
   the bottom-out thud would normally coincide with the click, not lag it by 25 ms.
3. **"Typing on a keyboard" / "pressing two keys on a mechanical keyboard."** Fit: each keystroke = switch click
   (crunchy tactile/click jacket, 5 to 10 ms) then bottom-out through the finger pad 10 to 25 ms later (soft pulse),
   desk thud if the recorder is on the desk; two keystrokes 133 ms apart is fast typing; steel mounting plate can ring
   near 800 Hz. Misfit: only two strokes, B and C differ in shape (press vs snap), and D/A are odd for typing.
4. **"Dropping something flat on the table" (phone, remote, book, box lid, chopping board).** Fit: A = first corner
   touch, B = edge landing that rolls onto a face (crescendo, then air-cushioned slap = delayed soft thud), C = second
   bounce/other end landing flat, D = final settle; wooden board or hard-plastic housing supplies the 791 Hz and the
   1 to 3 kHz comb; table supplies 62 Hz. Misfit: second landing louder than the first; 791 Hz only in the second.
5. **"Putting a wooden chopping board down on the bench."** Fit: hardwood board modes at ~470 and ~790 Hz with Q ~
   100, rocking board gives two clacks 133 ms apart, bench thud. Misfit: a board's landing clicks are usually single
   clean impacts, not 13 ms of chatter.
6. **"Snapping the lid onto a plastic container" / "pushing a lid down on a glass dish."** Fit: each press on a
   corner of the lid is a crunchy multi-contact snap followed by the hand's force thumping the bench; two presses 133
   ms apart; a glass dish damped by the lid/hand could ring at 791 Hz. Misfit: pure plastic containers cannot ring
   with Q 120; the second press should not be so much louder.
7. **"Closing a ring binder" / "snapping the rings of a ring binder shut."** Fit: trigger click (A), rings snapping
   (loud crunchy steel clacks with ~800 Hz ring and multi-part chatter), board of the binder thudding, two-stage as the
   rings seat then the covers drop. Misfit: binder rings usually ring brighter (1 to 2 kHz) and the 62 Hz thud needs
   a desk.
8. **"Pressing a toaster lever down" / "toaster popping up."** Fit: latch click then carriage/body thud; spring
   release clack with metal body ring. Misfit: usually a single stage per action and a longer, brighter metallic ring.
9. **"Flicking a light switch" (two rockers in one swipe).** Fit: snap-action clicks, finger follow-through pushes
   the wall plate (plasterboard panels have modes near 60 Hz), two clicks 133 ms apart. Misfit: a plastic rocker has
   no Q-120 part at 791 Hz; switch clicks are shorter and cleaner than 13 ms.
10. **"Using a pump soap dispenser" (press and release).** Fit: press = plastic crunch, bottle thumps the bench under
    the hand, release = spring clack. Misfit: usually a squelch/liquid noise and a weaker, duller release.
11. **"Clicking a computer mouse" / "double-clicking."** Fit: two clicks 133 ms apart, desk-coupled recorder. Misfit:
    microswitch clicks are 1 to 3 ms clean events, no 25 ms-delayed thud, no 791 Hz ring.
12. **"Opening/closing a clipboard clip."** Fit: lever press (click) then spring snap (loud clack) 100 to 200 ms apart,
    board resonates (low mode) and steel clip rings ~800 Hz. Misfit: board modes would be above 62 Hz unless the board
    is on a desk; press stage is quieter than measured.
13. **"Clicking a pen" (press and release).** Fit: two-stage click 100 to 200 ms apart, crunchy plastic mechanism.
    Misfit: tiny object, no thud, pen rings above 1.5 kHz; only fits if the pen is pressed hard against a desk.
14. **"Clipping your nails" / "nail clippers."** Fit: cut click (sharp) then lever release clack ~100 ms later with
    metal ring. Misfit: no desk thud unless hands rest on a table; nail cut is a single ~2 ms click.
15. **"Knocking on a door" (two knocks) / "a door knocker."** Fit: hollow door has a ~60 Hz first mode and 170 to 210 Hz
    modes, two hits 133 ms apart, metal knocker rings. Misfit: a knock's force and click are simultaneous (no 25 ms
    delay), knuckle clicks are short and dull, and a double knock at 133 ms is very fast.
16. **"Closing a cupboard door" (two doors) / "closing a drawer."** Fit: latch click then panel thud, large damped
    surface. Misfit: two doors 133 ms apart needs two hands; the clicks are brighter than a cupboard catch.
17. **"Putting down a glass / a jar on the bench."** Fit: held glass damped to Q ~ 100 at 791 Hz, bench thud,
    rocking gives two contacts. Misfit: glass contact clicks are cleaner and higher; 791 Hz would appear in both.
18. **"Taking a photo with a camera" (DSLR mirror/shutter).** Fit: multi-stage mechanical sequence of ~100 ms with a
    precursor click. Misfit: all stages 50 to 100 ms apart with body modes in the hundreds of Hz, not 62 Hz; no
    desk-type thud; shutter sequences are three or four clean clicks.
19. **"Rolling dice on a table."** Fit: several clicks at ~100 ms spacing, chattering contacts. Misfit: dice are too
    light to thump a table at this level; no soft delayed pulse; no 791 Hz ring.
20. **"Closing a wheelie bin lid" / "closing a plastic bin lid."** Fit: clack then slam-thud with bounce. Misfit: not
    close-miked/dry, no 791 Hz with Q 120, bounces are quieter.

## 4. Measurements that would separate the top candidates

Record each candidate with the same phone in two conditions: phone lying on the same table/bench as the object, and
phone held 30 cm away in the air. Then compare on these five measurements (scripts in `analysis/mnc/fable_fresh/`
can be run on any 48 kHz mono WAV by changing the path):

1. **Thud delay and shape.** Plot the <250 Hz waveform against the >2 kHz envelope. The target shows the big low swing
   starting 15 ms after the click and peaking at 22 to 30 ms, with a growing-then-decaying 62 Hz oscillation (first
   cycle ~86 Hz). Stapler/punch/keyboard/lid-press (hand follow-through) and flat-landing objects should reproduce a
   delayed, soft pulse; knocks, switches, mouse clicks and door knockers will show the thud coincident with the click
   or absent. If the thud disappears when the phone is lifted off the table, the 62 Hz is the table and the recorder
   was on it (favours desk actions and dropped objects; disfavours doors/walls/bins).
2. **791 Hz ring Q and which stage excites it.** Narrow-band (771 to 811 Hz) envelope: target has T60 0.33 s, excited
   at the start of the second event and re-excited ~25 ms later, 20 dB weaker after the first event. Tap-test the
   candidate's parts (stapler arm, punch lever, keyboard plate, binder rings, board, dish): the ringing part should
   give 790 ± 30 Hz with T60 0.25 to 0.45 s while in its working position (bolted/held/resting). A stapler or punch
   must show this ring on the release stroke and not on the press stroke.
3. **Internal texture of the clicks.** >2 kHz, 0.2 ms envelope: target B is a 13 ms crescendo of ~1 ms grains ending
   in its loudest grain, C is an abrupt 2 ms onset with 13 ms of decaying chatter. Press-then-release mechanisms
   should show exactly this asymmetry (press = crescendo crunch, release = abrupt snap); a bouncing object should show
   abrupt onsets for both; a keyboard shows two similar onsets.
4. **Mode comb after each stage.** 1/3-octave spectra of 0.13 to 0.24 s after each event: target has the same comb
   (1125, 1300, 1700, 1850, 2035, 2570, 3190 Hz; T60 0.11 to 0.19 s) after both events. A candidate must have the same
   body struck both times; two different objects (two dice, two doors) will give different combs.
5. **Inter-event timing and level ratio.** Target: B→C 133 ms with C 3 dB louder and A 54 ms before B at -10 dB,
   D 95 ms after C at -37 dB. For a mechanism the 133 ms will vary with the user's speed between takes (any 80 to
   250 ms is fine, but the order "quieter crunch, then louder snap" must hold); for a bounce the interval sequence must
   shrink geometrically and the second impact is normally quieter, so a candidate that only reproduces the timing by
   bouncing is suspect.

Secondary checks: dryness (4 to 8 kHz down 20 dB within ~5 ms of each click) confirms the mic distance; absence of
any sustained noise between 0.13 and 0.24 s (target's >2 kHz level there is -40 to -50 dB, i.e. silence apart from
the ringing) rules out anything that scrapes, slides or hisses between the two stages.
