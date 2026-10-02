#!/usr/bin/env python3
"""Build and validate the production content pack for the Azure Learning app.

Reads the per-course question lists under ``tool/content/``, validates them
against the azpack-v2 schema plus the azlegal-db-v1 rights-basis enum and
terminology rules, then writes the merged pack to
``mobile/assets/content-pack.json``.

The generated JSON is the shipped artifact. The Python modules under
``tool/content/`` are the reviewable authoring source.

Validation mirrors ``ContentPackValidator`` from the mobile app and the
terminology rules from azlegal-db-v1 section 2:
  - formatVersion, packId, packVersion, title, source, rightsBasis required
  - every question has id/text/>=2 options/in-range correctOptionIndex/
    domain/difficulty/source/rightsBasis/courseId
  - rightsBasis is one of the azlegal-db-v1 permitted values
  - retired/non-exam wording does not appear (course-scoped)
  - ambiguous abbreviations (bare "RBAC") are course-qualified
"""

import hashlib
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(HERE, "content")
ASSET_PATH = os.path.join(HERE, "..", "assets", "content-pack.json")

FORMAT_VERSION = "azpack-v2"

PERMITTED_RIGHTS_BASES = [
    "original-human",
    "original-human-ai-assisted",
    "licensed-cc-by-4.0",
    "licensed-commercial",
    "public-domain",
]

# Course identifiers this launch ships.
ALL_COURSES = ["az-900", "dp-900", "ai-901"]

# Retired/non-exam wording that must not appear in learner-facing content.
# Pattern -> (replacement, courses where enforced)
RETIRED_TERMS = [
    ("Azure AD", "Microsoft Entra ID", ALL_COURSES),
    ("Azure Active Directory", "Microsoft Entra ID", ALL_COURSES),
    ("Azure Security Center", "Microsoft Defender for Cloud", ALL_COURSES),
    ("Azure Defender", "Microsoft Defender for Cloud", ALL_COURSES),
    ("Azure Blueprints", "deprecated (do not use)", ALL_COURSES),
    ("LUIS", "retired AI-901 study-resource wording", ALL_COURSES),
    ("Language Understanding", "retired AI-901 study-resource wording", ALL_COURSES),
    ("Anomaly Detector", "retired AI-901 study-resource wording", ALL_COURSES),
    ("Azure Bot Service", "retired AI-901 study-resource wording", ALL_COURSES),
    ("Form Recognizer", "Azure Content Understanding in Foundry Tools", ["ai-901"]),
    ("Azure AI Document Intelligence", "Azure Content Understanding in Foundry Tools", ["ai-901"]),
    ("geo redundant zones", "geo-zone-redundant storage (GZRS)", ALL_COURSES),
    ("AI-900", "AI-901", ALL_COURSES),
    ("Azure AI Foundry", "Microsoft Foundry", ["ai-901"]),
    ("Azure OpenAI", "Microsoft Foundry", ["ai-901"]),
    ("Azure Speech service", "Azure Speech in Foundry Tools", ["ai-901"]),
    ("Azure AI Speech", "Azure Speech in Foundry Tools", ["ai-901"]),
    ("Azure AD B2B", "external identities", ["az-900"]),
    ("Azure AD B2C", "external identities", ["az-900"]),
    ("Azure AD Conditional Access", "Microsoft Entra Conditional Access", ALL_COURSES),
    ("regional pairs", "region pairs", ["az-900"]),
    ("paired regions", "region pairs", ["az-900"]),
    ("VM scale sets", "Azure Virtual Machine Scale Sets", ["az-900"]),
    ("Service Trust Portal", "Microsoft Service Trust Portal (SC-900 only)", ["az-900"]),
]

# Ambiguous acronyms that must carry their course-qualified phrase in the same
# field. acronym -> {courseId: required qualified phrase}
AMBIGUOUS_ACRONYMS = {
    "RBAC": {
        "az-900": "Azure role-based access control (RBAC)",
    },
}


def load_questions():
    """Import each course module and return a flat list of question dicts."""
    sys.path.insert(0, CONTENT_DIR)
    questions = []
    for mod_name in (
        "az900_cloud",
        "az900_architecture",
        "az900_governance",
        "az900_add",
        "dp900",
        "dp900_add",
        "ai901",
        "ai901_add",
    ):
        mod = __import__(mod_name)
        qs = getattr(mod, "QUESTIONS")
        questions.extend(qs)
    return questions


def check_question(q, i, errors):
    prefix = f"Question {i} ({q.get('id', '<no id>')})"

    def req(key):
        v = q.get(key)
        if not isinstance(v, str) or not v.strip():
            errors.append(f"{prefix}: missing or empty {key}")
            return None
        return v

    qid = req("id")
    req("text")
    req("domain")
    req("difficulty")
    req("source")
    req("rightsBasis")
    req("courseId")

    options = q.get("options")
    if not isinstance(options, list) or len(options) < 2:
        errors.append(f"{prefix}: options must be a list of >= 2 strings")
        options = []
    else:
        for oi, o in enumerate(options):
            if not isinstance(o, str) or not o.strip():
                errors.append(f"{prefix}: option {oi} must be a non-empty string")

    ci = q.get("correctOptionIndex")
    if not isinstance(ci, int) or ci < 0 or ci >= len(options):
        errors.append(
            f"{prefix}: correctOptionIndex {ci!r} out of range (0..{len(options) - 1})"
        )

    expl = q.get("explanation")
    if expl is not None and (not isinstance(expl, str) or not expl.strip()):
        errors.append(f"{prefix}: explanation must be a non-empty string")

    rb = q.get("rightsBasis")
    if isinstance(rb, str) and rb not in PERMITTED_RIGHTS_BASES:
        errors.append(f"{prefix}: rightsBasis {rb!r} not in {PERMITTED_RIGHTS_BASES}")

    course = q.get("courseId")
    if isinstance(course, str) and course not in ALL_COURSES:
        errors.append(f"{prefix}: courseId {course!r} not in {ALL_COURSES}")

    # Terminology lint over text, options, explanation.
    if isinstance(course, str):
        fields = {"text": q.get("text", "")}
        for oi, o in enumerate(options):
            fields[f"option {oi}"] = o
        if expl:
            fields["explanation"] = expl
        for fname, fval in fields.items():
            _lint_field(qid, course, fname, fval, errors)


def _lint_field(qid, course, field, value, errors):
    lower = value.lower()
    for pattern, replacement, courses in RETIRED_TERMS:
        if course not in courses:
            continue
        # Match the retired term as a whole token/word so that a legitimate
        # current term is not flagged by a substring overlap (e.g. the
        # official "Azure Advisor" must not be flagged by the retired
        # "Azure AD").
        needle = re.escape(pattern.lower())
        if re.search(r"(?<![a-z0-9])" + needle + r"(?![a-z0-9])", lower):
            errors.append(
                f"Question {qid} ({field}): retired wording {pattern!r} -> use {replacement!r}"
            )
    for acronym, course_phrases in AMBIGUOUS_ACRONYMS.items():
        required = course_phrases.get(course)
        if required is None:
            continue
        if acronym.lower() in lower and required.lower() not in lower:
            errors.append(
                f"Question {qid} ({field}): bare {acronym!r} must be qualified as {required!r}"
            )


def _spread_options(q):
    """Deterministically reorder options so the correct answer is spread
    across positions, and update correctOptionIndex.

    The authoring source keeps the correct answer first for readability; this
    step ensures the shipped pack does not expose a fixed answer position. It
    uses a stable SHA-256 hash of the item id, so regeneration is reproducible
    and does not depend on process-local hash randomization.
    """
    options = q.get("options")
    if not isinstance(options, list) or len(options) < 2:
        return q
    ci = q.get("correctOptionIndex")
    if not isinstance(ci, int) or not (0 <= ci < len(options)):
        return q
    qid = str(q.get("id", ""))
    seed = int(hashlib.sha256(qid.encode("utf-8")).hexdigest(), 16)
    target = seed % len(options)
    correct = options[ci]
    rest = [o for i, o in enumerate(options) if i != ci]
    new_options = rest[:target] + [correct] + rest[target:]
    out = dict(q)
    out["options"] = new_options
    out["correctOptionIndex"] = target
    return out


def _check_position_spread(questions, errors):
    """Fail the build if the answer key is positionally biased."""
    if not questions:
        return
    c = Counter(q["correctOptionIndex"] for q in questions)
    total = len(questions)
    pos, cnt = c.most_common(1)[0]
    share = cnt / total
    if share > 0.60:
        errors.append(
            f"answer key positional bias: correctOptionIndex distribution "
            f"{dict(sorted(c.items()))}; position {pos} holds {share:.0%} of keys"
        )


def main():
    questions = load_questions()
    errors = []

    if not questions:
        errors.append("no questions loaded")

    # Spread the correct answer across option positions before validation so
    # the shipped pack never exposes a fixed answer position.
    questions = [_spread_options(q) for q in questions]
    _check_position_spread(questions, errors)

    seen_ids = set()
    for i, q in enumerate(questions):
        qid = q.get("id")
        if qid in seen_ids:
            errors.append(f"duplicate id {qid!r}")
        elif qid:
            seen_ids.add(qid)
        check_question(q, i, errors)

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    pack = {
        "formatVersion": FORMAT_VERSION,
        "packId": "com.example.studyapp.content.v1",
        "packVersion": 1,
        "title": "Azure Learning Launch Content",
        "source": (
            "Original AI-fleet-authored content with substantive human review "
            "by the publisher (Dimitri Meier); facts verified against Microsoft "
            "Learn study guides, retrieved 2026-10-02"
        ),
        "rightsBasis": "original-human-ai-assisted",
        "lastVerifiedAt": "2026-10-02",
        "questions": questions,
    }

    os.makedirs(os.path.dirname(ASSET_PATH), exist_ok=True)
    with open(ASSET_PATH, "w", encoding="utf-8") as f:
        json.dump(pack, f, indent=2, ensure_ascii=False)
        f.write("\n")

    per_course = {}
    for q in questions:
        per_course.setdefault(q["courseId"], []).append(q)

    print("OK: wrote", ASSET_PATH)
    for course in sorted(per_course):
        print(f"  {course}: {len(per_course[course])} questions")
    print(f"  total: {len(questions)} questions")


if __name__ == "__main__":
    main()
