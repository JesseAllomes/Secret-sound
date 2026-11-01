# Session status (31 Oct 2026 evening) — read this first after a context reset

Owner rules: CLAUDE.md, plus (DC:DECISIONS in .agent/drainclamp-state.md): never start Fable unless asked; keep MNC and
Bendigo separate; ALL sound downloads only through GitHub workflows (Freesound, BBC, fetch-clips); listening = A/B only
(clue then a same-length candidate slice, x4, single mp3s, never full recordings, no zips unless asked); push DC state
after every DrainClamp write (`tools/dc_push.sh`); drop only exact wrong on-air actions, never whole objects.

## Where it stands
**Bendigo (VIC, owner can enter) — call: "Winding up an old wind-up alarm clock"** (`analysis/bendigo/fable_final.md`).
- Owner's ear: grandfather-clock winding (Freesound 27149) is the closest of everything: "same ratchet cadence, just a
  differing pitch or resonance". Pitch-shifting it did not help. Everything non-ratchet was way off; library alarm /
  mantel / cuckoo / toy / timer recordings were not closer (libraries lack clean small-clock winding takes).
- Fable: same click-pawl ratchet as the clock, smaller damped resonator (2.32/2.55 kHz pair = twin bells), key flips;
  fits I'm a classic / I need a hand / I'm old school; "clock ticking" is the only clock on the wrong list.
  Backups: grandfather clock, mantel clock with key, cuckoo clock chain, carriage clock, playing the spoons.
- Podcast: all 887 Cogho & Jules episodes transcribed (`analysis/bendigo/podcast_hits.md`): nothing about this sound;
  previous sound won 16 Sep 2026. Page (`node tools/bendigo_page.js`): unchanged, 42 wrong guesses, $750 heading.
**Mid North Coast (NSW) — call: "Pushing the lever down on a rice cooker"** (`analysis/mnc/fable_final.md`), reasoned,
  NOT confirmed by ear: two independent Fables chose it (sound = spring lever travel, stop, latch snap in a small
  plastic/thin-steel housing; Sarge's "pushing the ... down / to turn it on" hints; "cheap and tacky"; never guessed).
- Owner's ear: only Freesound 641862 "Key_Old_Recorder" sounds close ("not it, but the button mechanism is close";
  best slice 7.04 s, 0.883). Way off: keyboards, fans (owner's own hunch), disc trays, lids, staplers, switches, latches,
  clips, camera shutter, binding machines. Library rice cooker / toaster-lever clips: none match (closest
  Rice_cooker_C 211926). Recorder key has no pack/useful metadata; Freesound "similar sounds" sent (turn-signal stalk,
  Keurig, bike levers, A/C knob, calculator) — awaiting owner's ear.
- Fable reports: fable_fresh_step1/2.md, fable_recorder.md, fable_final.md. Backups: toaster lever, SodaStream, bin
  lid button, push light, VCR play/eject.

## Next
- Owner's ear on the recorder-similar A/Bs (`listening/mnc/recorder_similar/`); search around anything close.
- Owner decides whether to call either station with the calls above.

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
