"""Annotated overview figure: stacked waveform, >2 kHz click envelope, <250 Hz thud waveform, 791 Hz band."""
import numpy as np, soundfile as sf, scipy.signal as ss
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
ROOT = '/home/user/secret-sound'; OUT = f'{ROOT}/analysis/mnc/fable_fresh'
stk, sr = sf.read(f'{ROOT}/clues/mnc/clue_stacked.wav'); OFF = 0.05
t = np.arange(len(stk))/sr - OFF
def env(x, ms):
    n = int(sr*ms/1000); return 20*np.log10(np.sqrt(np.convolve(x**2, np.ones(n)/n, 'same'))+1e-9)
hp = ss.sosfiltfilt(ss.butter(4, 2000, 'high', fs=sr, output='sos'), stk)
lp = ss.sosfiltfilt(ss.butter(4, 250, 'low', fs=sr, output='sos'), stk)
b791 = ss.sosfiltfilt(ss.butter(4, [771, 811], 'band', fs=sr, output='sos'), stk)
fig, ax = plt.subplots(4, 1, figsize=(14, 11), sharex=True)
ax[0].plot(t, stk, lw=0.5); ax[0].set_ylabel('waveform (stacked)')
for name, tt, y in [('A', 0.0635, 0.5), ('B', 0.1175, 0.85), ('C', 0.2507, 0.95), ('D', 0.345, 0.3)]:
    ax[0].annotate(name, (tt, y), fontsize=12, ha='center')
ax[0].annotate('thud', (0.150, -0.55), fontsize=10, ha='center'); ax[0].annotate('thud', (0.287, -0.55), fontsize=10, ha='center')
ax[1].plot(t, env(hp, 0.5), lw=0.7); ax[1].set_ylabel('>2 kHz env (dB)'); ax[1].set_ylim(-75, 0)
ax[2].plot(t, lp, lw=0.8); ax[2].set_ylabel('<250 Hz waveform')
ax[3].plot(t, env(b791, 2), lw=0.8); ax[3].set_ylabel('791 Hz band (dB)'); ax[3].set_ylim(-80, -15)
for a in ax:
    a.grid(alpha=.3); a.set_xlim(0.02, 0.40)
    for tt in [0.0635, 0.1175, 0.2507, 0.345]: a.axvline(tt, color='r', lw=0.5, alpha=0.5)
ax[-1].set_xlabel('time from original clip start (s)')
plt.tight_layout(); plt.savefig(f'{OUT}/overview.png', dpi=100)
