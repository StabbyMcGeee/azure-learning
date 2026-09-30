# Terminology And Sources — Azure Learning handoff archive

This file preserves dated project handoff entries from `HANDOFF.txt`.
Do not delete or rewrite history; add new dated sections at the bottom.

## Microsoft Learn terminology alignment — 2026-09-26
- Audited all 133 AZ-900 question records against their Microsoft Learn terminology and source links, focusing on current Microsoft product names and terminology likely to appear on the exam.
- Updated `az900-016` to use the full product name `Microsoft Entra Conditional Access` and its canonical Entra source URL. Updated `az900-022` to the Microsoft Entra ID-specific Learn article. Replaced `az900-030`'s unrelated Azure Boards citation with the Azure Resource Manager template overview.
- Replaced the retired wording `Reservierte Instanzen (Reserved Instances)` with the current Microsoft term `Azure-Reservierungen (Azure Reservations)` in `az900-122` through `az900-124`.
- Replaced the retiring Azure Blueprints distractor in `az900-132` with `Azure Deployment Stacks` and updated its explanation. Existing terminology for Microsoft Entra ID, Defender for Cloud, Microsoft Purview, region pairs, and VM Scale Sets required no changes.
- Validation: `python3 -m py_compile azure_learning_app.py` passed. A fresh temporary SQLite database reconciled and loaded all 133 questions; IDs were unique; updated answers and canonical URLs were asserted; retired terms and stale Entra/Azure Boards URLs no longer occur in the bank (`TERMINOLOGY_AND_FRESH_DB_AUDIT: PASS`).
- Rebuilt via `./build-linux.sh`. Root, `dist`, release, and Desktop executables are identical and executable: SHA-256 `1c2354efaebc66c2cd1122b4322ae7ac2ef715d2029363ef73f86fb771e593f7`.
- Files touched: `azure_learning_app.py`, `HANDOFF.txt`.


---

## Microsoft Learn source-link completion — 2026-09-26
- Completed the terminology audit with an individual live check of all 86 unique source URLs used by the 133 AZ-900 question records. All terminology used in prompts, options, answers, and explanations remains aligned with current Microsoft terminology after the earlier product-name corrections.
- Replaced 30 stale, redirecting, or broken source references with current canonical Microsoft Learn pages. This includes the Azure Fundamentals learning path, Microsoft Entra ID documentation, Well-Architected Performance Efficiency and Reliability pillars, Cloud Adoption Framework, Azure Monitor Fundamentals, Azure networking overview, Azure Functions overview, the compute decision tree, Azure Policy, migration's "6 Rs," and the EU Data Boundary article.
- No stale Azure AD, Azure Blueprints, Reserved Instances, retired Well-Architected pillar paths, invalid cloud-concepts module paths, or broken governance/migration/EU Data Boundary links remain in `QUESTION_BANK`.
- Validation: all 13 newly selected canonical URLs returned HTTP 200; `python3 -m py_compile azure_learning_app.py` passed; a fresh temporary SQLite database reconciled and loaded all 133 unique records; and the stale-link scan was empty (`FULL_SOURCE_ALIGNMENT_DB_AUDIT: PASS`).
- Rebuilt via `./build-linux.sh`. Root, `dist`, release, and Desktop executables are identical and executable: SHA-256 `bbc84f001d57bc7bb532e6e82ab63f0c8dcb3a628c5396e5499cec4169f45a9b`.
- Files touched: `azure_learning_app.py`, `HANDOFF.txt`.


---
