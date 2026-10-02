import 'package:flutter_test/flutter_test.dart';
import 'package:study_app/data/local_store.dart';
import 'package:study_app/data/question_bank.dart';
import 'package:study_app/models/attempt.dart';
import 'package:study_app/models/session.dart';

import 'test_helpers.dart';

void main() {
  setUpAll(initTestDatabase);

  group('LocalStore persistence', () {
    late LocalStore store;

    setUp(() async {
      final db = await openTestDatabase();
      store = LocalStore.withDatabase(db);
    });

    tearDown(() async {
      await store.close();
    });

    test('inserts and retrieves questions', () async {
      final questions = QuestionBank.syntheticFixtures();
      await store.insertQuestions(questions);
      final loaded = await store.getQuestions();
      expect(loaded.length, questions.length);
      expect(loaded.first.id, questions.first.id);
    });

    test('records and retrieves attempts', () async {
      final attempt = Attempt(
        questionId: 'fixture-001',
        selectedOptionIndex: 1,
        correct: false,
        timestamp: DateTime.now(),
      );
      await store.recordAttempt(attempt);
      final attempts = await store.getAttemptsFor('fixture-001');
      expect(attempts.length, 1);
      expect(attempts.first.selectedOptionIndex, 1);
      expect(attempts.first.correct, false);
    });

    test('saves and retrieves sessions', () async {
      final session = StudySession(
        id: 's-1',
        mode: 'exam',
        startedAt: DateTime.now().subtract(const Duration(minutes: 5)),
        finishedAt: DateTime.now(),
        questionCount: 10,
        correctCount: 7,
        scorePercent: 70,
      );
      await store.saveSession(session);
      final sessions = await store.getSessions(mode: 'exam');
      expect(sessions.length, 1);
      expect(sessions.first.correctCount, 7);
    });

    test('clearAllData removes everything', () async {
      await store.insertQuestions(QuestionBank.syntheticFixtures());
      await store.recordAttempt(Attempt(
        questionId: 'fixture-001',
        selectedOptionIndex: 0,
        correct: true,
        timestamp: DateTime.now(),
      ));
      await store.clearAllData();
      expect(await store.getQuestions(), isEmpty);
      expect(await store.getAttempts(), isEmpty);
    });
  });
}
