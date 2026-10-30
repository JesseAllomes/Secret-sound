<!-- drainclamp-build: state; schema=1; generation=5 -->
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
- fable -> never started unless the owner asks in the conversation; fresh no-context Fable for MNC asked, not yet answered (user)
- exclusions -> none outright; weight candidates; wrong on-air guesses are information (user)
- mechanism -> describe the sound, do not steer with "spring"; resonance may be any mechanical resonance (user)
- jackpot -> record amount and date whenever a segment is transcribed (user)
- api budget -> refine searches before spending Freesound requests; bots input defaults to 1 (user)
- keys -> Freesound keys only in ~/.secret-song/ and GitHub secrets; never printed, logged or committed (user)
- sound-matching index -> yes, build a CLAP embedding index (user, 30 Oct)
- clap model -> laion/clap-htsat-unfused, same as sfx_match.py, CPU torch in repo .venv (repo convention)
- big audio -> ~1 GB work zip stays on Drive/Dropbox; repo holds manifest + checksums + fetch script; >100 MB never in git (repo convention; GitHub limit)
- audio in git -> owner said "everything needs to go there": small clue/listening audio force-added; bulk clip sets re-fetchable by script stay out (user + GitHub limits)
<!-- /DC:DECISIONS -->

<!-- DC:ROADMAP -->
| id | goal | files | status | deps |
|---|---|---|---|---|
| m1 | MNC harvest reaches round start; rebuild evidence package; sync into repo | harvest/mnc/harvest.jsonl;harvest/mnc/package/mnc_evidence.md;STATUS.md | active | |
| m2 | CLAP sound-matching index: embed clip folders once, cache, rank against a clue (MNC and Bendigo separately) | clap_index.py;tests/test_clap_index.py;requirements.txt;README.md | pending | |
| m3 | import the ~1 GB work zip: fetch from share link, manifest with checksums, index it with m2 | tools/fetch_zip.sh;data_manifests/work_zip.tsv | pending | m2 |
| m4 | fresh no-context Fable on MNC evidence (only if owner approves) | analysis/mnc/fable_fresh.md | pending | m1 |
| m5 | next refined Freesound/BBC run from m2/m4 leads, A/B for owner | jobs/mnc_next.txt | pending | m2 |
<!-- /DC:ROADMAP -->

<!-- DC:VERIFY -->
```json
[
  {"id": "unit", "argv": [".venv/bin/python", "-m", "pytest", "-q", "tests/"], "cwd": ".", "tier": "fast", "timeout_s": 600}
]
```
<!-- /DC:VERIFY -->

<!-- DC:LOG -->
<!-- /DC:LOG -->
