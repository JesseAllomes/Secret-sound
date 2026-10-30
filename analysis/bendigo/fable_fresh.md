# Bendigo Secret Sound (Cogho & Jules, Triple M Bendigo): fresh measurement-based analysis

Date: 30 Oct 2026. Source: `clues/bendigo/clue_b.wav` (decode of `bendigo_secret_sound_210926.mp3`, the station's
0.273 s clip). Scripts and figures: `analysis/bendigo/fable_fresh/` (`s1_basic.py` to `s9_hits.py`, `fig_*.png`).
No audio was listened to; everything below is measured. Confidence tags: **H** (robust across methods), **M** (one
method, or near resolution limits), **L** (suggestive).

## 0. File facts

| Item | Value | Conf |
|---|---|---|
| Length | 12 032 samples at 44.1 kHz = 272.8 ms; dual mono (L and R identical) | H |
| Level | peak -20.3 dBFS, RMS -36 dBFS, no clipping, no DC | H |
| Encoding | LAME mp3 at ~154 kb/s, 16 kHz low-pass (nothing above 16.5 kHz); content 8-16 kHz survives | H |
| Start | sample 1 is already mid-waveform (no fade-in); the envelope at t = 0 is -36 dBFS with the low band (40-300 Hz) at its maximum for the whole clip, so the clip opens inside the low thump of a strike that happened a few ms before the cut | H |
| End | the last 5 ms are at -43 dBFS and still carry the 2.3/2.55 kHz ring; nothing resembles a natural end | H |
| `bendigo_secret_sound_x4.mp3` | just the same clip repeated four times with silence between (a listening aid); not used | H |

## 1. What the sound is, by measurement

### 1.1 Events and rhythm (fig_time.png, fig_zoom.png)

Full-band envelope onsets (a > 9 dB jump within 1.5 ms, high-passed at 1.5 kHz, plus the broadband envelope):

| Hit | Onset (ms) | Peak (dBFS) | 10-90 % rise (ms) | Chatter sub-impacts inside the hit (ms after onset) |
|---|---|---|---|---|
| pre-0 | < 0 (cut off) | >= -27 at t = 0 | - | - |
| E1 | 14.6 | -20.9 | 0.95 | +13, +15, +20, +22 (HF clicks at 30.0 and 36.9 ms) |
| E2 | 92.4 | -22.1 | 0.73 | +1, +4, +6, +8, +11, +13 |
| E3 | 145.7 | -25.6 | 2.4 | +1, +5, +11, +17 |
| E4 | 212.7 | -29.8 | 3.7 | +6, +10 |
| E5 | 258.6 | -30.6 | 0.79 | +4 |

- Five strike clusters inside the 273 ms window, plus at least one heavier strike just before the cut. **H**
- Intervals between main onsets: **77.8, 53.3, 67.0, 45.9 ms** (12.9, 18.8, 14.9, 21.8 per second). The pattern is
  long-short-long-short, with both the long and the short interval shrinking by about 14 % per cycle. Two-hit cycle
  length 131 ms then 113 ms (7.6 then 8.8 cycles/s). **H** for the timings, **M** for calling it an alternation (only
  two cycles are visible).
- Loudness falls monotonically after E1: -21, -22, -26, -30, -31 dBFS, i.e. about 10 dB over 250 ms. **H**
- Each main hit is not one clean impact but a cluster of 2-6 sub-impacts spread over 5-15 ms with shrinking gaps
  (e.g. E2: 6.8, 2.5 ms), i.e. a bouncing/chattering contact. **H** (visible in the waveform, the 6-15 kHz impulse
  track and the 73 Hz amplitude modulation of the ring band in E1/E2).
- Within E1 (0-60 ms) the 300-700 Hz band pulses every 10-12 ms (at 1.5, 11.6, 22.5, 36.9, 46.1, 56.0 ms): a rattle at
  ~90 Hz rides on the first, heavy strike. **M**
- The envelope autocorrelation has no strong periodic peak beyond 3 ms (r = 0.36 at 13.9 ms, 0.18 at 24.5 ms): the
  rhythm is not machine-regular. **H**

### 1.2 Tonal / resonant components (fig_spectrum.png, fig_spec_tonal.png, s5/s7 outputs)

Every hit re-excites the same set of lines; the lines do not move by more than ~1 % between hits, so one fixed
resonator (or a fixed pair) is being struck repeatedly. **H**

| Line (Hz) | Level rel. strongest (dB), per-hit tail | T60 (ms) / Q (narrow-band fits) | Notes | Conf |
|---|---|---|---|---|
| **2318-2330** | -8 (E1), -5 (E2), -3 (E3), **0 (E4)**, -5 (E5) | 80-200 / 90-210 | second principal line; dominates the last two hits | H |
| **2548-2580** | **0 (E1, E2, E3)**, -7 (E4), absent (E5) | 80-250 / 90-290 (longer, ~1 s, in the quiet gaps where only this line is left) | principal line; instantaneous frequency 2560-2580, drifting +10 Hz from E1 to E2 | H |
| 2450-2460, 2613-2640 | -17 to -21 | ~100 / 110-150 | satellites of the pair | M |
| 2744, 2820 | -9 to -20 | 70-180 | | M |
| 3085-3130 | -10 to -14 | 120 | | M |
| 3620-3760 | -3 to -13 | 100-280 | cluster | H |
| 3935-4005 | -5 to -12 | 100-150 | | H |
| 4155-4245 | -3 to -12 | 110-210 | | H |
| 4335-4440 | -3 to -18 | 65-220 | | M |
| 4890-5050 | -10 to -16 | 65-150 | | M |
| 6490-6570, 7510-7530 | -15 to -20 | 70-140 | | M |
| 11 600 (weak) | -30 | - | | L |

- Spectral energy: 2-3 kHz holds the most (-3.5 dB rel. total), 3-5 kHz -6 dB, 5-8 kHz -12 dB, 8-12 kHz -22 dB. **H**
- Modal density: 6-8 lines within 14 dB of the strongest below 5 kHz, dozens of weaker ones; this is a moderately
  rich spectrum, richer than a single thick-walled cup but far sparser than a cymbal or a bunch of keys. **M**
- Decay: T60 of the principal lines is **80-250 ms** (Q 100-300). Free-ringing brass, bronze, glass or a bell would
  be 1-5 s; the resonator is therefore damped: hand-held, coated (enamel, paint), clamped, resting on something, or
  thin tinplate with a seam. **H**
- The ring is also cut short before each next hit (the 2.57 kHz line falls 25-30 dB in the 50 ms between E2 and E3
  but only ~10 dB per 50 ms when left alone at 180-250 ms): the next contact, or the hand, chokes it. **M**
- Which of the two principal lines wins changes with the hit (2.55 kHz for E1-E3, 2.32 kHz for E4-E5). Either the
  strike point moves around one object with a split degenerate mode pair, or two similar objects are struck in turn.
  The 2.32/2.55 split is 9.5 %: too wide for a near-symmetric dome or bell (typically < 3 %), right for an object with
  a deliberate asymmetry (a handle, a slot, a mounting lug) or for two nominally-identical objects. **M**

### 1.3 Low-frequency content (fig_bands.png, s6/s9 outputs)

- 40-120 Hz: a **60-90 Hz thump** (lines at 64 and 79-86 Hz, period 13-18 ms) peaks at t = 0 and decays with T60
  ~120-250 ms; it is at -29 dBFS at the cut and 14 dB below the 2-5 kHz band at the E1 onset. On E2-E5 it is 11-16 dB
  below the ring (E4 -2 dB, but E4 is quiet). So: the strike before the cut was heavy and excited something low
  (table, floor, a body cavity, the player's thigh), later strikes did not. **H**
- 120-300 Hz: 133, 181-205, 235-254 Hz, again strongest at t = 0 and at 12 and 26 ms. **M**
- 300-700 Hz: **342, 408-427, 477-491, 595-608 Hz** ring only after the first strike (481 Hz is the strongest line
  in the 18-88 ms tail below 1.5 kHz, with a long decay); they are 16 dB below the ring on E2/E3. A lower mode of
  the struck object (a bottom plate, a cavity, a rim mode) that only a hard, central or bottom contact excites. **H**

### 1.4 Noise and impact character

- No continuous component: between hits the floor is -43 to -45 dBFS (22-25 dB below the hits) and it is dominated by
  the dying ring, not by hiss, motor, gear, friction or air noise; spectral flatness stays < 0.01 everywhere. **H**
- The impacts are not bright. In the first 2.5 ms of each hit the 6-15 kHz band is 7-16 dB below 2-5 kHz; a small
  hard point contact (steel ball, coin edge, glass marble) would put them within a few dB. Contact is either broad
  (curved metal on metal, a flat pawl on a tooth, a clapper), or one side is softer (wood, plastic, finger, glazed
  ceramic). **M** (mp3 keeps this band, so it is not an encoding artefact.)
- Rise times of 0.7-1 ms on the clean hits are metallic-fast; E3/E4 (2.4/3.7 ms) are slurred by their chatter. **M**

### 1.5 What the trimming hides

- Before 0: at least one strike, heavier than any in the clip (it owns the 60-90 Hz thump and the 480 Hz group), no
  more than ~20 ms before the cut (the thump is still at its peak). If the long-short pattern holds backwards, there
  may be a strike near -60 to -80 ms as well, but there is no evidence either way. We cannot know whether the sound
  started with this heavy strike (an object landing, a hand grabbing) or whether the clip is from the middle of a run.
- After 273 ms: E5 is only 14 ms old at the cut. Extrapolating the shrinking intervals (next gap ~58 ms) and the
  10 dB/250 ms fade, the sound probably carries on for 1-3 more hits and dies within ~300 ms, or the action repeats.
  The station's clip is therefore a 0.27 s excerpt of something that lasted perhaps 0.5-1 s.

## 2. Physics: what can make exactly this

### 2.1 The resonator

- Principal modes at 2.3 and 2.55 kHz with a rich set to 7.5 kHz and T60 0.1-0.25 s. For a thin plate/shell of
  steel, tinplate, brass or aluminium the lowest flexural mode at ~2.3 kHz means roughly: a free disc 40-60 mm across
  at 0.5-1 mm thick; a dome/cup/bell 40-70 mm across in 0.5-1 mm steel; a spoon bowl; a tin can 70-100 mm in 0.2-0.3
  mm tinplate (n = 2-4 ring modes); a 20-40 cm tube or rod in its higher modes. For glazed stoneware a mug/cup of
  80-100 mm gives (2,0) at 2-3 kHz with (3,0) at 4-5 kHz, which also fits the 2.3/2.55 + 3.6-4.4 + 7.5 kHz layout.
- The 9.5 % split of the principal pair is the most specific fact: it wants either an asymmetric body (handle,
  slot, screw boss, cut-out, two welded halves) or two similar bodies. A mug with a handle, a bell with a clapper
  boss and thumb lever, a cowbell, a pair of spoons, a pair of alarm-clock bells, a tin with a seam and a lid all
  qualify. A plain coin, washer, bottle cap or ball bearing does not: their own modes are 6-20 kHz and they would
  ring bright, not at 2.3 kHz.
- The damping (Q 100-300) says the resonator is touched: held in a hand, resting on a knee, clamped to a frame,
  enamelled or painted, or pressed against another part. A free brass hand bell, wine glass, tuning fork or a loose
  coin on a hard floor is ruled out (Q would be thousands).

### 2.2 The striker and the drive

- Each hit is a bouncing contact that settles in 5-15 ms: something loose or springy (a pawl snapping onto a tooth, a
  clapper, a second spoon, dice, a key, a lid), not a rigidly guided hammer or a solenoid.
- Hit rate 13-22/s, uneven, with long-short alternation and both intervals shrinking: a hand-driven cycle with two
  contacts per cycle (to-and-fro: knee/hand, two walls, two bells, two stops; or a half-turn push/pull of a crank)
  that is speeding up slightly while the strikes get lighter. A free-running mechanism (motor, governor, spinning
  rotor at constant speed, clock escapement) would be even; a pure bounce-to-rest sequence would be strictly
  geometric (ratios ~0.7-0.8 every gap) with no alternation; a ratchet turned by hand gives exactly this kind of
  wobble but no reason to fade unless the hand is easing off.
- The heavy first strike with a 60-90 Hz thump and extra 340-600 Hz modes is a different contact from the rest:
  harder, more central, or against a second body (table, floor, thigh, the bottom of a container). It is what you
  get when the action starts (an object landed, a key engaged, the first stroke on the knee) rather than a steady state.
- No motor, gear, spring-wind, air or friction noise at all: whatever drives it is quiet between hits. Hand-driven.

### 2.3 Ruled out or disfavoured by the measurements

- Anything continuous or whirring (whipper snipper, motorbike, sewing machine running, hand drill, grinder, rotary
  dial governor, egg beater gears, fan): the floor between hits is clean. 
- Anything with high-Q free ringing (brass bell, glass, tuning fork, triangle, wind chime, typewriter bell on its
  own): T60 is only 0.1-0.25 s.
- Single-event mechanisms (latch, stapler, doorstop, flap, lid, pen click, mousetrap): there are 5+ similar hits.
- Small hard bright objects as the resonator (coins, marbles, ball bearings, bottle caps, jacks, keys as the
  ringing body): the ring is at 2.3 kHz with weak 8-15 kHz content.
- Wood, plastic, leather, cardboard, rubber as the resonator: no 2.3 kHz line with Q > 100.
- Regular machine rhythm (clock tick, metronome, escapement, constant-speed rotor): intervals vary 46-78 ms.

## 3. Reading the clues and the wrong-guess list

Clues: (1) "I'm a classic" (2) "I need a hand" (3) "I'm old school". Station clues are usually puns on the answer.
"Hand" can mean: done by hand / hand-held / hand-cranked / hand-wound; has a handle; has hands (a clock); a hand of
cards; "give me a hand" (applause, or help). "Classic" and "old school" both say vintage, and "old school" may also be
literal school (bell, chalk, desk, ruler, pencil case).

What callers hear (42 rejections, grouped by what they share):
- Rapid metallic clatter/ratchet: dragging a stick along a fence, finger along a shutter blind, flipping a ruler,
  clock ticking, hills hoist winder, handbrake ratchet, sewing-machine pedal, gumball machine, spinning top,
  twisting doorbell, pinball flippers. These confirm a 10-25 Hz metallic repetition.
- Something dropped into a container and chattering: coin into jar / collection box / parking meter, pen into tin,
  spoon into cup, tin lid into can, coins from a machine, air-hockey puck into slot. These confirm "small metal
  object + ringing container + chatter". Five variants of "drop X into metal/ceramic Y" are now rejected, so that
  whole family is weakened (but only the exact actions are out).
- Spring-loaded clunks and bangs: doorstop, gate latch, gates, letterbox flap, fuel flap, saucepan lid, hammer on
  pole, sledgehammer on star picket, card imprinter. Suggests the first (heavy) strike is prominent on air.
- Games and toys: Trouble (pop-o-matic), Hands Down, spinning top, pinball, gumball, air hockey.

Notable absences from the list given the clues: playing the spoons; winding an alarm clock, a tin toy or a music box;
a bicycle bell; a cowbell / cheap steel hand bell; stirring or tapping a teaspoon in a mug; dice in a cup; a ratchet
spanner; a fishing-reel clicker; a rotary phone dial; a typewriter carriage return; handcuffs; a Morse key.

## 4. Ranked candidates (phrased as a caller would)

Scores: measurements (M) and clues (C) out of 5. "List" says whether the exact action or a near version is rejected.

| # | Caller's phrase | M | C | Why it fits / fails | List |
|---|---|---|---|---|---|
| 1 | **Playing the spoons** (two spoons slapped between knee and hand) | 5 | 4 | Two near-identical steel bowls ring at 2-5 kHz, hand-damped (Q 100-300); knee stroke heavy with a thigh thud (60-90 Hz), hand stroke light: long-short alternation; the two spoons chatter against each other inside each hit; a flourish that fades; which spoon's line dominates changes with the stroke. "Needs a hand", classic, old school (bush band). | not on list |
| 2 | **Winding up an old wind-up alarm clock** (key ratchet) | 4 | 5 | Pawl clicks at 10-25/s with the push/pull halves of each turn giving long-short gaps; each click bounces; the two steel bells on top (two slightly different domes: 2.32 and 2.55 kHz) and the tin case ring; picking the clock up gives the thump. Fails on the fade (winding clicks do not get quieter unless the hand eases). Clock has hands; classic; old school; "clock ticking" rejected shows clocks are in callers' minds. | near: clock ticking (different action) |
| 3 | **Stirring / tapping a teaspoon in a china or enamel mug** | 5 | 3 | Mug (2,0) pair split by the handle (9 % split is typical), (3,0) at 4-5 kHz, glazed-ceramic damping, dull impacts (weak 8-15 kHz), spoon taps twice per stir cycle (long-short), first tap on the bottom goes to the table (thump + 480 Hz). "Needs a hand(le)"; a classic cuppa. | near: dropping a spoon into a cup (rejected) |
| 4 | **Ringing a cowbell / shaking a small steel hand bell** (clapper type) | 4 | 4 | One shake: clapper swings back and forth hitting both sides, hits alternate and fade, pressed-steel bell has low Q and a dense spectrum, hand on the handle. A brass school bell is out on Q, a cheap steel/tin one is in. Hand bell, old school bell, "more cowbell" classic. | not on list |
| 5 | **Winding up a tin wind-up toy / a jack-in-the-box / a music box** | 4 | 4 | Hand-turned key ratchet, uneven, tin body rings with many modes, key bounce = chatter. Fade unexplained. Classic old-school toy, needs a hand. | not on list |
| 6 | **Ringing a bike bell** (thumb-flick rotary "ring-ring") | 3 | 5 | Steel dome at 2-4 kHz, two pivoting hammers bounce on the dome, lever thump at the start. Fails on rate (a brrring is 30-60 hits/s, ours 13-22) and on fading while speeding up. Classic, old school, needs a thumb. | not on list (surprising if it sounded like one) |
| 7 | **Clicking a ratchet spanner / socket wrench backwards** | 4 | 3 | Pawl clicks 15-40/s following the hand, each click bounces, steel handle/socket ring 2-5 kHz. Fade unexplained. Hand tool; classic/old school weak. | near: handbrake ratchet, hills hoist (rejected) |
| 8 | **Shaking dice in a cup** (tin, enamel or china cup) | 4 | 4 | Two wall hits per shake (long-short), several dice chatter, plastic dice give dull impacts, cup rings. Needs the cup to be metal/ceramic. Classic game, needs a hand; Trouble and Hands Down rejected show callers think games. | near: Trouble game (different) |
| 9 | **Dropping keys / a bottle top / a spoon into a tin and letting it rattle** | 4 | 2 | Bottom thump first then wall-to-wall bounces that fade: the best fit for the fade. Clues weak; five siblings rejected. | near: pen into tin, spoon into cup, tin lid into can, coin into jar/box (all rejected) |
| 10 | **Winding an Alvey / old fishing reel** (clicker) | 3 | 4 | Ratchet clicker on a hand crank, metal spool rings. Fade unexplained. Alvey is an Aussie classic, needs a hand, old school. | not on list |
| 11 | **Spinning a coin or a jar lid on a metal tray / tin** and it settling | 3 | 2 | Rattle that speeds up and fades fits; needs a ringing surface, and no alternation is expected. Spinning top rejected. | near: spinning top |
| 12 | **Closing handcuffs** (ratchet) | 3 | 3 | 15-25 clicks/s steel ratchet with bounce and a ringing cuff. "I need a hand" pun. Not an everyday action. | not on list |
| 13 | **Dialling a rotary phone** | 2 | 5 | Finger-wind clicks at 10-20/s in some dials; but the return has a governor whirr and 10 pps pulses (no whirr here). Classic, old school, needs a finger; two phone guesses rejected. | near: hanging up pay phone, phone address book |
| 14 | **Tapping a Morse key** | 2 | 4 | Contact clicks at 10-20/s with bounce; base usually wood/bakelite (low Q), fade unexplained. Hand key, classic, old school. | not on list |
| 15 | **Shaking a spray can / tin of paint** (ball bearing inside) | 3 | 1 | Two hits per shake, thin steel can rings with dense modes; steel ball impacts should be brighter than measured. | near: can opener (different) |
| 16 | **Winding down an old car window** (manual winder) | 2 | 4 | Classic car, old school, hand crank; but the sound is a grind/whirr, not discrete rings. | not on list |
| 17 | **Typewriter carriage return** (with the bell) | 2 | 4 | Return zip is 50-100 clicks/s and the bell rings for a second; our rate is slower and ring shorter. | near: pressing typewriter (rejected) |
| 18 | **Hand-crank egg beater in a metal bowl** | 2 | 4 | Beaters tick the bowl, bowl rings; but gears give continuous noise which is absent. | not on list |
| 19 | **Shaking a sleigh / jingle bell** | 3 | 2 | Loose ball in a steel shell, chaotic 10-40 hits/s, dense shimmering spectrum, hand-damped. Clues weak (not Christmas). | not on list |
| 20 | **Card in the spokes of a bike wheel** | 2 | 3 | Periodic slaps 20-40/s, too regular; spokes ping but the card is dull. "A hand of cards" pun, classic trick. | not on list |
| 21 | **Playing knucklebones / jacks** | 1 | 4 | Hand game, classic, old school; but jacks ring at 5-10 kHz and the ball thud is soft. | not on list |
| 22 | **Marbles in a tin** | 2 | 3 | Tin rings; marble clicks are bright glass, measured impacts are dull. | not on list |
| 23 | **Cranking an old cash register / adding machine** | 2 | 3 | Mechanism clatter plus a bell; rhythm would be mechanical. | near: card imprinter |
| 24 | **Hand-crank pencil sharpener** | 1 | 4 | Grinding, continuous; no. | not on list |
| 25 | **Clicking a tin frog clicker** | 2 | 3 | Two clicks per press, thin tin rings; a fast run of presses could give 10-20/s with alternation. Old-school tin toy. | not on list |

Bottom line: the measurements favour a hand-driven two-stroke action on a damped, hand-held metal (or glazed ceramic)
resonator with a built-in asymmetry, starting with one heavier contact and fading. The three best joint fits are the
spoons, winding an old alarm clock, and a teaspoon in a mug. The uncut on-air version (does it begin with the heavy
strike? does it fade out or keep going? how many hits?) would separate them.

## 5. Sound-library search terms (1-2 words each) and what a match must show

Terms: `spoons`, `playing spoons`, `bones percussion`, `alarm clock`, `clock winding`, `wind-up`, `ratchet click`,
`tin toy`, `music box`, `jack-in-the-box`, `bike bell`, `bicycle bell`, `cowbell`, `hand bell`, `tin bell`,
`teaspoon mug`, `stir tea`, `cup clink`, `enamel mug`, `dice cup`, `dice shake`, `keys tin`, `coin tin`,
`coin spin`, `lid spin`, `metal tray`, `spray can`, `can shake`, `socket wrench`, `ratchet spanner`,
`fishing reel`, `reel click`, `handcuffs`, `rotary dial`, `telephone dial`, `morse key`, `typewriter return`,
`typewriter bell`, `egg beater`, `window winder`, `jingle bell`, `sleigh bell`, `bike spokes`, `knucklebones`,
`jacks game`, `marbles tin`, `cash register`, `clicker toy`, `bottle cap`, `pawl`.

A matching recording must show (measure the candidate with the same scripts):
1. Discrete hit clusters at 13-22 per second with uneven, preferably long-short, gaps, and a clean floor (> 20 dB
   down) between them; no whirr or hiss.
2. Each hit followed by 2-6 chatter sub-impacts inside 5-15 ms.
3. A fixed set of ring lines re-excited by every hit, with two principal lines 8-12 % apart in the 2-3 kHz region
   (absolute values may scale +-20 % for a different specimen) and a cluster at 1.5-1.8x that, with T60 0.08-0.25 s.
4. Weak high band: 6-15 kHz at least 7 dB below 2-5 kHz in the first 2.5 ms of a hit.
5. One heavier hit at the start with a 60-90 Hz thump and extra 300-600 Hz modes, then lighter hits that fade ~10 dB
   over 250 ms.
6. Loudness alternating with the principal line (which of the two lines dominates should change between hits).

## 6. Figures and scripts

- `fig_time.png`: waveform, envelopes (full and > 1.5 kHz), dB/ms slope, < 300 Hz band.
- `fig_spec_fine.png` (n = 512, to 16 kHz) and `fig_spec_tonal.png` (n = 2048, to 8 kHz): spectrograms.
- `fig_spectrum.png`: whole-clip spectrum. `fig_bands.png`: five band-passed waveforms. `fig_zoom.png`: the three
  main hits with the 6-15.5 kHz impulse track overlaid.
- `s1_basic.py` file facts; `s2_time.py` envelopes/onsets/autocorrelation; `s3_spec.py` spectrograms and peaks;
  `s4_events.py` refined onsets and per-event spectra; `s5_decay.py` T60/Q per line per hit; `s6_lf_noise.py` low
  bands, flatness, HF impulses; `s7_modes_hires.py` high-resolution lines per tail; `s8_micro.py` chatter, AM,
  phase continuity; `s9_hits.py` per-hit hardness and line ratios. Outputs in the matching `*.out` files.
