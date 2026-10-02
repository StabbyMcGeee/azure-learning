# Content provenance register (launch packs)

This file records the rights basis and source evidence for the launch content
pack shipped at `assets/content-pack.json`. It is a reviewer-facing record; it
does **not** by itself prove rights clearance. A qualified human (the captain,
as publisher) reviews and attests before sale, per the settled authoring route.

No external rights database backs this record. The rights-basis enum and the
terminology register it relies on are the ones declared in
`tool/build_content_pack.py` (`PERMITTED_RIGHTS_BASES` and `RETIRED_TERMS`);
the full rights audit lives outside this repository and is not duplicated
into it.

The pack is generated from the authoring sources under `tool/content/` by
`tool/build_content_pack.py`. Edit the authoring sources, then regenerate:

```bash
python3 tool/build_content_pack.py
```

## Authoring route (settled 2026-10-02)

- Content is authored by the AI fleet (firstmate + crew) as fresh originals.
- The captain supplies substantive human review/authorship; there are no
  in-house or freelance human authors.
- This is the accepted weaker-ownership route recorded in
  `archive/handoff/product-scope-and-content-rights-2026-10.md`.

**Review status: PENDING.** The captain's substantive human review has **not**
yet been performed. It must happen before paid sale. The per-item `source`
field records the review as pending, not as done.

**Rights basis per item:** `original-human-ai-assisted` (the human publisher
makes the substantive expressive choices through review; the AI fleet drafts).
This is one of the permitted values in `PERMITTED_RIGHTS_BASES`
(`tool/build_content_pack.py`). Every question in the pack carries this value in
its `rightsBasis` field.

## Source discipline

Each item was authored from, and only from:

1. The snapshotted public skills-measured outline (objective scope), and
2. Standard Microsoft Learn product facts (terminology, capabilities).

No question text from the 133-question desktop bank, no recalled exam item,
and no vendor bank was read or reused. The existing 133-question bank was
used only as a coverage index (metadata only: id, category, type, difficulty,
source URL); each slot was then rewritten from scratch, so no slot ships with
the original wording or a legal issue carried over. The resulting
slot-to-objective mapping is recorded in the coverage tables below and in the
`tool/content/` module docstrings.

## Outline snapshots (authoritative exam wording)

| Course | Study guide | Skills measured as of | Retrieved |
|---|---|---|---|
| AZ-900 | `https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-900` | July 20, 2026 | 2026-10-02 |
| DP-900 | `https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/dp-900` | July 21, 2026 | 2026-10-02 |
| AI-901 | `https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-901` | April 15, 2026 | 2026-10-02 |

AI-900 is retired (2026-06-30); the current exam code is AI-901. SC-900 is
staged after launch and is not part of this pack.

## Terminology preserved verbatim

Exact official Azure terminology is preserved per the terminology register in
`tool/build_content_pack.py` (`RETIRED_TERMS`). Notable verbatim terms used in
this pack include:

- `Microsoft Entra Conditional Access`
- `region pairs` (never "regional pairs" or "paired regions")
- `locally redundant storage (LRS)`, `zone-redundant storage (ZRS)`,
  `geo-redundant storage (GRS)`, `geo-zone-redundant storage (GZRS)` (never
  "geo redundant zones")
- `Microsoft Entra ID` (never "Azure AD" / "Azure Active Directory")
- `Microsoft Defender for Cloud` (never "Azure Security Center")
- `Azure Virtual Machine Scale Sets` (never "VM scale sets")
- `Azure role-based access control (RBAC)` (always qualified; never bare "RBAC")
- `external identities` (never "Azure AD B2B/B2C")
- AI-901: `Microsoft Foundry`, `Foundry portal`, `Foundry SDK`,
  `Azure Speech in Foundry Tools`, `Azure Content Understanding in Foundry Tools`

Retired AI-901 study-resource wording (LUIS, Language Understanding, Anomaly
Detector, Azure Bot Service, Form Recognizer, Azure AI Document Intelligence,
Azure OpenAI, Azure AI Foundry) is not used.

## Coverage

| Course | Items | Basis |
|---|---|---|
| az-900 | 152 | 129 existing-bank slots rewritten as fresh originals on their public objective, 6 out-of-scope topics re-scoped, 7 outline gap topics added, plus 16 domain-weighting and missing-objective items (az-900-141..156, ending with storage tiers and defense-in-depth) |
| dp-900 | 57 | Authored from the DP-900 skills outline (all four domains) |
| ai-901 | 49 | Authored from the AI-901 skills outline (both domains) |

Domain weighting is aligned to the published study-guide bands:

| Course | Domain weighting |
|---|---|
| az-900 | Cloud Concepts 26.3% (25-30), Architecture 39.5% (35-40), Management and Governance 34.2% (30-35) |
| dp-900 | Core 28.1% (25-30), Relational 22.8% (20-25), Non-relational 19.3% (15-20), Analytics 29.8% (25-30) |
| ai-901 | AI Concepts and Capabilities 44.9% (40-45), Microsoft Foundry 55.1% (55-60) |

### AZ-900 re-scoped slots (out-of-scope bank topic -> nearest objective)

| Bank slot | Bank topic (out of scope) | Replacement objective |
|---|---|---|
| az-900-078 | Azure Backup | AA.2 availability sets |
| az-900-087 | "6 Rs" of app modernization | AA.3 Azure Migrate |
| az-900-108 | Cloud Adoption Framework | DC.2 benefits of cloud services |
| az-900-125 | Azure support plans | MG.1 Microsoft Cost Management |
| az-900-126 | Service Trust Portal | MG.2 Microsoft Purview |
| az-900-132 | Azure Lighthouse | MG.3 Azure Arc-enabled Kubernetes |

### AZ-900 bank slots dropped as duplicate topics

The shipped AZ-900 ids run `001`..`156`. Four bank slots have no shipped id
because their topic was already covered by a stronger item and keeping both
would ship near-duplicate questions. Their subject is not lost:

| Dropped slot | Duplicate topic | Retained coverage |
|---|---|---|
| az-900-019 | private IP address inside a virtual network | az-900-043, az-900-102 |
| az-900-056 | what ExpressRoute provides | az-900-013, az-900-070 |
| az-900-061 | private endpoint benefit for storage | az-900-063, az-900-102 |
| az-900-090 | availability-zone characteristics | az-900-010, az-900-015, az-900-128, az-900-129 |

### AZ-900 gap topics added (not covered by the 133-question bank)

Azure Virtual Desktop (az-900-134), sovereign regions (az-900-135), Microsoft
Entra Domain Services (az-900-136), external identities (az-900-137), AzCopy
(az-900-138), Azure File Sync (az-900-139), Azure Storage Explorer
(az-900-140). Missing-objective items added: storage tiers (az-900-155),
defense-in-depth (az-900-156).

## Validation

- `python3 tool/build_content_pack.py` regenerates the pack and enforces:
  schema shape, unique ids, correctOptionIndex in range, rightsBasis enum,
  courseId enum, and terminology lint (retired wording and bare "RBAC").
- `flutter test test/content_pack_production_test.dart` validates the shipped
  artifact with the app's own `ContentPackValidator`.
- `flutter analyze` is clean; the full mobile test suite passes.

## Open item for the content-integrity gate

The content-integrity branch (`fm/azcontent-gate-v1`) ships a terminology lint
that currently matches retired wording by naive substring. That lint would
falsely flag the official term "Azure Advisor" as retired wording "Azure AD".
This pack uses "Azure Advisor" (an MG.4 outline term) correctly; the lint
should use whole-word matching before it gates this content.
