import 'dart:math';

import 'package:sqflite_common_ffi/sqflite_ffi.dart';

import 'package:study_app/data/local_store.dart';
import 'package:study_app/data/question_bank.dart';
import 'package:study_app/models/attempt.dart';
import 'package:study_app/models/question.dart';
import 'package:study_app/models/session.dart';

/// Initializes the FFI sqlite implementation used by unit/integration tests on
/// desktop/WSL Linux where the mobile sqflite implementation is unavailable.
///
/// Note: sqflite_common_ffi cannot be exercised inside widget tests because the
/// Flutter test binding's fake async/clock deadlocks the FFI isolate. Widget
/// tests use [FakeLocalStore] instead.
void initTestDatabase() {
  sqfliteFfiInit();
  databaseFactory = databaseFactoryFfi;
}

/// Opens an in-memory database with the study app schema created.
Future<Database> openTestDatabase() async {
  final db = await openDatabase(
    inMemoryDatabasePath,
    singleInstance: false,
  );
  await LocalStore.createSchema(db);
  return db;
}

/// Returns a LocalStore backed by an in-memory FFI database seeded with
/// synthetic test fixtures.
Future<LocalStore> seededStore() async {
  final db = await openTestDatabase();
  final store = LocalStore.withDatabase(db);
  await store.insertQuestions(QuestionBank.syntheticFixtures());
  return store;
}

/// In-memory, synchronous implementation of [LocalStore] for widget tests.
///
/// This avoids the sqflite FFI isolate that hangs under the Flutter test
/// binding's fake async. It keeps the same public API so screens can consume
/// it through [Provider].
class FakeLocalStore extends LocalStore {
  final List<Question> _questions = [];
  final List<Attempt> _attempts = [];
  final List<StudySession> _sessions = [];

  FakeLocalStore([List<Question>? questions]) {
    if (questions != null) _questions.addAll(questions);
  }

  @override
  Future<void> close() async {}

  @override
  Future<void> insertQuestions(List<Question> questions) async {
    _questions.addAll(questions);
  }

  @override
  Future<List<Question>> getAllQuestions() async => List.unmodifiable(_questions);

  @override
  Future<Question?> getQuestion(String id) async {
    try {
      return _questions.firstWhere((q) => q.id == id);
    } on StateError {
      return null;
    }
  }

  @override
  Future<void> recordAttempt(Attempt attempt) async => _attempts.add(attempt);

  @override
  Future<List<Attempt>> getAttemptsFor(String questionId) async =>
      _attempts
          .where((a) => a.questionId == questionId)
          .toList()
          .reversed
          .toList();

  @override
  Future<List<Attempt>> getAllAttempts() async =>
      List.unmodifiable(_attempts.reversed.toList());

  @override
  Future<void> saveSession(StudySession session) async =>
      _sessions.add(session);

  @override
  Future<List<StudySession>> getSessions({String? mode}) async {
    var result = List<StudySession>.from(_sessions);
    if (mode != null) {
      result = result.where((s) => s.mode == mode).toList();
    }
    result.sort((a, b) => b.finishedAt.compareTo(a.finishedAt));
    return List.unmodifiable(result);
  }

  @override
  Future<List<ReviewItem>> getDueReviewItems() async {
    final now = DateTime.now();
    final List<ReviewItem> due = [];
    for (final q in _questions) {
      final attempts = (await getAttemptsFor(q.id)).reversed.toList();
      if (attempts.isEmpty) {
        due.add(ReviewItem(question: q, nextReview: now, consecutiveCorrect: 0));
        continue;
      }
      final last = attempts.last;
      final consecutiveCorrect = _consecutiveCorrectCount(attempts);
      final interval = _nextReviewInterval(consecutiveCorrect, last.correct);
      final nextReview = last.timestamp.add(interval);
      if (!nextReview.isAfter(now)) {
        due.add(ReviewItem(
          question: q,
          nextReview: nextReview,
          consecutiveCorrect: consecutiveCorrect,
        ));
      }
    }
    return due;
  }

  int _consecutiveCorrectCount(List<Attempt> attempts) {
    int count = 0;
    for (final a in attempts) {
      if (a.correct) {
        count++;
      } else {
        break;
      }
    }
    return count;
  }

  Duration _nextReviewInterval(int consecutiveCorrect, bool lastCorrect) {
    if (!lastCorrect) return const Duration(minutes: 1);
    const baseMinutes = [1, 10, 60, 240, 1440, 4320, 10080];
    final idx = min(consecutiveCorrect, baseMinutes.length - 1);
    return Duration(minutes: baseMinutes[idx]);
  }

  @override
  Future<void> clearAllData() async {
    _questions.clear();
    _attempts.clear();
    _sessions.clear();
  }
}
