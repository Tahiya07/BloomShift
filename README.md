# BloomShift

BloomShift is a dataset-focused repository for Bloom's Taxonomy question transformation research. It contains a curated **silver candidate** dataset for transforming instructor-authored questions across Bloom cognitive levels while preserving the original content and context as far as the automated construction process supports.

## v0.1.0 — Curated silver candidate

- 888 transformation records
- 238 unique source questions
- Train / validation / test: 660 / 114 / 114
- Six target Bloom levels: Remember, Understand, Apply, Analyze, Evaluate, Create
- No identity transformations
- Source groups are disjoint across train, validation, and test
- 28 of 30 possible non-identity source-to-target transitions are represented
- 228 validation/test records are reserved for independent human review

This release is **not a human-certified gold dataset**. Human validation and agreement analysis are intentionally kept separate from the candidate data.

## Repository structure

```text
BloomShift/
├── README.md
├── CITATION.cff
├── dataset/
│   └── v0.1.0/
│       ├── train.json
│       ├── validation.json
│       └── test.json
├── annotations/
│   └── v0.1.0/
│       ├── annotation_manifest.json
│       ├── annotation_calibration.csv
│       ├── reviewer_1.csv
│       ├── reviewer_2.csv
│       ├── supervisor_annotation.csv
│       └── annotation_agreement_template.csv
├── audits/
│   └── v0.1.0/
│       └── audit.json
├── scripts/
│   ├── audit_bloomshift_candidate.py
│   └── analyze_annotation_agreement.py
└── docs/
    ├── DATASET_CARD.md
    ├── ANNOTATION_PROTOCOL.md
    └── CHANGELOG.md
```

## Human validation

The 228 validation/test examples are intended for independent annotation. The reviewer worksheets are blank by design.

Reviewers assess Bloom alignment, Bloom level, content preservation, context preservation, meaningful transformation, pedagogical validity, clarity/grammar, and a final decision. A 20-example calibration batch is excluded from reported agreement.

The `supervisor_annotation.csv` file uses the same blank schema as the reviewer worksheets. It is retained as an optional third independent annotation/adjudication worksheet and is not included in the current two-rater agreement calculation.

The recommended human-validated release criteria are:

1. All 228 held-out examples are independently reviewed by at least two annotators.
2. Rejected examples are excluded from the gold release.
3. Revised examples are corrected and re-reviewed.
4. Inter-annotator agreement is reported.
5. The 32 pre-annotation semantic/content-preservation flags receive explicit review.
6. Dataset, annotations, and audit files are synchronized.

## Known candidate-level risks

The automated audit found two near-duplicate source pairs and recurring target templates across splits. These are documented as review/evaluation risks rather than silently removed. In particular, 34 recurring cross-split templates were associated with only one target Bloom level, so a template-held-out evaluation is preferable when measuring generalization.

The current candidate should therefore not be described as template-disjoint or human-validated.

## Audit

Run:

```bash
python scripts/audit_bloomshift_candidate.py \
  --root dataset/v0.1.0 \
  --output audits/v0.1.0/recomputed_audit.json
```

After independent annotation is complete:

```bash
python scripts/analyze_annotation_agreement.py \
  --reviewer1 annotations/v0.1.0/reviewer_1.csv \
  --reviewer2 annotations/v0.1.0/reviewer_2.csv \
  --output annotations/v0.1.0/annotation_agreement.json
```

The agreement script refuses to compute statistics while required human labels remain blank.

## Relationship to EduGuard

BloomShift is maintained as a standalone dataset repository so that the dataset, annotation protocol, audit trail, and future releases can be cited and versioned independently of the EduGuard application.

## Provenance and licensing

The current dataset records provenance through source/group identifiers and transformation metadata, but it does not include source-license URLs or ownership assertions for the underlying third-party question text. A repository-level license should therefore **not** be added until the redistribution rights, attribution requirements, and any applicable source licenses have been reviewed.

If redistribution rights cannot be established for a source subset, that source material should be removed or replaced before a public dataset release.

## Status

**v0.1.0 — curated silver candidate; human validation pending.**
