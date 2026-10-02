# Offline content packs

The mobile app uses a bounded, versioned offline content-pack format called
**azpack-v2**. A pack is a single JSON file that carries both pack-level and
per-question provenance metadata. The app parses, validates, and applies packs
atomically to its SQLite question bank. Missing or invalid packs leave the bank
empty and preserve all user attempt/session history.

> **Important:** Provenance metadata is required, but it does **not** by itself
> prove that a question is rights-cleared. Real curriculum must be human-authored
> or commercially licensed and reviewed by the project before it is shipped.

## Where packs are loaded from

On startup the app attempts to load a bundled asset at:

```
assets/content-pack.json
```

If the asset is absent, malformed, unsupported, or invalid, the loader returns
`false` and the app keeps the current empty production bank. No error is shown
to the user. To ship a pack, place the prepared JSON file at that path and make
sure it is listed in the `assets` section of `pubspec.yaml`.

## Pack format (`azpack-v2`)

```json
{
  "formatVersion": "azpack-v2",
  "packId": "com.example.studyapp.az900.v1",
  "packVersion": 1,
  "title": "Example AZ-900 Study Pack",
  "source": "Original human-authored content",
  "rightsBasis": "original-human",
  "lastVerifiedAt": "2026-10-02",
  "questions": [
    {
      "id": "az-900-001",
      "text": "Which cloud trait lets you pay only for resources you use?",
      "options": [
        "High availability",
        "Fault tolerance",
        "Scalability",
        "Elasticity"
      ],
      "correctOptionIndex": 3,
      "explanation": "Elasticity is the ability to scale resources up or down and pay for what you use.",
      "domain": "Cloud Concepts",
      "difficulty": "easy",
      "source": "Original human-authored content",
      "rightsBasis": "original-human",
      "courseId": "az-900"
    }
  ]
}
```

### Top-level fields

| Field              | Type   | Required | Description                                                          |
|--------------------|--------|----------|----------------------------------------------------------------------|
| `formatVersion`    | string | yes      | Must be exactly `azpack-v2`.                                         |
| `packId`           | string | yes      | Stable reverse-DNS identifier for this pack.                         |
| `packVersion`      | int    | yes      | Monotonically increasing pack revision, `>= 1`.                      |
| `title`            | string | yes      | Human-readable title.                                                |
| `source`           | string | yes      | Where the pack content came from (e.g. author, licensee).            |
| `rightsBasis`      | enum   | yes      | One of `original-human`, `original-human-ai-assisted`, `licensed-cc-by-4.0`, `licensed-commercial`, `public-domain`. |
| `licenseRef`       | string | cond     | Required when `rightsBasis` starts with `licensed-`.                  |
| `attributionText`  | string | cond     | Required when `rightsBasis` is `licensed-cc-by-4.0`.                 |
| `lastVerifiedAt`   | string | no       | ISO-8601 date shown in About & Legal as the content-last-verified date. |
| `questions`        | array  | yes      | List of question objects.                                              |

### Per-question fields

| Field                 | Type    | Required | Description                                                                    |
|-----------------------|---------|----------|--------------------------------------------------------------------------------|
| `id`                  | string  | yes      | Unique identifier within the pack.                                             |
| `text`                | string  | yes      | Question prompt.                                                               |
| `options`             | array   | yes      | At least two strings.                                                          |
| `correctOptionIndex`  | int     | yes      | Zero-based index into `options`.                                               |
| `explanation`         | string  | no       | Explanation shown after answering.                                             |
| `domain`              | string  | yes      | Domain or topic tag.                                                           |
| `difficulty`          | string  | yes      | Difficulty label.                                                              |
| `source`              | string  | yes      | Per-question source; can differ from pack-level source.                        |
| `rightsBasis`         | enum    | yes      | Per-question rights basis; can differ from pack-level rightsBasis.             |
| `licenseRef`          | string  | cond     | Required when the per-question `rightsBasis` starts with `licensed-`.          |
| `attributionText`     | string  | cond     | Required when the per-question `rightsBasis` is `licensed-cc-by-4.0`.        |
| `courseId`            | string  | yes      | Course identifier this question belongs to; supplied by the pack.              |

The `courseId` is never hardcoded in the app. A learner can select any course
present in the loaded packs, and study, practice, exam, review, and progress
screens scope their content to that selection.

## Validation

Before any database write the parser/validator checks:

- The JSON is well-formed.
- `formatVersion` is exactly `azpack-v2`.
- `packVersion` is an integer `>= 1`.
- All required pack-level and per-question string fields are present and non-empty.
- Optional string fields (`licenseRef`, `attributionText`, `lastVerifiedAt`) are
  strings when present; non-string values throw `FormatException`.
- Every question has at least two options.
- `correctOptionIndex` is within the range of the options array.
- All question IDs are unique within the pack.
- The pack does not exceed the question-count bound (`contentPackMaxQuestions`).
- The `rightsBasis` value is checked against the azlegal-db-v1 permitted
  values (`original-human`, `original-human-ai-assisted`, `licensed-cc-by-4.0`,
  `licensed-commercial`, `public-domain`). Any other value rejects the pack.
- `licensed-*` bases require a non-empty `licenseRef`; `licensed-cc-by-4.0`
  also requires a non-empty `attributionText`.
- `lastVerifiedAt`, when present, must be a valid ISO-8601 date. It is stored
  and displayed in About & Legal as the content-last-verified date.
- `courseId` must be one of the registered launch-course values (`az-900`,
  `sc-900`, `ai-901`).
- A terminology lint runs over every question's text, options, and
  explanation against the azlegal-db-v1 register. Retired product names,
  bare ambiguous abbreviations such as `RBAC`, misspellings, unverified product
  terms, and incorrect course-scoped terms are reported with the item, field,
  and expected wording, and the pack is rejected.

Validation errors are returned as a list of strings; the pack is not applied if
the list is non-empty.

## Pack version ledger

The database keeps a `pack_ledger` table recording the latest applied version of
each `packId`. The loader rejects any pack whose `packVersion` is lower than the
one already recorded. Equal and higher versions are accepted, making repeat
loads and upgrades safe. The ledger entry is written inside the same transaction
as the question rows, so a failed write never leaves a stale ledger behind.

## Atomic application and repeat safety

Packs are applied inside a single SQLite transaction. If any part of the write
fails, the whole transaction rolls back and the database is unchanged.

Question rows are keyed by `id`. Re-applying the same pack, or applying a newer
version with overlapping IDs, replaces the matching question rows but never
touches the `attempts` or `sessions` tables. This makes repeat loading safe and
keeps user history intact.

## Schema migration from v1

The original v1 `questions` table did not store provenance. The v2 schema adds:

```sql
ALTER TABLE questions ADD COLUMN source TEXT;
ALTER TABLE questions ADD COLUMN rightsBasis TEXT;
```

The v3 schema, introduced for course and pack identity, adds:

```sql
ALTER TABLE questions ADD COLUMN packId TEXT;
ALTER TABLE questions ADD COLUMN courseId TEXT;
ALTER TABLE sessions ADD COLUMN courseId TEXT;

CREATE TABLE pack_ledger(
  packId TEXT PRIMARY KEY,
  version INTEGER NOT NULL,
  appliedAt INTEGER NOT NULL
);

CREATE TABLE settings(
  key TEXT PRIMARY KEY,
  value TEXT
);
```

Existing rows receive `NULL` pack/course identity. The migrations run
automatically when an older database is opened at version 3.

## How to prepare a future human-authored or licensed pack

1. Produce or license original questions.
2. Record, for every question, the source author/licensor, the rights basis,
   and a stable `courseId` supplied by the pack.
3. Build a JSON file matching the `azpack-v2` schema above and run the
   terminology lint over the content (the validator does this automatically).
4. Validate the file locally:
   - Run the mobile tests, which exercise the validator with synthetic fixtures,
     or run `tool/build_content_pack.py` to regenerate and validate the
     production pack.
   - Run `dart run tool/validate_evidence_register.dart` to validate the
     private evidence register (`data/evidence-register.json`).
5. Place the validated file at `assets/content-pack.json` and register it in
   `pubspec.yaml`. Keep the private evidence register out of `assets/`.
6. Update `packVersion` when you revise content so the app can detect and
   replace older rows.

Do not reuse the legacy 133 desktop questions unless their rights are
independently cleared. Do not ship the synthetic demo fixture as production
content.

## Example: loading a pack in a test

```dart
final jsonString = await File('test/fixtures/synthetic-demo-pack.json').readAsString();
final pack = ContentPack.parse(jsonString);
final errors = ContentPackValidator(pack).validate();
expect(errors, isEmpty);
await store.applyContentPack(pack);
```
