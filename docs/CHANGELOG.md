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


## Unreleased — Action-verb rewrite revision

- Reconstruct all 888 target rewrites to begin with an action verb aligned to the requested target Bloom level.
- Synchronize the supervisor annotation worksheet with the revised validation/test rewrites.
- Keep the existing source-group-disjoint 660/114/114 split; do not inflate held-out counts by duplicating records or moving training sources.
- Expansion to more unique source questions remains pending access to the original 2,330-row source CSV, which is not included in this repository.
- Require fresh human review because the target rewrite text has changed.


## v0.2.0 — Action-verb rewrites and larger held-out splits

- Added a new version without overwriting v0.1.0.
- Expanded validation and test from 114 to 138 rows each (23 examples per target Bloom level).
- Rebuilt train from earlier candidate records after removing every source group used by either held-out partition; verified zero group overlap.
- Rewrote 553 WH-starting target rewrites with target-level action-verb openings and synchronized all 276 held-out supervisor annotation rows.
- Added an audit manifest. Human semantic, content/context preservation, Bloom alignment, and pedagogical review remain required.
