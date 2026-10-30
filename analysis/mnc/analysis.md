# Sarge's Secret Sound (Triple M Mid North Coast, round at $2,800) - acoustic analysis

Source material: `clue.wav` (48 kHz mono, user crop 0-0.631 s) plus 12 further plays of the same
sound located by normalised cross-correlation in the three podcast episodes and the on-air clip
(ep0 511.98 / 519.60 / 1345.74 s; ep1 497.19 / 1077.50 / 1250.20 / 1260.62 s; ep2 557.61 / 571.19 /
1153.45 / 1162.85 s; on-air 6.98 / 14.60 s; NCC 0.81-1.00). All plays are the same recording through
slightly different processing; figures below are medians over the four cleanest plays
(clue, ep1 1260.62, ep2 571.19, on-air 14.60) unless stated. Scripts `a1..a7_*.py`, plots `*.png`
in this folder (clue_overview, clue_spectrogram, stack_*, modes_*, zoom_*).

## 1. Measured facts

### Framing
- The effect begins at crop t = 0: the noise floor steps from -46 dB (station silence) to -42 dB and
  a faint 3-8 kHz hiss rises to about -32 dB by 55 ms (handling/friction before the first click).
- The sound is over by ~390 ms. Speech starts at ~640 ms in the clue; the 400-620 ms tail of the clue
  is station noise (hum lines 111/220/407/661 Hz are also present in the silence before the sound in
  other plays), not part of the effect.
- No room reverb: after the last event the level falls from 0 to -40 dB in 113 ms and that decay is
  the object's own 790 Hz ring, not a diffuse tail. Close-miked, dry recording (studio/foley style).

### Event structure (0 dB = loudest peak, event C)
| Event | HF onset | Peak | Level | 10-90 % rise | Decay to -20 / -40 dB | Character |
|---|---|---|---|---|---|---|
| A | 58.7 ms | 63.7 ms | -9 dB | 4.8 ms | 8 ms / (buried) | dry click, two sub-clicks 59.8 + 63.7 ms, tiny 3rd at 83 ms (-20 dB) |
| B | 108-111 ms | 117-124 ms | -1 dB | 12.8 ms | 55 ms / >90 ms | broadband "crunch": micro-impacts at 117, 135, 139, 152, 165 ms |
| C | 246-248 ms | 256 ms | 0 dB | 8.4 ms | 11 ms / 113 ms | single clean snap + metallic ring; secondary ticks at 270, 281 ms |

Spacing: A->B 47 ms, B->C 137 ms (onset 110 -> 248 ms; peak 123 -> 256 ms). The B->C gap is the same
in every play (sample-exact), so it is in the effect, not an edit.

### Low-frequency thump lags the click in both big events
Zero-phase band envelopes (40-200 Hz vs 2-8 kHz), medians over 6 plays:
- B: HF onset 111 ms, LF onset 132 ms, LF peak 155 ms -> LF starts 21 ms after the click, peaks 37 ms after.
- C: HF onset 248 ms, LF onset 275 ms, LF peak 285 ms -> LF starts 27 ms after the click, peaks 37 ms after.
- A has no LF at all (40-200 Hz band -24 dB below C's LF).
The LF is a damped oscillation at 62 Hz (zero-crossing periods 15-17 ms; ~80 Hz at the start of B
settling to 62 Hz), T60 ~0.2-0.3 s, Q ~ 6-13. The same 62 Hz follows both B and C. In the clue crop
the 20-150 Hz band holds 35 % of the energy (broadcast median is 3-5 dB less bassy, so part of that
is processing, but the lag and the 62 Hz mode are in every play).

### Spectral content
- A: centroid 4.0 kHz, 55 % of energy above 4 kHz, 2 % above 8 kHz; peaks 5.5-6 kHz and 1.36 kHz;
  noise-like click. HPSS harmonic/percussive ratio 0.28.
- B body (112-135 ms): peaks 1025, 1151, 1837 Hz (0 to -3 dB), 432 Hz (-7), 2.9-4.9 kHz (-10 to -14);
  energy to 12 kHz. HPSS 0.39 (percussive). 400-1000 and 1-2.5 kHz bands peak at 123 ms.
- B ring (130-240 ms): 63 Hz dominant, 92 and 164 Hz (-12, -18 dB); 790 Hz only -26 dB (weakly excited).
- C body (246-262 ms): 773 Hz (0 dB), 1296 (-7), 1687 (-6), 2915 (-14). Onset order: 8-15 kHz first
  (246 ms), 2-8 kHz (247.6), 400-1500 Hz (251): a ~4 ms high-frequency slip/scrape just before the
  mid-frequency snap. HPSS 1.55.
- C ring (262-390 ms): 62 Hz (0 dB) and a narrow line at 790-792 Hz (-7 dB) with T60 ~ 330 ms,
  Q ~ 120 (visible for >130 ms); 773/1296/1687 are not a harmonic series (ratios 1.68, 2.18) ->
  bending modes of a solid part, not a cavity or string. Autocorrelation of the ring: 787 Hz,
  r = 0.67. HPSS 26.
- Energy shares, clue 0-700 ms: 20-150 Hz 35 %, 150-400 9 %, 400-1000 21 %, 1-2.5 k 22 %,
  2.5-5 k 4 %, 5-9 k 3 %, 9-16 k 0.5 %. Nothing above 16 kHz (broadcast/podcast low-pass).

### Noise vs tonal, air, friction
- Only pitched component: the 790 Hz ring after C (faintly after B). No sustained tone, no Helmholtz
  "pop" tone, no harmonic series.
- No air/whoosh/suction: between A and B the envelope drops to -30 dB; after C there is no hiss; the
  only friction-like noise is the faint -32 dB rise in the 55 ms before A.
- All events are percussive with sub-13 ms rise times; nothing sweeps in frequency over tens of ms.

## 2. What the physics implies

**Two strokes of one spring mechanism, 137 ms apart.** B and C are equal in level (-1 vs 0 dB); each
is a sharp click followed 21-27 ms later by a heavier low-frequency seating thump. That is the
signature of a lever/plunger/latch being driven to an end-stop: the catch releases (click), the moving
part travels a few millimetres, then the mass lands (thump). Two such strokes 137 ms apart with
similar energy is a press-and-release (or over-centre open-then-close) action at a brisk human tempo.
Hand-timed separate actions (e.g. closing two latches) are usually >250 ms apart; a bounce would be
much weaker than the first hit. So the second stroke is powered by a spring, not by the hand.

**The release stroke rings metal; the press stroke does not.** C carries a 790 Hz mode with Q ~ 120
(T60 ~ 0.3 s). Moulded plastic has Q ~ 10-40 at that frequency (dies in <100 ms); Q ~ 100+ at 790 Hz
means a free steel/aluminium part (arm, plate, bolt, strip spring) a few to ten-odd cm long. In B the
same mode is 20 dB weaker: during the press the part is loaded by finger/paper and damped; on release
it springs free and rings. Typical of spring-return levers (stapler arm, stamp frame, door-handle
latch, binder ring plate); untypical of plastic push-buttons.

**B is a crunch, C is a snap.** B contains five micro-impacts over 50 ms (117-165 ms) with a broad
1-2 kHz plateau: something deforming or several parts seating in quick succession (staple legs
folding, paper being pierced, several rings/teeth closing, a rocker rattling home). C is one impact
with a 4 ms high-frequency slip immediately before it: a catch sliding off its lip, then letting go.

**The 62 Hz thump is a large panel, not the small object.** A damped 62 Hz oscillation with Q ~ 10
needs a panel the size of a desk top, door, cabinet side or appliance housing. The object is
therefore resting on, or fixed to, something big: a desk/bench (stapler, stamp, binder, clipboard),
a door (handle, bolt), or a wall/cabinet (switch). Its 20-27 ms lag behind the click shows the panel
is excited by the second, heavier phase of each stroke (the mass landing), not by the click itself.

**A is a pre-click, not a separate action.** Faint, high (4-6 kHz), no LF, 47 ms before B: first
contact or take-up of play as the finger starts the stroke (arm touching paper, latch clearing a
notch, toggle leaving its detent).

Ruled out or unlikely:
- Suction / pop / bottle / pill container: no cavity tone, no air noise, two equal strokes not one.
- Spray / pump / liquid: no hiss or fluid texture anywhere.
- Simple hinged lid closing: one impact, no spring-timed second stroke, no sustained metal ring.
- Sliding mechanism (tape measure, barrel bolt): no sustained friction right before the impacts.
- Single electrical snap switch (one toggle/rocker flick): one click+thump, not two equal strokes
  137 ms apart. A double flick or two switches in one sweep fits the timing (the BBC "several light
  switches" reference clip has two 0 dB clicks 135 ms apart), but a plastic rocker does not ring at
  790 Hz for 100+ ms.
- Multi-tooth detent / ratchet (shower nozzle, measuring cups): would give a train of similar
  clicks, not click-crunch-snap with a dominant final metal ring.
- Heavy impacts (door slam, car door): whole sound is 0.33 s and dry; the 62 Hz is only -7 dB in the
  broadcast median.
- Already-wrong family (microwave/toaster buttons, kettle lid, pen clip, tape recorder, hole punch):
  the hole punch is acoustically the nearest wrong guess; the real answer is probably its neighbour
  on a desk, not another kitchen-appliance button.

Best single description: a spring-loaded metal lever or latch pressed and released on or against a
large flat surface, dry close-miked (library/foley style), the whole action 0.33 s.

## 3. Ranked guesses (object + action), wrong guesses excluded

1. **A stapler stapling paper** - press: arm contact click (A), staple crunching through paper
   (B, five micro-impacts) with desk thump; release: steel arm springs up and clacks (C) ringing at
   790 Hz; 137 ms press-release. Nearest cousin of the wrong "hole punch". Confidence ~18 %.
2. **Pushing a door handle down and letting it go** - latch withdrawing (pre-click hiss, A), handle
   hitting its stop (B) with the door booming at 62 Hz; release: handle/latch snap back (C) with
   steel latch ring. ~13 %.
3. **Pressing a self-inking (date) stamp onto paper** - plunger slides (pre-hiss), die flips (click),
   face hits desk (thump); spring return flips die back and body clacks its top stop with metal-frame
   ring. ~10 %.
4. **Snapping the rings of a ring binder shut** - rings closing not quite together (B crunch), steel
   over-centre plate snapping (C) with ring, binder on desk (62 Hz). ~7 %.
5. **Flicking a light switch on and off (or two switches at once)** - two equal clicks 135-137 ms
   apart match the BBC switch clip; wall-plate thump; but the long 790 Hz ring needs a metal toggle,
   not a plastic rocker. ~6 %.
6. **Snapping a clipboard clip down** - clip lifted (B) and released onto hardboard (C): big thump
   plus steel spring ring. ~5 %.
7. **Clamping a bulldog (fold-back) clip onto papers** - squeeze click then release snap with steel
   ring; weaker thump than measured. ~5 %.
8. **Clicking a retractable pen (the push button, not the clip)** - textbook press/release double
   click ~130 ms apart; against it: the 62 Hz desk thump and a ring too low for a pen spring. ~5 %.
9. **Cutting a nail with nail clippers** - snip (sharp high click) then lever flipping back with
   steel ring; no panel thump unless on a bench. ~4 %.
10. **Pressing the tail switch on a metal torch** - press and release clicks in a metal tube that
    rings; thump only if on a table. ~3 %.
11. **Clicking a computer mouse** - press/release 100-140 ms; but no 790 Hz metal ring. ~3 %.
12. **Pulling the trigger on a BBQ/gas lighter** - piezo snap then trigger return clack; no thump. ~3 %.
13. **Stepping on a pedal bin** - linkage click, lid hitting stop with steel-body boom; return stroke
    too slow for 137 ms. ~3 %.
14. **Plugging a seatbelt into its buckle** - metallic snap with ring; but one stroke, not two. ~2 %.
15. **Squeezing a label maker / price gun** - lever press crunch and spring return clack. ~2 %.

