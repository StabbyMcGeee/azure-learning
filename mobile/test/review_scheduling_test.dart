import 'package:flutter_test/flutter_test.dart';
import 'package:study_app/data/local_store.dart';
import 'package:study_app/data/question_bank.dart';
import 'package:study_app/models/attempt.dart';

import 'test_helpers.dart';

void main() {
  setUpAll(initTestDatabase);

  group('Review scheduling', () {
    late LocalStore store;

    setUp(() async {
      final db = await openTestDatabase();
      store = LocalStore.withDatabase(db);
      await store.insertQuestions(QuestionBank.syntheticFixtures());
    });

    tearDown(() async {
      await store.close();
    });

    test('unattempted questions are immediately due', () async {
      final due = await store.getDueReviewItems();
      expect(due.length, QuestionBank.syntheticFixtures().length);
    });

    test('correct answer pushes next review into the future', () async {
      final q = QuestionBank.syntheticFixtures().first;
      await store.recordAttempt(Attempt(
        questionId: q.id,
        selectedOptionIndex: q.correctOptionIndex,
        correct: true,
        timestamp: DateTime.now(),
      ));
      final due = await store.getDueReviewItems();
      final ids = due.map((d) => d.question.id);
      expect(ids, isNot(contains(q.id)));
    });

    test('wrong answer keeps question due quickly', () async {
      final q = QuestionBank.syntheticFixtures().first;
      await store.recordAttempt(Attempt(
        questionId: q.id,
        selectedOptionIndex: 0,
        correct: false,
        timestamp: DateTime.now().subtract(const Duration(minutes: 10)),
      ));
      final due = await store.getDueReviewItems();
      expect(due.map((d) => d.question.id), contains(q.id));
    });
  });
}
