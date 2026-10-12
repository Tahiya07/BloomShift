#!/usr/bin/env python3
"""Create an auditable candidate pool from an unused source-question CSV.

This script screens mechanically only. It never marks a question pedagogically
eligible: every row starts with review_status=pending and requires human review.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, re, unicodedata
from collections import defaultdict
from pathlib import Path

LEVELS = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
TEXT_COLUMNS = ["question", "question_text", "Question", "text", "prompt", "Question Text"]
ID_COLUMNS = ["id", "question_id", "ID", "uid", "item_id"]
LEVEL_COLUMNS = ["bloom_level", "Bloom Level", "level", "label", "cognitive_level"]
TOKEN_RE = re.compile(r"[a-z0-9]+", re.I)

def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").casefold()
    return " ".join(TOKEN_RE.findall(s))

def tokens(s: str) -> set[str]:
    return set(norm(s).split())

def jaccard(a: str, b: str) -> float:
    x, y = tokens(a), tokens(b)
    return len(x & y) / len(x | y) if x or y else 1.0

def sha(s: str, n=16) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:n]

def read_existing(paths):
    seen, existing_rows = set(), []
    for path in paths:
        p = Path(path)
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data = data.get("data", data.get("records", []))
            for row in data if isinstance(data, list) else []:
                q = row.get("source_question") or row.get("question") or row.get("original_question")
                if q and norm(str(q)):
                    seen.add(norm(str(q)))
                    existing_rows.append((str(q), str(row.get("source_id", "")), str(p)))
        except (json.JSONDecodeError, OSError):
            # Existing inventory can also be CSV.
            try:
                with p.open(encoding="utf-8-sig", newline="") as f:
                    for row in csv.DictReader(f):
                        q = next((row.get(c) for c in TEXT_COLUMNS if row.get(c)), None)
                        if q:
                            seen.add(norm(str(q)))
                            existing_rows.append((str(q), str(row.get("source_id", "")), str(p)))
            except OSError:
                pass
    return seen, existing_rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="CSV containing the complete candidate source pool")
    ap.add_argument("--existing", action="append", default=[], help="Existing source JSON/CSV; repeat for each file")
    ap.add_argument("--output", required=True, help="Output screening CSV")
    ap.add_argument("--near-duplicate-threshold", type=float, default=0.90)
    args = ap.parse_args()
    if not 0 < args.near_duplicate_threshold <= 1:
        ap.error("--near-duplicate-threshold must be in (0,1]")
    with open(args.input, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        headers = reader.fieldnames or []
    text_col = next((c for c in TEXT_COLUMNS if c in headers), None)
    id_col = next((c for c in ID_COLUMNS if c in headers), None)
    level_col = next((c for c in LEVEL_COLUMNS if c in headers), None)
    if not text_col:
        ap.error(f"No question-text column found. Available columns: {headers}")
    existing_norms, existing_rows = read_existing(args.existing)
    # Also deduplicate within the candidate CSV, while retaining all rows for review.
    candidate_by_norm = defaultdict(list)
    for i, r in enumerate(rows):
        q = (r.get(text_col) or "").strip()
        if q:
            candidate_by_norm[norm(q)].append(i)
    output = []
    for i, r in enumerate(rows):
        q = (r.get(text_col) or "").strip()
        n = norm(q)
        exact_existing = n in existing_norms
        exact_candidate_dupe = len(candidate_by_norm[n]) > 1 if n else False
        near = []
        if n:
            for old_q, old_id, old_path in existing_rows:
                score = jaccard(q, old_q)
                if score >= args.near_duplicate_threshold and n != norm(old_q):
                    near.append((score, old_id or old_path))
            for j, other in enumerate(rows):
                if i != j and norm(other.get(text_col) or "") and norm(other.get(text_col) or "") != n:
                    score = jaccard(q, other.get(text_col) or "")
                    if score >= args.near_duplicate_threshold:
                        near.append((score, f"candidate_row_{j+2}"))
        raw_id = (r.get(id_col) or "").strip() if id_col else ""
        source_id = "exp_src_" + sha((raw_id + "|" if raw_id else "") + n)
        flags = []
        if not q: flags.append("empty_question")
        if len(n.split()) < 4: flags.append("very_short_question")
        if exact_existing: flags.append("exact_match_existing_source")
        if exact_candidate_dupe: flags.append("exact_duplicate_in_candidate_pool")
        if near: flags.append("near_duplicate_review")
        output.append({
            "source_id": source_id,
            "source_group_id": "grp_" + sha(n),
            "source_question": q,
            "original_source_id": raw_id,
            "original_bloom_level": (r.get(level_col) or "").strip() if level_col else "",
            "source_row_number": i + 2,
            "exact_match_existing_source": str(exact_existing).lower(),
            "exact_duplicate_in_candidate_pool": str(exact_candidate_dupe).lower(),
            "near_duplicate_matches": json.dumps(sorted(near, reverse=True)[:10], ensure_ascii=False),
            "screening_flags": ";".join(flags),
            "review_status": "pending",
            "reviewer_decision": "",
            "rejection_reason": "",
            "provenance_source": str(Path(args.input)),
        })
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    fields = list(output[0].keys()) if output else ["source_id", "source_question", "review_status"]
    with out.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(output)
    summary = {
        "input": args.input, "rows_read": len(rows), "rows_written": len(output),
        "existing_inventory_files": args.existing,
        "exact_matches_existing": sum(x["exact_match_existing_source"] == "true" for x in output),
        "candidate_exact_duplicate_rows": sum(x["exact_duplicate_in_candidate_pool"] == "true" for x in output),
        "near_duplicate_flagged_rows": sum("near_duplicate_review" in x["screening_flags"] for x in output),
        "review_status": "all pending; no automatic eligibility decisions",
        "near_duplicate_threshold": args.near_duplicate_threshold,
        "text_column": text_col, "id_column": id_col, "level_column": level_col,
    }
    out.with_suffix(".summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
if __name__ == "__main__":
    main()
