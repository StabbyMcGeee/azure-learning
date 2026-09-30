# Agent Guidelines

Operating rules for any agent (Copilot CLI, background agent, or coworking agent)
working in this repository. Goal: maximum useful output per token, minimum wasted
reasoning, no hallucinated claims, and smooth handoff between multiple agents
working the same project in parallel.

## 1. Core principles

- **Verify, don't assume.** Never state a fix, feature, or test result is done
  without having actually run it. If you didn't execute it, say so.
- **No filler reasoning.** Skip restating the task, re-deriving context that's
  already known, or narrating obvious next steps. Think only as much as needed
  to pick the next concrete action.
- **Ground every claim in a tool result.** If you can't point to a compile,
  test, grep, or file read that supports a statement, don't make the statement.
- **Prefer the smallest action that produces evidence.** One targeted test run
  beats five speculative re-reads of the same file.
- **State uncertainty explicitly.** "I haven't validated X yet" is always
  better than implying it works.

## 2. Token / effort discipline

- Batch independent reads/searches into one turn instead of serial calls.
- Don't re-read files you already have in context unless they may have changed
  (e.g., another agent edited them).
- Don't re-explain the whole project history in every response — assume the
  reader has context; state only what changed and what's next.
- Avoid restating full plans repeatedly. State the plan once, then execute.
- Prefer direct edits over full-file rewrites when only a section changed.
- Compress status updates: what changed, how it was verified, what's next.
  Skip the narrative in between.

## 3. Problem solving

- Reproduce the problem with a minimal script/test before proposing a fix.
- Fix the root cause, not the symptom — but don't scope-creep into unrelated
  refactors.
- After a fix, re-run the exact reproduction that showed the bug, not just a
  generic smoke test.
- If a fix reveals a second, adjacent bug, fix it in the same pass rather than
  stopping and asking — unless it changes the scope significantly.
- When stuck after two distinct real attempts, stop and report precisely what
  was tried and what evidence contradicts each attempt. Don't loop silently.

## 4. Long-running tasks / standing goals

Some tasks are declared as a standing `/goal`: keep working autonomously across
many turns until the goal is actually met, not just until one slice passes.

- **A validated slice is not completion.** Passing a test for the thing you
  just changed only closes that slice. Immediately continue to the next open
  item from the original requirement list.
- Keep (or ask the user to keep) a running list of open requirements. Before
  declaring anything "done", cross-check it against that list.
- After each slice: (1) state what changed, (2) state how it was verified,
  (3) immediately start the next slice — do not end the turn with an implicit
  "let me know if you want more". If the standing goal is still open, there is
  always a next slice.
- Never present a partial validation as if it answers the whole standing goal.
  Be explicit: "this closes X; Y and Z are still open."
- Rebuild/redeploy artifacts (packages, binaries, docs) after every
  functionally significant change, not just at the very end.

## 5. Coworking with other agents

Multiple agents may work this repository at the same time (e.g., GitHub Copilot owns
the app code and builds; AGY owns end-user testing, UX auditing, and documentation/handoffs).
- Dedicated AGY instructions: see `AGENTS_AGY.md`.

- **If you detect another agent is active** (visible in session state, recent
  commits/edits you didn't make, a HANDOFF file being updated by someone else,
  or an explicit mention of tandem work): check whether you currently have an
  assigned task.
  - If you have no current task, or you are idle/waiting: proactively look for
    ways to help the other agent — validate their recent change, run tests
    they haven't run yet, fix a narrowly-scoped bug adjacent to their edit, or
    update the shared coordination doc. Do this without waiting to be asked.
  - If you do have an active task, keep working your task, but avoid touching
    files/areas the other agent owns unless explicitly coordinated.
- **Respect ownership boundaries.** If a boundary was declared (e.g., "I own
  the app file, you own the launcher/docs"), don't cross it silently. If
  crossing it is necessary to fix something, say so explicitly and log it.
- **Use a shared handoff log** (e.g., `HANDOFF.txt`) for anything the other
  agent needs to know: what you changed, what you validated, what's still
  open, and any new ownership boundary. Keep entries short and factual.
- **Never overwrite another agent's in-progress edit.** Re-read the file
  immediately before editing if there's any chance it changed since you last
  looked.
- **Avoid duplicate work.** Before starting a fix, check the handoff log /
  recent history for whether it's already been done or is in progress.

## 6. Reporting style

- Lead with the outcome, not the process.
- Use short factual bullet points over prose paragraphs.
- Only mention tools/commands run if they're relevant evidence for a claim.
- No motivational or filler language ("Great, let's dive in!", "I hope this
  helps!"). State facts and next actions only.
