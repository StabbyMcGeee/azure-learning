"""Focused regression coverage for AZ-900 desktop exam behaviour.

These tests drive the real AzureLearningApp with a temporary database and a
hidden Tk root. They verify the two correctness fixes from azdeskfix-f3:

1. Unanswered exam questions count as wrong for scoring but are never persisted
   as attempts and never added to the spaced-repetition schedule.
2. Question selection uses the same authoritative blueprint weights as score
   calculation (EXAM_DOMAIN_WEIGHTS), matching the current official AZ-900
   July 2026 skills outline.
"""

import os
import random
import tempfile
import tkinter as tk

import pytest

import azure_learning_app

os.environ.setdefault("DISPLAY", ":0")


@pytest.fixture
def app():
    tmp_path = tempfile.mktemp(suffix=".db")
    azure_learning_app.DB_PATH = tmp_path
    root = tk.Tk()
    root.withdraw()
    app = azure_learning_app.AzureLearningApp(root)
    yield app
    app.db.close()
    root.destroy()
    try:
        os.remove(tmp_path)
    except FileNotFoundError:
        pass


def _single_choice_questions(app, n):
    """Return the first n single-choice questions from the loaded bank."""
    return [q for q in app.questions if q["type"] == "single"][:n]


def _run_finish_exam(app, questions, answers):
    """Finish an exam without requiring live widget state."""
    app.exam_questions = questions
    app.exam_answers = answers
    app.exam_touched = set(answers.keys())
    app.exam_initial_answers = {}
    app.exam_marked = set()
    app.exam_review_active = True
    app.exam_timer_id = None
    app._finish_exam()


def _category_counts(questions):
    counts = {"cloud": 0, "architecture": 0, "governance": 0}
    for question in questions:
        counts[question["category"]] += 1
    return counts


def test_exam_selection_uses_authoritative_blueprint_weights(app):
    """A 40-question exam set follows the same weights used for scoring."""
    weights = azure_learning_app.EXAM_DOMAIN_WEIGHTS
    expected = {
        category: round(40 * weight) for category, weight in weights.items()
    }
    # The rounding shortcut undercounts by one for the current midpoints;
    # the implementation adds the missing slot to architecture.
    expected["architecture"] += 40 - sum(expected.values())

    for seed in range(20):
        random.seed(seed)
        exam_set = app._build_exam_set(40)
        counts = _category_counts(exam_set)
        assert len(exam_set) == 40
        assert len({q["id"] for q in exam_set}) == 40
        assert counts == expected, f"seed {seed}: {counts} != {expected}"


def test_blank_exam_records_no_attempts_or_reviews(app):
    """A completely unanswered exam must not write attempts or SR rows."""
    questions = _single_choice_questions(app, 5)
    _run_finish_exam(app, questions, {})

    result = app.last_exam_result
    assert result["correct"] == 0
    assert result["total"] == 5
    assert len(result["unanswered"]) == 5

    attempts = app.db.execute("SELECT COUNT(*) AS c FROM attempts").fetchone()["c"]
    reviews = app.db.execute(
        "SELECT COUNT(*) AS c FROM review_schedule"
    ).fetchone()["c"]
    assert attempts == 0
    assert reviews == 0


def test_partial_exam_records_attempts_only_for_answered_items(app):
    """Only touched, answered questions become attempts/schedule rows; blanks do not."""
    questions = _single_choice_questions(app, 3)
    answers = {
        questions[0]["id"]: questions[0]["answer"],  # correct
        questions[1]["id"]: "wrong answer",           # wrong
        # questions[2] left blank
    }
    _run_finish_exam(app, questions, answers)

    result = app.last_exam_result
    assert result["correct"] == 1
    assert result["total"] == 3
    assert len(result["unanswered"]) == 1

    attempts = app.db.execute(
        "SELECT COUNT(*) AS c FROM attempts WHERE mode = 'exam'"
    ).fetchone()["c"]
    reviews = app.db.execute(
        "SELECT COUNT(*) AS c FROM review_schedule"
    ).fetchone()["c"]
    assert attempts == 2
    assert reviews == 2


def test_untouched_ordering_drag_drop_exam_records_no_attempts(app):
    """Untouched ordering/drag-drop defaults must not count as answered attempts."""
    ordering = [q for q in app.questions if q["type"] == "ordering"][:2]
    drag_drop = [q for q in app.questions if q["type"] == "drag_drop"][:2]
    questions = ordering + drag_drop

    app.exam_questions = questions
    # Provide deliberately wrong non-empty defaults as if the widget had never
    # been interacted with.
    app.exam_answers = {
        q["id"]: ([q["options"][-1]] + q["options"][:-1]) for q in questions
    }
    app.exam_touched = set()
    app.exam_initial_answers = {}
    app.exam_marked = set()
    app.exam_review_active = True
    app.exam_timer_id = None
    app._finish_exam()

    result = app.last_exam_result
    assert result["total"] == len(questions)
    assert len(result["unanswered"]) == len(questions)

    attempts = app.db.execute("SELECT COUNT(*) AS c FROM attempts").fetchone()["c"]
    reviews = app.db.execute("SELECT COUNT(*) AS c FROM review_schedule").fetchone()["c"]
    assert attempts == 0
    assert reviews == 0

    # If the same answers are explicitly marked as touched, they should persist.
    _run_finish_exam(app, questions, app.exam_answers)
    attempts = app.db.execute("SELECT COUNT(*) AS c FROM attempts").fetchone()["c"]
    assert attempts == len(questions)


def test_untouched_ordering_drag_drop_exam_records_no_attempts(app):
    """Untouched ordering/drag-drop defaults must not count as answered attempts."""
    ordering = [q for q in app.questions if q["type"] == "ordering"][:2]
    drag_drop = [q for q in app.questions if q["type"] == "drag_drop"][:2]
    questions = ordering + drag_drop

    app.exam_questions = questions
    # Provide deliberately wrong non-empty defaults as if the widget had never
    # been interacted with.
    app.exam_answers = {
        q["id"]: ([q["options"][-1]] + q["options"][:-1]) for q in questions
    }
    app.exam_touched = set()
    app.exam_initial_answers = {}
    app.exam_marked = set()
    app.exam_review_active = True
    app.exam_timer_id = None
    app._finish_exam()

    result = app.last_exam_result
    assert result["total"] == len(questions)
    assert len(result["unanswered"]) == len(questions)

    attempts = app.db.execute("SELECT COUNT(*) AS c FROM attempts").fetchone()["c"]
    reviews = app.db.execute("SELECT COUNT(*) AS c FROM review_schedule").fetchone()["c"]
    assert attempts == 0
    assert reviews == 0

    # If the same answers are explicitly marked as touched, they should persist.
    _run_finish_exam(app, questions, app.exam_answers)
    attempts = app.db.execute("SELECT COUNT(*) AS c FROM attempts").fetchone()["c"]
    assert attempts == len(questions)
