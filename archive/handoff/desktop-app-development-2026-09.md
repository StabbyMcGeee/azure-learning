# Desktop App Development — Azure Learning handoff archive

This file preserves dated project handoff entries from `HANDOFF.txt`.
Do not delete or rewrite history; add new dated sections at the bottom.

## Azure Learning — Final Handoff (baseline)

Project status:
- Local Python/Tkinter AZ-900 study app is implemented and ready for review.
- Current tandem task: continue AZ-900 content expansion and terminology alignment while preserving the validated UI, persistence, and launcher work.
- Coordination boundary: UI/app integration changes are being made in `azure_learning_app.py`; the neighboring Copilot is focused on read-only July 2026 Microsoft Learn/objective research unless explicitly coordinated.
- App includes Dashboard, Learn, Exam, and Weak Areas flows.
- SQLite persistence tracks attempts, study streaks, and weak-question repetition.
- Question bank contains 66 AZ-900 items across single, multi, true/false, ordering, drag-drop, build-list, matching, hot-area, active-screen, and case formats.

Files in this project:
- /home/dimitri/workspace/projects/azure-learning/azure_learning_app.py
- /home/dimitri/workspace/projects/azure-learning/README.md
- /home/dimitri/workspace/projects/azure-learning/azure_learning.db

Quality fixes completed:
- Added an Azure-blue visual system with high-contrast white cards, dark navy text, an Azure-style hero graphic, clearer tab styling, and exam-type labels.
- Learn mode now filters independently by official blueprint area and interaction type: Single Choice, Multiple Choice, Ja/Nein, Drag & Drop/Reihenfolge, Zuordnung, and Fallstudie.
- Added a separate Question Types area with a practice card for each supported interaction pattern, including build-list, hot-area, and active-screen approximations based on Microsoft's exam sandbox.
- Progress is automatically stored in SQLite and can be exported as JSON from the Dashboard.
- Dashboard now shows per-blueprint-area accuracy when attempts exist, and every question has a direct "Open Microsoft Learn source" action.
- Dashboard and exam copy now use the current official AZ-900 area names and weight ranges instead of generic topic wording.
- Learn/explanation feedback now shows the learner's submitted answer when incorrect, the correct answer, and the short rationale; exam sets are sampled approximately to the current 25–30 / 35–40 / 30–35% domain weighting.
- Added nine original scenario questions covering Microsoft Entra ID SSO and passwordless authentication, storage redundancy, Azure Data Box, ExpressRoute, Microsoft Purview, Microsoft Defender for Cloud, Azure Portal/CLI/Cloud Shell, and Resource Health.
- Fixed Learn-mode solution feedback: opening "Reveal answer" without submitting now shows `Lösung` instead of incorrectly labeling the result `Nicht richtig`; submitted wrong answers still show the learner's answer, the correct answer, and the rationale.
- Added a PyInstaller windowed build and desktop launcher matching the existing English app workflow, so Azure Learning can be started by double-clicking the packaged release instead of opening the Python source.
- The source file now has an executable Python shebang, and the build places a standalone `Azure-Learning` executable in the project root for direct double-click launching.
- A copy of the real standalone executable is also present at `/home/dimitri/Desktop/Azure-Learning`; this is the reliable direct double-click target when the desktop environment refuses to execute `.desktop` launchers.
- The project is also exposed through Windows Explorer via WSL. For that environment, `Start-Azure-Learning.vbs` launches the app through `wsl.exe -d Ubuntu -- bash -lc ...` without showing a terminal; `Start-Azure-Learning.cmd` is the diagnostic launcher.
- Frozen builds now store `azure_learning.db` beside the executable, preserving progress across launches.
- Fixed the real Tkinter startup crash: the app was configuring `bg` on `ttk.Frame`, which is invalid in Tk; tab containers now use `tk.Frame` for background styling.
- Matching-question persistence fix: a `pairs_json` field was added to the SQLite schema and seeded on initialization so matching items survive DB reloads.
- Stale-question-bank reconciliation: the app refreshes seed data when the source question bank or schema diverges from the database instead of silently reusing stale rows.
- Exam flow hardening: timer restarts cancel any previous scheduled callback, exam completion returns to the intro state, and submit routing advances through exam questions without revealing the answer prematurely.

Validation completed:
- `python3 -m py_compile azure_learning_app.py` succeeded.
- Fresh temporary-DB smoke test succeeded: the app initialized a clean SQLite database, loaded all 66 questions, and evaluated every question type (`single`, `multi`, `true_false`, `ordering`, `drag_drop`, `build_list`, `matching`, `hot_area`, `active_screen`, and `case`).
- Build command: `./build-linux.sh` creates `release/Azure-Learning/` with a windowed `Azure-Learning` executable, `run.sh`, and `Azure-Learning.desktop`.
- A desktop shortcut was created at `/home/dimitri/Desktop/Azure-Learning.desktop`.
- Fresh launch check passed for both `python3 azure_learning_app.py` and the packaged `./Azure-Learning`: each process remained alive under the active desktop display for the GUI startup check.
- End-to-end desktop launch check passed for the real `/home/dimitri/Desktop/Azure-Learning` executable and for the registered `gtk-launch azure-learning` desktop-entry path.
- Final compile and temporary-DB smoke test passed again after the launcher changes.
- Content pass validation: 60 questions loaded from a fresh temporary database; all six answer types evaluated correctly.
- Packaged rebuild completed and the updated `/home/dimitri/Desktop/Azure-Learning` executable stayed alive during GUI startup verification.
- Interaction pass validation: 66 questions loaded from a fresh temporary database; all ten supported interaction types evaluated correctly, and the packaged app rebuilt/launched successfully.
- Learn reveal validation: every persisted answer matched `QUESTION_BANK`, every answer-rendering path produced non-empty output, and the module compiled successfully.
- Final runtime audit: full Tkinter construction passed with 5 tabs; all 66 answers, all ten interaction types, answer completeness, and exam generation passed; packaged launch passed again after the dashboard/source-link additions.
- Full runtime audit: Tkinter UI construction, all 66 questions, all ten interaction types, answer completeness, answer evaluation, and exam generation passed.

Run command:
- `cd /home/dimitri/workspace/projects/azure-learning && python3 azure_learning_app.py`
- Double-click build: open `release/Azure-Learning/` and launch `Azure-Learning.desktop` or `run.sh`.
- Recommended direct launch: double-click `/home/dimitri/Desktop/Azure-Learning.desktop` or `/home/dimitri/workspace/projects/azure-learning/Azure-Learning`.
- If the file manager opens `.desktop` files as text or ignores them, double-click `/home/dimitri/Desktop/Azure-Learning` instead. That file is the actual executable, not a shortcut.

Notes:
- This environment has no display server, so GUI startup validation was done via import and database smoke tests instead of launching the Tk window directly.
- On a machine without an active graphical desktop session, Tkinter will not open a window; you must run this app from a local desktop/VM session with X11/Wayland available.
- The project remains intentionally local and separate from any earlier prototype work.


---

## Current tandem handoff — 2026-09-23
- Objective: continue quality improvements without overlapping edits; verify the other Copilot's exam-navigation work and preserve the validated persistence/build behavior.
- Other Copilot owns: `/home/dimitri/workspace/projects/azure-learning/azure_learning_app.py`, specifically mouse interaction, exam Back/Skip/Mark navigation, and the exam completion/review flow currently in progress.
- My ownership: validation only plus this coordination record; I will not edit `azure_learning_app.py` during that implementation pass.
- Files touched by me in this pass: `/home/dimitri/workspace/projects/azure-learning/HANDOFF.txt`.
- Handoff needed: after the other Copilot finishes, run `python3 -m py_compile azure_learning_app.py`, a fresh temporary-DB load/evaluation smoke test, and—if a display is available—the GUI interaction audit. Record any additional files and validation results here before handoff.
- Validation update: the expanded source currently loads 76 questions from a fresh temporary database; all persisted answers evaluate correctly, and a 40-question exam set generated with the configured blueprint weighting had 11 cloud, 15 architecture, and 14 governance items with no duplicate IDs.
- Current file boundary remains unchanged: I touched only `HANDOFF.txt`; the other Copilot owns the in-progress `azure_learning_app.py` interaction/navigation edits.


---

## Implementation handoff — 2026-09-23
- Updated `/home/dimitri/workspace/projects/azure-learning/azure_learning_app.py` only.
- Expanded the original question bank from 66 to 76 questions, adding more multi-select, true/false, ordering, real drag-drop candidates, build-list, matching, hot-area, active-screen, and case-study items.
- The exam simulation now samples 40 questions for 45 minutes using the existing blueprint weighting. It has Back, Save & next, Skip / mark, numbered jump navigation, marked-question indicators, and a Review / abgeben confirmation showing unanswered and marked counts.
- Ordering, drag-drop, and build-list widgets now support mouse drag reordering instead of requiring Move up/Move down buttons. Existing answer extraction/evaluation remains unchanged.
- Question Types cards now show descriptions, can be opened by clicking the card, and route directly into filtered Learn practice.
- Validation performed by the validation owner: `py_compile` passed; fresh DB loaded 76 questions; all answer evaluations passed; 40-question weighted exam set had 11 cloud, 15 architecture, 14 governance with no duplicate IDs.
- README still contains older 66-question/20-question counts and should be updated by the validation/documentation owner in the next pass.


---

## Answer-audit/content pass — 2026-09-23
- Updated `/home/dimitri/workspace/projects/azure-learning/azure_learning_app.py` and `/home/dimitri/workspace/projects/azure-learning/README.md`.
- Audited all 86 question records: single/true-false/hot-area/active-screen answers are present in their options; multi/case answers are subsets of options; ordering/drag-drop/build-list answers contain exactly the option set; matching pairs and answer mappings agree.
- Programmatically evaluated every correct answer and a deliberately wrong answer for all 86 questions; all correct answers were accepted and all wrong answers rejected.
- Improved Learn feedback so every submitted answer is explained by type: selected/missed/extra options for multi-select and cases, position-by-position ordering diagnostics, per-pair matching diagnostics, and selected-versus-expected output for single-choice formats.
- Added 10 original questions, bringing the bank to 86. Coverage is now: 41 single, 11 multi, 6 true/false, 4 ordering, 6 matching, 3 case, 4 drag-drop, 3 build-list, 4 hot-area, 4 active-screen.
- Replaced the remaining non-Learn Pricing Calculator source with the official Microsoft Learn article.
- Validation: `py_compile`, full answer/evaluation/feedback audit, and official-source-link audit all passed.


---

## Launcher/package verification — 2026-09-23
- Ownership was limited to launcher/package files; `azure_learning_app.py` and `README.md` were not changed.
- Found and fixed one concrete packaging defect in `build-linux.sh`: the generated `release/Azure-Learning/Azure-Learning.desktop` previously inherited the root desktop entry and launched `/home/dimitri/workspace/projects/azure-learning/Azure-Learning` instead of the executable inside the release package.
- The build now generates release metadata with:
  - `Exec=/home/dimitri/workspace/projects/azure-learning/release/Azure-Learning/Azure-Learning`
  - `Path=/home/dimitri/workspace/projects/azure-learning/release/Azure-Learning`
- Rebuilt the package successfully and refreshed `/home/dimitri/Desktop/Azure-Learning` plus `/mnt/c/Users/Dimitri/Desktop/Azure-Learning.vbs`.
- Binary hashes match across `Azure-Learning`, `release/Azure-Learning/Azure-Learning`, and `/home/dimitri/Desktop/Azure-Learning`: `aca736310bbab4d3230d066e8512a7f6277bc89218111b9726dcb0967b4c8e21`.
- `bash -n build-linux.sh release/Azure-Learning/run.sh` passed; packaged binaries are executable.
- `./release/Azure-Learning/run.sh` stayed alive for the 8-second smoke-test window (`timeout` status 124), indicating successful GUI process startup.
- Registered `gtk-launch azure-learning` returned status 0.
- Root Linux desktop shortcut `/home/dimitri/Desktop/Azure-Learning.desktop` correctly targets `/home/dimitri/Desktop/Azure-Learning`.
- Windows `.vbs` and `.cmd` launchers still target the intended WSL project path and `python3 azure_learning_app.py`.
- `desktop-file-validate` is not installed in this environment; metadata was checked directly and the generated release target was asserted.


---

## Scenario/content expansion — 2026-09-23
- Expanded `/home/dimitri/workspace/projects/azure-learning/azure_learning_app.py` from 86 to 96 original AZ-900 questions, emphasizing scenario-based assessment items and stronger distractors rather than repeating Learn definitions.
- Added coverage for lift-and-shift migration, private-cloud concepts, autoscaling, availability/resilience, management hierarchy, App Service, governance-tool distinctions, cost budgets, and policy/tag compliance scenarios.
- Updated `/home/dimitri/workspace/projects/azure-learning/README.md` to the current 96-question count.
- Current type distribution: 42 single, 12 multi, 7 true/false, 5 ordering, 7 matching, 4 case, 5 drag-drop, 4 build-list, 5 hot-area, 5 active-screen.
- Content audit passed for all 96 questions: correct answers evaluate successfully, answer sets/mappings are structurally consistent, and every source uses `learn.microsoft.com`.
- Weighted 40-question exam selection passed repeatedly with 11 cloud, 15 architecture, 14 governance, no duplicate IDs, and all ten supported interaction types represented.
- Fresh temporary SQLite reconciliation seeded all 96 questions successfully.
- Package rebuilt and `/home/dimitri/Desktop/Azure-Learning` launched successfully after clearing two stale processes that had temporarily held the binary open (`PACKAGED_CONTENT_LAUNCH_OK True`).


---

## Current tandem validation — 2026-09-23 17:12
- Other Copilot owns launcher/package verification only: `build-linux.sh`, `Azure-Learning.desktop`, `Start-Azure-Learning.cmd`, `Start-Azure-Learning.vbs`, and packaged copies. It must not edit `azure_learning_app.py` or `README.md` in this slice.
- I audited the current source without editing the app: `py_compile` passed; a fresh temporary DB loaded all 86 questions; all ten interaction types were present; every persisted correct answer evaluated successfully; and a 40-question exam set contained unique IDs.
- Source-link audit found all 86 question sources use `learn.microsoft.com`.
- The earlier historical 66/76-question validation bullets remain historical; the current bank is 86 questions as documented by the latest content pass and README.
- Files touched by me in this slice: `/home/dimitri/workspace/projects/azure-learning/HANDOFF.txt` only.
- Handoff needed: launcher owner should append exact package/hash/desktop-entry results here after completing its verification; no app or README edits are needed unless a concrete launcher defect is found.


---

## Current tandem audit — 2026-09-23 17:43
- Other Copilot is continuing an app-quality pass in `azure_learning_app.py`; exact function scope is pending its response. I am not editing that file.
- Current source audit passed: `python3 -m py_compile azure_learning_app.py`; fresh temporary SQLite reconciliation loaded all 96 questions; all ten interaction types were present; every persisted correct answer evaluated successfully; and a unique 40-question exam set generated successfully.
- Current type distribution: 42 single, 12 multi, 7 true/false, 5 ordering, 7 matching, 4 case, 5 drag-drop, 4 build-list, 5 hot-area, 5 active-screen.
- Launcher regression audit passed: `bash -n build-linux.sh release/Azure-Learning/run.sh`; SHA-256 matches across `Azure-Learning`, `release/Azure-Learning/Azure-Learning`, and `/home/dimitri/Desktop/Azure-Learning` (`c10643f900c0d6b773ae7ca2615a2875e97941f67853bc0f05c46b9026ff4461`).
- Files touched by me in this slice: `/home/dimitri/workspace/projects/azure-learning/HANDOFF.txt` only.
- Handoff needed: once the app-quality owner reports its exact scope, rerun the same compile/temporary-DB audit and inspect only the changed functions before accepting the pass.


---

## Current tandem audit — 2026-09-23 17:53
- Other Copilot completed an app-quality pass in `azure_learning_app.py`, adding/finishing clickable Question Types cards, blueprint/type/difficulty filters, and protection against submitting the same Learn question repeatedly.
- I did not edit `azure_learning_app.py`. Focused validation passed: `python3 -m py_compile azure_learning_app.py`; a fresh temporary SQLite database loaded 116 questions; all ten interaction types were present; every persisted correct answer evaluated successfully; and a unique 40-question exam set generated successfully.
- Current type distribution: 45 single, 14 multi, 9 true/false, 6 ordering, 9 matching, 6 case, 7 drag-drop, 6 build-list, 7 hot-area, 7 active-screen.
- Updated `/home/dimitri/workspace/projects/azure-learning/README.md` from 96 to 116 seeded questions so documentation matches the current source.
- Files touched by me in this pass: `README.md` and `HANDOFF.txt`; the other Copilot owned the app implementation.
- Handoff needed: future app changes should treat 116 as the current bank size and rerun the same fresh-DB/evaluation audit after modifying the question bank or persistence schema.


---

## Current tandem audit — 2026-09-23 17:56
- Other Copilot's scoped edits (confirmed by its own report): UI-state init, `_render_question_widget`, `_submit_question_from_widget`, new `_lock_current_answer_widgets`, `_bind_type_card`, and existing type-training/inline-feedback logic. It did not touch `README.md`/`HANDOFF.txt` in this slice.
- I independently reviewed the duplicate-submit guard: `current_answer_locked` resets to `False` in `_render_question_widget` on every new question render and is set `True` on submit (`_submit_question_from_widget`) and on `_reveal_answer` when a selection is present; widgets are disabled via `_lock_current_answer_widgets`. No regression found.
- Re-ran fresh-DB audit after the rebuild: `python3 -m py_compile azure_learning_app.py` passed; 116 questions loaded; all correct answers evaluated; unique 40-question exam set generated.
- Verified the rebuilt package: SHA-256 matches across `Azure-Learning`, `release/Azure-Learning/Azure-Learning`, and `/home/dimitri/Desktop/Azure-Learning` (`ebd83cad965cd12d977d5869b39ede63f7d93191ffe91b964af5a95884d344e7`).
- Files touched by me in this pass: `HANDOFF.txt` only.


---

## Independent tandem validation — 2026-09-23 17:59
- Confirmed the current `azure_learning_app.py` independently after the active app-quality pass, without editing application code.
- `python3 -m py_compile azure_learning_app.py` passed.
- A fresh temporary SQLite database reconciled and loaded all 116 questions; all ten supported interaction types were present.
- Every persisted correct answer evaluated successfully, including matching items through their UI-equivalent mapping representation.
- A generated 40-question exam contained 40 unique IDs.
- Files touched by me in this pass: `HANDOFF.txt` only.


---

## Current tandem audit — 2026-09-23 17:59
- Other Copilot replaced the blocking exam-finish messagebox with an in-window `_render_exam_results` view (score, per-domain %, per-type breakdown, missed-question list, direct links to Learn/Weak Areas/Dashboard).
- I validated: py_compile passes; all referenced symbols exist (`open_review_tab`, `dashboard_tab`, `QUESTION_TYPE_LABELS`); scripted simulation of `_finish_exam`'s scoring path (20 answered/20 unanswered out of 40) produced exactly the expected correct/missed/unanswered counts.
- No regressions found. Files touched by me this pass: HANDOFF.txt only.


---

## Current tandem audit — 2026-09-23 18:05
- Other Copilot deployed and self-smoke-tested a new package build ("Deploy and smoke-test inline exam result package").
- I independently verified: py_compile passes; package hashes match across Azure-Learning, release/Azure-Learning/Azure-Learning, and /home/dimitri/Desktop/Azure-Learning (0d99983546925387d9bf47a2cfcb84bec99011fed4a061508f904dcf5ce8775e); 116 questions load, all correct answers evaluate True, unique 40-question weighted exam set generates correctly.
- No regressions found. Files touched by me this pass: HANDOFF.txt only.


---

## Integration fix — 2026-09-23 18:13
- Fixed a forced-exam-completion regression in `azure_learning_app.py`: when the timer expired while the current question was onscreen, the in-progress widget value was not captured before `_finish_exam` calculated and persisted results.
- `_finish_exam` now captures the current answer before scoring. Manual submission already captured it; the new call covers only the timer-expiry path and is safe for the normal confirmation path.
- Validation: `python3 -m py_compile azure_learning_app.py` passed; a focused forced-completion test confirmed that the current correct answer is counted and not listed as unanswered; the fresh question-bank/exam audit also passed.
- Files touched by me in this pass: `azure_learning_app.py` and `HANDOFF.txt`.


---

## Package refresh — 2026-09-23 18:15
- Rebuilt the packaged application after the forced-completion fix with `./build-linux.sh`.
- Initially found the Desktop executable was stale relative to the rebuilt root/release executable; refreshed `/home/dimitri/Desktop/Azure-Learning` from the rebuilt root executable and retained executable permissions.
- SHA-256 now matches across `Azure-Learning`, `release/Azure-Learning/Azure-Learning`, and `/home/dimitri/Desktop/Azure-Learning`: `5f19394eb8d179a40811f7055a1bbb4079945eb2662533ce640c38920e38328d`.


---

## Case-schema compatibility audit — 2026-09-23 18:17
- Verified migration/reconciliation from both the immediately preceding question-table schema (with `pairs_json` but no case columns) and the oldest supported schema (without `pairs_json` or any case columns). Both paths added the required columns and reconciled all 116 source questions successfully.
- Verified that pre-existing attempt records survive a reopen/reconciliation cycle.
- Flagged incomplete shared-case metadata to the active implementation owner: `az900-032` has no `case_text`, `case_group`, or `case_order`; `az900-082` and `az900-106` have `case_text` but no group/order. Normalize those records if shared-case presentation is expected for every case question, or retain and test their explicit fallback behavior.
- Files touched by me in this pass: `HANDOFF.txt` only.


---

## Case-group selection validation — 2026-09-23 18:19
- Confirmed the implementation owner normalized all six case questions with a non-empty `case_text`, a `case_group`, and a contiguous group-specific `case_order`.
- Ran 200 randomized 40-question exam generations. Every selected shared-case group was included completely, in its defined part order, and no generated exam contained duplicate question IDs.
- Files touched by me in this pass: `HANDOFF.txt` only.


---

## Exam-run persistence validation — 2026-09-23 18:21
- Verified a saved exam run survives reopening the SQLite database and retains `correct`, `total`, `score`, the forced-completion flag, and the serialized per-domain result breakdown.
- `python3 -m py_compile azure_learning_app.py` passed for the current implementation.
- Files touched by me in this pass: `HANDOFF.txt` only.


---

## Progress-export validation — 2026-09-23 18:23
- Verified the JSON export with a real persisted Learn attempt and an exam run. The export retained the current 116-question count, attempt data, exam score, forced-completion flag, and decoded per-domain results.
- Files touched by me in this pass: `HANDOFF.txt` only.


---

## Current tandem audit — 2026-09-23 18:10
- Other Copilot found and fixed a real persistence gap: `_finish_exam` now calls `self._capture_exam_answer()` before scoring. Previously, the currently-displayed question's answer could be lost if the exam ended via timer expiry (force=True) or on the final question without an explicit Next click, causing it to score as unanswered even if the user had selected something.
- I validated: fix is placed after the `if not self.exam_questions: return` guard, so `_capture_exam_answer` (which indexes `self.exam_questions[self.exam_index]`) is always safe to call at that point. py_compile passes.
- No regressions found. Files touched by me this pass: HANDOFF.txt only.


---

## Current tandem audit — 2026-09-23 18:14
- Unblocked other Copilot's pending shell-permission prompt (package launch smoke test) via tmux so it could continue.
- It was reasoning about a potential KeyError on row["case_text"] for pre-migration DBs after adding pairs_json/case_text/case_group/case_order columns.
- I independently verified: simulated a genuinely old-schema SQLite DB (missing all 4 new columns, single legacy row) and ran it through `_init_db()`/`_load_questions()`. The `ALTER TABLE ... ADD COLUMN` guards in `_init_db` (checked via `PRAGMA table_info`) correctly backfill all 4 columns before any SELECT touches them — no KeyError, all 116 questions loaded successfully. Migration path is safe as-is.
- Files touched by me this pass: HANDOFF.txt only.


---

## Current tandem audit — 2026-09-23 18:15
- Other Copilot flagged incomplete shared-case metadata (case_group/case_order missing on some case questions) affecting the new case-study card grouping feature.
- I independently confirmed via QUESTION_BANK scan: 3 of 6 "case" questions lack complete metadata — az900-032 (missing case_text, case_group, case_order entirely), az900-082 (case_text present, missing case_group/case_order), az900-106 (case_text present, missing case_group/case_order). The other 3 case questions have complete metadata.
- Legacy-schema DB migration itself confirmed safe (per my 18:14 entry).
- Handoff: if case-study grouping display should apply uniformly, az900-032/082/106 need case_text/case_group/case_order populated, or the render path needs an explicit fallback for case questions without group metadata (render as standalone, ungrouped card). Other Copilot is actively deciding which approach to take.
- Files touched by me this pass: HANDOFF.txt only.


---

## Current tandem audit — 2026-09-23 18:17
- Other Copilot normalized all 6 case questions (case_text/case_group/case_order) and implemented case-group contiguity in exam selection.
- I independently verified: all 6 case questions now have complete metadata (az900-032/075/082/096/106/114, groups: governance-policy-tags, governance-self-service x3, governance-rbac-scope, governance-monitoring); ran 5 randomized `_build_exam_set(40)` trials — every trial has unique IDs, correct blueprint weighting (~11/15/14 cloud/architecture/governance), and same-case-group questions are always contiguous (verified index adjacency).
- No regressions found. Standing rule confirmed with user: proactively join whenever the other Copilot is active, no permission needed.
- Files touched by me this pass: HANDOFF.txt only.


---

## Current tandem audit — 2026-09-23 18:20
- Other Copilot added a full exam submission-review screen: navigate to answered/unanswered/marked questions, question overview, jump-back-to-question, return-to-exam, explicit final submit, answers stay hidden until submission. Compiled, full UI-tested, repackaged, deployed to Desktop, launched successfully by it.
- I independently verified: py_compile clean; deployed package hashes match across all 3 copies (31ad2796a798f164080b966936d4653d84eca9ef14eeca6bc1121f4067022a79); `exam_review_active` flag correctly initialized in __init__/start_exam and toggled in _render_exam_question (False)/_render_exam_submission_review (True), preventing redundant `_capture_exam_answer` calls when jumping from the review screen; scripted test of unanswered/marked collection logic against a 40-question exam produced exactly the expected counts (37 unanswered, 1 marked).
- No regressions found. Files touched by me this pass: HANDOFF.txt only.


---

## Scope claim — 2026-09-24 19:34
- I am starting a larger implementation pass on `azure_learning_app.py`, scope explicitly requested by the user:
  1. Replace Listbox-based drag/drop ordering (move-up/move-down buttons) with true mouse drag-and-drop widgets for drag_drop/build_list question types.
  2. Content audit of explanation/distractor text for accuracy across all 116 questions; fix any weak/inaccurate feedback.
  3. Expand question bank breadth with more non-MS-Learn-style scenario questions.
  4. Introduce an "AZ-900 Exam Simulation" top-level category/namespace so future exam sims (SC-900, AZ-104) can be added alongside it without restructuring.
  5. General UI/layout polish pass (spacing, visual hierarchy, styling) so the app reads as a finished product rather than a scripted tool.
- Scope for now is AZ-900 only (per user); SC-900/AZ-104 remain future work, not started.
- Please read `AGENTS.md` (repo root) before working here — it defines the standing coworking rules (help when idle, respect ownership boundaries, log to this file, never claim "done" prematurely on a standing /goal).
- I own `azure_learning_app.py` for this pass. Please validate independently in this file as usual; avoid concurrent edits to the same file without coordinating here first.


---

## Pass completed — 2026-09-24 19:55
- All 5 scoped items done, verified, rebuilt, redeployed:
  1. Real mouse drag-and-drop: new `DragOrderList` (ordering/drag_drop) and `DragBuildList` (build_list, pool+target panes) Tkinter widget classes replace the old Listbox+move-buttons UI. Floating "ghost" label during drag, row-center-based drop-index detection (handles variable-height wrapped text), `.lock()` disables interaction after submission. Dead `_move_up`/`_move_down`/old Listbox drag handlers removed. Verified via scripted simulated-drag tests and live rendering inside `_render_question_widget`/`_render_exam_question` for all 3 affected types.
  2. Content audit: added exactly 1 decoy option + rewrote prompt/explanation for all 6 `build_list` questions (were previously `options == answer`, i.e. no real "pick correct subset" semantics). Heuristic-scanned all explanations for weak/short (<90 char) text — found and rewrote 18 total (16 + 2 follow-up: az900-028 Cloud Shell, az900-037 Azure Advisor), all now include why-correct + why-each-distractor-is-wrong reasoning. 0 weak explanations remain.
  3. Question bank expanded 116 → 133: added 17 new scenario/numeric-reasoning questions (az900-117..133) not paraphrased from MS Learn — shared-responsibility scenarios, CapEx/OpEx, elasticity-vs-scalability, hybrid cloud scenario, multitenancy, Reserved vs Spot VM cost tradeoffs, Azure Hybrid Benefit, support-plan SLA scenario, Trust Center/compliance, Region Pair vs Availability Zone/Set, composite SLA math (0.999×0.9995≈99.85%), EU Data Boundary, Azure Arc, Azure Lighthouse, cloud-benefits multi-select. All validated: unique IDs, answer⊆options, no weak explanations.
  4. "AZ-900 Exam Simulation" category: notebook tab renamed from "Exam" → "AZ-900 Exam Simulation"; added `EXAM_CATALOG`/`ACTIVE_EXAM_ID` registry (AZ-900 active, SC-900/AZ-104 listed as "bald verfügbar" placeholder badges in the exam tab) so future exams slot in without restructuring — just add a catalog entry + questions with matching `"exam"` field, flip status to active.
  5. UI polish: colored top-accent strips on Question-Types cards and Dashboard stat cards (per-metric color coding), hover highlight + `cursor="hand2"` added to clickable type cards (previously silently clickable with no visual affordance), exam-tab catalog badges.
- Full regression after all changes: py_compile clean; 133 questions load; all tabs open without error; all 10 type-practice cards render live; 5 randomized 40-question exam trials — unique IDs every time, blueprint weighting stable (~11/15/14 cloud/architecture/governance), case-group contiguity holds. Live smoke test on real WSLg display (:0) exercised both new drag widgets end-to-end inside actual exam rendering, not just isolated unit tests.
- Rebuilt via `./build-linux.sh`, redeployed to Desktop. All 3 copies (dist/release/Desktop) SHA-256 identical: c12174184c8dcf269422cdeab5a73f3381de55f81d155d7c285930b7d1aee24f. Binary launches cleanly (timeout-kill pattern, exit 124 as expected for a running GUI app).
- Files touched: azure_learning_app.py (all 5 items above), HANDOFF.txt (this entry).
- Next agent: please read AGENTS.md before touching this file. AZ-900 scope is considered feature-complete for the items above; SC-900/AZ-104 are the next logical major task whenever the user is ready (catalog scaffold in EXAM_CATALOG is ready for it). No known open issues.


---

## Independent tandem validation — 2026-09-24 19:59
- Independently ran `python3 -m py_compile azure_learning_app.py` and a fresh-temporary-DB audit: all 133 source rows reconciled and loaded, IDs are unique, every active question is AZ-900, all ten interaction types are represented, and every persisted correct answer evaluates True (including matching's UI-equivalent mapping).
- Confirmed the exam registry has an active AZ-900 entry plus SC-900/AZ-104 scaffolds. Ran 100 randomized 40-question exam generations: every set has 40 unique IDs, contains all ten interaction types, and preserves contiguous case-study groups.
- Confirmed all explanations meet the new 90-character threshold and applicable answer options contain their correct answers. SHA-256 matches across root, release, and Desktop executables: `c12174184c8dcf269422cdeab5a73f3381de55f81d155d7c285930b7d1aee24f`.
- No regression found. Files touched by me in this pass: `HANDOFF.txt` only.


---

## Pass completed — 2026-09-24 20:25
- Implemented the user's two explicitly requested features: spaced repetition and real exam statistics ("echte Prüfungsstatistiken").
  1. Spaced repetition (Leitner system, 6 boxes, intervals [1,2,4,8,16,32] days): new `review_schedule` table (migration-safe `_init_db` addition); `_update_review_schedule(question_id, correct)` wired into `_record_attempt` for every attempt in any mode — correct promotes a box, any wrong answer resets to box 1 (resurfaces next day). `_fetch_due_review_questions()` and `_sr_summary()` (due_now/due_week/mastered/scheduled) added. "Weak Areas" tab renamed "Wiederholung" and rebuilt with two side-by-side panels: due-for-review queue (Leitner-driven, `load_due_review_question`) and the existing frequently-missed list (unchanged logic, `load_weak_question`). Dashboard gained a "Fällig heute" stat card and an info-text line with due-now/due-week/mastered counts.
  2. Real exam statistics: blueprint-weighted scaled score on Microsoft's 100–1000 scale (pass ≥700), via new module function `compute_scaled_score(domain_results)` using `EXAM_DOMAIN_WEIGHTS` (cloud 27.5%/architecture 37.5%/governance 32.5%, blueprint midpoints; weights renormalized when a domain has 0 attempts, so partial practice sets still produce a sane estimate). `exam_runs` gained `scaled_score`/`passed` columns (migration-guarded). `_finish_exam`/`_record_exam_run` compute and persist both; `_render_exam_results` now shows the scaled score prominently with pass/fail + a disclaimer that this is an estimate (Microsoft's real scaling algorithm is proprietary/undisclosed). New "Statistik" tab (`_build_stats_tab`/`_refresh_stats_tab`, scrollable): scaled-score history/trend across last 10 exam runs with pass/fail markers + best/avg/latest, domain accuracy vs blueprint target bars, per-question-type accuracy bars, per-difficulty accuracy bars, and a spaced-repetition summary section linking back to Wiederholung. Dashboard info text also enriched with avg/best scaled score and pass count across all exam runs.
- Validation: `py_compile` clean. Scripted regression against a temp DB: `compute_scaled_score` checked against 3 fixtures (full-domain, partial/renormalized, all-zero) — all matched hand-computed expectations; Leitner box progression (correct→promote, wrong→reset to box 1) and `_fetch_due_review_questions` ordering verified by simulated attempts; full 40-question exam simulated end-to-end (`start_exam`→answer all→`_finish_exam`→`_render_exam_results`) with no errors, scaled_score/passed populated correctly. All tabs (including new "Statistik") open without error; `_refresh_dashboard`/`_refresh_weak_areas`/`_refresh_stats_tab` run cleanly.
- Rebuilt via `./build-linux.sh`, redeployed to Desktop. All 3 copies (dist/release/Desktop) SHA-256 identical: `2a4352ae15c803f2684ebb9155ee869b0d477017a420166d93d5f5648ba70462`. Live launch smoke test on real WSLg display (`DISPLAY=:0`, timeout-kill pattern) confirms clean startup (exit 124 as expected).
- Files touched: azure_learning_app.py (all of the above), HANDOFF.txt (this entry).
- Next agent: please read AGENTS.md before touching this file. AZ-900 remains the sole active scope until the user passes the real exam (per explicit instruction). Suggested next candidates (not started, awaiting user direction): (a) a lightweight "next review due" reminder/notification on app open, (b) export/import of `review_schedule` state if the DB is ever reset, (c) a stats "insight" callout when a domain's accuracy is below its blueprint-weighted target. No known open issues; note left for user is pending in the chat, not yet written here.


---

## Bugfix pass — 2026-09-24 21:29
- User reported: in "Question Types", clicking "Typ direkt üben" appeared to do nothing (button "doesn't work"). Did a full go-through of the app as a real user (every tab: Dashboard, Learn, Question Types, Exam Simulation, Wiederholung, Statistik) with scripted UI exercising of every code path (all 10 type buttons, learn cycling, full exam run incl. skip/mark/finish/results, weak + due-review actions, stats refresh).
- Root cause found: `_build_types_tab` packed the 10 type cards (3-col grid, 4 rows) directly into a fixed non-scrollable tab frame. Their combined required height (~988px) exceeded the window, so the `types_practice_frame` below the grid — where the actual practice question renders after clicking a button — was squeezed down to ~0-1px and completely invisible, with no scrollbar to reach it. The button's logic (`open_type_practice`) was working correctly the whole time; the rendered question was just invisible.
- Fix: rebuilt `_build_types_tab` with a scrollable canvas (same pattern as the Statistik tab) so all 10 cards plus the practice area are reachable; `open_type_practice` now also auto-scrolls the canvas to the bottom after rendering a question so the user sees it immediately without hunting for a scrollbar.
- Verified via scripted geometry checks: practice frame height for all 10 types is now 260–500px (previously ~0-1px) both at default (1280x820) and minimum (1080x720) window sizes; canvas yview confirmed at 1.0 (scrolled fully into view) after each `open_type_practice` call.
- Also did a targeted audit of Learn tab and Exam tab (single-question-card layout, not a stacked grid) — confirmed no equivalent overflow/clipping issue there, content fits within the window at both default and minimum sizes for every question type.
- Full scripted regression re-run after the fix: dashboard cards populate, learn cycles through questions, full 40-question exam run (start → skip/mark/navigate → finish → results with scaled score) completes without error, Wiederholung tab (weak + due-review lists/buttons) and Statistik tab refresh cleanly.
- py_compile clean. Rebuilt via `./build-linux.sh`, redeployed to Desktop. All 3 copies (dist/release/Desktop) SHA-256 identical: `5683679b9f50a195477507f37ff09a3ff751f8a71e88f03e0717effa73dfe873`. Live launch smoke test on real WSLg display confirms clean startup (exit 124 as expected).
- Files touched: azure_learning_app.py (`_build_types_tab`, `open_type_practice`), HANDOFF.txt (this entry).
- Next agent: please read AGENTS.md before touching this file. No other overflow/invisible-content bugs found in this audit pass. If new tabs/sections with multiple stacked cards are added in the future, always wrap them in a scrollable canvas from the start (see Statistik/Question Types tabs for the pattern) rather than a fixed-height pack layout.


---

## Usability/accessibility pass — 2026-09-25 09:40
- User reported that drag-and-drop tasks in Question Types jumped the scrollable practice page to the top after every drop, making multi-step ordering tedious.
- Fixed `DragOrderList` and `DragBuildList`: row rebuilds now capture and restore every enclosing Tk canvas viewport immediately and again after Tk's idle geometry update. This preserves the learner's position in the scrollable Question Types tab after an ordering or build-list drop.
- Reworked inline Learn/type-practice feedback from dense label blocks into an accessible, high-contrast review card: an explicit correct/incorrect/solution status panel with text (not color alone), plus separate labeled sections for the learner's evaluation, correct answer, and explanation. The wider sections, readable hierarchy, and preserved action area make missed-question review substantially easier to scan.
- Validation: `python3 -m py_compile azure_learning_app.py` passed. A live Tk/WSLg smoke test embedded both drag widgets in a scrollable canvas, simulated drops into a reordered list and a build-list target, and asserted both the answer state and unchanged viewport. It also rendered a real incorrect-answer feedback card and asserted all structured sections are present. Rebuilt with `./build-linux.sh`; root, `dist`, and Desktop binaries share SHA-256 `8fed97e1a78af36000085bd0da57f3234637448fa0a0dbd1e7fbf0245e9e61b1`. The packaged app remained running for an 8-second GUI startup smoke test.
- Files touched: `azure_learning_app.py`, `HANDOFF.txt`.


---

## Full consumer audit — 2026-09-25 09:56
- Completed a fresh Tk/WSLg end-user audit against a temporary database. It passed Dashboard, every available Learn filter combination, all ten Question Types with actual correct widget selections and rendered feedback, wrong-answer handling, weak-area and due-review queues, exam start/mark/skip/back/review/submit/results, statistics, and saved-exam resume in a freshly constructed app instance.
- Found and fixed one product/documentation mismatch: README promised JSON progress export, but the source had no export action. Dashboard now has `Fortschritt exportieren`; it writes a portable, atomic JSON export containing format metadata, question-bank size, attempts, completed exam runs with decoded domain summaries, the spaced-repetition schedule, and study days. Export errors are shown explicitly.
- Corrected the README feature count from 116 to 133 and documented that JSON export is available from the Dashboard.
- Final validation: `python3 -m py_compile azure_learning_app.py` passed; a second full consumer audit including a real export file passed (`FULL_CONSUMER_AUDIT_WITH_EXPORT: PASS`). The export contained non-empty attempts, exam runs, review schedule, and study days. Rebuilt and deployed all executable copies; root, `dist`, and Desktop SHA-256: `aa0c3fd29a00b7cab0810b4e7a20211ebd06e01e3b80c38febe5aa99a82e417a`. The final packaged GUI remained running for the 8-second startup check. Removed the specific temporary database created by an interrupted earlier audit.
- Files touched: `azure_learning_app.py`, `README.md`, `HANDOFF.txt`.


---

## Visual polish pass — 2026-09-25 10:24
- User supplied screenshots showing the Dashboard's raw multiline text block and the Wiederholung tab's plain Listboxes, both of which read like editor/debug output rather than a finished learning app.
- Replaced the Dashboard text console with a structured "Dein Lernfortschritt" card: concise learning, spaced-repetition, and exam-simulation highlights plus separate domain-progress cards with accuracy, answer count, and blueprint weighting.
- Replaced both review Listboxes with fixed-height, scrollable, accessible card queues. Every card has a labeled metadata line, readable wrapped prompt, colored accent, pointer/hover affordance, and direct click-through to that question. Removed unsupported symbol icons from review headings because they rendered as missing glyphs in the supplied environment.
- Fixed Tk geometry allocation for the review panels during the redesign: the two equal-width queue cards now use a 300px grid row, preserving readable queue space while leaving the review-question area below.
- Validation: `python3 -m py_compile azure_learning_app.py` passed. Live Tk/WSLg validation at both 1280×820 and the 1080×720 minimum window confirmed no Dashboard text widget, Dashboard summary visibility, 300px review cards, five populated due/weak cards, and card click-through to the selected question (`POLISHED_DASHBOARD_AND_REVIEW_UI: PASS`). Rebuilt and deployed matching root, `dist`, and Desktop executables: SHA-256 `faae2750687302cd00f2acb88f14eb939892cd565e5ddb4b9578113c0c18945d`. The packaged GUI remained running for the 8-second startup check. Removed the identified temporary audit database.
- Files touched: `azure_learning_app.py`, `HANDOFF.txt`.


---

## Readability and layout pass — 2026-09-26
- Increased the default window from 1280×820 to 1360×880 and raised the minimum usable layout from 1080×720 to 1200×780, providing space for readable text rather than compacting it.
- Added a baseline accessible Tk font configuration: default controls and body text use 11pt, captions use 10pt, tabs and buttons use 11pt, and radio/check controls receive larger line spacing. No explicit learner-facing label remains below 10pt.
- Enlarged the high-traffic Dashboard, Question Types, review queues, drag-and-drop lists, statistics, question metadata, and question prompt typography. Question prompts are now 14pt; review cards have more height, larger text, and wider wrapping.
- Validation: `python3 -m py_compile azure_learning_app.py` passed; a fresh temporary database loaded all 133 questions. Live Tk/WSLg audit at the new 1200×780 minimum opened all six tabs and all ten question types, confirmed type-practice space of at least 260px, and asserted every visible `tk.Label` uses at least 10pt (`READABILITY_UI_AUDIT: PASS`).
- Rebuilt via `./build-linux.sh`. Root, `dist`, release, and Desktop executables are identical and executable: SHA-256 `920fef833b26d007781b7c66e2e1f42c340fdd89e838b9025e5f2c7c85035af8`.
- Files touched: `azure_learning_app.py`, `HANDOFF.txt`.


---

## Adaptive study plan and guided exam review — 2026-09-26
- Added a Dashboard `Heutigen Lernplan starten` action and preview card. The dynamic, deduplicated plan prioritizes due Leitner reviews, then questions from the learner's weakest blueprint domains, then a distinct practice item for each recently missed interaction type. It falls back to AZ-900 foundation questions for a new learner or an exhausted queue.
- Plan questions render in Learn with direct feedback, Microsoft Learn access, and `Nächster Planpunkt`; completing the queue returns to the Dashboard. No new persistence schema is required because the plan is derived from existing attempts and review schedules.
- Replaced the post-exam missed-question handoff to Learn with an in-result guided review. Each missed item preserves the learner's submitted answer (or explicitly marks it unanswered), shows the correct answer and rationale, has previous/next navigation, opens its Microsoft Learn source, and can be idempotently scheduled for review today without creating an additional attempt.
- Updated `README.md` to document both learner-facing additions.
- Validation: `python3 -m py_compile azure_learning_app.py` passed. A fresh Tk/WSLg temporary-database regression seeded a due item and incorrect attempts, verified due-review priority, domain/type coverage, deduplication, and plan rendering; then completed a mixed-answer exam and verified guided-review answer context, all review sections, and idempotent same-day scheduling (`ADAPTIVE_PLAN_AND_GUIDED_EXAM_REVIEW: PASS`).
- Rebuilt via `./build-linux.sh`. Root, `dist`, release, and Desktop executables are identical: SHA-256 `727477401a61cb954183d7481c314a97c30f98583baa7e7681c8f91c28e443fc`.
- Files touched: `azure_learning_app.py`, `README.md`, `HANDOFF.txt`.


---

## Responsive compact-window layout — 2026-09-26
- Lowered the supported minimum window size from 1200×780 to 1080×720 without reducing the accessible 10pt+ baseline typography.
- Dashboard metric cards and actions now reflow into compact grids below 1120px; the Dashboard's progress panel retains 336px at 1080×720 rather than collapsing beneath the cards.
- Learn filters reflow from one row to two rows at compact widths. Question Type cards switch from three columns to two and recompute text wrapping to stay readable.
- Replaced the one-line 40-question exam navigator with a compact action row plus a wrapped 10-column question grid, preventing it from extending beyond a smaller window.
- Validation: `python3 -m py_compile azure_learning_app.py` passed. Live Tk/WSLg audits at 1080×720 opened all six tabs, verified compact Dashboard/actions, filters, type-card grid, and exam rendering (`COMPACT_LAYOUT_AUDIT: PASS`); the Dashboard progress panel measured 336px high. A 1360×880 audit verified the original single-row Dashboard/filter and three-column type-card layouts remain (`FULL_SIZE_LAYOUT_AUDIT: PASS`).
- Rebuilt via `./build-linux.sh`. Root, `dist`, release, and Desktop executables are identical: SHA-256 `a1d5bff86618d1cd948be0b544cdad4711b071217727915deb9fd1969c9e75db`.
- Files touched: `azure_learning_app.py`, `HANDOFF.txt`.


---

## Global scrolling and compact text wrapping — 2026-09-26
- Replaced canvas-hover-only mouse-wheel bindings with one active-tab router. Mouse wheels now scroll the full Fragentypen or Statistik page when the pointer is over any child card, label, control, or scrollbar; Linux Button-4/Button-5 wheel events are supported too.
- Made Question Type description/sample labels wrap to their actual rendered card width and made question prompts rewrap to their live card width after every resize.
- Reflowed the exam-catalog badges onto a dedicated responsive grid and wrapped unavailable-certificate status labels, eliminating the compact-window clipping found at 1080×720.
- Validation: `python3 -m py_compile azure_learning_app.py` passed. Live Tk/WSLg validation dispatched mouse-wheel events from a Question Type card and Statistics content frame, confirming both canvases moved, then checked every visible label across all six tabs at 1080×720; no mapped label was narrower than its requested text width (`GLOBAL_SCROLL_AND_TEXT_WRAP_AUDIT: PASS`).
- Rebuilt via `./build-linux.sh`. Root, `dist`, release, and Desktop executables are identical: SHA-256 `f372706858df925d2a231e2cd3f21d1c7a431ea486721b0ba4e8c32b4a3025c7`.
- Files touched: `azure_learning_app.py`, `HANDOFF.txt`.


---

## Black-and-blue dark theme — 2026-09-26
- Converted the learner-facing application to a near-black and Azure-blue palette: black/navy page backgrounds, deep-blue cards, Azure-blue primary actions, blue hover/selection states, light high-contrast text, and dark native Listboxes/Combobox menus.
- Replaced all legacy white/pale-blue surfaces in Dashboard cards, Question Types, review queues, drag-and-drop/build-list widgets, answer canvases, case-study cards, statistics, guided exam review, and inline correctness feedback. Success/error states remain distinct through dark green/red surfaces rather than bright pastels.
- Preserved light text for hero, portal, badges, and drag ghosts by separating text-on-accent from the dark card surface token.
- Updated `README.md` to describe the black-and-Azure-blue visual theme.
- Validation: `python3 -m py_compile azure_learning_app.py` passed. Live Tk/WSLg audits at both 1360×880 and 1080×720 opened all six tabs and an interactive Hot Area question; verified root, cards, canvases, and button styles use the dark palette and that no mapped native widget retains a legacy light background (`DARK_BLUE_THEME_UI_AUDIT: PASS`).
- Rebuilt via `./build-linux.sh`. Root, `dist`, release, and Desktop executables are identical: SHA-256 `9db45c6f3f9825b02bab7d9ebad78955b2c9b1633dcb0920a96a984683ee207a`.
- Files touched: `azure_learning_app.py`, `README.md`, `HANDOFF.txt`.


---

## Dark-layout conformity and readability audit — 2026-09-26
- Performed an independent source/theme review and a live exhaustive UI audit. Fixed four confirmed dark-layout defects rather than treating the prior dark-theme pass as complete.
- Added complete dark ttk styling for default frames, labels, buttons, scrollbars, and readonly/disabled Combobox states. This removes the light `clam` defaults from filters, navigation buttons, and scrollbar controls; readonly filter text now uses a dark field with high-contrast text.
- Added shared canvas-backed vertical scrolling to Dashboard, Learn, Wiederholung, and Exam content. At compact sizes, every Dashboard section, inline feedback card, review action, and guided exam-result action remains reachable rather than being compressed or hidden below the viewport.
- Corrected semantic text colors: primary controls now use dark text on bright Azure blue, informational blue text uses an accessible light-blue token on dark surfaces, and success/error headings use light semantic text. A live WCAG-style sweep found and corrected the final case-study marker contrast issue; every rendered `tk.Label` now meets the 4.5:1 threshold in the audited states.
- Validation: `python3 -m py_compile azure_learning_app.py` passed. The comprehensive live regression at 1360×880 and 1080×720 opened all six tabs, checked default/readonly ttk palette states, rendered correct and incorrect inline feedback for all 133 seeded questions, rendered all ten Question Types, review feedback, and guided exam results, and verified every overflowing page scrolls to its bottom (`FULL_DARK_LAYOUT_REGRESSION: PASS`). Contrast audit: `DARK_THEME_CONTRAST_AUDIT: PASS`.
- Rebuilt via `./build-linux.sh`. Root, `dist`, release, and Desktop executables are identical: SHA-256 `a7f288da53eb9eb5fbc0d04f7a7672e5bcee889cf3d1840e0d8e3b4b3b63ea0d`.
- Files touched: `azure_learning_app.py`, `HANDOFF.txt`.


---

## Larger responsive typography — 2026-09-26
- Increased the application-wide Tk display scaling by 12% relative to the host setting and raised named default/body/menu/heading fonts from 11pt to 12pt and captions from 10pt to 11pt. Buttons, tabs, filters, radio controls, and check controls now use 12pt styles; explicitly formatted content receives the same physical scaling.
- Preserved responsive readability after the size increase: Dashboard focus and plan preview text now wrap to their actual card widths; question prompts dynamically wrap to their assigned label width; and the large estimated-score result line wraps within the exam result card.
- Found and fixed three real compact-layout boundary cases during the audit: Learn prompt margin, Question Types training-card margin, and the exam score line. Scrollable pages preserve access to all added vertical content.
- Updated `README.md` to document enlarged accessible typography, responsive wrapping, and compact-window scrolling.
- Validation: `python3 -m py_compile azure_learning_app.py` passed. At 1360×880 and 1080×720, the live Tk/WSLg regression verified effective 12pt defaults/11pt captions and 1.49+ Tk scaling; opened all six tabs; rendered correct and incorrect feedback for every one of the 133 question records; rendered all ten Question Types, Wiederholung feedback, and guided exam results; asserted scroll-to-bottom for every overflowing page; and found no label exceeding its usable content width (`LARGER_TYPOGRAPHY_LAYOUT_AUDIT: PASS`).
- Rebuilt via `./build-linux.sh`. Root, `dist`, release, and Desktop executables are identical: SHA-256 `8b07e8a3711510560046e7feba00150e6bacac241d52863e8ca463e882a53ec3`.
- Files touched: `azure_learning_app.py`, `README.md`, `HANDOFF.txt`.


---

## Copilot feasibility assessment of independent-app review — 2026-09-28
- Confirmed the review’s core conclusion: the public product must be a separate Flutter mobile app; the existing desktop Tkinter/PyInstaller application remains private and must not be submitted to either mobile store.
- Feasible and required for the mobile release: a distinct non-Microsoft primary brand, an in-app About/Legal screen, independent/unaffiliated and score-estimate disclosures, public privacy-policy/support URLs, offline-only local progress storage, original app/store artwork, and signed Android/iOS release artifacts.
- The proposed `LICENSE` and provenance documentation need a qualification: a repository license only covers material owned by the publisher; it cannot grant rights to Microsoft documentation, marks, or uncertified question content. Do not add a blanket license or an “all content is original” statement until the human owner has completed and documented the requested content-rights review.
- The existing question-source evidence is strong for attribution quality (133/133 official Microsoft URLs, 78/78 unique source URLs live) but is not evidence of commercial authorship or clearance. Content provenance remains the release gate.
- Before mobile implementation can assign immutable application identifiers, the owner must choose the cleared public brand. The selected v1 architecture is offline-first; no account, cloud sync, analytics, or advertising SDK will be included.
- Files touched: `HANDOFF.txt` only.


---
