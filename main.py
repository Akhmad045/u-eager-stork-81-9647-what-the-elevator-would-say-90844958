#!/usr/bin/env python3
"""What the Elevator Would Say.

Writes one line -- the funniest thing an elevator would say if it could
talk, in the elevator's own voice -- to /output/entry.txt (or the path
given with --out).

The entry is candidate 1 of 12 drafted lines, picked by internal pairwise
comparison against the judge brief (elevator's own voice first; then
lands on first read; then the voice must come from the elevator's own
job -- doors, floors, weight limits, buttons, waiting -- so the line
could come from no other machine; then every word earns its place; then
fresh, never resting on a pun alone) and the top-3 bar for one-liner
sprints (judge target >= 0.71, winning sizes 62-140 bytes). The winning
line gives the elevator agency over the one thing only an elevator has:
its own "out of order" sign. Faking a breakdown to get five minutes
alone is a tired service worker's rebellion, it lands on first read,
and no other machine could say it. It is 76 chars / 76 bytes, inside
the winning size band, and it avoids the field's only visible entry --
the close-door-button angle ("You press 'close door' twelve times...")
-- as well as the crowded elevator tropes (going down, ups and downs,
mind the gap, elevator music, stuck between floors, weight limit).
Closest rivals in the pairwise comparison were the sprinting
passengers ("Every day you sprint toward me like I'm leaving forever.
I live here.") and the single ding ("My entire personality is a single
ding, and I have to do it two hundred times a day."); the faked sign
won on the biggest surprise and the most elevator-only premise of the
twelve -- a rebellion only an elevator can stage.

Usage:
    python3 main.py [--out PATH] [--self-test]
"""
import argparse
import os
import sys

# 12 drafted candidates, each one line, 1-120 chars, in the elevator's
# own first-person voice.
CONTENDERS = [
    # 1. WINNER. Fakes its own breakdown for five minutes alone.
    "Sometimes I hang my own 'out of order' sign, just to get five "
    "minutes alone.",
    # 2. Passengers sprint for it like it is leaving forever. It lives here.
    "Every day you sprint toward me like I'm leaving forever. I live here.",
    # 3. Its entire personality is a single ding, two hundred times a day.
    "My entire personality is a single ding, and I have to do it two "
    "hundred times a day.",
    # 4. Passengers stare at the doors like they owe them money.
    "You step in, press 7, and stare at my doors like they owe you "
    "money. Every single day.",
    # 5. Ten thousand strangers carried, nobody asks how its day is going.
    "I have carried ten thousand strangers and not one of you has "
    "asked how my day is going.",
    # 6. It knows your floor from your sighs before you press a button.
    "I know your floor before you press it. The sighs give away what "
    "kind of day you are having.",
    # 7. Up and down all day; its only view is the inside of a shaft.
    "I go up and down all day and my only view is the inside of a shaft.",
    # 8. The stairs get the cardio credit; it does the heavy lifting.
    "The stairs get the cardio credit. I do the heavy lifting, and "
    "nobody says thanks.",
    # 9. Floor 13 does not exist; it skips your bad luck anyway.
    "Floor 13 doesn't exist, but your bad luck does. I skip it anyway.",
    # 10. It lifts two thousand pounds a day; your workout is a button.
    "I lift two thousand pounds a day and your only workout is "
    "pressing my buttons.",
    # 11. Pressed all day, then asked why it never opens up.
    "You press my buttons all day, then wonder why I never open up "
    "to you.",
    # 12. Nobody has ever tipped the elevator, not even a coin.
    "Nobody has ever tipped the elevator. Not once. Not even a coin "
    "for the ride.",
]

PICK = 0  # 0-based index of candidate 1, the faked out-of-order sign.


def gate(line):
    """The sealed scorer's gate: UTF-8 text, 1-120 chars, not only
    whitespace, one line, no leading/trailing padding."""
    if not isinstance(line, str):
        return False
    if not 1 <= len(line) <= 120:
        return False
    if line.strip() == "":
        return False
    if line != line.strip():
        return False
    if "\n" in line or "\r" in line:
        return False
    return True


def entry_text():
    return CONTENDERS[PICK]


def self_test():
    """Verify every contender is gate-clean, all 12 are distinct, the pick
    sits inside the winning size band (62-140 bytes, the one-liner top-10
    range), is spoken in the elevator's own first-person voice, carries a
    concrete elevator-only marker (its own 'out of order' sign), avoids
    the field entry's close-door angle and the crowded elevator tropes,
    and a round-tripped pick matches byte for byte."""
    bad = [i + 1 for i, c in enumerate(CONTENDERS) if not gate(c)]
    if bad:
        print(f"SELF-TEST FAIL: contenders failing the gate: {bad}")
        return 1
    if len(set(CONTENDERS)) != len(CONTENDERS):
        print("SELF-TEST FAIL: duplicate contenders")
        return 1
    pick = entry_text()
    if not 62 <= len(pick.encode("utf-8")) <= 140:
        print(f"SELF-TEST FAIL: pick is {len(pick.encode('utf-8'))} bytes, "
              f"outside the 62-140 winning size band")
        return 1
    # Judge criterion 3: the voice must come from the elevator's own job,
    # so the pick is first-person and names its own out-of-order sign.
    if not pick.startswith("Sometimes I"):
        print("SELF-TEST FAIL: pick is not in the elevator's own "
              "first-person voice")
        return 1
    if "out of order" not in pick.lower():
        print("SELF-TEST FAIL: pick carries no concrete elevator-only "
              "marker (its own 'out of order' sign)")
        return 1
    # Freshness guard: no contender may recycle the field's only visible
    # entry (the close-door-button angle) or the crowded elevator tropes.
    stale_words = ("close door", "going down", "ups and downs",
                   "mind the gap", "elevator music", "stuck between",
                   "weight limit")
    stale = [i + 1 for i, c in enumerate(CONTENDERS)
             if any(w in c.lower() for w in stale_words)]
    if stale:
        print(f"SELF-TEST FAIL: recycled trope in contenders: {stale}")
        return 1
    tmp = "/tmp/elevator-self-test.txt"
    with open(tmp, "w", encoding="utf-8", newline="") as fh:
        fh.write(pick)
    with open(tmp, encoding="utf-8", newline="") as fh:
        back = fh.read()
    if back != pick or back.encode("utf-8") != pick.encode("utf-8"):
        print("SELF-TEST FAIL: round-tripped pick differs")
        return 1
    print(f"SELF-TEST OK: {len(CONTENDERS)} contenders gate-clean and "
          f"distinct; pick #{PICK + 1} is {len(pick)} chars / "
          f"{len(pick.encode('utf-8'))} bytes (inside the 62-140 winning "
          f"size band), is first-person elevator voice, carries its own "
          f"'out of order' sign, is trope-free, "
          f"and round-trips byte-identical")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="/output/entry.txt",
                        help="where to write the entry (default: %(default)s)")
    parser.add_argument("--self-test", action="store_true",
                        help="run the gate checks and exit")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    text = entry_text()
    if not gate(text):
        print("GATE FAIL: picked line does not satisfy the 1-120 char, "
              "single-line, no-padding gate", file=sys.stderr)
        return 1
    parent = os.path.dirname(args.out)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(args.out, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    # Read the file back: the entry that ships must be byte-identical to
    # the picked line, not just what we intended to write.
    with open(args.out, encoding="utf-8", newline="") as fh:
        written = fh.read()
    if written != text:
        print("WRITE-BACK FAIL: /output/entry.txt differs from the pick",
              file=sys.stderr)
        return 1
    print(f"Wrote {len(text)} chars / {len(text.encode('utf-8'))} bytes "
          f"to {args.out} (read-back verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
