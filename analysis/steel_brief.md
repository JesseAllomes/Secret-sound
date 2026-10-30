# Steel/spring follow-up brief (30 Oct 2026, 18:55 AEDT; the run stopped when the laptop slept)

Next task: test your steel/spring-lever reading against real recordings until one mechanism clearly wins. The user says 18% is too low.

1. TARGETED PULL. Use `C:\Users\jallomes\Projects\personal\secret-song-toolkit\freesound_pull.py`.
   - Key: `~/.secret-song/freesound.key`.
   - Limit is 60 API calls a minute. The script already spaces its calls; leave that alone.
   - Write a queries file to your scratch folder, then run: `python freesound_pull.py <toolkit>\data\freesound_steel --queries <file> --per-query 150 --max-seconds 30`.
   - Use many phrasings for each mechanism, for example:
     - staplers: stapler, stapling paper, desk stapler, heavy duty stapler, long arm stapler, stapler empty, staple gun;
     - door handles: door handle, door lever handle, door handle press release, door latch;
     - stamps: date stamp, self inking stamp, rubber stamp, office stamp;
     - binders: ring binder, binder rings, lever arch file;
     - clips: clipboard, bulldog clip, fold back clip, money clip;
     - nail clippers, metal torch switch, toggle switch metal, light switch;
     - toaster lever, pedal bin, label maker, price gun, embosser, paper punch;
     - spring latch, spring clamp, mousetrap, garlic press, secateurs, tin snips;
     - anything else your physics points to.
   - Already-pulled ids are skipped. The 15,421 general effects in `data\freesound` stay as a baseline.

2. FINGERPRINT SCORER. A library take will never be sample-identical, so waveform NCC is the wrong test. Build the score from your measured facts, applied to every candidate stroke pair in every file:
   - pre-click, then stroke, then a second stroke about 137 ms later;
   - the first stroke is a multi-impact crunch, the second a single clean snap;
   - a low-frequency thump lagging each stroke by 20–30 ms;
   - a narrow, long-T60 ring at 600–1000 Hz after the second stroke, weaker after the first;
   - a dry recording.
   Allow timing tolerance, since people press at different speeds; report the gap you find. Combine this with the CLAP/mel event similarity in `sfx_match.py` (`.venv-sound`). Calibrate on the clue's own 12 plays (they should score near the top) and on the general set as a null.

3. EVIDENCE PER MECHANISM. For each mechanism, report:
   - how many recordings it has;
   - the best score and the median of its top 5;
   - which features match and which never do.
   Then update the ranked list with real confidences. Base them on that evidence, not on priors.

4. A/B FILES for the top 5 individual recordings across all mechanisms.
   - Format: the clue (user crop 0–0.631 s, untouched; never re-trim the clue yourself), a short gap, then the matched candidate excerpt of the same length starting at its aligned event. Repeat that pair ×4, as mp3.
   - Name them `AB_steel<n>_<mechanism>_<freesoundid>.mp3`.
   - Write them to `C:\Users\jallomes\OneDrive\Secret Song\secret-sound_mnc_2026-10-30\`.

Rules:
- Everything stays local. No git commits or pushes; Secret Sound stays out of the repos.
- Run heavy jobs at low priority.
- Don't touch the song collector process (PID 49712).
- No desktop windows or pop-ups.
- Kill only processes you started.
- Write the report as `analysis_steel.md` next to `analysis.md`.

Hand back:
- the revised top 5 with confidences;
- the A/B file paths;
- one line per mechanism on what its evidence showed.
