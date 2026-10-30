# Bendigo Secret Sound vs grandfather-clock winding (Freesound 27149, 805328)

Date: 30 Oct 2026. Scripts/outputs in `analysis/bendigo/fable_fresh/`: `c0_overview.py` (whole-file click train,
`fig_c27149_overview.png`, `fig_c805328_overview.png`), `c1_features.py` (same feature set as the clue analysis on any
window: `c1_clue.out`, `c1_27149.out` at 4.19 s, `c1_27149b.out` at 6.60 s, `c1_27149c.out` at 1.55 s,
`c1_805328.out` at 2.00 s), `c2_compare.py` (1/3-octave spectra, centroids, stroke structure; `fig_clock_thirdoct.png`),
`c3_stroke.py` (click intervals vs level inside each winding stroke). Clue features are from `fable_fresh.md`.

## 1. The two clock recordings

**27149 Grandfather-Clock-Winding** (12.5 s, peak -2 dBFS, close-miked, **band-limited to 7.8 kHz**: nothing at all
above 8 kHz, so brightness above 8 kHz cannot be compared). Four long crank strokes (at 1.2, 3.8, 6.3, 8.5 s; 0.7-1.05 s
each, 13-19 pawl drops per stroke) plus short partial strokes. Within a stroke the pawl drops come every 50-56 ms
(18-20/s) in the middle, slower (70-100 ms) at the ends; loudness swells and fades over the stroke. Every pawl drop
is a **double click** (two impacts 4-7 ms apart, 56 of 151 loud intervals fall in 4-6 ms), and a quieter secondary
click follows 13-18 ms after most loud drops. Level: drops at -4 to -10 dBFS, floor between -28 to -31 dBFS.
Ring: strongest sustained lines in the tails are **1.13-1.47 kHz** (1134, 1155, 1351, 1470 Hz; T60 0.2-1.9 s) and
**3.3-3.65 kHz** (T60 0.13-0.5 s), with 2.46-2.58 kHz (T60 ~50-165 ms), 4.0-4.1, 4.86-4.94 kHz. Low band: 40-120 Hz is
20-30 dB below 2-5 kHz; 275-345 Hz and 534-560 Hz lines present.

**805328 CLOCKMech Samsung Galaxy CU Grandfather** (4.1 s, phone recording, peak -19 dBFS, full band). Pawl clicks
12-22/s, irregular (intervals 7-32 ms, median 36 ms between detected onsets), very weak (-29 to -35 dBFS, floor -45).
Ring: 2.1-2.35 kHz (2141-2206, 2309-2348 Hz; T60 0.12-0.8 s), 1.48-1.6 kHz, 2.6 kHz, 5.9-6.0 kHz, 7.4-7.8 kHz. Strong
low content: 144-240 Hz are the loudest lines in the window, 53-69 Hz present, 40-120 Hz at -2 to -10 dB rel 2-5 kHz.
Clicks are bright (6-15 kHz at +2 to +8 dB rel 2-5 kHz in the first 2.5 ms): a phone mic close to a steel click.

## 2. Feature-by-feature comparison with the clue

| Feature | Clue (273 ms) | 27149 at 4.19 s (273 ms) | 805328 at 2.0 s | Verdict |
|---|---|---|---|---|
| Main hit rate | 5 hits, gaps 78/53/67/46 ms = 13-22/s | pawl drops at 28, 74, 125, 174, 228 ms = gaps 46/50/50/53 ms = 19-22/s | 12-22/s | **Match** (rate) |
| Rhythm | long-short-long-short, both shrinking 14 %/cycle | even 50 ms, slow at stroke ends; no alternation | irregular | Partial: clue is less regular |
| Micro-structure of a hit | 2-6 sub-impacts in 5-15 ms, spacing 2-7 ms, plus a weaker click 8-15 ms later (E2 -> 100.7 -> 110.5; E3 -> 156.5 -> 163) | double click 4-7 ms apart, then a quieter click 13-18 ms later | some doubles 6-7 ms | **Match** (pawl drop + bounce + secondary) |
| Loudness profile | fades 10 dB over 250 ms after a heavy first hit | swells and fades over a 0.8-1 s stroke; any 273 ms window shows +-6 dB wander, loud drops alternate with -10 dB ones | flat | Partial: clue looks like the END of a stroke |
| Dynamic range hit/floor | 25 dB | 27 dB | 10-15 dB (noisy phone) | Match (27149) |
| Continuous noise | none | none (clean between clicks) | phone hiss | Match (27149) |
| Strongest sustained ring between hits | **2.32 and 2.55 kHz** (two lines 9.5 % apart), T60 80-250 ms | **1.13-1.47 kHz** (T60 0.2-1.9 s) and **3.3-3.65 kHz** (T60 0.13-0.5 s); 2.5-2.57 kHz only -7 dB and short | 2.1-2.35 kHz (T60 0.1-0.8 s), 1.5 kHz | **Differs**: clock's main ring is ~10-11 semitones lower (1.35 vs 2.55 kHz) AND it has a second cluster 5-7 semitones higher (3.3-3.6 kHz) |
| Ring decay | 0.08-0.25 s (damped, hand-held/small) | 0.2-1.9 s on the 1.1-1.5 kHz lines (big free-ringing brass/steel + wooden case) | 0.1-0.8 s | **Differs**: clock rings 3-8x longer |
| Upper cluster | 3.6-4.4 kHz (-3 to -12 dB), 5.0, 6.5, 7.5 kHz | 4.0-4.1, 4.86-4.94 kHz (0 to -4 dB, strongest in whole-window spectrum) | 5.9-6.0, 7.4-7.8 kHz | Differs in position; the clock's loudest whole-window lines are at 4.9 kHz |
| Spectral centroid 40-8 kHz | 2556 Hz | 3347 Hz (3105 Hz over the whole stroke) | 1601 Hz | 27149 is centroid-higher, 805328 lower |
| Band energy 2-3 kHz / 3-5 kHz (rel total) | -3.5 / -6.4 dB | -8.9 / -2.8 dB | -10.3 / -12.3 dB | Clue is 2-3 kHz-centred, 27149 is 3-5 kHz-centred |
| Brightness above 8 kHz | 8-12 kHz at -22 dB, 12-16 kHz at -25 dB (present) | nothing (file low-passed at 7.8 kHz) | present, strong | Clue has a brighter click than 27149 can show |
| Impact tilt (6-15 kHz minus 2-5 kHz, first 2.5 ms) | -7 to -16 dB | -8 to -28 dB (unfair: 8 kHz cut) | +2 to +8 dB | 805328 is far brighter than the clue; 27149 duller (partly the file) |
| Low thump 40-120 Hz (30 ms after hit, rel 2-5 kHz) | -2 to -12 dB; a 60-90 Hz thump peaks before the cut; 79-86 Hz line at -2 dB whole-window | -20 to -30 dB; no 60-90 Hz line (75 Hz at -17, 118 Hz at -13) | -2 to -10 dB; 53-69 Hz present | **Differs**: the clue has a heavy low thump the big clock lacks |
| 300-700 Hz group | 342/480/606 Hz after the first hit only | 275-345, 534-560 Hz in every hit (-2 to -15 dB) | 425-478 Hz dominant | Similar presence, clue only on the heavy hit |
| Onsets per 273 ms (all > 9 dB jumps) | 28 | 29 | 17 | Match (density of events) |

### What the owner is most likely hearing as "pitch"

The click rate is the same (18-22/s), the event density is the same, and the pawl-drop micro-structure is the same,
which is why it sounds "almost identical". The one thing that is unambiguously **lower** in the clock is the
**sustained ring between clicks**: 1.13-1.47 kHz with a long tail, against the clue's 2.32/2.55 kHz pair. That is a
10-11 semitone difference, outside the +-6 semitones that were tried; and a global shift cannot fix it anyway because
the clock also carries a 3.3-3.65 kHz and a 4.9 kHz cluster above the clue's 2.55 kHz, so shifting the clock up by
10 semitones to put 1.4 kHz on 2.5 kHz pushes those to 6-9 kHz and the sound gets thin and glassy, while shifting
it down makes the low ring even lower. Two further things pull the same way: the clock's long 0.2-1.9 s ring
(a big brass ratchet wheel and a wooden case) versus the clue's 0.1-0.25 s choke (a small, hand-held, damped body),
and the clue's heavy 60-90 Hz thump on its first hit, which the clock lacks. In short: same mechanism, same winding
speed, **smaller and deader resonator, with a bump on the table**.

## 3. Physical reading: what would turn the grandfather clock into the clue

Same mechanism: a click (pawl) spring dropping onto the teeth of a ratchet wheel on a winding arbor, turned by hand,
with the pawl bouncing once (double click) and a quieter secondary click (the tooth tip or a second click) each time.

| Property | Grandfather clock (27149) | Clue | Physical change |
|---|---|---|---|
| Clicks per second | 18-20 in the middle of a 1 s crank stroke | 13-22, shrinking gaps, fading | Same hand speed in clicks/s. With fewer teeth per turn (small ratchet wheel, 8-16 teeth) the key/knob turns at 1-2 rev/s, i.e. a thumb-and-finger key or a small knob rather than a crank. The fade + heavy first hit + only ~6 clicks look like one **half-turn flip of a key** (butterfly/wing key or small crank): engage (thump), accelerate, ease off. |
| Main ring | 1.1-1.5 kHz, T60 0.2-1.9 s | 2.3-2.55 kHz pair, T60 0.08-0.25 s | A ringing part about **half the linear size** (plate/dome frequency ~ thickness / diameter^2) or 2x stiffer: a 40-70 mm steel ratchet wheel, bell dome, back plate or tin case instead of a large brass wheel; and **damped**: held in the hand, screwed into a small tin/pressed-steel case, enamel or paint, sitting on a table, not a free wheel in a wooden cabinet. |
| 9.5 % split pair | not seen (single lines) | 2.32 vs 2.55 kHz | The clue's body has a built-in asymmetry (two bells, a handle, a slot, a wheel with a boss) or two similar parts that the click excites in turn. |
| Upper cluster 3.3-4.9 kHz dominant | present, loudest | 3.6-4.4 kHz but 3-12 dB below the 2.5 kHz pair | A less massive, less bright click: thinner wire click spring or lighter pawl on smaller teeth, not a heavy flat steel click on a big brass wheel. |
| Double click 4-7 ms | strict, every drop | 2-7 ms chatter, less strict | Lighter pawl with less spring preload bounces less regularly (a wire spring, a stamped pawl). |
| Low thump 60-90 Hz | absent | strong on the first hit | The object is light enough to rock or knock on a table/desk, or is held against the chest/lap, or has a shallow cavity; a 5-50 kg floor clock does nothing like it. |
| Clicks above 8 kHz | unknown (file cut) | present but modest | The clue click is metallic-sharp but not a close-miked bare steel click; consistent with a small enclosed mechanism. |

So the target is: a small, hand-held or table-top spring-driven thing with a click-pawl ratchet, wound by a key or
knob in short flips at ~15-20 clicks/s, whose case or bells ring at 2.3-2.6 kHz and die in a quarter second.

## 4. Other click-pawl-ratchet winding mechanisms, ranked

Ranking = fit to the measured difference (small damped 2.3-2.6 kHz resonator, flip-wound at 13-22 clicks/s with
a fade, thump on engagement) first, clues second ("I'm a classic", "I need a hand", "I'm old school").
"List" marks the station's wrong-guess list: X = this exact action is rejected; near = a different action on the same
or a sibling object is rejected; - = not on it.

| # | Caller's phrase | Fit (diff) | Clues | List | Notes |
|---|---|---|---|---|---|
| 1 | Winding up an old wind-up alarm clock (the key on the back) | 5 | 5 | near (clock ticking) | Twin steel bells 40-55 mm on top ring at 2-4 kHz and are two slightly different domes (the 2.32/2.55 pair); tinplate case; butterfly key flipped in half-turns at ~2/s with 8-12 teeth per turn = 15-25 clicks/s in bursts of 4-6 that fade; you pick it up (thump). Clock has hands. |
| 2 | Winding up a mantel clock / carriage clock / cuckoo clock with its key | 4 | 5 | near (clock ticking) | Same click, smaller than a longcase but a wooden or brass case rings longer than the clue; carriage clock (brass, 2-3 kHz gong) and cuckoo (wooden case, small bell) are both plausible; key turned in flips. |
| 3 | Winding up a wind-up kitchen timer / egg timer (the twist kind) | 4 | 3 | - | Small tinplate bell body at 2-4 kHz, hand-held, but the winding is a twist of the whole dial: mostly a spring rasp, the ratchet only clicks on some models. |
| 4 | Winding up a tin wind-up toy (robot, car, chook) with its key | 4 | 4 | - | Small key, 6-10 teeth, tin body rings with many lines, held in the hand (damped), knocks when set down. Classic old-school toy. |
| 5 | Winding up a music box / jewellery box | 4 | 4 | - | Key or crank, small steel ratchet, case rings; the comb notes would appear as fixed pitches only when it plays, not when wound. |
| 6 | Winding up a jack-in-the-box | 4 | 4 | - | Crank-wound music box in a tin box: the clicks and the tin ring; the lid pop would be the heavy hit. |
| 7 | Winding an old pocket watch / wristwatch with the crown | 2 | 4 | - | Right mechanism, but far too small and quiet: ring would be 5-10 kHz and faint. |
| 8 | Winding on an old film camera (the film-advance lever / thumb wheel) | 4 | 4 | - | Lever flip gives 10-20 ratchet clicks in a burst that stops; metal body rings 2-4 kHz, hand-held. Classic, old school, needs a thumb. |
| 9 | Winding a Box Brownie / rewinding the film with the knob | 3 | 4 | - | Knob-wound, slower clicks, cardboard/metal body. |
| 10 | Winding up a wind-up torch / dynamo radio | 2 | 2 | - | Crank gives a continuous whirr; wrong. |
| 11 | Winding the handle on a hand-crank fishing reel (Alvey) with the clicker on | 4 | 4 | - | Ratchet clicker 10-30/s at hand speed; metal spool/back plate rings; Aussie classic. |
| 12 | Clicking a ratchet spanner / socket wrench backwards | 4 | 3 | near (handbrake, Hills hoist) | Steel pawl on a 36-72 tooth wheel, the handle rings 2-5 kHz, hand-driven bursts that stop. |
| 13 | Clicking a ratchet screwdriver | 4 | 3 | near | As above, smaller, bursts of 3-8 clicks per wrist turn. |
| 14 | Winding up the rope on a rotary hoist (Hills hoist) | - | - | X | Rejected. |
| 15 | Winding the handle on a car window (old manual winder) | 1 | 4 | - | No pawl click; a geared grind. Classic car, old school. |
| 16 | Pulling on the handbrake (the ratchet) | - | - | X | Rejected. |
| 17 | Winding up a wind-up gramophone / record player | 3 | 5 | - | Crank with a click, big wooden case rings long and low like the grandfather clock: too big, but a very "classic, old school" guess. |
| 18 | Winding up a hand-crank egg beater | 1 | 4 | - | Gears, no pawl; continuous. |
| 19 | Winding up a clockwork train set / tin train | 4 | 4 | - | As the tin toy; a key in the loco. |
| 20 | Winding up a wind-up chattering teeth / wind-up toy from a showbag | 3 | 3 | - | Plastic body: too dull, but the key ratchet rate is right. |
| 21 | Winding up a metronome | 3 | 4 | - | Key-wound clockwork in a wooden pyramid case: ring lower and longer than the clue. |
| 22 | Winding a cuckoo clock's chain / weight | 2 | 4 | - | Chain over a sprocket with a click: slower, chain rattle. |
| 23 | Setting an old alarm clock (turning the knob to set the hands) | 3 | 5 | near (clock ticking) | Hand-setting knob clicks through a friction/ratchet on some clocks; "I need a hand" fits best of all. |
| 24 | Reeling in a tape measure (the old push-button steel tape) | 2 | 3 | - | Ratchet-free spring return: a whirr, not clicks. |
| 25 | Cocking / winding a cap gun | 2 | 4 | - | One or two clicks per cock; too few. |
| 26 | Winding a yo-yo string / winding up a spinning top | - | - | X (spinning top) | Spinning top rejected; a yo-yo has no ratchet. |
| 27 | Twisting an old mechanical doorbell | - | - | X | Rejected; its hammer-on-dome sound is the nearest rejected relative of a bell-and-ratchet. |
| 28 | Winding up a toy monkey with cymbals / a tin drummer | 3 | 3 | - | Tin toy with cymbals that would ring 3-6 kHz; the key clicks. |
| 29 | Winding the crank on a hand-crank pencil sharpener | 1 | 4 | - | Grinding; no pawl. |
| 30 | Winding up a clockwork kitchen scale / a wind-up mouse | 3 | 3 | near (kitchen scales) | Kitchen scales rejected (that was the spring platform); a clockwork mouse is another tin/plastic toy. |

Lead: candidates 1, 2 and 8 fit the measured difference best; 1 also fits all three clues and sits right next to the
rejected "clock ticking", which tells us callers already hear a clock in it.

## 5. Search terms for the top 15 (1-2 words)

1 `alarm clock`, `clock wind`, `clock key`; 2 `mantel clock`, `carriage clock`, `cuckoo wind`; 3 `kitchen timer`,
`egg timer`; 4 `tin toy`, `wind-up toy`, `clockwork toy`; 5 `music box`; 6 `jack-in-the-box`; 7 `watch wind`;
8 `film advance`, `camera wind`; 9 `brownie camera`; 10 `dynamo torch`; 11 `fishing reel`, `reel clicker`;
12 `socket wrench`, `ratchet spanner`; 13 `ratchet screwdriver`; 15 `window winder`; 17 `gramophone wind`.

What a match must show against the clue: 13-22 pawl drops per second in a burst of 5-8 that fades, each drop with a
2-7 ms bounce and a weaker click 8-18 ms later; between-click ring dominated by two lines 8-12 % apart in 2.2-2.7 kHz
(a 3.6-4.4 kHz cluster 3-12 dB lower) with T60 0.08-0.25 s; a clean floor; and a 60-90 Hz thump on the first drop.
A recording whose ring sits at 1.1-1.5 kHz or lasts more than 0.4 s is the grandfather-clock case again, not the clue.
