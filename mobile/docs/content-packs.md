# Offline content packs

The mobile app uses a bounded, versioned offline content-pack format called
**azpack-v1**. A pack is a single JSON file that carries both pack-level and
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
to the user. To ship a pack, place the prepared JSON file at that path and add
it to the `assets` section of `pubspec.yaml`.

## Pack format (`azpack-v1`)

```json
{
  "formatVersion": "azpack-v1",
  "packId": "com.example.studyapp.az900.v1",
  "packVersion": 1,
  "title": "Example AZ-900 Study Pack",
  "source": "Original human-authored content",
  "rightsBasis": "original",
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
      "rightsBasis": "original"
    }
  ]
}
```

### Top-level fields

| Field            | Type   | Required | Description                                                          |
|------------------|--------|----------|----------------------------------------------------------------------|
| `formatVersion`  | string | yes      | Must be exactly `azpack-v1`.                                         |
| `packId`         | string | yes      | Stable reverse-DNS identifier for this pack.                         |
| `packVersion`    | int    | yes      | Monotonically increasing pack revision, `>= 1`.                      |
| `title`          | string | yes      | Human-readable title.                                                |
| `source`         | string | yes      | Where the pack content came from (e.g. author, licensee).            |
| `rightsBasis`    | string | yes      | Legal basis for use (e.g. `original`, `licensed-xyz`, `public-domain`).|
| `questions`      | array  | yes      | List of question objects.                                              |

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
| `rightsBasis`         | string  | yes      | Per-question rights basis; can differ from pack-level rightsBasis.             |

## Validation

Before any database write the parser/validator checks:

- The JSON is well-formed.
- `formatVersion` is exactly `azpack-v1`.
- `packVersion` is an integer `>= 1`.
- All required pack-level and per-question string fields are present and non-empty.
- Every question has at least two options.
- `correctOptionIndex` is within the range of the options array.
- All question IDs are unique within the pack.
- The pack does not exceed the question-count bound (`contentPackMaxQuestions`).

Validation errors are returned as a list of strings; the pack is not applied if
the list is non-empty.

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

Existing rows receive `NULL` provenance. The migration runs automatically when a
v1 database is opened at version 2.

## How to prepare a future human-authored or licensed pack

1. Produce or license original questions.
2. Record, for every question, the source author/licensor and the rights basis.
3. Build a JSON file matching the `azpack-v1` schema above.
4. Validate the file locally:
   - Use `ContentPackLoader.dryRun(jsonString)` in a Dart script or test.
   - Or run the mobile tests, which exercise the validator with synthetic fixtures.
5. Place the validated file at `assets/content-pack.json` and register it in
   `pubspec.yaml`.
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
