import 'dart:math';

import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

import '../models/attempt.dart';
import '../models/content_pack.dart';
import '../models/question.dart';
import '../models/session.dart';
import '../models/study_status.dart';

/// Thrown when a content pack is rejected because its version is lower than the
/// version already recorded in the local pack ledger.
class PackVersionTooLowException implements Exception {
  const PackVersionTooLowException();
}

/// Local SQLite persistence for offline-first study data.
///
/// Tests can inject an in-memory [Database] via [LocalStore.withDatabase].
/// For in-memory tests, call [LocalStore.createSchema] on the opened database
/// before constructing the store so tables exist.
class LocalStore {
  final Database? _testDb;
  Database? _db;

  LocalStore() : _testDb = null;

  LocalStore.withDatabase(Database db) : _testDb = db, _db = db;

  Future<Database> get database async => _testDb ?? (_db ??= await _initDb());

  // Column definitions are the single owner of the table shapes. A fresh
  // install and the migrations both derive from these lists, so a column can
  // never be added to one path and forgotten in the other.

  static const List<String> _questionsV1Columns = [
    'id TEXT PRIMARY KEY',
    'text TEXT NOT NULL',
    'options TEXT NOT NULL',
    'correctOptionIndex INTEGER NOT NULL',
    'explanation TEXT',
    'domain TEXT NOT NULL',
    'difficulty TEXT NOT NULL',
  ];

  static const List<String> _questionsV2Columns = [
    ..._questionsV1Columns,
    'source TEXT',
    'rightsBasis TEXT',
  ];

  static const List<String> _questionsV3Columns = [
    ..._questionsV2Columns,
    'packId TEXT',
    'courseId TEXT',
  ];

  static const List<String> _attemptsColumns = [
    'id INTEGER PRIMARY KEY AUTOINCREMENT',
    'questionId TEXT NOT NULL',
    'selectedOptionIndex INTEGER NOT NULL',
    'correct INTEGER NOT NULL',
    'timestamp INTEGER NOT NULL',
  ];

  static const List<String> _sessionsV1Columns = [
    'id TEXT PRIMARY KEY',
    'mode TEXT NOT NULL',
    'startedAt INTEGER NOT NULL',
    'finishedAt INTEGER NOT NULL',
    'questionCount INTEGER NOT NULL',
    'correctCount INTEGER NOT NULL',
    'scorePercent INTEGER',
  ];

  static const List<String> _sessionsV3Columns = [
    ..._sessionsV1Columns,
    'courseId TEXT',
  ];

  static const List<String> _packLedgerColumns = [
    'packId TEXT PRIMARY KEY',
    'version INTEGER NOT NULL',
    'appliedAt INTEGER NOT NULL',
  ];

  static const List<String> _settingsColumns = [
    'key TEXT PRIMARY KEY',
    'value TEXT',
  ];

  static Future<void> _createTable(
    Database db,
    String table,
    List<String> columns,
  ) async {
    await db.execute(
      'CREATE TABLE IF NOT EXISTS $table(${columns.join(', ')})',
    );
  }

  static Future<void> _addColumns(
    Database db,
    String table,
    List<String> columns,
  ) async {
    for (final column in columns) {
      await db.execute('ALTER TABLE $table ADD COLUMN $column');
    }
  }

  /// Creates the current (v4) schema for a fresh database.
  static Future<void> createSchema(Database db) async {
    await _createTable(db, 'questions', _questionsV3Columns);
    await _createTable(db, 'attempts', _attemptsColumns);
    await _createTable(db, 'sessions', _sessionsV3Columns);
    await _createTable(db, 'pack_ledger', _packLedgerColumns);
    await _createTable(db, 'settings', _settingsColumns);
    await db.execute('''
      CREATE TABLE IF NOT EXISTS study_status(
        courseId TEXT NOT NULL,
        questionId TEXT NOT NULL,
        status TEXT NOT NULL,
        updatedAt INTEGER NOT NULL,
        PRIMARY KEY (courseId, questionId)
      )
    ''');
  }

  /// Creates the original v1 schema without provenance, pack, or course
  /// columns.
  ///
  /// This helper exists only for migration testing; production code always
  /// uses [createSchema] for new databases.
  static Future<void> createV1Schema(Database db) async {
    await _createTable(db, 'questions', _questionsV1Columns);
    await _createTable(db, 'attempts', _attemptsColumns);
    await _createTable(db, 'sessions', _sessionsV1Columns);
  }

  /// Migrates an existing v1 database to v2, adding provenance columns.
  static Future<void> migrateV1ToV2(Database db) async {
    await _addColumns(
      db,
      'questions',
      _questionsV2Columns.sublist(_questionsV1Columns.length),
    );
  }

  /// Migrates an existing v2 database to v3, adding pack/course identity
  /// columns and the pack ledger and settings tables.
  static Future<void> migrateV2ToV3(Database db) async {
    await _addColumns(
      db,
      'questions',
      _questionsV3Columns.sublist(_questionsV2Columns.length),
    );
    await _addColumns(
      db,
      'sessions',
      _sessionsV3Columns.sublist(_sessionsV1Columns.length),
    );
    await _createTable(db, 'pack_ledger', _packLedgerColumns);
    await _createTable(db, 'settings', _settingsColumns);
  }

  /// Migrates an existing v3 database to v4, adding the per-course study
  /// status table.
  static Future<void> migrateV3ToV4(Database db) async {
    await db.execute('''
      CREATE TABLE IF NOT EXISTS study_status(
        courseId TEXT NOT NULL,
        questionId TEXT NOT NULL,
        status TEXT NOT NULL,
        updatedAt INTEGER NOT NULL,
        PRIMARY KEY (courseId, questionId)
      )
    ''');
  }

  static Future<Database> _initDb() async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, 'study_app.db');
    return openDatabase(
      path,
      version: 4,
      onCreate: (db, version) async => createSchema(db),
      onUpgrade: (db, oldVersion, newVersion) async {
        if (oldVersion < 2) {
          await migrateV1ToV2(db);
        }
        if (oldVersion < 3) {
          await migrateV2ToV3(db);
        }
        if (oldVersion < 4) {
          await migrateV3ToV4(db);
        }
      },
    );
  }

  Future<void> close() async {
    if (_testDb == null && _db != null) {
      await _db!.close();
      _db = null;
    }
  }

  /// Atomically applies a validated [ContentPack] to the question bank.
  ///
  /// The pack's previous rows (by `packId`) are replaced in full: questions
  /// present in the new pack version are inserted or updated, and questions
  /// dropped from a newer version are deleted. Attempt and session history is
  /// left untouched because those rows live in separate tables. Repeat calls
  /// with the same or a higher version are safe. A lower version than the one
  /// recorded in the pack ledger is rejected and leaves the bank unchanged.
  Future<void> applyContentPack(ContentPack pack) async {
    final db = await database;
    await db.transaction((txn) async {
      await applyContentPackToTransaction(txn, pack);
    });
  }

  /// Variant of [applyContentPack] that writes into an already-open
  /// [Transaction]. This is exposed for tests that want to verify rollback
  /// behavior. It also performs the pack-version ledger check and records the
  /// applied version inside the same transaction.
  Future<void> applyContentPackToTransaction(
    Transaction txn,
    ContentPack pack,
  ) async {
    final existing = await txn.query(
      'pack_ledger',
      where: 'packId = ?',
      whereArgs: [pack.packId],
      limit: 1,
    );
    if (existing.isNotEmpty) {
      final existingVersion = existing.first['version'] as int;
      if (pack.packVersion < existingVersion) {
        throw const PackVersionTooLowException();
      }
    }

    await txn.insert(
      'pack_ledger',
      {
        'packId': pack.packId,
        'version': pack.packVersion,
        'appliedAt': DateTime.now().millisecondsSinceEpoch,
      },
      conflictAlgorithm: ConflictAlgorithm.replace,
    );

    // Clear previously stored content-last-verified dates only for the courses
    // present in this pack, preserving dates for unrelated courses.
    final courseIds = pack.questions
        .map((q) => q.courseId)
        .where((c) => c.isNotEmpty)
        .toSet();
    if (courseIds.isNotEmpty) {
      await txn.delete(
        'settings',
        where:
            "key = 'contentLastVerifiedAt' OR "
            "key IN (${List.filled(courseIds.length, '?').join(',')})",
        whereArgs: courseIds.map((c) => 'contentLastVerifiedAt_$c').toList(),
      );
    } else {
      await txn.delete(
        'settings',
        where: "key = 'contentLastVerifiedAt'",
      );
    }

    // Replace this pack's existing rows inside the same transaction so a
    // question dropped from a newer pack version is removed from the bank
    // rather than left behind. This is pack-scoped replace-on-upgrade, not
    // withdrawal: the ledger entry above is kept.
    await txn.delete(
      'questions',
      where: 'packId = ?',
      whereArgs: [pack.packId],
    );

    // Record content-last-verified dates from the pack metadata. A per-course
    // date is recorded for every course present in the pack, plus a global date.
    if (pack.lastVerifiedAt != null && pack.lastVerifiedAt!.isNotEmpty) {
      final courseIds = pack.questions
          .map((q) => q.courseId)
          .where((c) => c.isNotEmpty)
          .toSet();
      await txn.insert(
        'settings',
        {'key': 'contentLastVerifiedAt', 'value': pack.lastVerifiedAt},
        conflictAlgorithm: ConflictAlgorithm.replace,
      );
      for (final courseId in courseIds) {
        await txn.insert(
          'settings',
          {
            'key': 'contentLastVerifiedAt_$courseId',
            'value': pack.lastVerifiedAt,
          },
          conflictAlgorithm: ConflictAlgorithm.replace,
        );
      }
    }

    final batch = txn.batch();
    for (final q in pack.questions) {
      batch.insert(
        'questions',
        q.toQuestion(packId: pack.packId).toMap(),
        conflictAlgorithm: ConflictAlgorithm.replace,
      );
    }
    await batch.commit(noResult: true);
  }

  /// Removes every question introduced by [packId] and deletes the ledger
  /// entry for that pack.
  ///
  /// Attempts and sessions are not touched, and questions from other packs
  /// remain in the bank.
  Future<void> withdrawPack(String packId) async {
    final db = await database;
    await db.transaction((txn) async {
      await txn.delete(
        'questions',
        where: 'packId = ?',
        whereArgs: [packId],
      );
      await txn.delete(
        'pack_ledger',
        where: 'packId = ?',
        whereArgs: [packId],
      );
    });
  }

  /// Returns the version last recorded for [packId], or null if the pack has
  /// never been applied or has been withdrawn.
  Future<int?> getAppliedPackVersion(String packId) async {
    final db = await database;
    final rows = await db.query(
      'pack_ledger',
      where: 'packId = ?',
      whereArgs: [packId],
      limit: 1,
    );
    if (rows.isEmpty) return null;
    return rows.first['version'] as int?;
  }

  /// Returns the last content-verified date recorded for [courseId], or the
  /// global date when [courseId] is omitted.
  Future<String?> getContentLastVerifiedAt({String? courseId}) async {
    final db = await database;
    final key = courseId == null
        ? 'contentLastVerifiedAt'
        : 'contentLastVerifiedAt_$courseId';
    final rows = await db.query(
      'settings',
      where: 'key = ?',
      whereArgs: [key],
      limit: 1,
    );
    if (rows.isEmpty) return null;
    final value = rows.first['value'] as String?;
    if (value == null || value.isEmpty) return null;
    return value;
  }

  Future<void> insertQuestions(List<Question> questions) async {
    final db = await database;
    final batch = db.batch();
    for (final q in questions) {
      batch.insert('questions', q.toMap(),
          conflictAlgorithm: ConflictAlgorithm.replace);
    }
    await batch.commit(noResult: true);
  }

  /// All questions, optionally filtered to a single course.
  Future<List<Question>> getQuestions({String? courseId}) async {
    final db = await database;
    final rows = courseId == null
        ? await db.query('questions')
        : await db.query(
            'questions',
            where: 'courseId = ?',
            whereArgs: [courseId],
          );
    return rows.map(Question.fromMap).toList();
  }

  Future<Question?> getQuestion(String id) async {
    final db = await database;
    final rows = await db.query(
      'questions',
      where: 'id = ?',
      whereArgs: [id],
      limit: 1,
    );
    if (rows.isEmpty) return null;
    return Question.fromMap(rows.first);
  }

  /// Returns the distinct course identifiers currently present in the bank,
  /// in ascending order.
  Future<List<String>> getCourses() async {
    final db = await database;
    final rows = await db.rawQuery(
      "SELECT DISTINCT courseId FROM questions "
      "WHERE courseId IS NOT NULL AND courseId != '' "
      "ORDER BY courseId",
    );
    return rows.map((r) => r['courseId'] as String).toList();
  }

  /// Returns the learner-selected course, or null when no course is selected.
  ///
  /// A stored id whose course is no longer in the bank (its pack was withdrawn
  /// or replaced) is cleared here, so the dropdown and every other consumer
  /// read the same selection instead of filtering to a course that has no
  /// content.
  Future<String?> getSelectedCourseId() async {
    final db = await database;
    final rows = await db.query(
      'settings',
      where: "key = 'selectedCourseId'",
      limit: 1,
    );
    if (rows.isEmpty) return null;
    final value = rows.first['value'] as String?;
    if (value == null || value.isEmpty) return null;
    final courses = await getCourses();
    if (!courses.contains(value)) {
      await setSelectedCourseId(null);
      return null;
    }
    return value;
  }

  /// Stores or clears the learner-selected course.
  Future<void> setSelectedCourseId(String? courseId) async {
    final db = await database;
    await db.insert(
      'settings',
      {'key': 'selectedCourseId', 'value': courseId ?? ''},
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  /// Persist the learner's study status for a single question.
  Future<void> saveStudyStatus({
    required String courseId,
    required String questionId,
    required StudyMaterialStatus status,
    DateTime? updatedAt,
  }) async {
    final db = await database;
    final record = StudyStatusRecord(
      courseId: courseId,
      questionId: questionId,
      status: status,
      updatedAt: updatedAt ?? DateTime.now(),
    );
    await db.insert(
      'study_status',
      record.toMap(),
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  /// Load all study statuses for a course, keyed by question id.
  Future<Map<String, StudyMaterialStatus>> getStudyStatusesForCourse(
      String courseId) async {
    final db = await database;
    final rows = await db.query(
      'study_status',
      where: 'courseId = ?',
      whereArgs: [courseId],
    );
    return {
      for (final row in rows)
        row['questionId'] as String:
            StudyMaterialStatusX.fromStorage(row['status'] as String),
    };
  }

  Future<void> recordAttempt(Attempt attempt) async {
    final db = await database;
    await db.insert('attempts', attempt.toMap());
  }

  Future<List<Attempt>> getAttemptsFor(String questionId) async {
    final db = await database;
    final rows = await db.query(
      'attempts',
      where: 'questionId = ?',
      whereArgs: [questionId],
      orderBy: 'timestamp DESC',
    );
    return rows.map(Attempt.fromMap).toList();
  }

  /// All recorded attempts, optionally filtered to a single course by joining
  /// with the current question bank.
  ///
  /// Rows that cannot be attributed to any course - a question with no
  /// `courseId`, or a question whose pack has been withdrawn - belong to every
  /// course scope, so selecting a course never hides earlier history.
  Future<List<Attempt>> getAttempts({String? courseId}) async {
    final db = await database;
    final rows = courseId == null
        ? await db.query('attempts', orderBy: 'timestamp DESC')
        : await db.rawQuery(
            '''
            SELECT a.* FROM attempts a
            LEFT JOIN questions q ON q.id = a.questionId
            WHERE q.courseId = ? OR q.courseId IS NULL
            ORDER BY a.timestamp DESC
            ''',
            [courseId],
          );
    return rows.map(Attempt.fromMap).toList();
  }

  Future<void> saveSession(StudySession session) async {
    final db = await database;
    await db.insert(
      'sessions',
      session.toMap(),
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
  }

  /// Sessions, optionally filtered by mode and course.
  ///
  /// Sessions without a `courseId` - every session recorded before courses
  /// existed - belong to every course scope.
  Future<List<StudySession>> getSessions({String? mode, String? courseId}) async {
    final db = await database;
    final conditions = <String>[];
    final whereArgs = <Object?>[];
    if (mode != null) {
      conditions.add('mode = ?');
      whereArgs.add(mode);
    }
    if (courseId != null) {
      conditions.add('(courseId = ? OR courseId IS NULL)');
      whereArgs.add(courseId);
    }
    final rows = conditions.isEmpty
        ? await db.query('sessions', orderBy: 'finishedAt DESC')
        : await db.query(
            'sessions',
            where: conditions.join(' AND '),
            whereArgs: whereArgs,
            orderBy: 'finishedAt DESC',
          );
    return rows.map(StudySession.fromMap).toList();
  }

  /// Build review items for questions that are due now or have never been seen,
  /// optionally scoped to a single course.
  Future<List<ReviewItem>> getDueReviewItems({String? courseId}) async {
    final questions = await getQuestions(courseId: courseId);
    if (questions.isEmpty) return const [];

    final now = DateTime.now();
    final List<ReviewItem> due = [];

    for (final q in questions) {
      final attempts = await getAttemptsFor(q.id);
      if (attempts.isEmpty) {
        due.add(ReviewItem(
          question: q,
          nextReview: now,
          consecutiveCorrect: 0,
        ));
        continue;
      }
      final last = attempts.first;
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
    // Reset interval after a wrong answer.
    if (!lastCorrect) return const Duration(minutes: 1);
    const baseMinutes = [1, 10, 60, 240, 1440, 4320, 10080]; // 1m,10m,1h,4h,1d,3d,7d
    final idx = min(consecutiveCorrect, baseMinutes.length - 1);
    return Duration(minutes: baseMinutes[idx]);
  }

  Future<void> clearAllData() async {
    final db = await database;
    await db.delete('questions');
    await db.delete('attempts');
    await db.delete('sessions');
    await db.delete('pack_ledger');
    await db.delete('settings');
    await db.delete('study_status');
  }
}
