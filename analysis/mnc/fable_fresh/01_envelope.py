"""Envelope, onsets and coarse timeline of the clue (original and stacked).
All times printed in ORIGINAL clip time (stacked t - 0.05)."""
import numpy as np, soundfile as sf, scipy.signal as ss, sys, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

ROOT = '/home/user/secret-sound'
OUT = os.path.join(ROOT, 'analysis/mnc/fable_fresh')
orig, sr = sf.read(f'{ROOT}/clues/mnc/clue.wav')
stk, sr2 = sf.read(f'{ROOT}/clues/mnc/clue_stacked.wav')
assert sr == sr2 == 48000
OFF = 0.05  # stacked t = orig t + 0.05

def env_db(x, win_ms=1.0):
    n = int(sr*win_ms/1000)
    e = np.sqrt(np.convolve(x**2, np.ones(n)/n, mode='same'))
    return 20*np.log10(e+1e-9)

def band(x, lo, hi, order=4):
    sos = ss.butter(order, [lo, hi], btype='band', fs=sr, output='sos')
    return ss.sosfiltfilt(sos, x)

t_o = np.arange(len(orig))/sr
t_s = np.arange(len(stk))/sr - OFF

# 1 ms envelope table, 5 ms steps, stacked
print("=== stacked, 1 ms RMS envelope (dB re full scale), printed every 5 ms, orig time ===")
E = env_db(stk, 1.0)
for i in range(0, len(stk), int(sr*0.005)):
    print(f"{t_s[i]:+.3f}s  {E[i]:6.1f} dB  {'#'*int(max(0,E[i]+70)//2)}")

# Onsets: fast attack detection on the 0.25 ms envelope slope
Ef = env_db(stk, 0.25)
Ebg = np.median(Ef[(t_s< -0.02)])
print(f"\nstacked background level before clip (0.25 ms env median): {Ebg:.1f} dB")
# find local maxima of envelope > bg+15 separated by 8 ms
pk, pr = ss.find_peaks(Ef, height=Ebg+15, distance=int(sr*0.008), prominence=6)
print("\n=== envelope peaks (stacked), orig time, level, prominence ===")
for p, h, pm in zip(pk, pr['peak_heights'], pr['prominences']):
    print(f"  t={t_s[p]:+.4f}s  {h:6.1f} dB  prom {pm:4.1f}")

# Same on original for cross-check
Efo = env_db(orig, 0.25)
Ebgo = np.median(Efo[t_o<0.03])
pko, pro = ss.find_peaks(Efo, height=Ebgo+12, distance=int(sr*0.008), prominence=6)
print(f"\noriginal background (first 30 ms) {Ebgo:.1f} dB; peaks:")
for p, h, pm in zip(pko, pro['peak_heights'], pro['prominences']):
    print(f"  t={t_o[p]:+.4f}s  {h:6.1f} dB  prom {pm:4.1f}")

# Band envelopes
bands = [(20,150),(150,500),(500,1500),(1500,4000),(4000,8000),(8000,16000),(16000,23000)]
fig, ax = plt.subplots(len(bands)+2, 1, figsize=(14, 2.2*(len(bands)+2)), sharex=True)
ax[0].plot(t_s, stk, lw=0.4); ax[0].set_ylabel('stacked'); ax[0].set_xlim(-0.05, 0.45)
ax[1].plot(t_o, orig, lw=0.4); ax[1].set_ylabel('orig')
for k,(lo,hi) in enumerate(bands):
    ax[k+2].plot(t_s, env_db(band(stk,lo,hi),1.0), lw=0.7, label='stacked')
    ax[k+2].plot(t_o, env_db(band(orig,lo,hi),1.0), lw=0.7, alpha=0.6, label='orig')
    ax[k+2].set_ylabel(f'{lo}-{hi}'); ax[k+2].set_ylim(-80,-5)
ax[2].legend(loc='upper right')
ax[-1].set_xlabel('orig time (s)')
plt.tight_layout(); plt.savefig(f'{OUT}/env_bands.png', dpi=110)

print("\n=== band envelope peaks (stacked, 1 ms env), per band ===")
for lo,hi in bands:
    e = env_db(band(stk,lo,hi),1.0)
    bg = np.median(e[t_s<-0.02])
    pk, pr = ss.find_peaks(e, height=bg+10, distance=int(sr*0.010), prominence=5)
    s = ', '.join(f"{t_s[p]:+.3f}s/{h:.0f}dB" for p,h in zip(pk, pr['peak_heights']))
    print(f"  {lo:5d}-{hi:5d} Hz  bg {bg:6.1f}:  {s}")
