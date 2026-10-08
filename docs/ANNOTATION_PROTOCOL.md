# BloomShift Human Annotation Protocol

## Purpose

Human annotation is intended to determine whether each held-out transformation preserves the source content and context while achieving the intended target Bloom level.

## Population

Annotate the 228 validation/test examples in `reviewer_1.csv` and `reviewer_2.csv`.

The separate 20-example calibration batch is for reviewer familiarization and must not be included in reported agreement.

## Required fields

For each example, independently record:

- `bloom_aligned`: Yes / No
- `reviewer_bloom_level`: Remember / Understand / Apply / Analyze / Evaluate / Create / Unclear
- `content_preserved`: Yes / Partial / No
- `context_preserved`: Yes / Partial / No
- `meaningful_transformation`: Yes / Partial / No
- `pedagogically_valid`: Yes / Partial / No
- `clear_and_grammatical`: Yes / Partial / No
- `final_decision`: Accept / Revise / Reject
- `corrected_question`: fill only when a revision is needed
- `reason`: concise evidence-based rationale for partial, negative, revise, or reject judgments

## Annotation principles

### 1. Bloom alignment

Judge the cognitive operation actually required by the rewritten question, not only the presence of a familiar Bloom verb.

### 2. Content preservation

The rewrite should retain the central concept, object, task domain, and relevant constraints of the source question.

### 3. Context preservation

Do not introduce a materially different scenario, entity, product, dataset, or subject context unless that change is necessary for the intended cognitive transformation and remains faithful to the source.

### 4. Meaningful transformation

The target should change the dominant cognitive demand rather than merely replacing a verb.

### 5. Pedagogical validity

The question should be answerable as an educational assessment prompt and should plausibly elicit the intended cognitive process.

### 6. Clarity and grammar

Flag malformed, ambiguous, internally inconsistent, or ungrammatical questions.

## Revision and adjudication

A reviewer should use `corrected_question` only when a concrete revision is needed. A corrected example must be re-reviewed before inclusion in a human-validated release.

Negative or partial decisions should include a short evidence-based rationale.

## Agreement

With two annotators, the provided analysis script computes Cohen's kappa independently for each required categorical field. If more than two annotators contribute labels, use an appropriate multi-rater statistic such as Krippendorff's alpha instead.

Agreement must not be computed while required labels remain blank.
