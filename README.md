# Secret Sound

Tools and analysis for **Sarge's Secret Sound** (Triple M Mid North Coast, NSW, $2,800 round).
This repo was put together on 30 Oct 2026 after the work laptop went to sleep partway through
the analysis. Before that, the Secret Sound tools were deliberately kept local (outside
`secret-song-toolkit`).

## What's here and where it came from

| File | Status | Source |
|---|---|---|
| `freesound_pull.py` | **original** | Rebuilt by replaying the original write plus 6 edits from the session log; the same size (7,875 bytes) as the OneDrive backup copy |
| `sfx_match.py` | **original** | Read from the OneDrive backup (`Backups/builds/Personal/_folders/personal/secret-song-toolkit`), 4,567 bytes |
| `sound_id.py`, `candidates.txt` | **original** | Copied from `secret-song-toolkit` main (committed 30 Oct, 11:15) |
| `steel_score.py` | **new** | The fingerprint scorer from the steel/spring brief (`analysis/steel_brief.md`, step 2): evidence per mechanism and A/B files |
| `tests/test_steel_score.py` | **new** | Synthetic checks: a sound built to the measured fingerprint scores 0.98, decoys score far lower |
| `analysis/analysis.md` | **original** | Fable's full acoustic analysis, read back in the session log (the plots and a1–a7 scripts are still only on the laptop) |
| `analysis/fable_handback.md` | original | Fable's summary hand-back |
| `analysis/fable_brief.md` | original | What Fable was asked (the clue, wrong guesses, past winners) |
| `analysis/steel_brief.md` | original | The steel/spring follow-up that was running when the laptop slept |
| `analysis/freesound_mnc_summary.md` | original | Waveform-match run over 13,092 Freesound clips: no exact match (best NCC 0.450) |

## Where the data is
- **Freesound clips (about 1.8 GB) and the `fs_mnc` scoring folder:** on the laptop under
  `secret-song-toolkit\data\`, and backed up to OneDrive under
  `Backups/builds/Personal/_folders/personal/secret-song-toolkit/data/`.
- **The clue:** `OneDrive\Secret Song\secret-sound_mnc_2026-10-30\clue.wav`, crop 0–0.631 s
  (`clue.crop.json`).
- **The Freesound API key:** `~/.secret-song/freesound.key`, never in this repo.

## Running the steel/spring step again

```
python freesound_pull.py data\freesound_steel --queries steel_queries.txt --per-query 150 --max-seconds 30
python steel_score.py data\freesound_steel --meta data\freesound_steel\meta.json --null data\freesound --jobs 4 --csv steel.csv
.venv-sound\Scripts\python sfx_match.py clue.wav data\freesound_steel --out sfx_steel.json
python steel_score.py data\freesound_steel --meta data\freesound_steel\meta.json --sfx-json sfx_steel.json ^
    --ab 5 --clue clue.wav --out "%OneDrive%\Secret Song\secret-sound_mnc_2026-10-30"
```

Calibrate first by running `steel_score.py` on a folder that holds the clue's own 12 plays.
They should score near the top, against the general Freesound set as the null.

`steel_score.py` prints the best stroke pair per file: the gap in ms, ring frequency and T60, the six
feature scores, and then the evidence per search query (count, best score, median of the top 5, which
features match and which never do).
