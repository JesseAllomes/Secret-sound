# Unknown "click ... click-clack" sound: acoustics research and candidate map

Purpose: broad, physically reasoned candidate generation for a later narrowing step. Nothing here is a final answer. Where a statement is my own derivation or recollection rather than something I fetched from a source, it is marked **[own calc]** or **[not sourced]**.

## 0. The measurements, restated in the shorthand used below

| Tag | Feature |
|---|---|
| **A** | faint, dry, 3-8 kHz click at ~64 ms, no bass |
| **B** | loudest attack at ~112 ms; "crunchy" = ~5 micro-impacts in ~27 ms |
| **C** | single cleaner snap/clack at ~250 ms; **B to C = 138 ms** |
| **Th** | damped ~60 Hz thump peaking ~30-40 ms *after* B and after C |
| **R** | narrow ~790 Hz mode, strong after C, ~17 dB weaker after B; companions 1296 and 1687 Hz |
| **Sp** | listener hears "spring or other resonance"; staplers/door handles "too sharp, no resonance" |

Mode ratios of the measured set: 1296/790 = 1.640, 1687/790 = 2.135.

---

## 1. Physics of the resonance

### 1.1 What the ring tells us before any geometry

- **Decay vs Q.** T60 = ln(1000)/(sigma) with sigma = pi f/Q, so **T60 = 6.91 Q/(pi f) = 2.2 Q/f** (the 2.2/bandwidth rule; [Wikibooks Engineering Acoustics](https://en.wikibooks.org/wiki/Engineering_Acoustics/Characterizing_Damped_Mechanical_Systems) gives tau = Q/(pi f) for the 1/e time, [DSPRelated](https://www.dsprelated.com/freebooks/filters/Quality_Factor_Q.html) covers Q; the 6.91 factor is my own ln(1000)). At 790 Hz:
  - T60 0.3 / 0.4 / 0.5 s corresponds to Q ~ 108 / 144 / 180.
  - The stated Q 60-120 corresponds to T60 ~ 0.17-0.33 s. **The two numbers in the brief are slightly inconsistent** (T60 0.3-0.5 s needs Q ~ 110-180). Either is "lightly damped": this is a metal (or glass/ceramic/hard-plastic-under-tension) element that is not being squeezed by a hand or sitting in rubber/foam. **[own calc]**
  - Only ~80 ms of audio exists after C (0.33 s total, C at 0.25 s), so T60 was extrapolated from a short decay. See uncertainties.
- **It is not an air-cavity resonance.** Helmholtz/cavity resonators have low Q because radiation loss is large; loudspeaker designers who want a Helmholtz port have to *add* damping to bring Q to 0.25-2 ([patent US5261006, as returned by search](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5261006)), and the Q of a radiation-limited Helmholtz resonator depends on volume ([Gough, IOA](https://www.ioa.org.uk/system/files/publications/CE%20GOUGH%20RADIATION%20EFFICIENCIES%20OF%20MUSICAL%20INSTRUMENTS.pdf)). Q of 100+ at 790 Hz points to a structural (solid) mode. Pipe/tube air columns also give the wrong ratios: open-open 1:2:3, closed-open 1:3:5. A quarter-wave tube at 790 Hz would be ~10.9 cm and a half-wave one ~21.7 cm **[own calc]**.
- **Why C rings but B barely does.** A crunchy B made of ~5 small impacts is a dissipative event (sliding, ratchet teeth, bouncing parts, fracture) that puts little coherent impulse into one mode; a single clean "snap" (C) is a hard, short, one-shot impulse that excites a mode efficiently. Equivalent statement: the resonator is *hit* at C and merely *brushed* at B. This is classical impact-excited-structure behaviour; see the vibro-impact oscillator work: [arXiv 2108.12804](https://arxiv.org/pdf/2108.12804) (spring-mass-damper hitting a barrier; coefficient of restitution and spring stiffness dominate the radiated sound). The ring being ~17 dB lower after B could also mean the resonant part is damped (held/clamped) during B and released before C (e.g. a clip held closed, then freed).
- **Why Th arrives 30-40 ms after the click.** A damped 60 Hz resonator hit by an impulse peaks within ~4 ms (quarter period), not 30-40 ms. A *delayed* LF peak instead means a **slower, heavier force pulse**: a mass actually arriving (lid, plunger, hammer, flap), or a finger/hand/body pressing a table or housing. Free-fall equivalents **[own calc]**: 30-40 ms corresponds to only 4-8 mm of drop; B to C of 138 ms is 93 mm of free fall, or a bounce with ~23 mm apex. Spring-driven parts travelling a few mm to a couple of cm at ~0.3-0.5 m/s give the same delay. So the click (A/B/C) is most likely a *trigger or release* and the thump is the *mass landing*; or the click is a finger-down/finger-up and the thump is the table taking the load.
- **B to C = 138 ms** is a very natural **finger press-and-release dwell** (a deliberate tap is ~80-200 ms), a **ratchet/pawl-and-return** time, a **shutter exposure time** (1/8 s = 125 ms), or a **flap bounce**. It does not by itself pick one.

### 1.2 Mode-ratio fingerprints (the measured set is 1 : 1.64 : 2.14)

| Geometry (boundary) | Mode ratio pattern | Fits 1 : 1.64 : 2.14? | Source |
|---|---|---|---|
| Free-free bar / tube flexure; also fixed-fixed | 1 : 2.76 : 5.4 : 9.0 (formula (2n+1)^2/9); fixed-fixed 1 : 2.75 : 5.39 | **No** (second mode far too high) | [Penn State, Russell](https://www.acs.psu.edu/drussell/Demos/Flexural-Bar/flexural.html) |
| Cantilever / clamped-free tine, leaf, wire leg | 1 : 6.27 : 17.55 | **No** (extremely steep) | [Rutgers lab handout](https://www.physics.rutgers.edu/~jackph/2005s/PS11.pdf) |
| Ideal coil spring, longitudinal (fixed-fixed or free-free) | ~harmonic 1 : 2 : 3 for supple springs; stiff/short springs "detuned or unpredictable" overtones; transverse modes string-like | **No** for one family; **possible** only if several families (longitudinal, transverse, torsional) interleave | [Barth Hopkin, coil springs as sound sources](https://barthopkin.com/coil-springs-as-sound-sources/) |
| Coil spring with end mass (fixed-free, mass M, spring mass m_s) | root of x tan x = m_s/M. For m_s/M = 1: x = 0.860, 3.426, ratio 3.98; for M to 0 the ratio tends to 3 | **No** (>= 3) | **[own calc]** from standard mass-loaded-rod theory |
| Thin ring / cylindrical shell (n = 2,3,4 circumferential) | ~1 : 2.8 : 5.4 from n(n^2-1)/sqrt(n^2+1) | **No** for a thin ring; short, stiff cans with end caps are less steep but I have no source | **[own calc / not sourced]** |
| **Circular membrane / tensioned disc** (clamped edge, (0,1), (1,1), (2,1), (0,2), (3,1)) | 1 : **1.59** : **2.14** : 2.30 : 2.65 (Bessel zeros 2.405, 3.832, 5.136, 5.520, 6.380) | **Close**: 1.64 vs 1.59 (3% high), **2.135 vs 2.136 (essentially exact)** | [Stony Brook solutions](https://www.math.stonybrook.edu/~tony/archive/341f11/solutions5a.pdf), [Wikipedia: Vibration of a circular membrane](https://en.wikipedia.org/wiki/Vibration_of_a_circular_membrane) |
| **Free circular plate**, nu = 0.3: (2,0), (0,1), (3,0), (1,1), (4,0) | coefficients 5.359, 9.005, 12.441, 20.489, 21.840 give ratios 1 : **1.68** : **2.32** : 3.82 : 4.08 | **Partial**: second mode good, third 8% high | FE table 1 in [Malison et al., Eng. Trans.](https://ph02.tci-thaijo.org/index.php/ET/article/download/244797/166000/858618) (ratios computed by me) |
| Clamped circular plate, nu = 0.3 | 10.217, 21.279, 34.917, 39.853 gives 1 : 2.08 : 3.42 : 3.90 | **No** | same table |
| Simply supported circular plate | 4.936, 13.906, 25.634 gives 1 : 2.82 : 5.19 | **No** | same table |
| **Clamped circular plate under tension** (stiff diaphragm), my Ritz calculation | ratio 1.64 occurs at a stiffness-to-tension parameter where the third ratio is ~2.33; a pure membrane limit gives 1.59/2.14; no single stiffness hits both | **Near-miss** (bracket the measurement from both sides) | **[own calc]** (reproduced clamped-plate 10.216, 21.26, 34.88 as a check) |
| Free rectangular plate, nu = 0.3 | square: 1 : 1.45 : 1.80 : 2.58 : 2.58. Strongly aspect-dependent: at a/b ~ 2.7-2.75 modes 2,3,4 give **1 : 1.65 : 2.13** | **Possible but not diagnostic**, aspect ratio is a free parameter and many aspects give some subset match | **[own calc]** (Ritz with Legendre basis; validated on the square-plate values 13.47, 19.60, 24.27, 34.80) |
| Chladni law (flat circular plates, f ~ (m+2n)^2) | only an asymptotic guide; not accurate for lowest modes | n/a | [Wikipedia: Chladni's law](https://en.wikipedia.org/wiki/Chladni%27s_law) |

**Reading of the table.** A *compressed* ratio set (second mode only 1.6x the first) is a **two-dimensional** signature: discs, lids, diaphragms, domes, flat panels, membranes, or rectangular plates of moderate aspect ratio. One-dimensional structures (bars, tines, tubes, rings, springs as ideal rods) give much steeper or exactly harmonic sets. Therefore the *ringing part is more likely a small thin metal plate-like element* (lid, flap, diaphragm, dome, tin/can end, spring-steel clip *face*, housing panel, bell-less gong) than a coil or a tine. The closeness to a membrane-like spectrum (third ratio 2.135) is striking but, with only two measured ratios and measurement tolerance unstated, it is a clue and not proof.

**Sizing for a small steel/aluminium plate** (own derivation from thin-plate theory with the plate wave speed, for steel and aluminium the factor is ~same) **[own calc]**:

- Free circular disc, (2,0) mode: f ~ 1300 x h/a^2 Hz (h thickness, a radius, metres). For 790 Hz, h/a^2 ~ 0.61 per metre: a = 2 cm needs h ~ 0.24 mm; a = 3 cm needs h ~ 0.55 mm; a = 5 cm needs h ~ 1.5 mm. (Cross-check: a 25 cm diameter, 0.7 mm steel bin lid would ring near 60 Hz, far too low, so large thin lids are out unless heavily stiffened by ribs/domes.)
- Free-free bar: f1 ~ 5200 x h/L^2 (steel); 790 Hz needs h/L^2 ~ 0.15 (L = 5 cm, h ~ 0.4 mm). Cantilever: f1 ~ 816 x h/L^2; 790 Hz needs h/L^2 ~ 0.97 (L = 2-3 cm, h ~ 0.4-0.9 mm), but the overtones would then be at ~4.9 kHz, not 1296 Hz.
- Coil spring surge (longitudinal) f1 ~ (d / (2 pi N D^2)) sqrt(G/2 rho) for fixed-fixed (roymech/Vibrationdata discuss end-condition factors; I did not find a source that pins the constant, so treat as approximate): wire 0.5 mm, coil 5 mm, 8 coils gives ~890 Hz; 0.7/7/6 gives ~850 Hz; 1/10/10 gives ~360 Hz. So small few-coil springs (pen, latch, small button springs) can sit near 800 Hz as the *first axial* mode, but then the next modes are ~2x, 3x, not 1.64x. Sources: [Roymech spring surge](https://roymech.org/Useful_Tables/Springs/Springs_Surge.html), [Vibrationdata](https://blog.vibrationdata.com/?p=151029).

### 1.3 Coil springs, specifically (the listener's word "spring")

- Springs have two main vibration families, transverse (string-like, poorly coupled to a flat radiator) and longitudinal (air-column-like, couple to a diaphragm); real springs also have torsional motion ([Barth Hopkin](https://barthopkin.com/coil-springs-as-sound-sources/)). Higher modes of long soft springs crowd into a dense pitchless "sizzle"; small stiff ones can give a definite pitch when one mode dominates.
- A struck/flicked spring doorstop is the archetypal "boing"; Freesound has recordings titled "doorstopperspring2.mp3 (vibrating after being flicked)", "SpringDoorStop.wav (pinged)" and "door_stop.wav" ([search page](https://freesound.org/search/?q=spring+doorstop)). Its character is a *pitched, long, slightly dispersive* twang, not a narrow 790 Hz line with Q ~100 that begins only at the second event. I could not find rigorous published physics for doorstop pitch/decay; informal sources only.
- Slinky-type dispersion (chirps/"whistlers") exists for long, soft, low-pitch springs held at both ends ([arXiv 1403.6809 mentions Crawford's whistlers](https://ar5iv.labs.arxiv.org/html/1403.6809)); I found no source tying chirps to small mechanism springs in the 0.3 s range. A downward-sweeping chirp would show on a spectrogram; the brief reports a *steady* narrow line, which argues against a long dispersive spring.
- Spring-ping in keyboard switches is real but described in vendor language ("clack" above ~2 kHz, "thock" below ~500 Hz; no standard measurement, [Attack Shark blogs](https://attackshark.com/blogs/knowledges/spring-crunch-leaf-ping-fix-keyboard-noise)); the patent literature describes axial and transverse spring vibration with the middle coils moving most ([US12278063 as returned by search](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12278063)).

### 1.4 What "spring or other resonance" most plausibly means physically

Four physical stories are compatible with the measurements, and they point to different objects:

1. **A spring-driven part hits a thin plate-like metal element at C** (stamped metal flap, lid, diaphragm, cap, housing wall). The *spring* supplies the energy and snap; the *plate* supplies the ring and the compressed-ratio mode set. The listener hears "spring" because the sound is a snap-then-ring.
2. **A genuine coil spring rings after C** (a spring released or struck). Needs interleaved mode families to give 1.64 and 2.14; cannot be excluded.
3. **A spring-steel clip/strip rings** (bistable or leaf geometry). One-dimensional ratios would predict 1:2.8+ or 1:6.3, so only plate-like regions of the clip would match.
4. **A metal housing (tin, can, tube) rings**, with the ratio set coming from its end plate/wall, not from the cylinder bending modes.

---

## 2. Candidate table (44 object + action pairs)

Legend per column: **yes** = expected and consistent; **part** = partially / depends on design; **no** = expected to be absent or wrong; **?** = unknown. Columns: A pre-click, B/C = crunch then clean snap, Cad = a natural 138 ms gap between the two events, Th = a mass/surface thump ~35 ms after each event, R = a lightly damped ~800 Hz-class ring excited mainly by the second event, Sp = spring/resonant character. No candidate can be called "strong" because none of these has been compared with the audio; ratings reflect pattern match only. I mark the best patterns "plausible (top tier)".

| # | Category | Object + action | Expected signature | A | B/C | Cad | Th | R | Sp | Fit |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Stationery | Metal-barrel click pen: press then release plunger | cam-on-cam knock when the spring drives the rotating cam against the fixed cam ([patent US2018/0229541 describes this as the knock source](https://patents.justia.com/patent/20180229541)); two sounds per cycle | part (first cam tick) | part | yes (press/release dwell) | weak (tiny mass) | part (metal barrel rings, but usually >2 kHz) | yes | **plausible (top tier)**; note "pen clip" was a wrong guess, click mechanism is a different part |
| 2 | Stationery | Clipboard: lift clip, release it onto the board | spring-steel clip slaps hardboard: single sharp clack, board gives dull thud; Freesound has [clipboard snaps](https://freesound.org/search/?q=clipboard+clip) | yes (lift tick) | part | part | yes (board is a plate, but low modes ~100-300 Hz) | weak (clip rings high; board low) | part | plausible |
| 3 | Stationery | Ring binder: open rings, snap shut | spring-steel ring halves snap together with metallic "clack" and ring; Freesound has [three-ring binder snap open/close](https://freesound.org/search/?q=ring+binder) | part | part (ring teeth crunchy?) | part | part | **part** (steel rings and base are plate-like, small) | yes | plausible |
| 4 | Stationery | Lever-arch file: lift lever, snap down | lever on spring-loaded mechanism, plate with arch, cardboard body | part | part | part | yes (cardboard box thump) | weak (cardboard damps) | part | weak-plausible |
| 5 | Stationery | Binder/bulldog clip: squeeze wings, release onto paper | spring-steel clip bites onto paper stack: soft clack | no | weak | part | weak | weak | yes | weak |
| 6 | Stationery | Manual stapler: press, release | spring return then staple clinch; listener says staplers "too sharp, no resonance" | part | yes (clinch crunch) | yes | part | no | no | weak (already compared) |
| 7 | Stationery/garage | Heavy-duty (spring) staple gun: squeeze trigger, release | ratchet-compress then spring hammer fires: one loud clack; return clack. Freesound: [staple gun squeeze / dry-fire](https://freesound.org/search/?q=staple+gun) | part | part (ratchet crunch then fire) | part | yes (hand/handle) | part (steel body) | yes (spring hammer) | plausible, but usually sharper/louder than described |
| 8 | Stationery | Typewriter **space bar**: press then return | softer thud than letter keys, no platen strike; escapement tick then bar returns; cushion springs/stops used against rattle ([1930s patent US1955614](https://patents.google.com/patent/US1955614)); Freesound has several [typewriter space bar](https://freesound.org/search/?q=typewriter+space) recordings | part | part | yes (key down/up) | yes (heavy machine on desk) | part | part | plausible (top tier) |
| 9 | Stationery | Typewriter letter key / carriage return lever | typebar strike (clack) and rest-rail return; escapement; return spring "whirr" ([sound-design write-up via search](https://soundcy.com/article/what-a-typewirter-sounds-like)) | part | part | part | yes | part | yes | plausible |
| 10 | Electronics | Mechanical keyboard: space bar with stabiliser, press and release | actuation click, bottom-out thock, stabiliser rattle, release clack, spring ping | yes | part (stabiliser rattle crunch) | yes | yes (bottom-out thock) | weak (ping usually kHz, plate/case lower) | yes | plausible |
| 11 | Electronics | Computer mouse button: press and release | microswitch click on press, clack on release, shell thump | yes | part | yes | weak | weak (plastic) | part | weak-plausible |
| 12 | Electronics | SLR/film camera, slow shutter (~1/8 s): mirror up, exposure, close | mirror slap + shutter open (click), shutter close (clack); exposure 125 ms is close to 138 ms; body thump | yes | part (curtain bounce crunch) | **yes** | yes (mirror box) | part | part | plausible on cadence; less "everyday household" |
| 13 | Bathroom | Nail clipper: press lever, cut, release | lever pivot tick, nail cutting in several micro-fractures (crunch), spring return clack with metal ring ([Freesound](https://freesound.org/search/?q=nail+clipper) has 47 results) | yes | **yes** | yes | weak | part (small steel body rings, often >2 kHz) | part | plausible |
| 14 | Bathroom | Pull-cord light switch: pull, release | ratchet-pawl crunch (several teeth) then return clack in a plastic/metal housing ([Freesound pull switch](https://freesound.org/search/?q=pull+cord+switch)) | part | **yes** | yes | part (ceiling/wall) | weak | part | plausible (top tier) |
| 15 | Bathroom/house | Rocker/toggle light switch | single detent snap; BBC library version "closest, not it" | part | no (one stroke) | no | weak | part | part | weak (already tried) |
| 16 | House | Lever door handle: depress then release | latch retract, spring return; listener: "too sharp, no resonance" | part | part | part | yes | no | no | weak (already compared) |
| 17 | House/garden | Thumb latch / gate latch: press thumb piece, lift bar, drop onto keeper | metal lift click, drop clack, ring of bar/keeper, door thump | yes | part | yes | yes | **part** (steel bar/plate) | part | plausible |
| 18 | House | Letterbox flap: lift and let fall | hinged flap drops with chatter (micro-bounces = crunch), rebounds; spring flaps add twang; Freesound [letterbox flap](https://freesound.org/search/?q=letterbox+flap) | part | **yes** (bounces) | **yes** (rebound) | part | **yes** (small metal plate) | part | plausible (top tier) |
| 19 | House | Padlock: push shackle shut, or key in and turn | shackle detents (two clicks), body ring; five-pin lock: key insertion gives ~5 pin ticks | part | **yes** (pins/detents) | part | part | **yes** (solid steel body) | part | plausible |
| 20 | House | Briefcase/suitcase/toolbox latch: slide catch, lid pops | catch click then lid spring pops: "click-clunk", lid thump | yes | part | part | yes | part | yes | plausible |
| 21 | Smoking/lighters | Zippo-style metal lighter: flip lid, strike wheel, snap shut | cam click on lid open, flint-wheel rasp (crunch), clink on close; Zippo trademarked the click ([Zippo](https://zippo.co.uk/blogs/news/zippo-celebrates-its-signature-click-as-sound-trademark-is-secured)) | yes | **yes** (wheel rasp) | part (usually longer) | weak | yes (small steel lid, kHz) | yes | plausible |
| 22 | Smoking/kitchen | Disposable gas lighter: child-guard wheel strike + valve | ratchet/rasp crunch then valve release click | yes | yes | part | weak | weak | part | weak-plausible |
| 23 | Kitchen/BBQ | Piezo igniter push-button: press | spring-loaded hammer strikes crystal, hammer-on-stop click ([Wikipedia: Piezo ignition](https://en.wikipedia.org/wiki/Piezo_ignition)); single sharp event | part | no | no | weak | part | yes | weak |
| 24 | Garage | Caulking gun: squeeze trigger (ratchet), release plunger | rod-teeth ratchet crunch, release-lever clack, metal frame ring | part | **yes** | part | yes | part (steel frame) | yes | plausible |
| 25 | Garage/office | Retractable tape measure: unlock, blade snaps back / lock engages | lock "gives a snap feel and audible cue" ([patent US5806202](https://patents.justia.com/patent/5806202)); blade whip then end-hook clack | part | part | part | part | part (curved steel blade) | yes | plausible |
| 26 | Garage | Snap-off utility knife: slide blade through detents, snap segment | slider detent ticks (crunch) then segment snap | part | yes | part | weak | part | part | weak-plausible |
| 27 | Garage | Ratchet screwdriver/wrench: reverse | pawl ticks (crunch), one reverse clack | part | yes | part | weak | part (steel) | part | weak |
| 28 | Car | Seat-belt buckle: insert tongue, press release | spring-latch snap ("click is intentional feedback", [GMW14154 / patents](https://patents.google.com/patent/US6385823)); metal-on-metal, hard to damp | part | part | part | part | part | yes | plausible |
| 29 | Car | Glovebox / fuel flap / bonnet catch: release then flap drops and rebounds | button click, flap falls (thump), damper/rebound clack | yes | part | **yes** | **yes** | part | part | plausible |
| 30 | Car | Handbrake lever: pull (ratchet crunch), press button, release | multi-tooth ratchet crunch then pawl release clack, heavy body thump | part | **yes** | yes | **yes** | weak | part | plausible, but "household" unlikely |
| 31 | Toys | Cricket/tin clicker toy: press, release | steel tongue (leaf spring) snaps in and out: click then clack; tongue and frame ring | part | part | **yes** | weak | **part** (metal frame) | **yes** | plausible (top tier). (Freesound search "cricket clicker" returned 0 results; use "toy clicker" etc.) |
| 32 | Toys/clothes | Slap bracelet: slap, curl | thump on wrist, bistable steel-band snap, ring | no | part | part | yes | part | yes | weak-plausible |
| 33 | Toys | Foam-dart/toy-gun: cock (ratchet crunch), pull trigger | cocking ratchet = crunch, trigger release clack, plastic thump | part | **yes** | part | yes | weak (plastic) | yes | plausible |
| 34 | Household | Snap mouse trap: set (ratchet-like) and trip | arm lifted against spring, catch set (click), trip: sharp snap, wire/bar ring | part | part | part | yes | part (wire bar cantilever; wrong ratios) | yes | weak-plausible |
| 35 | Household | Spring door stopper: flick | long pitched twang. Freesound: [spring doorstop](https://freesound.org/search/?q=spring+doorstop) | no | no | no | no | part (but longer, pitch glide, no ratio match) | **yes** | weak (spring-only; no two-stroke) |
| 36 | Household | Mint/biscuit tin: open lid, close lid | hinge detent click, lid snap, thin-steel plate ring ~0.5-3 kHz, table thump | yes | part | yes | yes | **yes** (flat steel lid/base is 2D plate-like) | part | plausible (top tier) |
| 37 | Kitchen | Nutcracker (lever): squeeze, release | shell fractures (several micro-cracks = crunch), jaw/lever clack, metal ring | yes | **yes** | yes | part (hand/table) | part | part | plausible |
| 38 | Kitchen | Toaster lever: push down (latch), pop up | latch click, carriage drop, pop; already ruled out as "toaster buttons" | part | part | part | yes | part | part | weak (already wrong) |
| 39 | Hair/bathroom | Hair claw clip / snap barrette: open, release | spring hinge: small plastic or metal snap-clack | yes | part | yes | no | weak | yes | weak-plausible |
| 40 | Household | Clothes peg: open, release onto line/edge | torsion spring + wooden jaws: dull clack; wood damps (low Q) | no | no | part | weak | no | part | weak |
| 41 | Shop | Cash tin / cash-register drawer: press release, drawer springs out and hits stop | latch click, drawer slide rattle (crunch), stop clack, bell ring | yes | **yes** | part | yes | part (bell/steel) | part | plausible |
| 42 | Kitchen | Egg slicer / wire cutter: press, release | wires pluck harmonically (kHz), frame click | no | part | part | weak | no (harmonic wires) | yes | weak |
| 43 | Household | Wind-up kitchen timer: wind (ratchet crunch), bell | ratchet teeth crunch, long bell | no | yes | no | weak | weak | part | weak |
| 44 | Household | Spring-loaded flip-top (pedal) bin: pedal press, lid opens, lid closes | linkage tick, lid hits stop (clunk), rebound; steel lid rings low (large) | part | part | **yes** (lid rebound) | **yes** | weak (large lid too low, see 1.2) | part | weak-plausible |

(The table has 44 rows; fit ratings are pattern-based and none is "strong" because none has been checked against the waveform.)

### Where each family fails, stated plainly

- **Tine/leaf/clip/wire cantilevers (pen clip, mousetrap bar, peg legs, cricket tongue taken alone)**: mode ratios 1:6.27 or 1:2.76 do not match 1:1.64:2.14; their ring is usually >2 kHz for small parts. They can only fit if the *plate-like* part ringing is what we hear.
- **Hard single-impact devices (stapler, piezo igniter, nail gun, hole punch, door handle)**: one sharp, broadband event with little ring; hence "too sharp, no resonance". They also lack a second-event structure.
- **Pneumatic/combustion nail guns**: impact and exhaust events are separate ([NOISE-CON 2013 summary](https://stacks.cdc.gov/view/cdc/195517)), but they are far louder, have no spring "ring", and are not a household object.
- **Plastic housings alone (mouse, keyboard keycap, pill box, bottle cap)**: damping of plastic limits Q to well below 100 at 790 Hz, so the long ring fails unless a metal insert rings.
- **Pure springs (doorstop, Slinky, hand-grip exerciser)**: tend to give a *glide/dispersion* or harmonic series, no click-clack structure, no crunch.
- **Large thin metal panels (pedal-bin lid, car doors)**: fundamental well below 790 Hz (my calc ~60 Hz for a 25 cm, 0.7 mm steel disc), so only small stiffened elements can supply 790 Hz.
- **Bells/gongs**: ring for seconds, with steep or inharmonic ratios, typically >2 kHz in small desk/bike bells.

---

## 3. Top-tier patterns worth testing first (reasoning, no ranking by probability)

1. **Press-and-release device with a small stamped-metal flap/lid/plate** (tin lid, letterbox flap, clipboard/binder spring plate, cash tin): explains compressed plate-like ratios, ring only after the hard "clack", crunch from bounce/chatter, and the thump from the mounting surface.
2. **Ratchet-then-release mechanisms** (pull-cord switch, caulking gun, nail clipper, toy-gun cocking): the 5 micro-impacts in 27 ms are the natural signature of ~5 ratchet teeth passing a pawl at ~185 teeth/s; the clean snap is the release.
3. **Two-stage latch mechanisms** (padlock, briefcase latch, gate latch, car-door/glovebox): click-clunk language, heavy-mass thump 30-40 ms after the catch, metal ring.
4. **Press-release devices with timed dwell** (pen, typewriter bar, keyboard, camera shutter, mouse): 138 ms is a natural dwell; they differ in how much ring.

---

## 4. Search phrases (Freesound-style titles; 118)

Pages checked and returning results on Freesound at time of writing: "spring doorstop", "nail clipper", "ring binder", "typewriter space", "staple gun", "pull cord switch", "letterbox flap", "clipboard clip". "cricket clicker" returned zero, so alternative wording is listed.

**Stationery/office**
1. typewriter space bar
2. typewriter space key single
3. typewriter carriage return lever
4. typewriter key press and release
5. typewriter margin bell
6. stapler press and release
7. staple gun manual
8. staple gun trigger squeeze
9. staple gun dry fire
10. heavy duty staple gun spring
11. clipboard clip snap
12. clipboard clip release
13. ring binder open close
14. ring binder snap shut
15. lever arch file lever
16. binder clip squeeze release
17. bulldog clip
18. paper clip tin
19. hole punch (to rule out; "close but wrong")
20. click pen button
21. retractable pen click metal
22. pen click double
23. mechanical pencil click
24. tape dispenser cut
25. badge reel retract

**Electronics/keyboard**
26. mechanical keyboard space bar
27. keyboard spacebar stabilizer
28. keyboard switch click clack
29. mouse click press release
30. computer keyboard single key
31. spring ping keyboard switch
32. SLR camera shutter slow speed
33. film camera shutter mirror slap
34. camera shutter click clack
35. film camera advance lever
36. old telephone dial / rotary

**Switches/household**
37. pull cord switch bathroom
38. light pull cord ceiling
39. light switch toggle
40. light switch rocker click
41. dolly switch
42. door latch click
43. door handle lever
44. thumb latch gate
45. garden gate latch
46. letterbox flap
47. mail slot flap
48. padlock close
49. padlock shackle click
50. key in lock pins
51. deadbolt throw
52. briefcase latch
53. suitcase latch click
54. toolbox latch
55. guitar case latch
56. cash register drawer
57. cash tin open
58. metal tin lid
59. mint tin close
60. biscuit tin lid
61. foot pedal bin lid
62. glovebox open
63. fuel flap click
64. bonnet release latch
65. seat belt buckle click
66. handbrake ratchet
67. car central locking clunk

**Tools/garage**
68. caulking gun trigger
69. caulking gun release
70. tape measure lock
71. tape measure retract
72. tape measure snap back
73. utility knife blade slide click
74. snap off blade
75. ratchet screwdriver
76. ratchet wrench reverse
77. spring clamp
78. cable tie ratchet
79. nail gun trigger
80. nail gun spring (not pneumatic)

**Kitchen/bathroom/personal**
81. nail clipper
82. nail clippers snap
83. nutcracker crack
84. toaster lever pop up
85. zippo lighter open close
86. zippo flint wheel
87. lighter flint wheel
88. piezo igniter click
89. BBQ igniter click
90. garlic press squeeze
91. bottle opener lever
92. corkscrew waiters friend fold
93. egg slicer
94. hair clip snap
95. hair claw clip
96. razor cartridge click
97. clothes peg
98. wind-up kitchen timer
99. safety razor / shaving click

**Springs/toys**
100. spring doorstop
101. spring door stop twang
102. door stopper boing
103. spring flick metal
104. cricket toy
105. tin clicker toy
106. toy clicker
107. frog clicker
108. slap bracelet
109. foam dart gun cock
110. toy gun cocking click
111. mouse trap snap
112. mouse trap set
113. jack in the box latch
114. pez dispenser
115. spring loaded latch
116. spring loaded button click
117. metal spring release
118. coil spring compress release

(Tip: Freesound search is quote-aware and sorts by relevance; adding "foley", "household", "close mic" and "no reverb" narrows to dry recordings. Try both "press" and "release" as separate files and as one file.)

---

## 5. Key uncertainties

1. **Ratio tolerance unknown.** The measured 1:1.64:2.14 is compatible with a membrane/plate-like part, but I do not know how accurately 1296 and 1687 Hz were measured, whether they are true modes of the same structure, or whether 790 Hz is the fundamental (a lower, weaker mode could exist). With one free parameter (aspect ratio, tension, nu), many plates can mimic the set; it narrows families but cannot name an object.
2. **T60/Q are extrapolated from ~80 ms** of audio after C and may be affected by broadcast processing (compression, gating, truncation). The brief's T60 and Q figures disagree by up to ~1.7x.
3. **Th timing is ambiguous**: heavy mass arriving vs. finger/table loading. They imply different object classes (mechanism-internal mass vs. hand-operated device on a surface).
4. **A 138 ms gap** may be mechanical (spring/flap dynamics, shutter time) or human (press dwell). If human, any press-release device is back in play.
5. **Contradiction risk in "spring" language**: the listener's "spring" may describe the ring-after-snap perception rather than a coil. The mode-ratio analysis argues against an ideal coil or tine as the *only* resonator.
6. **Source quality**: bar/plate/membrane ratios are solid textbook numbers (sources above). Mechanism-level acoustics (pens, typewriters, lighters, buckles, doorstops, staplers) are mostly patents and informal sources; I found no measured spectra for them, so signatures in Section 2 are physical expectations, not published measurements.
7. **Recording conditions**: "dry, close-miked" suggests a studio/foley-style recording of a *single operation*; library-sourced sounds often come from specific brands/models whose mechanical details differ from my generic descriptions.

## 6. Sources used (all fetched or returned by search)

- Free-free/fixed-fixed bar: https://www.acs.psu.edu/drussell/Demos/Flexural-Bar/flexural.html
- Cantilever 6.27 and 17.55: https://www.physics.rutgers.edu/~jackph/2005s/PS11.pdf
- Coil springs as sound sources: https://barthopkin.com/coil-springs-as-sound-sources/
- Circular membrane zeros: https://www.math.stonybrook.edu/~tony/archive/341f11/solutions5a.pdf and https://en.wikipedia.org/wiki/Vibration_of_a_circular_membrane
- Circular plate frequency coefficient table (clamped/simply supported/free, nu = 0.3): https://ph02.tci-thaijo.org/index.php/ET/article/download/244797/166000/858618
- Chladni's law: https://en.wikipedia.org/wiki/Chladni%27s_law
- Q and decay: https://en.wikibooks.org/wiki/Engineering_Acoustics/Characterizing_Damped_Mechanical_Systems and https://www.dsprelated.com/freebooks/filters/Quality_Factor_Q.html
- Helmholtz Q/radiation: https://www.ioa.org.uk/system/files/publications/CE%20GOUGH%20RADIATION%20EFFICIENCIES%20OF%20MUSICAL%20INSTRUMENTS.pdf
- Spring surge: https://roymech.org/Useful_Tables/Springs/Springs_Surge.html and https://blog.vibrationdata.com/?p=151029
- Vibro-impact oscillator sound: https://arxiv.org/pdf/2108.12804
- Nail gun impact vs exhaust: https://stacks.cdc.gov/view/cdc/195517
- Click pen cam knock: https://patents.justia.com/patent/20180229541 and https://en.wikipedia.org/wiki/Retractable_pen
- Zippo click: https://zippo.co.uk/blogs/news/zippo-celebrates-its-signature-click-as-sound-trademark-is-secured
- Typewriter space bar patent: https://patents.google.com/patent/US1955614
- Tape measure lock patent: https://patents.justia.com/patent/5806202
- Seat-belt buckle patents: https://patents.google.com/patent/US6385823
- Dome switch snap (tactile click, under 5 ms snap): https://www.lcsc.com/blog/tactile-vs-nontactile-membrane-switch/
- Piezo ignition: https://en.wikipedia.org/wiki/Piezo_ignition
- Keyboard spring ping (vendor-level): https://attackshark.com/blogs/knowledges/spring-crunch-leaf-ping-fix-keyboard-noise
- Freesound search pages checked: spring doorstop, nail clipper, ring binder, typewriter space, staple gun, pull cord switch, letterbox flap, clipboard clip (all https://freesound.org/search/?q=...)
- Own computations (scripts): /tmp/claude-0/-home-user/28c1726f-2d94-5297-bac9-a599c7c278c0/scratchpad/research/plate_ratios.py (free rectangular plate Ritz) and /tmp/claude-0/-home-user/28c1726f-2d94-5297-bac9-a599c7c278c0/scratchpad/research/tensioned_disk2.py (clamped plate under tension). A free-circular-plate Ritz attempt was numerically unreliable and was dropped; free-circular values come from the FE table above.
