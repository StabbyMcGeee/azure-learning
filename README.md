# Azure Learning

Local, offline-first Tkinter study app for Microsoft Azure Fundamentals (AZ-900).
The project is deliberately separate from the earlier web prototype.

## Features

- 133 seeded AZ-900 practice questions covering the three current blueprint areas
- Single-choice, multi-select, true/false, ordering, drag-and-drop, build-list, matching, hot-area, active-screen, and case-study patterns
- Learn filters for both official blueprint area and question interaction type
- Separate Question Types area with a dedicated practice entry point for every supported interaction
- Adaptive Dashboard study plan that prioritizes due Leitner reviews, weak blueprint domains, and recently missed interaction types, with visible selection reason and progress
- JSON progress export from the Dashboard in addition to automatic SQLite persistence
- Black-and-Azure-blue visual theme with high-contrast dark cards and an in-app Azure-style hero graphic
- Enlarged accessible typography with responsive text wrapping and full-page scrolling at compact window sizes
- Learn mode with topic filtering, explanations, and source links
- 40-question, 45-minute exam assessment with every supported interaction type, scenario-weighted difficulty, grouped multi-part case scenarios, Back, Skip/Mark, navigation, a pre-submission review of answered/marked questions, sequential practice of selected unanswered/marked questions, and an inline results view with score, domain/type breakdowns, guided missed-question analysis, and direct next-step actions
- Separate Learn and Exam behavior: Learn provides explanations and Microsoft Learn links; Exam withholds solutions and source links until completion
- Weak Areas view that prioritizes questions previously answered incorrectly
- SQLite persistence for attempts, scores, study days, and streaks
- Dashboard with accuracy, attempt count, streak, weak-question totals, and the five most recent exam simulations
- July 2026 AZ-900-aligned terminology and focus across Cloud concepts, Azure architecture and services, and Azure management and governance

## Run

### Double-click version

Build the same kind of standalone desktop app as the English application:

```bash
./build-linux.sh
```

Then double-click the **Azure Learning** desktop launcher or the standalone
`Azure-Learning` executable. A desktop file is only a launcher/shortcut; if
your file manager opens `.desktop` files as text, double-click the actual
executable at `/home/dimitri/Desktop/Azure-Learning` instead. The packaged
application opens without a terminal window.

### Windows Explorer / WSL

If you are viewing this folder from Windows Explorer through
`\\wsl.localhost\Ubuntu\...`, do not launch the Linux `Azure-Learning` ELF
file or the `.desktop` file. Double-click `Start-Azure-Learning.vbs`; it
starts the Tkinter app through WSLg without opening a terminal window.
`Start-Azure-Learning.cmd` is the visible diagnostic version if startup
troubleshooting is needed.

### Python version

```bash
python3 azure_learning_app.py
```

The local database is created as `azure_learning.db` beside the application on
first run. The app uses only Python's standard library.

Question seed data is reconciled against the source bank at startup, including
question content and matching pairs. Existing attempts are retained while
stale question rows are refreshed. Weak Areas prioritizes unresolved misses and
repeats them before questions most recently answered correctly.

## Validation

```bash
python3 -m py_compile azure_learning_app.py
```

The seed smoke test can also run without a display server:

```bash
python3 - <<'PY'
import os
import tempfile
import azure_learning_app as mod
from azure_learning_app import QUESTION_BANK, AzureLearningApp

fd, path = tempfile.mkstemp(suffix=".db")
os.close(fd)
old_path = mod.DB_PATH
mod.DB_PATH = path
app = AzureLearningApp.__new__(AzureLearningApp)
app.db = app._init_db()
rows = app._load_questions()
assert len(rows) == len(QUESTION_BANK)
assert all(q["pairs"] or q["type"] != "matching" for q in rows)
app.db.close()
os.unlink(path)
mod.DB_PATH = old_path
print("seed smoke test: PASS")
PY
```
