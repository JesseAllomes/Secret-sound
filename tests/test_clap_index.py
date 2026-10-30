"""clap_index with a stand-in embedder (no model download): incremental build, ranking and A/B files."""
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import clap_index as ci  # noqa: E402

SR = ci.SR
rng = np.random.default_rng(3)


class Spectral:
    """Unit-length average log spectrum: similar sounds point the same way. Counts its calls."""

    calls = 0

    def embed(self, clips):
        Spectral.calls += len(clips)
        out = []
        for c in clips:
            s = np.log1p(np.abs(np.fft.rfft(c, 4096))[:1024])
            s = s - s.mean()
            out.append(s / (np.linalg.norm(s) + 1e-9))
        return np.array(out, np.float32)


def tone_hit(f, n=int(0.3 * SR)):
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * t) * np.exp(-t * 12)).astype(np.float32)


def clip(hit, at=0.5, length=1.5):
    y = 0.001 * rng.standard_normal(int(length * SR)).astype(np.float32)
    a = int(at * SR)
    y[a:a + len(hit)] += hit
    return y


def make_folder(tmp):
    d = tmp / "clips"
    d.mkdir()
    sf.write(d / "match.wav", clip(tone_hit(790)), SR)
    sf.write(d / "low.wav", clip(tone_hit(150)), SR)
    sf.write(d / "high.wav", clip(tone_hit(4000)), SR)
    (d / "meta.json").write_text('{"match": {"id": 1, "name": "the one", "query": "test hit"}}')
    return d


def test_build_is_incremental(tmp_path):
    d = make_folder(tmp_path)
    assert ci.build(d, Spectral(), win=0.32, log=lambda *_: None) == 3
    before = Spectral.calls
    assert ci.build(d, Spectral(), win=0.32, log=lambda *_: None) == 0
    assert Spectral.calls == before
    sf.write(d / "extra.wav", clip(tone_hit(300)), SR)
    assert ci.build(d, Spectral(), win=0.32, log=lambda *_: None) == 1
    idx = ci.load_index(d, 0.32)
    assert set(idx["file"].tolist()) == {"match.wav", "low.wav", "high.wav", "extra.wav"}
    assert idx["emb"].shape[0] == len(idx["at"])


def test_query_ranks_same_sound_first_and_writes_ab(tmp_path):
    d = make_folder(tmp_path)
    ci.build(d, Spectral(), win=0.32, log=lambda *_: None)
    clue = clip(tone_hit(790), at=0.05, length=0.32)
    rows = ci.query(clue, [d], Spectral(), log=lambda *_: None)
    assert rows[0]["id"] == "match"
    assert rows[0]["query"] == "test hit" and rows[0]["name"] == "the one"
    assert abs(rows[0]["at"] - 0.5) < 0.05
    assert rows[0]["mel"] is not None
    made = ci.write_ab(rows, 2, clue, "mnc", tmp_path / "ab")
    assert len(made) == 2 and all(p.exists() and p.name.startswith("AB_mnc_clap") for p in made)


def test_query_skips_unindexed_folder(tmp_path):
    d = make_folder(tmp_path)
    msgs = []
    assert ci.query(clip(tone_hit(790), 0.05, 0.32), [d], Spectral(), log=msgs.append) == []
    assert "no index" in msgs[0]
