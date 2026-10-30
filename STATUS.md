# Session status (31 Oct 2026 morning, after the overnight run) — read this first after a context reset

Owner rules: see CLAUDE.md (scripts for data collection, never start Fable unless asked, keep MNC and Bendigo separate).
DrainClamp state: `.agent/` (push it after every DrainClamp write: `tools/dc_push.sh`).

## Morning summary (overnight 30 Oct, owner asleep)
**Mid North Coast** — best leads, every A/B pack in `listening/mnc/` (all sent):
- Keyboard and player push-buttons lead on BOTH scorers (`analysis/mnc/combined_ranking.csv`, `tools/combine_mnc.py`):
  mechanical-keyboard spacebar / key presses (0.99 combined), a hotel door lock, tape-recorder / tape-deck buttons,
  CD/DVD trays. Highest single CLAP score: "Key_Old_Recorder" (0.854, wave 2).
- Sarge's warmest words: "pushing the [button/lock] [down/in]…" (27 Aug "first half almost correct"; 29 Jul toaster
  button "very close"; 1 Jul tape-player button "very close"; 13 Jul tape-deck buttons "really good words"; 19 Oct
  mouse switch after batteries "very very close"). His own cassette deck is in storage (15 Jul), so not the deck itself.
- Sprung lids / doors (wave 4) scored lower (top 0.766): weaker.
- Packs sent: work zip (v6b and stacked clue), local sets, 100 Fable searches, waves 2-4, combined top 20.
**Bendigo** — packs in `listening/bendigo/` (all sent):
- Best score: work-zip "Old Lever Pull" (0.855). A pulled lever with a ratchet fits the long-short metal clicks; a
  one-armed bandit / slot machine fits "classic / need a hand / old school" and is not on the wrong list. Wave 3
  (lever / slot machine, 30 searches) ran overnight: `results/bendigo_wave3` on the `results` branch.
- Other leaders: grandfather-clock winding (0.807), rotary phone dials (0.80), bike wheel / spokes, hand cranks, egg timer.
- Wave 3 result: coin/vending machines cluster just below the lever (vending.wav 0.854, coin coffee machine 0.834,
  coin into slot 0.828). Callers hear coins too (jar, collection box, parking meter, self-serve coins all wrong on the
  station list), so the exact action matters: a vending machine / coin-return / slot-machine lever is not on the list.
- Fresh Fable (no context): `analysis/bendigo/fable_fresh.md` (spoons, winding an alarm clock, teaspoon in a mug...).
**Freesound use overnight:** about 330 search requests on the SOUNDMAN key (bot 1 only): fable100 100, wave2 50,
wave3 30, wave4 35, Bendigo 50 + 30 + 30, plus ~10 name lookups. Downloads do not count.
**Next:** owner listens to the packs and says which are closest; search around those. Possible: a combined
CLAP + structure score for Bendigo (no structure scorer yet), and a Freesound run on the top leads with more results
per search.

## Mid North Coast (Sarge's Secret Sound, NSW) — $2,800 on Fri 30 Oct, +$25/weekday (Mon 2 Nov ≈ $2,825)
- Round started 13 May 2026 at $25 (10 plays that morning). Harvest complete: 105 episodes with plays, 423 plays, 200
  segments; every play (`harvest/mnc/plays/*.flac`) and segment (`harvest/mnc/segments/*.mp3`) saved.
- Clue audio: `clues/mnc/clue.wav` (original 0.631 s), `clue_v6b.wav` (owner's clean copy), **`clue_stacked.wav`**
  (median of 415 aligned broadcasts; use this for matching). Stack report (`harvest/mnc/stack/report.txt`): the
  recording common to every broadcast is ~0.05-0.36 s of the original clip; the rest is station background.
- Fresh Fable: `analysis/mnc/fable_fresh_step1.md` (audio only) and `fable_fresh_step2.md` (34 dated hints, revised
  candidates). On-air guesses: `analysis/mnc/onair_guesses.json` (196: 146 wrong, 37 warm, 13 unclear).
- `tools/wrong_filter.py` drops clips of exact wrong on-air actions (object + part + action), never whole objects.
- Rejected by owner's ear: staplers, door handles/latches, hole punches, light switches, BBC ticket machine, SLR shutter,
  binding/office machines, battery/cartridge/SD clips.

## Bendigo (Cogho & Jules' Secret Sound, VIC only) — $750 per page heading, +$25/day
- Clip `clues/bendigo/clue_b.wav` (0.273 s, trimmed both ends; only copy). Clues: I'm a classic / I need a hand /
  I'm old school. Station's wrong list as `analysis/bendigo/onair_guesses.json` (42).

## How to run things
- Freesound is blocked from this cloud IP: use GitHub Actions. `pull-and-score.yml` (inputs: name, queries jobs/*.txt,
  competition mnc|bendigo, per_query, max_seconds, bots default 1, ab, reuse_run to re-score an earlier pull with no
  Freesound requests). `clap-index.yml` ranks the 8,421-clip work zip (competition mnc|bendigo). `harvest.yml` = one
  runner per podcast episode. Results land on branch `results`. Use 1-2 word searches.
- Package: `tools/pack_ab.py <csv> <ab dir> <out> --skip-sent <listening dir>`. BBC works directly (`bbc_pull.py`).
- Local env: `.venv` (`tools/test.sh` runs the tests). The container can restart: background jobs then need restarting
  (clap_index builds are incremental).

## Where the work lives
- `harvest/mnc/`, `clues/`, `listening/` (packs sent), `analysis/{mnc,bendigo}/`, `jobs/` (search lists), `results/local/`.
- `data_manifests/work_zip.tsv` (+ `.url`): the owner's 994 MB OneDrive zip, fetched by `tools/fetch_zip.py`.
