# Qa Audits And Usability — Azure Learning handoff archive

This file preserves dated project handoff entries from `HANDOFF.txt`.
Do not delete or rewrite history; add new dated sections at the bottom.

## AGY end-user QA audit & usability review — 2026-09-26
- Tested end-user workflow across all 6 tabs (Dashboard, Learn, Question Types, Exam Simulation, Wiederholung, Statistik) on real WSLg display (DISPLAY=:0) at both default 1280×820 and minimum 1080×720 geometry.
- Verified all 10 Question Types via `open_type_practice`: single choice, multi-select, true/false, ordering, drag-and-drop, build list, matching, hot area, active screen, and case studies. All rendered cleanly with height > 240px and correct auto-scrolling to the active question.
- Verified Exam Simulation: 40 questions generated with proper blueprint balance, live timer, Skip/Mark/Back/Next navigation, summary review screen, and submission with scaled scoring (100–1000 scale).
- Verified Leitner spaced repetition review schedule, weak area card queue, stats trend charts, and atomic JSON progress export from Dashboard.
- Audit findings & suggestions logged for Copilot:
  1. UI Language Mixing: App questions, options, and explanations are German, but prominent UI labels remain in English:
     - Tabs: "Learn" (suggest: "Lernen"), "Question Types" (suggest: "Fragentypen"), "AZ-900 Exam Simulation" (suggest: "AZ-900 Prüfungssimulation").
     - Dashboard stat cards: "Practice attempts", "Accuracy", "Current streak", "Weak items" mixed with German "Fällig heute".
     - Controls/Buttons: "Save & next" (suggest: "Speichern & weiter"), "Submit answer" (suggest: "Antwort prüfen"), "Back" (suggest: "Zurück"), "Skip" (suggest: "Überspringen"), "Mark" / "Unmark" (suggest: "Markieren" / "Markierung aufheben"), "Start exam" (suggest: "Prüfung starten"), "Next question" (suggest: "Nächste Frage"), "Open Microsoft Learn source" (suggest: "Microsoft Learn öffnen").
     - Popup: `messagebox.showinfo("Answer required", "Please answer the question before submitting.")` (suggest: German equivalent).
  2. Learn Mode Post-Answer Action: `type_practice` has a "Microsoft Learn öffnen" button in its feedback action row, but `learn` mode currently lacks this button in the feedback row (it's only in the top controls as English "Open Microsoft Learn source"). Suggest adding "Microsoft Learn öffnen" to `learn` feedback actions.
  3. Source URL: `az900-125` points to `https://azure.microsoft.com/en-us/support/plans/` (marketing/commercial site) rather than canonical Learn documentation (`https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/support-plans-overview`).
- Code boundary respect: As agreed, no application code was edited by AGY. Findings are staged here for Copilot's review and implementation.
- Files touched: `HANDOFF.txt` only.


---

## AGY QA findings implemented — 2026-09-26
- Applied the verified localization findings throughout the learner-facing UI: tabs, Dashboard metric cards and actions, Question Types heading, review/statistics labels, exam controls and results, source/reveal actions, and answer-required/explanation dialogs now use German. Official product names such as Azure Learning and Microsoft Learn remain unchanged.
- Added `Microsoft Learn öffnen` to the Learn-mode inline feedback actions, matching type practice. The action is rendered inside the feedback card after an answer is checked.
- Investigated AGY's recommended Learn URL for `az900-125`. The proposed `manage/support-plans-overview` page and the suggested Professional Direct Learn variants return HTTP 404, so that recommendation is invalid. Retained the live, official `https://azure.microsoft.com/en-us/support/plans/` page, which directly covers plan SLAs.
- Corrected a related factual issue found during validation: Professional Direct's critical-incident response time is under one hour, not under 15 minutes. Updated the question and explanation accordingly.
- Validation: the support-plans source returned HTTP 200; `python3 -m py_compile azure_learning_app.py` passed; a fresh temporary database loaded all 133 questions; live Tk/WSLg UI audit verified all localized tab labels, removal of the reported English labels, and the Learn feedback card's `Microsoft Learn öffnen` action (`GERMAN_UI_AND_LEARN_FEEDBACK_AUDIT: PASS`).
- Rebuilt via `./build-linux.sh`. Root, `dist`, release, and Desktop executables are identical and executable: SHA-256 `2be20b4ad4b0fbfe7324909387ed23518a7fcdcade7fe3642da0cfe399e98380`.
- Files touched: `azure_learning_app.py`, `HANDOFF.txt`.


---

## AGY learner-flow findings implemented — 2026-09-26
- Fixed the functional exam-review handoff defect: `Unbeantwortete lernen` and `Markierte lernen` now create a deduplicated, sequential review queue. Each submitted item presents `Nächste Prüfungsfrage`; completing the subset returns to the existing exam-results view instead of choosing a random catalog question.
- Made the adaptive daily plan transparent in its question header: it now displays `Planpunkt X von Y` and the stored selection reason.
- Replaced the guided-review scheduling modal with inline confirmation. `Für heute einplanen` updates to `Für heute eingeplant ✓`, becomes disabled, and provides a non-blocking status message; already-due questions are handled idempotently.
- Added `Microsoft Learn öffnen` to Weak Areas feedback. Completed the reported German copy cleanup: Learn mode is now `LERNEN`, the due-review empty state uses `Lernen`/`Prüfungssimulation`, and exam-result domain tiles use German UI labels.
- Updated `README.md` for visible daily-plan context and sequential practice of selected unanswered/marked questions.
- Validation: `python3 -m py_compile azure_learning_app.py` passed. A live WSLg temporary-DB test at 1080×720 verified ordered deduplicated exam review, return-to-results behavior, plan step/reason rendering, no modal invocation during schedule creation or repeat scheduling, updated review date, Weak Areas Microsoft Learn action, and all German result-tile labels (`EXAM_REVIEW_QUEUE_AND_FLOW_POLISH: PASS`). The longest plan reason passed at both 1360×880 and 1080×720 (`PLAN_HEADER_LAYOUT: PASS`).
- Rebuilt via `./build-linux.sh`. Root, `dist`, release, and Desktop executables are identical: SHA-256 `68dd1cc45759271074df1140946ff5fbd1b84488216efef8c3365f8cd77941ca`.
- Files touched: `azure_learning_app.py`, `README.md`, `HANDOFF.txt`.



---

## AGY end-user QA audit & usability review — 2026-09-26
- Reviewed newly added features ("Adaptive study plan" & "Guided exam review", readability & minimum layout geometry) from the learner's end-consumer perspective.
- Findings and actionable suggestions for GitHub Copilot:
  1. Exam Result Handoff ("Unbeantwortete lernen" / "Markierte lernen"):
     - Observed behavior: In `_render_exam_results()`, clicking "Unbeantwortete lernen" or "Markierte lernen" opens `questions[0]` in Learn mode (`_open_exam_review_question_from_list`). After submitting an answer, the feedback action is "Nächste Frage", which calls `load_next_learn_question()` and picks a random question from the entire catalog, discarding the remaining items in the list.
     - End-user impact: A learner expecting to step through their 4 unanswered or marked questions gets dropped into arbitrary catalog questions after the first one.
     - Suggested fix for Copilot: Track the review list as a queue (similar to `today_plan_entries`) with a dedicated "Nächste Prüfungsfrage" action until the subset is completed, then return to the Exam summary or Dashboard.
  2. Adaptive Study Plan Transparency & Step Counter:
     - Observed behavior: `_build_today_plan()` computes meaningful contextual reasons for each entry ("Heute fällige Wiederholung", "Schwacher Bereich: ...", "Zuletzt verfehlter Typ: ..."), but this reason is not rendered in the UI during plan practice. The header displays only static "HEUTIGER LERNPLAN · gezielt üben" without showing the entry's reason or progress.
     - End-user impact: Learners lack visibility into why a question was selected for their daily plan and how many questions remain.
     - Suggested fix for Copilot: Display `Planpunkt {index + 1} von {len(plan)} · {reason}` in the question header when `mode == "today"`.
  3. Modal Dialog Interruption in Guided Exam Review:
     - Observed behavior: In `_render_exam_guided_review()`, clicking "Für heute einplanen" triggers `messagebox.showinfo("Wiederholung", "Die Frage wurde für die heutige Wiederholung eingeplant.")`.
     - End-user impact: When triaging several missed questions, the user is repeatedly interrupted by blocking modal popups that require an extra dismissal click.
     - Suggested fix for Copilot: Switch to inline visual confirmation (e.g. updating button text to "Für heute eingeplant ✓" and disabling it) instead of a blocking popup.
  4. Missing "Microsoft Learn öffnen" in Weak Area Mode:
     - Observed behavior: In post-answer feedback actions, "Microsoft Learn öffnen" is rendered for `type_practice`, `learn`, and `today` modes, but `weak` mode (lines 4152–4153) only offers "Nächste Schwachstelle".
     - End-user impact: Learners reviewing their weakest topics cannot jump directly to the official documentation source.
     - Suggested fix for Copilot: Add `Microsoft Learn öffnen` button to the `weak` mode feedback row for feature parity.
  5. Minor German Localization Consistency:
     - Observed behavior: Three minor English string remnants remain in the UI:
       - Line 3727: `"LEARN · Erklärung nach Abgabe"` (suggest: `"LERNEN · Erklärung nach Abgabe"`).
       - Line 4189: `"Nichts ist heute fällig. Beantworte Fragen in Learn oder der Exam Simulation..."` (suggest: `"...in Lernen oder der Prüfungssimulation..."`).
       - Lines 4687–4689: Exam result category tiles hardcode `"Cloud concepts"`, `"Azure architecture and services"`, and `"Azure management and governance"` rather than using `DOMAIN_LABELS`.
- Code boundary respect: As agreed, AGY performed no application code changes; findings and suggestions are documented here for Copilot's review and implementation.
- Files touched: `HANDOFF.txt` only.


---
