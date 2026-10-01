import 'dart:math';

import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

import '../models/attempt.dart';
import '../models/content_pack.dart';
import '../models/question.dart';
import '../models/session.dart';

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

  static Future<void> createSchema(Database db) async {
    await db.execute('''
      CREATE TABLE IF NOT EXISTS questions(
        id TEXT PRIMARY KEY,
        text TEXT NOT NULL,
        options TEXT NOT NULL,
        correctOptionIndex INTEGER NOT NULL,
        explanation TEXT,
        domain TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        source TEXT,
        rightsBasis TEXT
      )
    ''');
    await db.execute('''
      CREATE TABLE IF NOT EXISTS attempts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        questionId TEXT NOT NULL,
        selectedOptionIndex INTEGER NOT NULL,
        correct INTEGER NOT NULL,
        timestamp INTEGER NOT NULL
      )
    ''');
    await db.execute('''
      CREATE TABLE IF NOT EXISTS sessions(
        id TEXT PRIMARY KEY,
        mode TEXT NOT NULL,
        startedAt INTEGER NOT NULL,
        finishedAt INTEGER NOT NULL,
        questionCount INTEGER NOT NULL,
        correctCount INTEGER NOT NULL,
        scorePercent INTEGER
      )
    ''');
  }

  /// Creates the original v1 schema without provenance columns.
  ///
  /// This helper exists only for migration testing; production code always
  /// uses [createSchema] for new databases.
  static Future<void> createV1Schema(Database db) async {
    await db.execute('''
      CREATE TABLE IF NOT EXISTS questions(
        id TEXT PRIMARY KEY,
        text TEXT NOT NULL,
        options TEXT NOT NULL,
        correctOptionIndex INTEGER NOT NULL,
        explanation TEXT,
        domain TEXT NOT NULL,
        difficulty TEXT NOT NULL
      )
    ''');
    await db.execute('''
      CREATE TABLE IF NOT EXISTS attempts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        questionId TEXT NOT NULL,
        selectedOptionIndex INTEGER NOT NULL,
        correct INTEGER NOT NULL,
        timestamp INTEGER NOT NULL
      )
    ''');
    await db.execute('''
      CREATE TABLE IF NOT EXISTS sessions(
        id TEXT PRIMARY KEY,
        mode TEXT NOT NULL,
        startedAt INTEGER NOT NULL,
        finishedAt INTEGER NOT NULL,
        questionCount INTEGER NOT NULL,
        correctCount INTEGER NOT NULL,
        scorePercent INTEGER
      )
    ''');
  }

  /// Migrates an existing v1 database to v2, adding provenance columns.
  static Future<void> migrateV1ToV2(Database db) async {
    await db.execute('ALTER TABLE questions ADD COLUMN source TEXT');
    await db.execute('ALTER TABLE questions ADD COLUMN rightsBasis TEXT');
  }

  static Future<Database> _initDb() async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, 'study_app.db');
    return openDatabase(
      path,
      version: 2,
      onCreate: (db, version) async => createSchema(db),
      onUpgrade: (db, oldVersion, newVersion) async {
        if (oldVersion < 2) {
          await migrateV1ToV2(db);
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
  /// Existing questions with the same id are replaced, but attempt and session
  /// history is left untouched because those rows live in separate tables.
  /// Repeat calls with the same pack are safe.
  Future<void> applyContentPack(ContentPack pack) async {
    final db = await database;
    await db.transaction((txn) async {
      await applyContentPackToTransaction(txn, pack);
    });
  }

  /// Variant of [applyContentPack] that writes into an already-open
  /// [Transaction]. This is exposed for tests that want to verify rollback
  /// behavior.
  Future<void> applyContentPackToTransaction(
    Transaction txn,
    ContentPack pack,
  ) async {
    final batch = txn.batch();
    for (final q in pack.questions) {
      batch.insert(
        'questions',
        q.toQuestion().toMap(),
        conflictAlgorithm: ConflictAlgorithm.replace,
      );
    }
    await batch.commit(noResult: true);
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

  Future<List<Question>> getAllQuestions() async {
    final db = await database;
    final rows = await db.query('questions');
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

  Future<List<Attempt>> getAllAttempts() async {
    final db = await database;
    final rows = await db.query('attempts', orderBy: 'timestamp DESC');
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

  Future<List<StudySession>> getSessions({String? mode}) async {
    final db = await database;
    final rows = mode == null
        ? await db.query('sessions', orderBy: 'finishedAt DESC')
        : await db.query(
            'sessions',
            where: 'mode = ?',
            whereArgs: [mode],
            orderBy: 'finishedAt DESC',
          );
    return rows.map(StudySession.fromMap).toList();
  }

  /// Build review items for questions that are due now or have never been seen.
  Future<List<ReviewItem>> getDueReviewItems() async {
    final questions = await getAllQuestions();
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
  }
}
