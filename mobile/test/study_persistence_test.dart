import 'package:flutter_test/flutter_test.dart';

import 'package:study_app/data/local_store.dart';
import 'package:study_app/data/question_bank.dart';
import 'package:study_app/models/question.dart';
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
      final loaded = await store.getAllQuestions();
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

    test('getStudyProgress reflects only loaded course content', () async {
      final progress = await store.getStudyProgress('AZ-900');
      expect(progress.total, QuestionBank.syntheticFixtures().length);
      expect(progress.seen, 0);
      expect(progress.coverage, 0.0);

      await store.saveStudyStatus(
        courseId: 'AZ-900',
        questionId: 'fixture-001',
        status: StudyMaterialStatus.seen,
      );
      final updated = await store.getStudyProgress('AZ-900');
      expect(updated.seen, 1);
      expect(updated.needsReview, 0);
      expect(updated.coverage, 1 / QuestionBank.syntheticFixtures().length);
    });

    test('clearAllData removes study status rows', () async {
      await store.saveStudyStatus(
        courseId: 'AZ-900',
        questionId: 'fixture-001',
        status: StudyMaterialStatus.seen,
      );
      await store.clearAllData();
      expect(await store.getAllQuestions(), isEmpty);
      expect(await store.getStudyStatusesForCourse('AZ-900'), isEmpty);
    });

    test('progress stays correct when content changes', () async {
      // Mark all current AZ-900 fixtures as seen.
      for (final q in QuestionBank.syntheticFixtures()) {
        await store.saveStudyStatus(
          courseId: 'AZ-900',
          questionId: q.id,
          status: StudyMaterialStatus.seen,
        );
      }

      // Replace content with a single new question; previous statuses remain
      // in the table but should not count toward the new coverage total.
      await store.clearAllData();
      await store.insertQuestions(const [
        Question(
          id: 'new-001',
          text: 'New question',
          options: ['A', 'B'],
          correctOptionIndex: 0,
          explanation: 'Because A is correct.',
          domain: 'Cloud Concepts',
          courseId: 'AZ-900',
          difficulty: 'easy',
        ),
      ]);
      await store.saveStudyStatus(
        courseId: 'AZ-900',
        questionId: 'new-001',
        status: StudyMaterialStatus.seen,
      );

      final progress = await store.getStudyProgress('AZ-900');
      expect(progress.total, 1);
      expect(progress.seen, 1);
      expect(progress.complete, isTrue);
    });
  });
}
