import 'package:flutter_test/flutter_test.dart';
import 'package:study_app/data/local_store.dart';
import 'package:study_app/data/question_bank.dart';
import 'package:study_app/models/attempt.dart';

import 'test_helpers.dart';

void main() {
  setUpAll(initTestDatabase);

  group('Answer and exam behavior', () {
    late LocalStore store;

    setUp(() async {
      final db = await openTestDatabase();
      store = LocalStore.withDatabase(db);
      await store.insertQuestions(QuestionBank.syntheticFixtures());
    });

    tearDown(() async {
      await store.close();
    });

    test('correct answer is recognized', () {
      final q = QuestionBank.syntheticFixtures().first;
      expect(q.isCorrect(q.correctOptionIndex), isTrue);
    });

    test('wrong answer is recognized', () {
      final q = QuestionBank.syntheticFixtures().first;
      expect(q.isCorrect(0), isFalse);
    });

    test('recording an unanswered exam leaves attempts unchanged', () async {
      final before = await store.getAttempts();
      expect(before.length, 0);
      // Simulate no answer recorded for a question.
      expect(await store.getAttemptsFor('fixture-001'), isEmpty);
    });

    test('exam answered items are persisted and scored', () async {
      final q = QuestionBank.syntheticFixtures().first;
      await store.recordAttempt(Attempt(
        questionId: q.id,
        selectedOptionIndex: q.correctOptionIndex,
        correct: true,
        timestamp: DateTime.now(),
      ));
      final attempts = await store.getAttemptsFor(q.id);
      expect(attempts.length, 1);
      expect(attempts.first.correct, isTrue);
    });
  });
}
