import 'dart:math';

import 'package:sqflite_common_ffi/sqflite_ffi.dart';

import 'package:study_app/data/local_store.dart';
import 'package:study_app/data/question_bank.dart';
import 'package:study_app/models/attempt.dart';
import 'package:study_app/models/content_pack.dart';
import 'package:study_app/models/question.dart';
import 'package:study_app/models/session.dart';
import 'package:study_app/models/study_status.dart';

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
  final Map<String, int> _packVersions = {};
  final Map<String, String?> _settings = {};
  String? _selectedCourseId;
  final Map<String, Map<String, StudyMaterialStatus>> _studyStatuses = {};

  FakeLocalStore([List<Question>? questions]) {
    if (questions != null) _questions.addAll(questions);
  }

  @override
  Future<void> applyContentPack(ContentPack pack) async {
    final existing = _packVersions[pack.packId];
    if (existing != null && pack.packVersion < existing) {
      throw const PackVersionTooLowException();
    }
    _packVersions[pack.packId] = pack.packVersion;

    // Clear content-last-verified dates only for the courses this pack touches.
    final courseIds = pack.questions
        .map((q) => q.courseId)
        .where((c) => c.isNotEmpty)
        .toSet();
    _settings.remove('contentLastVerifiedAt');
    for (final courseId in courseIds) {
      _settings.remove('contentLastVerifiedAt_$courseId');
    }

    // Mirror production: replace this pack's rows in full so questions
    // dropped from a newer version are removed.
    _questions.removeWhere((q) => q.packId == pack.packId);

    if (pack.lastVerifiedAt != null && pack.lastVerifiedAt!.isNotEmpty) {
      _settings['contentLastVerifiedAt'] = pack.lastVerifiedAt;
      for (final courseId in courseIds) {
        _settings['contentLastVerifiedAt_$courseId'] = pack.lastVerifiedAt;
      }
    }
    for (final q in pack.questions) {
      _questions.add(q.toQuestion(packId: pack.packId));
    }
  }

  @override
  Future<void> applyContentPackToTransaction(
    Transaction txn,
    ContentPack pack,
  ) async => applyContentPack(pack);

  @override
  Future<void> close() async {}

  @override
  Future<void> insertQuestions(List<Question> questions) async {
    _questions.addAll(questions);
  }

  @override
  Future<List<Question>> getQuestions({String? courseId}) async {
    var result = List<Question>.from(_questions);
    if (courseId != null) {
      result = result.where((q) => q.courseId == courseId).toList();
    }
    return List.unmodifiable(result);
  }

  @override
  Future<Question?> getQuestion(String id) async {
    try {
      return _questions.firstWhere((q) => q.id == id);
    } on StateError {
      return null;
    }
  }

  @override
  Future<List<String>> getCourses() async {
    final ids = _questions
        .map((q) => q.courseId)
        .where((c) => c != null && c.isNotEmpty)
        .cast<String>()
        .toSet()
        .toList();
    ids.sort();
    return ids;
  }

  @override
  Future<String?> getSelectedCourseId() async {
    final courses = await getCourses();
    if (_selectedCourseId != null && !courses.contains(_selectedCourseId)) {
      _selectedCourseId = null;
    }
    return _selectedCourseId;
  }

  @override
  Future<void> setSelectedCourseId(String? courseId) async {
    _selectedCourseId = courseId;
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
  Future<List<Attempt>> getAttempts({String? courseId}) async {
    var result = List<Attempt>.from(_attempts);
    if (courseId != null) {
      result = result.where((a) => a.courseId == courseId || a.courseId == null).toList();
    }
    return List.unmodifiable(result.reversed.toList());
  }

  @override
  Future<void> saveSession(StudySession session) async => _sessions.add(session);

  @override
  Future<List<StudySession>> getSessions({String? mode, String? courseId}) async {
    var result = List<StudySession>.from(_sessions);
    if (mode != null) {
      result = result.where((s) => s.mode == mode).toList();
    }
    if (courseId != null) {
      result = result
          .where((s) => s.courseId == courseId || s.courseId == null)
          .toList();
    }
    result.sort((a, b) => b.finishedAt.compareTo(a.finishedAt));
    return List.unmodifiable(result);
  }

  @override
  Future<void> saveStudyStatus({
    required String courseId,
    required String questionId,
    required StudyMaterialStatus status,
    DateTime? updatedAt,
  }) async {
    _studyStatuses.putIfAbsent(courseId, () => {});
    _studyStatuses[courseId]![questionId] = status;
  }

  @override
  Future<Map<String, StudyMaterialStatus>> getStudyStatusesForCourse(
      String courseId) async {
    final statuses = _studyStatuses[courseId];
    if (statuses == null) return const {};
    return Map.unmodifiable(statuses);
  }

  @override
  Future<List<ReviewItem>> getDueReviewItems({String? courseId}) async {
    final now = DateTime.now();
    final List<ReviewItem> due = [];
    final questions = await getQuestions(courseId: courseId);
    for (final q in questions) {
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
  Future<String?> getContentLastVerifiedAt({String? courseId}) async {
    final key = courseId == null
        ? 'contentLastVerifiedAt'
        : 'contentLastVerifiedAt_$courseId';
    return _settings[key];
  }

  @override
  Future<void> clearAllData() async {
    _questions.clear();
    _attempts.clear();
    _sessions.clear();
    _packVersions.clear();
    _settings.clear();
    _selectedCourseId = null;
    _studyStatuses.clear();
  }
}
