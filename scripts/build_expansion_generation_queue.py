#!/usr/bin/env python3
"""Build a reproducible JSONL rewrite-generation queue from human-approved sources.

No model is called here. Output is a prompt queue, not validated dataset records.
Only review_status=approved rows are queued. Source/target level pairs are
configurable and source level is never inferred from lexical verbs.
"""
import argparse, csv, json, hashlib
from pathlib import Path

LEVELS = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]
OPENERS = {
 "Remember": "Identify, Define, List, State, Recall, Name",
 "Understand": "Explain, Summarize, Interpret, Classify, Describe, Compare",
 "Apply": "Apply, Calculate, Demonstrate, Implement, Use, Solve",
 "Analyze": "Analyze, Differentiate, Examine, Decompose, Trace, Investigate",
 "Evaluate": "Evaluate, Justify, Critique, Assess, Defend, Validate",
 "Create": "Design, Construct, Develop, Formulate, Propose, Compose",
}
PROMPT = """Transform the instructor-authored question to the requested revised Bloom level.
The first word of the rewrite must be an appropriate action verb, not a WH-question opening.
Choose an operation that genuinely requires the target cognitive process; an action verb alone
does not establish Bloom alignment. Preserve the source's subject, named entities, technical
terms, constraints, quantities, quoted text, negation, and context. Do not add facts, assumptions,
data, scenarios, or requirements absent from the source. Do not answer the question. If a meaningful
transformation cannot preserve the source context, return status=not_feasible and explain why.
Return one JSON object with keys: target_rewrite, target_bloom_level, opening_verb,
semantic_risks (array), feasibility (feasible/not_feasible), rationale. Do not claim human validation.
"""

def norm(s): return " ".join((s or "").casefold().split())
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True,help="Screening CSV from prepare_expansion_source_pool.py")
    p.add_argument("--output",required=True,help="Output JSONL prompt queue")
    p.add_argument("--target-levels",default="Remember,Understand,Apply,Analyze,Evaluate,Create")
    p.add_argument("--include-same-level",action="store_true")
    a=p.parse_args()
    targets=[x.strip() for x in a.target_levels.split(",") if x.strip()]
    unknown=set(targets)-set(LEVELS)
    if unknown: p.error(f"Unknown target levels: {sorted(unknown)}")
    out=[]; rejected=0
    with open(a.input,encoding="utf-8-sig",newline="") as f:
        for row in csv.DictReader(f):
            if row.get("review_status","").strip().casefold() != "approved":
                rejected+=1; continue
            q=row.get("source_question","").strip()
            if not q: continue
            source_level=row.get("original_bloom_level","").strip()
            for target in targets:
                if not a.include_same_level and source_level == target: continue
                key=f'{row.get("source_id","")}|{target}'
                out.append({
                    "generation_id":"gen_"+hashlib.sha256(key.encode()).hexdigest()[:16],
                    "source_id":row.get("source_id",""),
                    "source_group_id":row.get("source_group_id",""),
                    "source_question":q,
                    "source_bloom_level":source_level,
                    "target_bloom_level":target,
                    "preferred_opening_verbs":OPENERS[target],
                    "prompt":PROMPT,
                    "status":"pending_generation",
                    "model_id":"",
                    "prompt_version":"bloomshift-expansion-prompt-v1",
                    "generation_parameters":{},
                    "human_review_status":"not_reviewed",
                })
    path=Path(a.output); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",encoding="utf-8") as f:
        for r in out: f.write(json.dumps(r,ensure_ascii=False)+"\n")
    print(json.dumps({"approved_source_rows_queued":len({r["source_id"] for r in out}),"generation_jobs":len(out),"not_approved_rows_skipped":rejected,"target_levels":targets,"same_level_included":a.include_same_level,"output":str(path),"status":"generation queue only; no rewrites generated or validated"},indent=2))
if __name__=="__main__": main()
