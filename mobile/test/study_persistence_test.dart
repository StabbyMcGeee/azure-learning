import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:path/path.dart' as p;
import 'package:sqflite/sqflite.dart';

import 'package:study_app/data/local_store.dart';
import 'package:study_app/data/question_bank.dart';
import 'package:study_app/models/attempt.dart';
import 'package:study_app/models/content_pack.dart';
import 'package:study_app/models/study_status.dart';

import 'test_helpers.dart';

void main() {
  setUpAll(initTestDatabase);

  group('Study persistence', () {
    late LocalStore store;

    setUp(() async {
      final db = await openTestDatabase();
      store = LocalStore.withDatabase(db);
      await store.insertQuestions(QuestionBank.syntheticFixtures());
    });

    tearDown(() async {
      await store.close();
    });

    test('schema stores courseId on questions', () async {
      final loaded = await store.getQuestions();
      expect(loaded.every((q) => q.courseId?.isNotEmpty ?? false), isTrue);
    });

    test('saveStudyStatus stores and overwrites per course', () async {
      await store.saveStudyStatus(
        courseId: 'AZ-900',
        questionId: 'fixture-001',
        status: StudyMaterialStatus.seen,
      );
      var statuses = await store.getStudyStatusesForCourse('AZ-900');
      expect(statuses['fixture-001'], StudyMaterialStatus.seen);

      await store.saveStudyStatus(
        courseId: 'AZ-900',
        questionId: 'fixture-001',
        status: StudyMaterialStatus.needsReview,
      );
      statuses = await store.getStudyStatusesForCourse('AZ-900');
      expect(statuses['fixture-001'], StudyMaterialStatus.needsReview);
    });

    test('study statuses are isolated by course', () async {
      await store.saveStudyStatus(
        courseId: 'AZ-900',
        questionId: 'fixture-001',
        status: StudyMaterialStatus.seen,
      );
      await store.saveStudyStatus(
        courseId: 'AZ-104',
        questionId: 'fixture-001',
        status: StudyMaterialStatus.needsReview,
      );

      final az900 = await store.getStudyStatusesForCourse('AZ-900');
      final az104 = await store.getStudyStatusesForCourse('AZ-104');

      expect(az900['fixture-001'], StudyMaterialStatus.seen);
      expect(az104['fixture-001'], StudyMaterialStatus.needsReview);
    });

    test('clearAllData removes study status rows', () async {
      await store.saveStudyStatus(
        courseId: 'AZ-900',
        questionId: 'fixture-001',
        status: StudyMaterialStatus.seen,
      );
      await store.clearAllData();
      expect(await store.getQuestions(), isEmpty);
      expect(await store.getStudyStatusesForCourse('AZ-900'), isEmpty);
    });

    test('statuses survive content replacement and stay per course', () async {
      await store.saveStudyStatus(
        courseId: 'AZ-900',
        questionId: 'fixture-001',
        status: StudyMaterialStatus.needsReview,
      );

      // Content for the course is replaced by a pack carrying different ids.
      await store.applyContentPack(ContentPack.parse(_replacementPackJson));

      final statuses = await store.getStudyStatusesForCourse('AZ-900');
      expect(statuses['fixture-001'], StudyMaterialStatus.needsReview);
      expect(statuses.containsKey('replacement-001'), isFalse);
      final otherCourse =
          await store.getStudyStatusesForCourse('AZ-104');
      expect(otherCourse, isEmpty);
    });

    test('recorded attempt courseId scopes history and NULL stays visible',
        () async {
      await store.recordAttempt(Attempt(
        questionId: 'fixture-001',
        courseId: 'AZ-900',
        selectedOptionIndex: 0,
        correct: true,
        timestamp: DateTime.now(),
      ));
      await store.recordAttempt(Attempt(
        questionId: 'fixture-002',
        courseId: 'AZ-104',
        selectedOptionIndex: 0,
        correct: false,
        timestamp: DateTime.now(),
      ));
      await store.recordAttempt(Attempt(
        questionId: 'fixture-003',
        selectedOptionIndex: 0,
        correct: true,
        timestamp: DateTime.now(),
      ));

      final az900 = await store.getAttempts(courseId: 'AZ-900');
      final az104 = await store.getAttempts(courseId: 'AZ-104');

      expect(az900.map((a) => a.questionId), contains('fixture-001'));
      expect(az900.map((a) => a.questionId), isNot(contains('fixture-002')));
      expect(az900.map((a) => a.questionId), contains('fixture-003'));

      expect(az104.map((a) => a.questionId), contains('fixture-002'));
      expect(az104.map((a) => a.questionId), isNot(contains('fixture-001')));
      expect(az104.map((a) => a.questionId), contains('fixture-003'));
    });
  });

  group('Schema migration chain', () {
    test('v3 database migrates to v4 creating study_status', () async {
      final tempDir = Directory.systemTemp.createTempSync('azstudy-test-');
      final path = p.join(tempDir.path, 'v3-to-v4.db');
      var db = await openDatabase(
        path,
        version: 1,
        onCreate: (db, version) async => LocalStore.createV1Schema(db),
      );
      await db.close();

      db = await openDatabase(
        path,
        version: 4,
        onUpgrade: (db, oldVersion, newVersion) async {
          if (oldVersion < 2) await LocalStore.migrateV1ToV2(db);
          if (oldVersion < 3) await LocalStore.migrateV2ToV3(db);
          if (oldVersion < 4) await LocalStore.migrateV3ToV4(db);
        },
      );
      final tables = await db.rawQuery(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='study_status'",
      );
      expect(tables, isNotEmpty);
      await db.close();
      tempDir.deleteSync(recursive: true);
    });

    test('v4 database migrates to v5 adding attempts.courseId', () async {
      final tempDir = Directory.systemTemp.createTempSync('azstudy-test-');
      final path = p.join(tempDir.path, 'v4-to-v5.db');
      var db = await openDatabase(
        path,
        version: 1,
        onCreate: (db, version) async => LocalStore.createV1Schema(db),
      );
      await db.close();

      db = await openDatabase(
        path,
        version: 5,
        onUpgrade: (db, oldVersion, newVersion) async {
          if (oldVersion < 2) await LocalStore.migrateV1ToV2(db);
          if (oldVersion < 3) await LocalStore.migrateV2ToV3(db);
          if (oldVersion < 4) await LocalStore.migrateV3ToV4(db);
          if (oldVersion < 5) await LocalStore.migrateV4ToV5(db);
        },
      );
      final columns = await db.rawQuery(
        "PRAGMA table_info(attempts)",
      );
      final hasCourseId = columns.any((c) => c['name'] == 'courseId');
      expect(hasCourseId, isTrue);
      await db.close();
      tempDir.deleteSync(recursive: true);
    });
  });
}

const String _replacementPackJson = '''
{
  "formatVersion": "azpack-v2",
  "packId": "com.example.studyapp.replacement",
  "packVersion": 1,
  "title": "Replacement pack",
  "source": "Synthetic fixture",
  "rightsBasis": "synthetic-fixture",
  "questions": [
    {
      "id": "replacement-001",
      "text": "Replacement question?",
      "options": ["A", "B"],
      "correctOptionIndex": 0,
      "explanation": "A is correct.",
      "domain": "Cloud Concepts",
      "difficulty": "easy",
      "source": "Synthetic fixture",
      "rightsBasis": "synthetic-fixture",
      "courseId": "AZ-900"
    }
  ]
}
''';
