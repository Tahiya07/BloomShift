# BloomShift Benchmark Protocol Note

## Current candidate

BloomShift v0.1.0 is suitable for exploratory training and evaluation, but its ordinary source-group-disjoint split should not be interpreted as template-disjoint.

The current audit reports:

- 175 normalized target templates overall
- 35 normalized templates recurring across splits
- 34 recurring cross-split templates associated with only one target Bloom level

These patterns create a potential surface-form shortcut: a model may exploit recurring transformation templates that correlate with the target level rather than learning the intended cognitive transformation.

## Required reporting

Experiments using v0.1.0 should report:

1. source-group-disjoint train/validation/test splitting;
2. balanced target-level counts;
3. the template-recurrence limitation;
4. that Bloom validity and content preservation remain human-validation questions.

Do not claim that v0.1.0 provides template-disjoint generalization.

## Recommended stronger evaluation

For a later benchmark revision, construct a template-held-out evaluation partition in which normalized target templates appearing in the evaluation set are absent from training. The held-out partition should be created without changing the source content or target labels merely to improve the metric.

Template normalization must be treated as a diagnostic definition, not as a semantic equivalence rule. Any new split should be regenerated and audited from the underlying examples, with source groups remaining disjoint.

## Interpretation

A template-held-out result would provide stronger evidence that a transformation model generalizes beyond recurring linguistic scaffolds. It would complement, rather than replace, human judgments of Bloom alignment, content preservation, context preservation, meaningful transformation, and pedagogical validity.
