import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import 'package:study_app/data/content_pack_loader.dart';
import 'package:study_app/data/local_store.dart';
import 'package:study_app/models/attempt.dart';
import 'package:study_app/models/content_pack.dart';
import 'package:study_app/models/question.dart';
import 'package:study_app/models/session.dart';

import 'test_helpers.dart';

const String _validPackJson = '''
{
  "formatVersion": "azpack-v2",
  "packId": "com.example.test.synthetic",
  "packVersion": 1,
  "title": "Synthetic test pack",
  "source": "Test fixture",
  "rightsBasis": "original-human",
  "questions": [
    {
      "id": "q-001",
      "text": "Sample question one?",
      "options": ["A", "B", "C"],
      "correctOptionIndex": 1,
      "explanation": "B is correct.",
      "domain": "Domain A",
      "difficulty": "easy",
      "source": "Per-question fixture",
      "rightsBasis": "original-human",
      "courseId": "az-900"
    },
    {
      "id": "q-002",
      "text": "Sample question two?",
      "options": ["X", "Y"],
      "correctOptionIndex": 0,
      "explanation": "X is correct.",
      "domain": "Domain B",
      "difficulty": "medium",
      "source": "Per-question fixture",
      "rightsBasis": "original-human",
      "courseId": "az-900"
    }
  ]
}
''';

void main() {
  setUpAll(initTestDatabase);

  group('ContentPack parsing', () {
    test('parses a valid synthetic pack', () {
      final pack = ContentPack.parse(_validPackJson);
      expect(pack.formatVersion, 'azpack-v2');
      expect(pack.packId, 'com.example.test.synthetic');
      expect(pack.packVersion, 1);
      expect(pack.questions.length, 2);
      expect(pack.questions.first.id, 'q-001');
    });

    test('rejects invalid JSON', () {
      expect(() => ContentPack.parse('{'), throwsA(isA<FormatException>()));
    });

    test('rejects a pack with missing required fields', () {
      const badPack = '''
      {
        "formatVersion": "azpack-v1",
        "packId": "missing-fields"
      }
      ''';
      expect(() => ContentPack.parse(badPack), throwsA(isA<FormatException>()));
    });
  });

  group('ContentPack validation', () {
    test('accepts a valid synthetic pack', () {
      final pack = ContentPack.parse(_validPackJson);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, isEmpty);
    });

    test('rejects unsupported formatVersion', () {
      final json = _validPackJson.replaceFirst('azpack-v2', 'azpack-v1');
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('Unsupported formatVersion')));
    });

    test('rejects packVersion less than 1', () {
      final json = _validPackJson.replaceFirst('"packVersion": 1', '"packVersion": 0');
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('packVersion must be >= 1')));
    });

    test('rejects duplicate question ids within a pack', () {
      final json = _validPackJson.replaceFirst('"q-002"', '"q-001"');
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('duplicate id')));
    });

    test('rejects out-of-range correctOptionIndex', () {
      final json = _validPackJson.replaceFirst('"correctOptionIndex": 1', '"correctOptionIndex": 5');
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('out of range')));
    });

    test('rejects too few options', () {
      final json = _validPackJson.replaceFirst(
        '["A", "B", "C"]',
        '["A"]',
      );
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('at least two options')));
    });

    test('rejects missing per-question source', () {
      final json = _validPackJson.replaceFirst(
        '"source": "Per-question fixture"',
        '"source": ""',
      );
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('missing or empty source')));
    });

    test('rejects missing per-question rightsBasis', () {
      final json = _validPackJson.replaceFirst(
        '"source": "Per-question fixture",\n      "rightsBasis": "original-human",',
        '"source": "Per-question fixture",\n      "rightsBasis": "",',
      );
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('missing or empty rightsBasis')));
    });

    test('rejects missing per-question explanation', () {
      final json = _validPackJson.replaceFirst(
        '"explanation": "B is correct.",',
        '',
      );
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('missing or empty explanation')));
    });

    test('rejects missing per-question courseId', () {
      final json = _validPackJson.replaceFirst(
        '"courseId": "az-900"',
        '"courseId": ""',
      );
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('missing or empty courseId')));
    });

    test('rejects a rightsBasis outside the permitted values', () {
      final json = _validPackJson.replaceFirst(
        '"rightsBasis": "original-human"',
        '"rightsBasis": "invented-basis"',
      );
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('not one of the permitted values')));
    });

    test('rejects licensed-cc-by-4.0 without licenseRef and attributionText',
        () {
      final json = _validPackJson.replaceFirst(
        '"rightsBasis": "original-human"',
        '"rightsBasis": "licensed-cc-by-4.0"',
      );
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('requires a non-empty licenseRef')));
      expect(
        errors,
        contains(contains('requires a non-empty attributionText')),
      );
    });

    test('accepts licensed-cc-by-4.0 with companion fields', () {
      const json = '''
      {
        "formatVersion": "azpack-v2",
        "packId": "com.example.test.licensed",
        "packVersion": 1,
        "title": "Licensed test pack",
        "source": "Test fixture",
        "rightsBasis": "licensed-cc-by-4.0",
        "licenseRef": "https://example.com/cc-by-license",
        "attributionText": "CC BY 4.0 — Example Author",
        "questions": [
          {
            "id": "q-001",
            "text": "Sample question one?",
            "options": ["A", "B", "C"],
            "correctOptionIndex": 1,
            "explanation": "B is correct.",
            "domain": "Domain A",
            "difficulty": "easy",
            "source": "Per-question fixture",
            "rightsBasis": "original-human",
            "courseId": "az-900"
          }
        ]
      }
      ''';
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, isEmpty);
    });

    test('rejects an invalid pack-level lastVerifiedAt date', () {
      final json = _validPackJson.replaceFirst(
        '"packVersion": 1',
        '"packVersion": 1,\n  "lastVerifiedAt": "not-a-date"',
      );
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('lastVerifiedAt')));
    });

    test('terminology lint fails the pack on retired Azure AD wording', () {
      final pack = ContentPack(
        formatVersion: 'azpack-v2',
        packId: 'lint-test',
        packVersion: 1,
        title: 'Lint test',
        source: 'Test fixture',
        rightsBasis: 'original-human',
        questions: [
          PackQuestion(
            id: 'az900-lint',
            text: 'Which Azure AD feature provides SSO?',
            options: const ['SSO', 'MFA'],
            correctOptionIndex: 0,
            domain: 'Domain',
            difficulty: 'easy',
            source: 'Test fixture',
            rightsBasis: 'original-human',
            courseId: 'az-900',
          ),
        ],
      );
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('Azure AD')));
    });

    test('terminology lint fails the pack on bare RBAC', () {
      final pack = ContentPack(
        formatVersion: 'azpack-v2',
        packId: 'lint-rbac',
        packVersion: 1,
        title: 'Lint RBAC test',
        source: 'Test fixture',
        rightsBasis: 'original-human',
        questions: [
          PackQuestion(
            id: 'az900-rbac',
            text: 'Which RBAC role is read-only?',
            options: const ['Owner', 'Reader'],
            correctOptionIndex: 1,
            domain: 'Domain',
            difficulty: 'easy',
            source: 'Test fixture',
            rightsBasis: 'original-human',
            courseId: 'az-900',
          ),
        ],
      );
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('RBAC')));
    });

    test('rejects non-string optional fields', () {
      final json = _validPackJson.replaceFirst(
        '"source": "Test fixture"',
        '"source": "Test fixture",\n  "lastVerifiedAt": 2026',
      );
      expect(
        () => ContentPack.parse(json),
        throwsA(isA<FormatException>().having(
          (e) => e.message,
          'message',
          contains('lastVerifiedAt'),
        )),
      );
    });

    test('rejects non-string optional per-question companion fields', () {
      final json = _validPackJson.replaceFirst(
        '"rightsBasis": "original-human",\n      "courseId": "az-900"',
        '"rightsBasis": "original-human",\n      "licenseRef": 12345,\n      "courseId": "az-900"',
      );
      expect(
        () => ContentPack.parse(json),
        throwsA(isA<FormatException>().having(
          (e) => e.message,
          'message',
          contains('licenseRef'),
        )),
      );
    });

    test('rejects an unknown courseId', () {
      final json = _validPackJson.replaceFirst(
        '"courseId": "az-900"',
        '"courseId": "unknown-course"',
      );
      final pack = ContentPack.parse(json);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('not a registered course')));
    });

    test('rejects a pack with no questions', () {
      final pack = ContentPack(
        formatVersion: 'azpack-v2',
        packId: 'empty-pack',
        packVersion: 1,
        title: 'Empty',
        source: 'synthetic',
        rightsBasis: 'synthetic',
        questions: const [],
      );
      final errors = ContentPackValidator(pack).validate();
      expect(errors, contains(contains('at least one question')));
    });
  });

  group('ContentPack atomic application', () {
    late LocalStore store;

    setUp(() async {
      final db = await openTestDatabase();
      store = LocalStore.withDatabase(db);
    });

    tearDown(() async {
      await store.close();
    });

    test('applies a valid pack and persists provenance', () async {
      final success = await ContentPackLoader.loadPackFromString(store, _validPackJson);
      expect(success, isTrue);

      final questions = await store.getQuestions();
      expect(questions.length, 2);

      final first = questions.firstWhere((q) => q.id == 'q-001');
      expect(first.source, 'Per-question fixture');
      expect(first.rightsBasis, 'original-human');
    });

    test('invalid pack is rejected and writes nothing', () async {
      const badPack = '''
      {
        "formatVersion": "azpack-v1",
        "packId": "bad",
        "packVersion": 1,
        "title": "Bad",
        "source": "synthetic",
        "rightsBasis": "original-human",
        "questions": [
          {
            "id": "q-001",
            "text": "T",
            "options": ["A"],
            "correctOptionIndex": 0,
            "domain": "D",
            "difficulty": "easy",
            "source": "synthetic",
            "rightsBasis": "original-human"
          }
        ]
      }
      ''';
      final success = await ContentPackLoader.loadPackFromString(store, badPack);
      expect(success, isFalse);
      expect(await store.getQuestions(), isEmpty);
    });

    test('pack without an explanation is rejected and writes nothing', () async {
      final noExplanation = _validPackJson.replaceFirst(
        '"explanation": "B is correct.",',
        '',
      );
      final success =
          await ContentPackLoader.loadPackFromString(store, noExplanation);
      expect(success, isFalse);
      expect(await store.getQuestions(), isEmpty);
    });

    test('storage failures are reported as false instead of propagating',
        () async {
      final db = await openTestDatabase();
      final store = LocalStore.withDatabase(db);
      await store.applyContentPack(ContentPack.parse(_validPackJson));
      expect(await store.getQuestions(), hasLength(2));

      // Every write against a closed database fails.
      await db.close();

      final success = await ContentPackLoader.loadPackFromString(
        store,
        _validPackJson,
      );

      expect(success, isFalse);
    });

    test('repeat loading does not duplicate questions', () async {
      final pack = ContentPack.parse(_validPackJson);
      await store.applyContentPack(pack);

      final attempt = Attempt(
        questionId: 'q-001',
        selectedOptionIndex: 1,
        correct: true,
        timestamp: DateTime.now(),
      );
      await store.recordAttempt(attempt);
      await store.saveSession(
        StudySession(
          id: 's-1',
          mode: 'practice',
          startedAt: DateTime.now().subtract(const Duration(minutes: 1)),
          finishedAt: DateTime.now(),
          questionCount: 2,
          correctCount: 1,
        ),
      );

      // Load the same pack again.
      await store.applyContentPack(pack);

      final questions = await store.getQuestions();
      expect(questions.length, 2);
      expect(await store.getAttempts(), hasLength(1));
      expect(await store.getSessions(), hasLength(1));
    });

    test('reloading an updated pack replaces question content', () async {
      final initial = ContentPack.parse(_validPackJson);
      await store.applyContentPack(initial);

      final updatedJson = _validPackJson.replaceFirst(
        'Sample question one?',
        'Updated sample question one?',
      );
      final updated = ContentPack.parse(updatedJson);
      await store.applyContentPack(updated);

      final q = await store.getQuestion('q-001');
      expect(q, isNotNull);
      expect(q!.text, 'Updated sample question one?');
    });

    test('transaction failure rolls back the entire pack', () async {
      final db = await openTestDatabase();
      store = LocalStore.withDatabase(db);
      final pack = ContentPack.parse(_validPackJson);

      Object? caught;
      try {
        await db.transaction((txn) async {
          await store.applyContentPackToTransaction(txn, pack);
          throw Exception('forced transaction failure');
        });
      } catch (e) {
        caught = e;
      }

      expect(caught, isNotNull);
      expect(await store.getQuestions(), isEmpty);
    });
  });

  group('Schema migration', () {
    test('v1 database migrates to v2 with provenance columns', () async {
      final db = await openDatabase(
        inMemoryDatabasePath,
        singleInstance: false,
      );
      await LocalStore.createV1Schema(db);
      await db.insert('questions', {
        'id': 'legacy-q1',
        'text': 'Legacy question',
        'options': 'A\nB\nC',
        'correctOptionIndex': 0,
        'explanation': null,
        'domain': 'Legacy',
        'difficulty': 'easy',
      });

      await LocalStore.migrateV1ToV2(db);

      final rows = await db.query('questions');
      expect(rows.length, 1);
      expect(rows.first['id'], 'legacy-q1');
      expect(rows.first['source'], isNull);
      expect(rows.first['rightsBasis'], isNull);

      final question = Question.fromMap(rows.first);
      expect(question.source, isNull);
      expect(question.rightsBasis, isNull);

      final info = await db.rawQuery('PRAGMA table_info(questions)');
      final names = info.map((r) => r['name'] as String).toSet();
      expect(names, contains('source'));
      expect(names, contains('rightsBasis'));

      await db.close();
    });

    test('file-based v1 database upgrades to v2 on open', () async {
      final dbPath = await getDatabasesPath();
      final path = join(dbPath, 'migration_test.db');
      await deleteDatabase(path);

      final v1 = await openDatabase(
        path,
        version: 1,
        onCreate: (db, version) => LocalStore.createV1Schema(db),
      );
      await v1.insert('questions', {
        'id': 'legacy-file-q1',
        'text': 'Legacy file question',
        'options': 'A\nB',
        'correctOptionIndex': 0,
        'domain': 'Legacy',
        'difficulty': 'easy',
      });
      await v1.close();

      final v2 = await openDatabase(
        path,
        version: 2,
        onCreate: (db, version) => LocalStore.createSchema(db),
        onUpgrade: (db, oldVersion, newVersion) async {
          if (oldVersion < 2) {
            await LocalStore.migrateV1ToV2(db);
          }
        },
      );
      final rows = await v2.query('questions');
      expect(rows.length, 1);
      expect(rows.first['id'], 'legacy-file-q1');

      final info = await v2.rawQuery('PRAGMA table_info(questions)');
      final names = info.map((r) => r['name'] as String).toSet();
      expect(names, containsAll(['source', 'rightsBasis']));

      await v2.close();
      await deleteDatabase(path);
    });
  });

  group('Pack loader integration', () {
    test('loadPackFromString returns false for invalid JSON', () async {
      final db = await openTestDatabase();
      final store = LocalStore.withDatabase(db);
      final success = await ContentPackLoader.loadPackFromString(store, 'not-json');
      expect(success, isFalse);
      await store.close();
    });

    test('fixture file parses and validates', () async {
      final fixture = File('test/fixtures/synthetic-demo-pack.json');
      final jsonString = await fixture.readAsString();
      final pack = ContentPack.parse(jsonString);
      final errors = ContentPackValidator(pack).validate();
      expect(errors, isEmpty);
      expect(pack.questions.length, 2);
    });
  });
}
