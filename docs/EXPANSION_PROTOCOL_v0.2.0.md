# BloomShift v0.2.0 expansion protocol (working draft)

## Status and release policy

This is a protocol and tooling branch, not a completed expanded dataset. The existing
v0.1.0 release remains unchanged. No question is considered accepted merely because
a script can parse it; no generated rewrite is considered valid without review.

## Intended source pool

The working inventory has been described as 2,067 unused questions. This count must be
recomputed from the actual source file and the exact v0.1.0 source inventory before
being treated as verified. The source file, source URL/citation, license/redistribution
status, extraction date, and content hash must be recorded. Do not publish third-party
question text unless redistribution rights permit it.

## Workflow

1. Run `prepare_expansion_source_pool.py` on the full candidate CSV and all v0.1.0
   source inventories. It produces a screening worksheet and summary. All rows start
   as `pending`; exact duplicates are excluded from new-source counts, and near
   duplicates are flagged for manual review rather than silently deleted.
2. A reviewer records `approved` or `rejected` in `review_status`, with a reason
   for rejected rows. Approval should confirm the question is self-contained enough
   to transform, unambiguous, and traceable to its source. Resolve duplicates before
   assigning distinct source groups.
3. Run `build_expansion_generation_queue.py` only on the screened worksheet.
   It creates prompts for target levels, but does not call a model and does not create
   validated examples. Source-level labels must be supported by source metadata or
   annotation, not guessed from verb cues.
4. Generate rewrites with a pinned model/checkpoint, prompt version, decoding settings,
   and recorded timestamp. Store raw model output before parsing/correction. Keep
   rejected generations and reasons in an audit file; do not overwrite them.
5. Review each rewrite for (a) semantic/content preservation, (b) target Bloom operation,
   (c) clarity/answerability, (d) pedagogical validity. A target verb is a surface
   constraint only, not evidence of cognitive validity. Reject a rewrite if the target
   operation requires facts, context, constraints, or artifacts absent from the source.
6. Resolve near-duplicate sources and assign all source variants to a single group.
   Generate deterministic 75/15/10 group-level splits with a recorded seed. Verify
   no exact source text or known near-duplicate group crosses partitions.
7. Keep final evaluation sources out of prompt/model selection. The 228 v0.1.0
   validation/test records remain tied to v0.1.0 and must not be mixed into v0.2.0
   training data. Build a separate, preregistered human-reviewed evaluation subset for
   the expanded release. Two annotators independently review the evaluation examples;
   report per-dimension agreement, adjudication, exclusions, and final denominators.
8. Run structural and provenance audits, publish the manifest, counts, rejection log,
   license/provenance review, and a changelog. Release v0.2.0 only after those checks.

## Suggested screening fields

- `review_status`: pending / approved / rejected
- `reviewer_decision`, `rejection_reason`
- exact and near-duplicate flags
- source provenance and original source identifier
- source Bloom label and evidence for that label
- feasibility by intended target level
- generation model, prompt version, parameters, and raw-output reference
- semantic preservation, cognitive validity, clarity, pedagogical validity
- annotator IDs, independent labels, adjudication outcome, and revision history

## Split policy

Use a source-group-level 75/15/10 split (train/validation/test) as a target, not a
promise of exact row percentages. Group related/near-duplicate source questions before
splitting. Report both source-group counts and rewrite-record counts. Use a separate
template-held-out analysis where feasible because recurring transformation templates
can create target-label shortcuts.

## Release gate

A candidate may be called structurally audited only when the audit passes. It may be
called human-validated only after independent human labels, agreement analysis,
adjudication, and synchronization of data and annotation artifacts are complete.
Do not describe this protocol or the prompt queue as a completed expansion.
