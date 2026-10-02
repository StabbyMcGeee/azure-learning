---
name: azure-learning-history
description: Recover Azure Learning project history from the handoff archive. Loads the current HANDOFF.txt first, then reads only the archive files relevant to the requested topic, never the whole archive at once.
---

# Azure Learning project-history recovery

Use this skill when the user asks about the history, provenance, decisions,
audit results, legal/store gates, old validation runs, or previous handoff
entries of the Azure Learning project.

## How to recover history

`HANDOFF.txt` is a compact current-state/index, not a transcript. Keep it short; add durable detail to a focused dated archive and add one mapping row here instead of appending history to the handoff. Read only the archive topic needed for the current task.

1. **Read the current handoff first.** Always start by loading
   `HANDOFF.txt` so the response is grounded in the current state and archive
   index.

2. **Pick only the relevant archive files.** Use the topic mapping below.
   Read the listed archive file(s) and **no others**. Do not bulk-load the
   `archive/handoff/` directory. If the request spans multiple topics, read
   each relevant file; still skip unrelated archives.

3. **Answer from the original wording.** Preserve dates, provenance, URLs,
   SHA-256 hashes, caveats, and unresolved gates as written. Do not silently
   rewrite or drop historical facts. Quote specific archive sections when
   useful.

## Archive file map

| Topic | File to load |
|-------|--------------|
| Desktop app implementation, UI/theme work, packaging, validation runs, bugfixes, content expansion | `archive/handoff/desktop-app-development-2026-09.md` |
| Microsoft Learn source links, terminology alignment, retired-product renames, URL audits | `archive/handoff/terminology-and-sources-2026-09.md` |
| AGY QA/usability audits, findings, and the implementation responses that fixed them | `archive/handoff/qa-audits-and-usability-2026-09.md` |
| Mobile product concept, historical pricing, store-release requirements, legal/publishability audits, CloudCert Coach requirements | `archive/handoff/mobile-product-and-release-2026-09.md` |
| Current US$5 multi-course direction, deferred add-on pricing, AI-assisted original content, source-rights and provenance rules | `archive/handoff/product-scope-and-content-rights-2026-10.md` |
| Previous full current-state handoff snapshot (historical, may be superseded) | `archive/handoff/handoff-2026-10-01-pre-85-refresh.md` |
| Current unresolved gates and archive index | `HANDOFF.txt` (always read first) |

## Common trigger phrases

- "What is the history of ...?"
- "Show me previous handoff entries about ..."
- "Recover Azure Learning project history"
- "Why was X decided?"
- "What did the QA audit find?"
- "What are the legal/store blockers?"
- "Summarize the mobile release requirements"
- "What validation was run on the desktop build?"

## Response discipline

- Cite the archive file and dated section you are quoting.
- Distinguish resolved historical work from current open gates (which live in
  `HANDOFF.txt`).
- If the request does not match any archive topic, say so and offer the index
  from `HANDOFF.txt` instead of guessing.
