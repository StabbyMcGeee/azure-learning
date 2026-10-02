# Product scope and content-rights direction — 2026-10-01

## Product direction
The app's current price direction is US$5 one-time for a multi-course base app, not an AZ-900-only app. Larger courses such as AZ-104 may be considered as paid additions later; the captain deferred that pricing and in-app purchase design. The intent is to offer a useful service, cover platform/deployment costs, and leave a profit without paying the owner a salary. Apple Developer enrollment/payment and Google Play registration are postponed until the app is tested and consumer-ready. Known account charges are Apple US$99/year and Google US$25 once, plus store commissions. Do not cut product or legal quality to protect the provisional schedule.

The intended base course list is not decided. The code should support multiple selectable course packs without inventing a course list or silently pricing later add-ons.

## Content creation and use
The captain permits AI-assisted/original study material; human authorship is not a requirement. A content worker is requested to research sources online, screen the existing question bank item by item, verify source facts and commercial-use terms, and create original replacements when an item/source cannot be used.

This permission is not a legal clearance. Public availability does not itself grant commercial reuse. Do not copy, closely paraphrase, or redistribute material whose terms do not permit the intended use; do not use a paraphrase as a workaround for restricted expression. Do not reproduce, reconstruct, or use leaked/recalled real certification exam questions or answer keys. Prefer sources with explicit commercial-reuse permission and independently authored scenarios/questions grounded in verifiable facts. Keep item-level provenance: source title and URL, access date, exact applicable license/terms and version, factual claim supported, rights rationale, authoring method, and review notes. Never label AI-authored/reworked content human-authored.

The legacy 133-question desktop bank is not currently rights-cleared for paid mobile use. It may be retained only when item-specific provenance and rights are affirmatively established; otherwise replace it with original material from acceptable sources or omit it. Existing reports at `data/azcontent-a3/report.md` and `data/azstore-l5/report.md` provide the factual/content and legal/store audit context. A qualified human legal review remains necessary before paid release; an agent cannot guarantee that copyright, licensing, exam-provider terms, or other rights are cleared.

## Technical implications and release gates
The current mobile content-pack implementation supports a single pack; the product direction requires a multi-course catalog/selector and course-scoped progress/persistence. It currently contains no production questions. Extend the pack metadata to retain authoring method and per-item rights evidence. Keep the production bank empty until each item has been reviewed.

The provisional name ExamNimbus is not cleared for public use or final identifiers. Keep identifiers generic pending exact-name screening and human legal review. Android/iOS builds and device acceptance, accessibility/offline QA, privacy/support information, signing, and store review remain release requirements. Publishing fees stay deferred until the consumer-ready gate.

## Related archive
The previous current-state document is preserved at `archive/handoff/handoff-2026-10-01-pre-85-refresh.txt`; consult the archive map in `.agents/skills/azure-learning-history/SKILL.md` for older desktop, source, QA, mobile, and release history.
