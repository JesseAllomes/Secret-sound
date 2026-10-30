<!-- drainclamp-build: state; schema=1; generation=20 -->
# DrainClamp state

<!-- DC:ARCH -->
- freesound_pull.py → Freesound API search()/fetch(), key ~/.secret-song/freesound.key, 60 req/min
- pull_queries.py → pull exactly the searches in jobs/*.txt → <folder>/<id>.mp3 + meta.json
- bbc_pull.py → BBC Sound Effects search + mp3 → same meta.json shape
- steel_score.py → MNC fingerprint scorer (strokes B/C, thump, 790 Hz ring, isolation); --ab writes A/B mp3 (clue_v6b then candidate x4); MNC only
- res_score.py → resonance scorer (tone/soft/pitch/mode2, novelty gate); MNC
- sfx_match.py → CLAP (laion/clap-htsat-unfused) + log-mel per-event match of a clue against a clip folder
- sound_id.py → AST/CLAP label guesses for one clip
- extract_guesses.py, harvest/mnc/{harvest.py,find_plays.py,build_package.py} → MNC podcast: NCC play detection, faster-whisper transcription, guesses/jackpot, evidence package
- tools/sync_scratch.sh <scratchpad> → copy session scratch work into repo; tools/scratch/*.py one-off analysis
- .github/workflows/pull-and-score.yml → Freesound pull (1-2 bots) + steel_score + A/B → branch results (MNC only; Freesound blocks this cloud IP)
- clues/{mnc,bendigo}/ clue audio (force-added); listening/mnc/ A/B zips; analysis/{mnc,bendigo}/ write-ups; results/local/ CSVs
- Optimisation vectors: embed clips once and cache (sfx_match re-embeds every run); score on GitHub runners, not this IP-blocked session; short 1-2 word Freesound searches
<!-- /DC:ARCH -->

<!-- DC:DECISIONS -->
- repo -> every Secret Sound file goes to JesseAllomes/Secret-sound branch main; never BuildIt (user)
- separation -> Mid North Coast and Bendigo kept separate in files, indexes, scores and reports (user)
- data collection -> repeatable scripts that use no model tokens (user, CLAUDE.md)
- fable -> fresh no-context Fable for MNC APPROVED once data is ready (m1 done); two steps in one agent: (1) clue audio only -> describe + candidate mechanisms, (2) then transcripts and owner rejections (as owner listening, not exclusions) -> answer phrased as a caller guess + what to test; NO past winners (they anchor a category); give facts only (file meanings, "Absolutely not!" is a catchphrase, auto transcripts), no theories or focus hints (user, 30 Oct)
- exclusions -> none outright; weight candidates; wrong on-air guesses are information (user)
- mechanism -> describe the sound, do not steer with "spring"; resonance may be any mechanical resonance (user)
- jackpot -> record amount and date whenever a segment is transcribed (user)
- api budget -> refine searches before spending Freesound requests; bots input defaults to 1 (user)
- keys -> Freesound keys only in ~/.secret-song/ and GitHub secrets; never printed, logged or committed (user)
- sound-matching index -> yes, build a CLAP embedding index (user, 30 Oct)
- clap model -> laion/clap-htsat-unfused, same as sfx_match.py, CPU torch in repo .venv (repo convention)
- big audio -> ~1 GB work zip stays on Drive/Dropbox; repo holds manifest + checksums + fetch script; >100 MB never in git (repo convention; GitHub limit)
- audio in git -> owner said "everything needs to go there": small clue/listening audio force-added; bulk clip sets re-fetchable by script stay out (user + GitHub limits)
- dc state -> commit and push .agent/ (state, project json, resume, log archive) to GitHub after every DrainClamp write, always (user, 30 Oct)
- stacking -> align every broadcast play and stack (median/mean) for a cleaner clue and to test whether the recording runs past our crop (user, 30 Oct)
- wrong guesses -> drop clips matching an exact on-air WRONG guess, by action not object (pushing the microwave button != closing the microwave door); warm/unclear matches kept and marked; searches stay object-level (tools/wrong_filter.py + analysis/mnc/onair_guesses.json) (user, 30 Oct)
- mnc ear (31 Oct) -> only "Key_Old_Recorder" sounds close: not it, but the button mechanism is close (piano-key latching button); keyboards, disk tray, others "way off"; tape decks/recorders/CD players/old radio buttons already guessed wrong on air (user)
- bendigo ear (31 Oct) -> grandfather-clock winding (freesound 27149) is the closest of everything; pitch-shifted versions (up or down) were not closer; lever, vending, rotary dial, bike wheel, bigger winders (wave 4) are further off. Lead answer: "winding up a grandfather clock" (fits classic / need a hand / old school; not on the wrong list) (user)
- sound downloads -> ONLY through GitHub workflows (Freesound, BBC, full clips via fetch-clips.yml); never pulled in the cloud session (user, 31 Oct)
- listening -> ONLY A/B files: clue then a candidate excerpt of the same length (x4); never send full recordings (user, 31 Oct)
- mnc ear (31 Oct, rice cooker check) -> none of the rice cooker / toaster-lever library clips match; closest is Rice_cooker_C (Freesound 211926) but not right; old recorder key remains the closest overall (user)
<!-- /DC:DECISIONS -->

<!-- DC:ROADMAP -->
| id | goal | files | status | deps |
|---|---|---|---|---|
| m1 | MNC harvest reaches round start; rebuild evidence package; sync into repo | harvest/mnc/harvest.jsonl;harvest/mnc/package/mnc_evidence.md;STATUS.md | done | |
| m2 | CLAP sound-matching index: embed clip folders once, cache, rank against a clue (MNC and Bendigo separately) | clap_index.py;tests/test_clap_index.py;requirements.txt;README.md | active | |
| m3 | import the ~1 GB work zip: fetch from share link, manifest with checksums, index it with m2 | tools/fetch_zip.sh;data_manifests/work_zip.tsv | pending | m2 |
| m4 | fresh no-context Fable on MNC evidence (only if owner approves) | analysis/mnc/fable_fresh.md | done | m1 |
| m5 | next refined Freesound/BBC run from m2/m4 leads, A/B for owner | jobs/mnc_next.txt | active | m2 |
| m6 | Bendigo: fresh Fable analysis, search (Freesound bendigo mode + BBC), CLAP rank 0.28 s window, wrong-list filter, A/B | analysis/bendigo/fable_fresh.md;jobs/bendigo_fable.txt;analysis/bendigo/onair_guesses.json | active | |
<!-- /DC:ROADMAP -->

<!-- DC:VERIFY -->
```json
[
  {"id": "unit", "argv": ["bash", "tools/test.sh"], "cwd": ".", "tier": "fast", "timeout_s": 600}
]
```
<!-- /DC:VERIFY -->

<!-- DC:LOG -->
- 2026-10-30T13:43:35+00:00 d3338524 m1 done: harvest back to round start 13 May ($25), 423 plays saved, stack of 415, evidence package rebuilt; Fable step 1 running
- 2026-10-30T14:40:03+00:00 86ce44c1 Overnight: fable steps done; 196 on-air guesses + strict wrong filter; pack 1 sent; Bendigo fresh Fable done, searches running
- 2026-10-30T17:17:45+00:00 e6f3b7f6 Overnight: MNC waves 2-4 + combined ranking (keyboard/player push-buttons lead); Bendigo work zip + BBC + waves 2-3 (lever pull 0.855); STATUS.md morning summary
<!-- /DC:LOG -->
