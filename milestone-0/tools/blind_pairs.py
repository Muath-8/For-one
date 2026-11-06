#!/usr/bin/env python3
"""Make blind then-and-now pairs for rating (Milestone 0).

Input folder: one file per recording, named <ID>_<w0|w3>_<part>.<ext>, for example
    L03_w0_retell.ogg   L03_w3_retell.ogg
    L03_w0_opinion.ogg  L03_w3_opinion.ogg
    L03_w0_repeat1.ogg ... L03_w0_repeat8.ogg   (and w3)
Output folder: one folder per pair, in shuffled order (P01, P02, ...), each holding X and Y
(for the repeat task, X_1..X_8 and Y_1..Y_8), plus:
    pairs.csv  for raters: pair, part (no IDs, no weeks)
    key.csv    for unblinding: pair, ID, part, X_is (w0 or w3). Keep it closed until rating is done.

Usage: python blind_pairs.py <recordings folder> <output folder> [--seed N]
"""
import argparse
import csv
import os
import random
import re
import shutil
import sys
from collections import defaultdict

NAME = re.compile(r"^(?P<id>[A-Za-z]\d+)_(?P<week>w0|w3)_(?P<part>retell|opinion|repeat)(?P<n>\d*)\.(?P<ext>\w+)$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--seed", type=int, default=None)
    args = ap.parse_args()
    rng = random.Random(args.seed)

    groups = defaultdict(lambda: {"w0": [], "w3": []})
    skipped = []
    for f in sorted(os.listdir(args.src)):
        m = NAME.match(f)
        if not m:
            skipped.append(f)
            continue
        groups[(m["id"], m["part"])][m["week"]].append((int(m["n"] or 0), f, m["ext"]))

    complete = {k: v for k, v in groups.items() if v["w0"] and v["w3"]}
    incomplete = sorted(k for k in groups if k not in complete)
    if not complete:
        sys.exit("No learner has both a w0 and a w3 recording of the same part.")

    os.makedirs(args.dst, exist_ok=False)
    keys = list(complete)
    rng.shuffle(keys)
    key_rows, pair_rows = [], []
    for i, (lid, part) in enumerate(keys, 1):
        pair = f"P{i:02d}"
        os.makedirs(os.path.join(args.dst, pair))
        x_week = rng.choice(["w0", "w3"])
        y_week = "w3" if x_week == "w0" else "w0"
        for label, week in (("X", x_week), ("Y", y_week)):
            for n, f, ext in sorted(complete[(lid, part)][week]):
                name = f"{label}_{n}.{ext}" if part == "repeat" else f"{label}.{ext}"
                shutil.copy2(os.path.join(args.src, f), os.path.join(args.dst, pair, name))
        key_rows.append([pair, lid, part, x_week])
        pair_rows.append([pair, part])

    with open(os.path.join(args.dst, "key.csv"), "w", newline="") as f:
        csv.writer(f).writerows([["pair", "ID", "part", "X_is"]] + key_rows)
    with open(os.path.join(args.dst, "pairs.csv"), "w", newline="") as f:
        csv.writer(f).writerows([["pair", "part", "accuracy (X/Y/same)", "fluency", "complexity", "overall",
                                  "repeat: X total (0-32)", "repeat: Y total (0-32)"]] + [r + [""] * 6 for r in pair_rows])

    print(f"{len(keys)} pairs written to {args.dst}")
    if incomplete:
        print("Missing one of the two weeks (not paired):", ", ".join(f"{a} {b}" for a, b in incomplete))
    if skipped:
        print("Ignored files with unexpected names:", ", ".join(skipped))


if __name__ == "__main__":
    main()
