# Session status (30 Oct 2026, cloud session) — read this first after a context reset

Owner rules: see CLAUDE.md (scripts for data collection, never start Fable unless asked, keep MNC and Bendigo separate).

## Mid North Coast (Sarge's Secret Sound, NSW) — $2,800 on Fri 30 Oct, +$25/weekday (Mon 2 Nov ≈ $2,825)
- Clue audio: `clues/mnc/clue.wav` (original, 0.631 s), `clues/mnc/clue_v6b.wav` (owner's preferred clean copy).
  Measured: faint pre-click ~64 ms, crunch B ~112 ms (5 impacts/27 ms), clean snap C ~251 ms (B→C 138 ms), 62 Hz thump
  30-40 ms after each, object rings ~790 Hz (+~440 Hz) after C only. Station tones 110/194/220 Hz are background.
- **Sarge's hints** (`analysis/mnc/caller_guesses.md`): 25 Aug "putting toast in a toaster and pushing the toast down" →
  "had words that would be in the actual correct answer"; 27 Aug "pushing the button to open a microwave door" → "first
  half almost correct"; 16 Sep "putting a battery pack back into a drill / KitchenAid" → "right track"; 21 Sep "popping
  batteries into a compartment like a mouse" → "you're hot… close"; 15 Sep "toast pops up" → "move away from the toaster";
  12 Oct Ken "one of your guesses was remarkably close"; 19 Oct Auntie Julia "very very close".
- Rejected by owner's ear: staplers, door handles/latches, hole punches, light switches, BBC ticket machine, SLR shutter,
  binding/office machines, battery/cartridge/SD clips (A/B zips sent). steel_score.py: clue 0.99, best real 0.83-0.90.
- Podcast harvest (scripts in scratchpad `pods/`: harvest.py running → harvest.jsonl, transcripts/; extract_guesses.py;
  build_package.py → pods/package/mnc_evidence.md). Sound first seen 26 Jul so far; jackpot $1,225 on 27 Jul → round
  likely started mid-July. Waiting for harvest to reach the start (opening cryptic clues).
- **Next (owner agreed to wait):** when the harvest stops, run build_package.py, then ASK the owner before starting a
  fresh, no-context Fable with: clue audio, mnc_evidence.md, past winners (charger into power point, spray bottle,
  Switch into dock, measuring cups clipping, shower nozzle setting), rejected-by-ear list. No prior theories.
- Freesound: this cloud session's IP is blocked. Use GitHub Actions `.github/workflows/pull-and-score.yml`
  (secrets FREESOUND_KEY_SOUNDMAN, FREESOUND_KEY_SOUNDDETECTOR; inputs name, queries jobs/*.txt, per_query, max_seconds,
  bots default 1, ab). Results on branch `results`. Use short 1-2 word searches (multi-word phrases return 0).
  BBC library works directly (`bbc_pull.py`).

## Bendigo (Cogho & Jules' Secret Sound, VIC only) — $750 per page heading, +$25/day
- `analysis/bendigo/README.md`: clues (I'm a classic / I need a hand / I'm old school), 42 wrong guesses, Fable analysis
  (5 metal-on-metal hits, ring 2.32/2.55 kHz; top: playing the spoons, stirring tea with a teaspoon, winding an old
  alarm clock, hand-crank sewing machine). Page clip is trimmed both ends; Bendigo podcast has no plays.
