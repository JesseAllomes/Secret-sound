# Working rules for this repo (set by the owner)

- Collect and collate data with repeatable scripts that use no model tokens: downloads, podcast harvesting, play detection,
  transcription, guess/jackpot extraction, scoring, A/B building. Prefer extending a script over doing the work by hand.
- Never start Fable (or any Fable-model agent) unless the owner asks for it in that conversation. Fable is reserved for complex
  analysis, critical thinking or outside-the-box thinking.
- Don't exclude candidates outright; weight them. Wrong guesses made on air are information, not exclusions.
- Don't steer analysis with an unproven mechanism (e.g. "spring"); describe the sound, derive the mechanism from measurements.
- Whenever a podcast segment is transcribed, record the jackpot amount and date said on air.
- Audio, data and API keys stay out of git (see .gitignore).
