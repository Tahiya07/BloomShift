# Source inventory audit — expansion planning

**Audit date:** 2026-10-13  
**Status:** partial inventory audit; not a final eligible-source count.

## Directly verified counts

The EduGuard repository's `data/figshare_bloom_v1.csv` was read from the `main` branch. The current BloomShift `dataset/v0.1.0/{train,validation,test}.json` files were compared by normalized source-question text.

| Check | Observed |
|---|---:|
| Rows in Figshare CSV | 2,330 |
| Unique normalized question texts in CSV | 2,325 |
| Duplicate rows beyond unique question texts | 5 |
| BloomShift v0.1.0 records | 888 |
| Unique BloomShift v0.1.0 source IDs | 238 |
| Exact source texts represented in BloomShift v0.1.0 | 238 |
| Unique Figshare question texts not found in BloomShift v0.1.0 | 2,087 |

The currently stated figure of **2,067 unused questions is not reproduced by comparing only Figshare v1 with BloomShift v0.1.0**. That comparison yields 2,087 unique unused texts. This discrepancy is not yet resolved.

## Why 2,087 is not the final expansion count

The EduGuard project history includes earlier rewrite datasets and intermediate candidates. This audit did **not** compare against every historical/cleaned rewrite source inventory because those inventories were not available in the BloomShift release files fetched for this check. Consequently, some of the 2,087 may already have been used in earlier dataset versions.

Before generation, rerun the source inventory script against:
- the full Figshare CSV;
- all canonical BloomShift v0.1.0 source splits;
- the historical 628-source rewrite inventory and cleaned v2 inventory;
- any additional source questions already present in the current EduGuard multitask dataset.

Do not subtract record counts from source counts: compare normalized unique source-question texts and retain source provenance IDs.

## Reproduction

From a local checkout with the full source inventory files available, use the expansion script on a private/local copy of the source CSV. Do not commit third-party question text into this public repository until source licensing and redistribution rights have been confirmed.

The script is a screening aid. All candidates remain `pending`; duplicate and near-duplicate flags require review. A count of unused questions is not a count of eligible or validated rewrite sources.
