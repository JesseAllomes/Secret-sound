"""Synthetic checks for steel_score: a sound built to the measured fingerprint must beat decoys."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import steel_score as ss  # noqa: E402

SR = ss.SR
rng = np.random.default_rng(7)


def click(n_ms=1.5, amp=1.0):
    n = int(n_ms * SR / 1000)
    return amp * rng.standard_normal(n) * np.exp(-np.arange(n) / (n / 4))


def add(y, t, x):
    a = int(t * SR)
    y[a:a + len(x)] += x[:len(y) - a]


def thump(amp):
    t = np.arange(int(0.25 * SR)) / SR
    return amp * np.sin(2 * np.pi * 62 * t) * np.exp(-t * 2 * np.pi * 62 / (2 * 10))


def ring(amp, t60=0.33, f=790):
    t = np.arange(int(0.45 * SR)) / SR
    return amp * np.sin(2 * np.pi * f * t) * 10 ** (-3 * t / t60)


def clue_like(gap=0.137):
    y = 1e-4 * rng.standard_normal(int(0.8 * SR))
    tb = 0.115
    tc = tb + gap
    add(y, tb - 0.053, click(amp=0.25))                    # pre-click A, about -12 dB
    for k in range(5):                                     # B: five micro-impacts over 50 ms
        add(y, tb + k * 0.011, click(amp=0.9 - 0.1 * k))
    add(y, tc, click(amp=1.0))                             # C: one clean snap
    add(y, tb + 0.024, thump(0.5))                         # 62 Hz thump lagging each stroke
    add(y, tc + 0.024, thump(0.5))
    add(y, tc, ring(0.3))                                  # long 790 Hz ring after C
    add(y, tb, ring(0.03, t60=0.08))                       # weak, damped ring after B
    return y


def decoy_single():
    y = 1e-4 * rng.standard_normal(int(0.8 * SR))
    add(y, 0.2, click(amp=1.0))
    return y


def decoy_pop():
    """Two plastic-ish clicks far apart, no thump, no ring, a reverberant noise tail."""
    y = 1e-4 * rng.standard_normal(int(1.0 * SR))
    add(y, 0.10, click(amp=1.0))
    add(y, 0.33, click(amp=0.8))
    t = np.arange(int(0.5 * SR)) / SR
    add(y, 0.33, 0.05 * rng.standard_normal(len(t)) * np.exp(-t / 0.15))
    return y


def test_clue_like_scores_high_with_measured_gap():
    f = ss.score_signal(clue_like())
    assert f is not None
    assert abs(f["gap_ms"] - 137) < 6
    assert 700 <= f["ring_hz"] <= 880
    assert f["ring_t60"] > 0.15
    assert f["crunch"] >= 0.8 and f["pre"] >= 0.9
    assert f["score"] > 0.7


def test_timing_tolerance():
    near = ss.score_signal(clue_like(gap=0.150))["score"]
    far = ss.score_signal(clue_like(gap=0.240))["score"]
    assert near > far


def test_decoys_score_lower():
    good = ss.score_signal(clue_like())["score"]
    assert ss.score_signal(decoy_single()) is None
    pop = ss.score_signal(decoy_pop())
    assert pop is None or pop["score"] < good - 0.3


def test_mechanism_report_groups_by_query():
    base = {n: 0.5 for n in ss.WEIGHTS}
    rows = [{**base, "score": s, "query": q} for s, q in [(0.9, "stapler"), (0.8, "stapler"), (0.2, "lid")]]
    rep = ss.mechanism_report(rows)
    assert rep[0]["query"] == "stapler" and rep[0]["n"] == 2 and rep[0]["best"] == 0.9
