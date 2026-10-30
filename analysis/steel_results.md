# Steel/spring run (30 Oct 2026, cloud session)

Re-run of the steel/spring brief (`steel_brief.md`) after the laptop slept. 842 Freesound recordings
were pulled through the API for the 38 queries in `steel_queries.txt`, and scored with `steel_score.py`.
The null set was 514 generic everyday-object clips (321 had a stroke pair).

## Calibration on the real clue
The clue was taken from the user's `mnc_secret-sound_x4.mp3`. All 4 plays, and the clue inside the
BBC light-switch A/B file, measure identically: B→C gap 138.2 ms, ring 792 Hz with T60 0.47 s,
thumps 40 ms after each stroke, a 5-impact crunch and then a 3-impact snap, and the ring after C
17.5 dB stronger than after B. **Clue score 0.99.**

- Null: median 0.617, robust sd 0.081, p99 0.834.
- BBC light switch 07059069 (the closest one the user had heard): 0.888. Same gap and thump, but its
  first click is not a crunch, and both clicks ring equally (-2 dB), where the clue's second click rings 17.5 dB louder.

## Top 20
```
602 files with a stroke pair. Top 20 by score:
  1  0.899  gap 127.5 ms  ring  708 Hz T60 0.14  [gap 0.97 pre 1.00 crunch 1.00 thump 0.95 ring 0.65 dry 1.00 iso 1.00]  door handle turn.wav
  2  0.883  gap 145.2 ms  ring  713 Hz T60 0.41  [gap 0.98 pre 0.00 crunch 0.67 thump 1.00 ring 0.95 dry 0.97 iso 1.00]  Door-Handle-Open-01.wav
  3  0.873  gap 160.5 ms  ring  624 Hz T60 0.46  [gap 0.84 pre 0.40 crunch 1.00 thump 0.82 ring 0.82 dry 0.95 iso 1.00]  Door-Handle-Jiggle-01.wav
  4  0.870  gap 139.2 ms  ring  920 Hz T60 0.31  [gap 1.00 pre 0.00 crunch 1.00 thump 0.87 ring 0.89 dry 0.65 iso 0.92]  3holepunch1.wav
  5  0.854  gap 146.2 ms  ring  809 Hz T60 3.62  [gap 0.97 pre 1.00 crunch 0.67 thump 1.00 ring 0.63 dry 1.00 iso 1.00]  newport-hotel-door-lock.aif
  6  0.852  gap 142.4 ms  ring 1175 Hz T60 0.60  [gap 0.99 pre 1.00 crunch 0.67 thump 1.00 ring 0.61 dry 1.00 iso 1.00]  stamp, stamping, document, office
  7  0.845  gap 135.5 ms  ring  655 Hz T60 0.57  [gap 1.00 pre 0.00 crunch 0.50 thump 1.00 ring 0.88 dry 0.99 iso 1.00]  Small door latch (Contact mic)
  8  0.837  gap 139.9 ms  ring 1022 Hz T60 1.06  [gap 1.00 pre 0.00 crunch 0.83 thump 0.98 ring 0.66 dry 1.00 iso 1.00]  Staple Gun Shooting.wav
  9  0.836  gap 154.6 ms  ring  888 Hz T60 0.48  [gap 0.91 pre 1.00 crunch 0.50 thump 0.75 ring 0.89 dry 0.79 iso 1.00]  door wood gnarly apartment heavy back door to balcony push closed catch squeak,
 10  0.831  gap 131.3 ms  ring  776 Hz T60 0.33  [gap 0.99 pre 0.40 crunch 0.67 thump 0.88 ring 0.75 dry 0.87 iso 1.00]  short creaks creek creaky door open close.wav
 11  0.829  gap 126.6 ms  ring  508 Hz T60 0.84  [gap 0.97 pre 1.00 crunch 1.00 thump 0.85 ring 0.45 dry 0.88 iso 1.00]  CheckPress_STAMP_Fast_02.wav
 12  0.824  gap 106.9 ms  ring  639 Hz T60 1.07  [gap 0.75 pre 1.00 crunch 1.00 thump 0.91 ring 0.77 dry 0.20 iso 0.87]  door-shutting-opening.m4a
 13  0.821  gap 110.6 ms  ring 1095 Hz T60 0.20  [gap 0.80 pre 1.00 crunch 0.50 thump 1.00 ring 0.79 dry 0.56 iso 1.00]  Creaky wooden door handle (open & close)
 14  0.821  gap 170.7 ms  ring 1019 Hz T60 0.66  [gap 0.70 pre 1.00 crunch 0.83 thump 0.73 ring 0.78 dry 0.72 iso 1.00]  door latch.wav
 15  0.819  gap 140.5 ms  ring  754 Hz T60 0.46  [gap 1.00 pre 0.40 crunch 1.00 thump 0.76 ring 0.71 dry 0.54 iso 0.91]  door wood gnarly apartment heavy front door with loose handle latch open close 
 16  0.818  gap 135.2 ms  ring  655 Hz T60 0.63  [gap 1.00 pre 0.00 crunch 0.67 thump 0.86 ring 0.76 dry 1.00 iso 1.00]  Stapler On Paper
 17  0.817  gap 128.9 ms  ring  764 Hz T60 0.21  [gap 0.98 pre 0.00 crunch 0.75 thump 0.81 ring 0.76 dry 0.92 iso 1.00]  Paper Scrawling
 18  0.810  gap 139.4 ms  ring 1049 Hz T60 0.72  [gap 1.00 pre 0.00 crunch 1.00 thump 0.97 ring 0.50 dry 0.78 iso 1.00]  Paper Tearing
 19  0.808  gap 123.4 ms  ring  791 Hz T60 0.41  [gap 0.94 pre 1.00 crunch 0.67 thump 0.65 ring 0.68 dry 1.00 iso 1.00]  Light_Switch-0001-On-Held.wav
 20  0.807  gap 121.6 ms  ring  687 Hz T60 1.06  [gap 0.93 pre 1.00 crunch 1.00 thump 0.56 ring 0.55 dry 0.93 iso 1.00]  Door Handle 02
```

## Evidence per mechanism
```
  door handle                      n= 123 best 0.899 median-top5 0.873  matches gap,pre,crunch,thump,ring,dry,iso  never -
  door latch                       n= 109 best 0.854 median-top5 0.836  matches gap,pre,crunch,thump,ring,dry,iso  never -
  stapler                          n= 107 best 0.818 median-top5 0.789  matches gap,pre,crunch,thump,ring,dry,iso  never -
  light switch                     n=  22 best 0.808 median-top5 0.782  matches gap,pre,thump,dry,iso  never -
  office stamp                     n=  16 best 0.852 median-top5 0.769  matches gap,pre,crunch,thump,dry,iso  never -
  paper punch                      n=  27 best 0.870 median-top5 0.730  matches gap,crunch,thump,ring,dry,iso  never -
  mousetrap                        n=   9 best 0.749 median-top5 0.722  matches gap,crunch,thump,dry,iso  never pre
  ring binder                      n=   1 best 0.720 median-top5 0.720  matches gap,pre,ring,dry,iso  never -
  toaster lever                    n=   7 best 0.782 median-top5 0.716  matches gap,crunch,thump,ring,dry,iso  never -
  clipboard                        n=  46 best 0.817 median-top5 0.711  matches gap,crunch,thump,ring,dry  never -
  staple gun                       n=  17 best 0.837 median-top5 0.691  matches gap,crunch,thump,ring,dry,iso  never -
  stapling paper                   n=  13 best 0.810 median-top5 0.687  matches gap,pre,crunch,thump,dry,iso  never -
  price gun                        n=   4 best 0.732 median-top5 0.675  matches gap,iso  never -
  self inking stamp                n=  15 best 0.741 median-top5 0.670  matches gap,crunch,thump,ring,dry  never -
  nail clippers                    n=  12 best 0.705 median-top5 0.669  matches gap,thump,dry,iso  never -
  rubber stamp                     n=   6 best 0.772 median-top5 0.663  matches gap,crunch,thump,ring,dry,iso  never -
  door lever handle                n=  13 best 0.763 median-top5 0.663  matches gap,crunch,thump,ring,dry,iso  never -
  metal torch switch               n=   2 best 0.669 median-top5 0.659  matches gap,thump,dry,iso  never pre
  toggle switch metal              n=   5 best 0.745 median-top5 0.655  matches gap,thump,dry,iso  never pre
  date stamp                       n=   1 best 0.643 median-top5 0.643  matches gap,pre,crunch,thump,ring  never dry,iso
  spring latch                     n=   6 best 0.759 median-top5 0.641  matches gap,crunch,thump,ring,dry,iso  never pre
  money clip                       n=  16 best 0.723 median-top5 0.638  matches gap,pre,crunch,thump,dry  never -
  fold back clip                   n=   4 best 0.639 median-top5 0.621  matches gap,pre,thump,ring,dry  never iso
  embosser                         n=   3 best 0.627 median-top5 0.616  matches gap,pre,crunch,thump,dry  never iso
  label maker                      n=   9 best 0.635 median-top5 0.615  matches gap,pre,thump,ring  never dry,iso
  garlic press                     n=   1 best 0.608 median-top5 0.608  matches gap,pre,crunch,thump,dry  never iso
  spring clamp                     n=   2 best 0.578 median-top5 0.567  matches gap,thump  never -
  secateurs                        n=   1 best 0.556 median-top5 0.556  matches gap,pre,crunch,ring,dry  never iso
  pedal bin                        n=   4 best 0.697 median-top5 0.542  matches gap,pre,crunch,ring  never -
  stapler empty                    n=   1 best 0.424 median-top5 0.424  matches thump,ring,dry  never gap,pre,iso
```

## Reading
- **Door handle leads on the evidence** (median of the top 5: 0.873), then door latch (0.836), then
  stapler (0.789) and light switch (0.782). Fable's #2 beats its #1.
- No recording reaches the clue's own 0.99. The best is 0.90. That's expected for a different take,
  but it means none of these is the exact recording.
- The 3-hole punch scores 0.87 at #4, which fits the on-air hint that a hole punch was "close but wrong".
- A/B files for the top 5 plus the 3 best staplers: `AB_steel1..8_*.mp3`, sent to the user on 30 Oct
  (audio isn't kept in the repo).
