# BloomShift v0.1.0 Dataset Card

## Summary

BloomShift v0.1.0 is a curated silver candidate for transforming instructor-authored questions between Bloom's Taxonomy cognitive levels. Each record retains the source question and provenance fields and provides a target rewrite intended to change cognitive demand while preserving the underlying content and context.

## Composition

| Property | Value |
|---|---:|
| Total transformations | 888 |
| Unique source questions | 238 |
| Train | 660 |
| Validation | 114 |
| Test | 114 |
| Target levels | 6 |
| Identity transformations | 0 |
| Source-group overlap across splits | 0 |

The six target levels are Remember, Understand, Apply, Analyze, Evaluate, and Create.

## Intended use

The candidate can be used for model training, development, exploratory analysis, and controlled benchmarking of Bloom-level transformation systems.

It should not yet be presented as a human-certified gold-standard benchmark.

## Construction

The dataset was constructed by expanding source questions into non-identity target-level transformations. Source groups are kept disjoint across train, validation, and test. The release contains 28 of the 30 possible non-identity source-to-target transitions; Remember→Evaluate and Remember→Create are absent because the source pool contains only six Remember-level questions.

## Quality and audit status

Automated checks cover example IDs, split isolation, source grouping, identity transformations, transition coverage, recurring target templates, and mechanical wording artifacts. The audit also documents known near-duplicate source pairs and template recurrence.

There are 32 pre-annotation semantic/content-preservation flags. These are review flags, not automatic evidence that the corresponding transformations are incorrect.

## Human validation

The validation/test population contains 228 examples reserved for independent human annotation. Two blank reviewer worksheets and a calibration worksheet are included. The 20-example calibration batch is excluded from agreement calculations.

Human validation is pending in v0.1.0.

## Known limitations

- Target rewrites are synthetic and may contain template-like language.
- Recurring templates occur across splits; 34 cross-split recurring templates are associated with only one target Bloom level.
- Two near-duplicate source pairs remain as documented audit risks.
- Source expansion is nonuniform across source questions.
- Semantic preservation and pedagogical validity cannot be established by the automated structural audit alone.

## Provenance and licensing

Source questions originate from previously collected educational question material. This repository does not assert ownership of third-party source text. Before redistribution or publication, the provenance and licensing/attribution requirements of the underlying sources should be reviewed.

## Release status

**v0.1.0 — curated silver candidate; human validation pending.**
