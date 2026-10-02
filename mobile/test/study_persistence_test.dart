import 'package:flutter_test/flutter_test.dart';

import 'package:study_app/data/local_store.dart';
import 'package:study_app/data/question_bank.dart';
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
