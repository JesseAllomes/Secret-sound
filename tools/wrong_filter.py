"""Mark clips whose file name matches an exact on-air guess (analysis/mnc/onair_guesses.json), so A/B packs skip
actions already guessed wrong. Mid North Coast only.

    python tools/wrong_filter.py <scores.csv> [--guesses analysis/mnc/onair_guesses.json] [--out marked.csv]

Adds two columns: "onair" (the matching guess and date, or empty) and "onair_verdict" (wrong / warm / unclear).
A clip is dropped from A/B only when it matches a guess with verdict "wrong"; warm and unclear matches are kept and
marked. Matching is by action, not object: the clip's name must contain the guess's object, its specific part (if
any) and a word of its action class, so "opening the fridge door" does not catch "fridge door close", and "closing
the microwave door" does not catch a clip of pushing the microwave's button. Names with no action word are kept.
"""
import argparse
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


VERBS = {  # action classes; a clip name must contain one word of the guess's class
    "open": r"open", "close": r"clos|shut", "push": r"push|press|button", "click": r"click",
    "pop": r"pop|eject", "insert": r"insert|plug|put|slid|attach|connect|in\b", "latch": r"latch|lock|buckl|fasten|clip|snap",
    "pull": r"pull", "flick": r"flick|switch|toggle", "turn": r"turn|switch|on\b|off\b",
}
USE = re.compile(r"stapl|punch|stamp|gun|counter|clipper|opener|lighter|trolley|remover")   # the object names the action
GENERIC_PART = {"", "top", "toast", "buttons", "end", "side"}
GENERIC_HEAD = {"switch", "button", "key", "latch", "catch", "lever", "door", "lid", "clip", "lock", "plug"}  # need a qualifier
COMPOUND_TAIL = {"punch", "opener", "box", "gun", "can", "door", "recorder", "bin", "belt", "player", "deck", "remover",
                 "counter", "clippers", "lighter", "binder", "flap", "machine", "cooker", "press"}


def words_rx(phrase):
    """Regex for an object/part: its head noun, or its last two words when the head is a generic compound tail."""
    w = [x for x in re.findall(r"[a-z]+", phrase.lower()) if x not in ("the", "a", "an", "your", "old", "little")]
    if not w:
        return None
    if w[-1] in GENERIC_HEAD:
        if len(w) < 2:
            return None                         # "switch" alone is too vague to drop anything on
        head = w[-2:]
    else:
        head = w[-2:] if len(w) >= 2 and w[-1] in COMPOUND_TAIL else w[-1:]
    body = r"[\s_-]*".join(re.escape(x[:-1] if x.endswith("s") and len(x) > 3 else x) for x in head)
    return re.compile(rf"(?<![a-z]){body}", re.I)


def verb_rx(verb, own=""):
    """Action-class regex for a guess's verb; alternatives that are just the object/part's own words are dropped."""
    classes = [c for c, k in (("open", "open"), ("close", "clos|shut"), ("push", "push|press"), ("click", "click"),
                              ("pop", "pop|eject"), ("insert", "insert|plug|put|slide|attach|stick"),
                              ("latch", "latch|lock|clip|do up|buckl|snap|fasten"), ("pull", "pull"),
                              ("flick", "flick"), ("turn", "turn")) if re.search(k, verb.lower())]
    alts = [a for c in classes for a in VERBS[c].split("|") if not re.search(a, own)]
    return re.compile(r"(?<![a-z])(?:" + "|".join(alts) + ")", re.I) if alts else None


def load_guesses(path):
    """Strict matchers built from each guess's object, part and verb (all must match the clip name)."""
    out = []
    for g in json.loads(Path(path).read_text(encoding="utf-8")):
        obj = words_rx(g.get("object") or "")
        if obj is None:
            continue
        pats = [obj]
        part = (g.get("part") or "").lower()
        if part not in GENERIC_PART and part != (g.get("object") or "").lower():
            pr = words_rx(part)
            if pr is not None and pr.pattern != obj.pattern:
                pats.append(pr)
        if not USE.search((g.get("object") or "").lower()):
            v = verb_rx(g.get("verb") or "", f"{g.get('object') or ''} {part}".lower())
            if v is None:
                continue                        # no recognisable action: never used to drop a clip
            pats.append(v)
        out.append((g, pats))
    return out


def match(name, guesses):
    """Best on-air match for a clip name: a 'wrong' match wins only if no warm/unclear guess also matches."""
    hits = [g for g, pats in guesses if pats and all(p.search(name) for p in pats)]
    if not hits:
        return None
    keep = [g for g in hits if g.get("verdict") != "wrong"]
    return (keep or hits)[0]


def mark(rows, guesses, name_key="name"):
    for r in rows:
        g = match(r.get(name_key) or "", guesses)
        r["onair"] = f"{g['date']}: {g['guess']}" if g else ""
        r["onair_verdict"] = g.get("verdict", "") if g else ""
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--guesses", default=str(ROOT / "analysis/mnc/onair_guesses.json"))
    ap.add_argument("--out")
    args = ap.parse_args()
    rows = list(csv.DictReader(open(args.csv, encoding="utf-8")))
    mark(rows, load_guesses(args.guesses))
    out = args.out or args.csv.replace(".csv", "_marked.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["onair"])
        w.writeheader()
        w.writerows(rows)
    n = sum(r["onair_verdict"] == "wrong" for r in rows)
    print(f"{len(rows)} clips, {n} match a wrong on-air guess, "
          f"{sum(r['onair_verdict'] == 'warm' for r in rows)} match a warm one; wrote {out}")


if __name__ == "__main__":
    main()
