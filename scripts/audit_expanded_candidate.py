#!/usr/bin/env python3
"""Audit generated expansion JSONL and assign source-group-disjoint 75/15/10 splits.

Expected rows contain source_id, source_group_id, source_question, target_bloom_level,
target_rewrite and optionally generation_id, opening_verb, review_status.
This tool does not certify semantics or Bloom validity.
"""
import argparse, csv, hashlib, json, re, unicodedata
from collections import Counter, defaultdict
from pathlib import Path
LEVELS=["Remember","Understand","Apply","Analyze","Evaluate","Create"]
VERBS={x:set(v.lower().split(", ")) for x,v in {
"Remember":"Identify, Define, List, State, Recall, Name",
"Understand":"Explain, Summarize, Interpret, Classify, Describe, Compare",
"Apply":"Apply, Calculate, Demonstrate, Implement, Use, Solve",
"Analyze":"Analyze, Differentiate, Examine, Decompose, Trace, Investigate",
"Evaluate":"Evaluate, Justify, Critique, Assess, Defend, Validate",
"Create":"Design, Construct, Develop, Formulate, Propose, Compose"}.items()}
TOKEN=re.compile(r"[a-z0-9]+",re.I)
def norm(s): return " ".join(TOKEN.findall(unicodedata.normalize("NFKC",s or "").casefold()))
def group_split(group, seed):
    # Stable hash assignment independent of input row order.
    n=int(hashlib.sha256(f"{seed}|{group}".encode()).hexdigest()[:12],16)%10000/10000
    return "train" if n<.75 else ("validation" if n<.90 else "test")
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",required=True); p.add_argument("--output",required=True)
    p.add_argument("--seed",default="bloomshift-v0.2.0"); p.add_argument("--reviewed-only",action="store_true")
    a=p.parse_args(); rows=[]
    with open(a.input,encoding="utf-8-sig") as f:
        for line_no,line in enumerate(f,1):
            if not line.strip(): continue
            try: r=json.loads(line)
            except json.JSONDecodeError as e: raise SystemExit(f"Invalid JSON at line {line_no}: {e}")
            if a.reviewed_only and r.get("review_status")!="accepted": continue
            rows.append(r)
    groups=defaultdict(list)
    for r in rows:
        g=r.get("source_group_id") or r.get("source_id")
        if not g: raise SystemExit("Every row must have source_group_id or source_id")
        groups[str(g)].append(r)
    assigned={g:group_split(g,a.seed) for g in groups}
    for r in rows: r["split"]=assigned[str(r.get("source_group_id") or r.get("source_id"))]
    ids=[r.get("generation_id") or r.get("example_id") for r in rows]
    duplicate_ids=len(ids)-len(set(ids))
    source_texts=defaultdict(set)
    for r in rows: source_texts[norm(r.get("source_question",""))].add(str(r.get("source_group_id") or r.get("source_id")))
    cross_split_exact_sources=[]
    for q,gs in source_texts.items():
        if q and len({assigned[g] for g in gs})>1: cross_split_exact_sources.append(q)
    target_counts=Counter(r.get("target_bloom_level","") for r in rows)
    split_counts=Counter(r["split"] for r in rows)
    action_openings=Counter(); non_action=[]
    for r in rows:
        rw=(r.get("target_rewrite") or "").strip()
        first=(TOKEN.findall(rw) or [""])[0].lower()
        level=r.get("target_bloom_level","")
        if first in VERBS.get(level,set()): action_openings[level]+=1
        else: non_action.append({"generation_id":r.get("generation_id") or r.get("example_id"),"target_bloom_level":level,"first_token":first,"target_rewrite":rw})
    templates=defaultdict(set)
    for r in rows:
        # Keep target operation in the text; this is only a rough exact-template diagnostic.
        t=norm(r.get("target_rewrite",""))
        anchor=norm(r.get("source_question",""))
        if anchor: t=t.replace(anchor,"§source§")
        templates[t].add(r["split"])
    report={
      "rows_audited":len(rows),"unique_source_groups":len(groups),"duplicate_record_ids":duplicate_ids,
      "source_group_split_counts":dict(Counter(assigned.values())),"record_split_counts":dict(split_counts),
      "target_level_counts":dict(target_counts),"cross_split_exact_source_texts":len(cross_split_exact_sources),
      "cross_split_template_count":sum(len(s)>1 for s in templates.values()),
      "action_verb_opening_counts_by_target":dict(action_openings),
      "non_action_verb_openings":non_action[:200],
      "limitations":["Automatic checks do not establish semantic preservation, intended cognitive demand, clarity, or pedagogical validity.",
                    "Review near-duplicate sources and normalized-template leakage manually; exact text checks cannot detect all semantic duplicates.",
                    "A split is assigned by source group. If near-duplicate sources are later merged into a common group, rerun this audit and split."],
      "split_seed":a.seed,"status":"structural audit only; human validation required"
    }
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=="__main__": main()
