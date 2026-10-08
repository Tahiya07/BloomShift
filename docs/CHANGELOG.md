# Changelog

## v0.1.0 — Curated silver candidate

- Created a standalone BloomShift dataset release.
- Added 888 transformation records across train, validation, and test.
- Added source-group-disjoint splits.
- Added audit output and deterministic audit scripts.
- Added independent human-review worksheets for 228 held-out examples.
- Added a 20-example calibration batch.
- Documented two near-duplicate source pairs and recurring target-template risks.
- Documented 32 semantic/content-preservation flags for human review.
- Kept the release explicitly labeled as a silver candidate pending human validation.

## Planned next release

A future human-validated release may add reviewed labels, adjudication outcomes, agreement statistics, corrected questions, and an updated audit.
## 2026-10-08 — Release-readiness clarification

- Clarified that `supervisor_annotation.csv` is an optional third independent annotation/adjudication worksheet and is not used by the current two-rater agreement script.
- Clarified that no repository-level license should be added until redistribution rights and attribution requirements for underlying source material are reviewed.
- Reconfirmed template recurrence as a benchmark shortcut risk; future evaluation should report the limitation or use a template-held-out protocol.
