#!/usr/bin/env bash
# Copy a cloud session's scratchpad work into this repo (scripts, transcripts, results, small listening files).
#   tools/sync_scratch.sh <scratchpad dir>
# Leaves out what scripts can fetch again: podcast episodes and feeds, Freesound/BBC clip sets, temp renders.
set -euo pipefail
P=${1:?scratchpad dir}
R=$(cd "$(dirname "$0")/.." && pwd)
cp_some() { local dst=$1; shift; mkdir -p "$R/$dst"; for f in "$@"; do [ -e "$f" ] && cp -r "$f" "$R/$dst/"; done; return 0; }

# Mid North Coast podcast harvest
cp_some harvest/mnc "$P"/pods/{harvest.py,find_plays.py,build_package.py,extract_guesses.py,eps.json,harvest.jsonl,harvest.log,guesses.tsv,guesses.txt}
cp_some harvest/mnc "$P"/pods/transcripts
cp_some harvest/mnc/package "$P"/pods/package/mnc_evidence.md
# Mid North Coast clue versions and listening files
cp_some clues/mnc "$P"/aud/clue_v{3,4,5,6,7}.wav "$P"/aud/clue_clean.wav "$P"/aud/clue_bgnotch.wav "$P"/aud/clue_*x[234].mp3 \
  "$P"/aud/ring_after-second-click_only_x4.mp3
cp_some listening/mnc "$P"/aud/AB_*.zip "$P"/aud/ab_light.mp3 "$P"/aud/ab_mnc_over80/INDEX.txt
# Mid North Coast local scoring output and helper scripts
cp_some results/local "$P"/aud/{steel.csv,res_steel.csv,mnc_bbc_office.scores.csv}
cp_some tools/scratch "$P"/aud/*.py
cp_some analysis/mnc/research "$P"/research/*.md "$P"/research/*.py
# Bendigo
cp_some clues/bendigo "$P"/bendigo/{bendigo_secret_sound_210926.mp3,bendigo_secret_sound_x4.mp3,clue_b.wav}
cp_some harvest/bendigo "$P"/bendigo/{eps.json,s.json}
cp_some analysis/bendigo/fable "$P"/bendigo/fable/*.py "$P"/bendigo/fable/*.png

cd "$R"
git add -A tools harvest analysis results
git add -f clues listening
git status --short | sed -n '1,200p'
