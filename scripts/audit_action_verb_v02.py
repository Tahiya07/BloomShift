#!/usr/bin/env python3
"""Structural audit for BloomShift v0.2.0 action-verb candidate.

Run from the repository root:
    python scripts/audit_action_verb_v02.py

This checks data integrity and split leakage; it does not certify semantic
preservation, Bloom validity, or pedagogical quality.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "dataset" / "v0.2.0"
ANNOTATION = ROOT / "annotations" / "v0.2.0" / "supervisor_annotation.csv"
LEVELS = ("Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create")
ALLOWED = {
    "Remember": {"identify", "list", "state", "name", "recall", "define", "recognize", "select"},
    "Understand": {"explain", "describe", "summarize", "interpret", "classify"},
    "Apply": {"apply", "use", "implement", "calculate", "demonstrate", "solve", "execute"},
    "Analyze": {"analyze", "examine", "compare", "break"},
    "Evaluate": {"assess", "evaluate", "check", "justify", "verify", "critique", "compare"},
    "Create": {"design", "construct", "develop", "propose", "build", "create", "formulate"},
}
EXPECTED = {"train": 691, "validation": 138, "test": 138}


def load_split(split: str) -> list[dict]:
    with (DATA / f"{split}.json").open(encoding="utf-8") as f:
        rows = json.load(f)
    if not isinstance(rows, list):
        raise ValueError(f"{split}.json must contain a JSON list")
    return rows


def main() -> None:
    splits = {s: load_split(s) for s in EXPECTED}
    errors: list[str] = []
    all_rows = [r for rows in splits.values() for r in rows]

    for split, rows in splits.items():
        if len(rows) != EXPECTED[split]:
            errors.append(f"{split}: expected {EXPECTED[split]} rows, found {len(rows)}")
        if any(r.get("split") != split for r in rows):
            errors.append(f"{split}: embedded split field mismatch")
        counts = Counter(r.get("target_bloom_level") for r in rows)
        if split != "train" and any(counts[level] != 23 for level in LEVELS):
            errors.append(f"{split}: target levels are not balanced: {dict(counts)}")

    ids = [r.get("example_id") for r in all_rows]
    if len(ids) != len(set(ids)):
        errors.append("example_id values are not unique")

    group_sets = {
        split: {str(r.get("group_id")) for r in rows}
        for split, rows in splits.items()
    }
    for a, b in (("train", "validation"), ("train", "test"), ("validation", "test")):
        overlap = group_sets[a] & group_sets[b]
        if overlap:
            errors.append(f"source-group leakage {a}/{b}: {len(overlap)} groups")

    bad_openings = []
    for r in all_rows:
        match = re.match(r"^([A-Za-z]+)", str(r.get("target_rewrite", "")).strip())
        verb = match.group(1).lower() if match else ""
        level = r.get("target_bloom_level")
        if verb not in ALLOWED.get(level, set()):
            bad_openings.append((r.get("example_id"), level, verb))
    if bad_openings:
        errors.append(f"{len(bad_openings)} rewrites have a non-approved target-level opening")

    with ANNOTATION.open(encoding="utf-8-sig", newline="") as f:
        annotations = list(csv.DictReader(f))
    heldout = {r["example_id"]: r["target_rewrite"] for s in ("validation", "test") for r in splits[s]}
    if len(annotations) != len(heldout):
        errors.append(f"annotation rows {len(annotations)} != held-out rows {len(heldout)}")
    for row in annotations:
        expected = heldout.get(row.get("example_id"))
        if expected is None or row.get("target_rewrite") != expected:
            errors.append(f"annotation mismatch: {row.get('example_id')}")

    summary = {
        "rows_by_split": {s: len(rows) for s, rows in splits.items()},
        "total_rows": len(all_rows),
        "unique_source_ids": len({r.get("source_id") for r in all_rows}),
        "source_group_overlap": {
            f"{a}_{b}": len(group_sets[a] & group_sets[b])
            for a, b in (("train", "validation"), ("train", "test"), ("validation", "test"))
        },
        "target_counts": {s: dict(Counter(r.get("target_bloom_level") for r in rows)) for s, rows in splits.items()},
        "approved_action_opening_failures": len(bad_openings),
        "annotation_rows": len(annotations),
        "errors": errors,
    }
    print(json.dumps(summary, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
