import 'dart:convert';

import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import 'package:sqflite_common_ffi/sqflite_ffi.dart';
import 'package:study_app/data/content_pack_loader.dart';
import 'package:study_app/data/local_store.dart';
import 'package:study_app/models/attempt.dart';
import 'package:study_app/models/content_pack.dart';
import 'package:study_app/models/question.dart';
import 'package:study_app/models/session.dart';

import 'test_helpers.dart';

String _packJson({
  required String packId,
  required int packVersion,
  required String courseId,
  required List<String> questionIds,
}) {
  final questions = questionIds.map((id) => <String, Object?>{
    'id': id,
    'text': 'Question $id',
    'options': <String>['A', 'B'],
    'correctOptionIndex': 0,
    'explanation': 'A is correct.',
    'domain': 'Domain',
    'difficulty': 'easy',
    'source': 'Test fixture',
    'rightsBasis': 'original-human',
    'courseId': courseId,

  return '''
  {
    "formatVersion": "azpack-v2",
    "packId": "$packId",
    "packVersion": $packVersion,
    "title": "Test pack",
    "source": "Test fixture",
    "rightsBasis": "original-human",
    "questions": ${jsonEncode(questions)}
  }
  ''';
}

void main() {
  setUpAll(initTestDatabase);

  group('Course dimension', () {
    late LocalStore store;

    setUp(() async {
      final db = await openTestDatabase();
      store = LocalStore.withDatabase(db);
    });

    tearDown(() async {
      await store.close();
    });

    test('pack questions carry packId and courseId into the bank', () async {
      final pack = ContentPack.parse(_packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'az-900',
        questionIds: ['q-a1'],
      ));
      await store.applyContentPack(pack);

      final question = await store.getQuestion('q-a1');
      expect(question, isNotNull);
      expect(question!.packId, 'pack-a');
      expect(question.courseId, 'az-900');
    });

    test('banks for different courses are disjoint', () async {
      final packA = ContentPack.parse(_packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'az-900',
        questionIds: ['q-a1', 'q-a2'],
      ));
      final packB = ContentPack.parse(_packJson(
        packId: 'pack-b',
        packVersion: 1,
        courseId: 'sc-900',
        questionIds: ['q-b1'],
      ));
      await store.applyContentPack(packA);
      await store.applyContentPack(packB);

      final courses = await store.getCourses();
      expect(courses, ['az-900', 'sc-900']);

      final aQuestions = await store.getQuestions(courseId: 'az-900');
      final bQuestions = await store.getQuestions(courseId: 'sc-900');
      expect(aQuestions.map((q) => q.id), containsAll(['q-a1', 'q-a2']));
      expect(bQuestions.map((q) => q.id), ['q-b1']);
      expect(
        aQuestions.map((q) => q.id),
        isNot(contains('q-b1')),
      );
    });

    test('attempts and sessions are scoped per selected course', () async {
      final packA = ContentPack.parse(_packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'az-900',
        questionIds: ['q-a1'],
      ));
      final packB = ContentPack.parse(_packJson(
        packId: 'pack-b',
        packVersion: 1,
        courseId: 'sc-900',
        questionIds: ['q-b1'],
      ));
      await store.applyContentPack(packA);
      await store.applyContentPack(packB);

      await store.recordAttempt(Attempt(
        questionId: 'q-a1',
        selectedOptionIndex: 0,
        correct: true,
        timestamp: DateTime.now(),
      ));
      await store.recordAttempt(Attempt(
        questionId: 'q-b1',
        selectedOptionIndex: 0,
        correct: false,
        timestamp: DateTime.now(),
      ));
      await store.saveSession(StudySession(
        id: 's-a',
        mode: 'exam',
        courseId: 'az-900',
        startedAt: DateTime.now().subtract(const Duration(minutes: 1)),
        finishedAt: DateTime.now(),
        questionCount: 1,
        correctCount: 1,
        scorePercent: 100,
      ));
      await store.saveSession(StudySession(
        id: 's-b',
        mode: 'exam',
        courseId: 'sc-900',
        startedAt: DateTime.now().subtract(const Duration(minutes: 1)),
        finishedAt: DateTime.now(),
        questionCount: 1,
        correctCount: 0,
        scorePercent: 0,
      ));

      final aAttempts = await store.getAttempts(courseId: 'az-900');
      final bAttempts = await store.getAttempts(courseId: 'sc-900');
      expect(aAttempts.map((a) => a.questionId), ['q-a1']);
      expect(bAttempts.map((a) => a.questionId), ['q-b1']);

      final aSessions = await store.getSessions(courseId: 'az-900');
      final bSessions = await store.getSessions(courseId: 'sc-900');
      expect(aSessions.map((s) => s.id), ['s-a']);
      expect(bSessions.map((s) => s.id), ['s-b']);
    });

    test('course-scoped history keeps rows without course attribution',
        () async {
      final packA = ContentPack.parse(_packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'course-A',
        questionIds: ['q-a1'],
      ));
      final packB = ContentPack.parse(_packJson(
        packId: 'pack-b',
        packVersion: 1,
        courseId: 'course-B',
        questionIds: ['q-b1'],
      ));
      await store.applyContentPack(packA);
      await store.applyContentPack(packB);

      final base = DateTime(2026, 10, 2);
      Attempt attempt(String id, int minutes) => Attempt(
            questionId: id,
            selectedOptionIndex: 0,
            correct: true,
            timestamp: base.add(Duration(minutes: minutes)),
          );
      StudySession session(String id, String? courseId) => StudySession(
            id: id,
            mode: 'exam',
            courseId: courseId,
            startedAt: base,
            finishedAt: base,
            questionCount: 1,
            correctCount: 1,
            scorePercent: 100,
          );

      await store.recordAttempt(attempt('q-a1', 1));
      await store.recordAttempt(attempt('q-b1', 2));
      // Recorded before questions carried a course id, or against a question
      // the current bank no longer holds.
      await store.recordAttempt(attempt('pre-course-q1', 3));
      await store.saveSession(session('s-a', 'course-A'));
      await store.saveSession(session('s-b', 'course-B'));
      await store.saveSession(session('s-all', null));

      final aAttempts = await store.getAttempts(courseId: 'course-A');
      final bAttempts = await store.getAttempts(courseId: 'course-B');
      expect(aAttempts.map((a) => a.questionId).toSet(),
          {'q-a1', 'pre-course-q1'});
      expect(bAttempts.map((a) => a.questionId).toSet(),
          {'q-b1', 'pre-course-q1'});

      final aSessions = await store.getSessions(courseId: 'course-A');
      final bSessions = await store.getSessions(courseId: 'course-B');
      expect(aSessions.map((s) => s.id).toSet(), {'s-a', 's-all'});
      expect(bSessions.map((s) => s.id).toSet(), {'s-b', 's-all'});
    });

    test('review items are filtered by selected course', () async {
      final packA = ContentPack.parse(_packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'az-900',
        questionIds: ['q-a1'],
      ));
      final packB = ContentPack.parse(_packJson(
        packId: 'pack-b',
        packVersion: 1,
        courseId: 'sc-900',
        questionIds: ['q-b1'],
      ));
      await store.applyContentPack(packA);
      await store.applyContentPack(packB);

      final aDue = await store.getDueReviewItems(courseId: 'az-900');
      final bDue = await store.getDueReviewItems(courseId: 'sc-900');
      expect(aDue.map((i) => i.question.id), ['q-a1']);
      expect(bDue.map((i) => i.question.id), ['q-b1']);
    });

    test('selected course is persisted', () async {
      await store.applyContentPack(ContentPack.parse(_packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'course-A',
        questionIds: ['q-a1'],
      )));
      expect(await store.getSelectedCourseId(), isNull);
      await store.setSelectedCourseId('az-900');
      expect(await store.getSelectedCourseId(), 'az-900');
      await store.setSelectedCourseId(null);
      expect(await store.getSelectedCourseId(), isNull);
    });

    test('a selection whose course is withdrawn is cleared', () async {
      await store.applyContentPack(ContentPack.parse(_packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'course-A',
        questionIds: ['q-a1'],
      )));
      await store.applyContentPack(ContentPack.parse(_packJson(
        packId: 'pack-b',
        packVersion: 1,
        courseId: 'course-B',
        questionIds: ['q-b1'],
      )));
      await store.setSelectedCourseId('course-A');
      expect(await store.getSelectedCourseId(), 'course-A');

      await store.withdrawPack('pack-a');

      expect(await store.getSelectedCourseId(), isNull);
      final effective = await store.getSelectedCourseId();
      expect(await store.getQuestions(courseId: effective), hasLength(1));
    });

    test('history without course attribution stays visible in every course',
        () async {
      await store.applyContentPack(ContentPack.parse(_packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'course-A',
        questionIds: ['q-a1'],
      )));
      await store.applyContentPack(ContentPack.parse(_packJson(
        packId: 'pack-b',
        packVersion: 1,
        courseId: 'course-B',
        questionIds: ['q-b1'],
      )));

      // A question from before courses existed, plus its attempt and session.
      await store.insertQuestions(const [
        Question(
          id: 'legacy-001',
          text: 'Legacy question',
          options: ['A', 'B'],
          correctOptionIndex: 0,
          explanation: 'A is correct.',
          domain: 'Legacy',
          difficulty: 'easy',
        ),
      ]);
      await store.recordAttempt(Attempt(
        questionId: 'legacy-001',
        selectedOptionIndex: 0,
        correct: true,
        timestamp: DateTime.now(),
      ));
      await store.recordAttempt(Attempt(
        questionId: 'q-a1',
        selectedOptionIndex: 0,
        correct: true,
        timestamp: DateTime.now(),
      ));
      await store.recordAttempt(Attempt(
        questionId: 'q-b1',
        selectedOptionIndex: 0,
        correct: false,
        timestamp: DateTime.now(),
      ));
      await store.saveSession(StudySession(
        id: 'legacy-session',
        mode: 'exam',
        startedAt: DateTime.now().subtract(const Duration(minutes: 1)),
        finishedAt: DateTime.now(),
        questionCount: 1,
        correctCount: 1,
        scorePercent: 100,
      ));
      await store.saveSession(StudySession(
        id: 'b-session',
        mode: 'exam',
        courseId: 'course-B',
        startedAt: DateTime.now().subtract(const Duration(minutes: 1)),
        finishedAt: DateTime.now(),
        questionCount: 1,
        correctCount: 0,
        scorePercent: 0,
      ));

      final aAttempts = await store.getAttempts(courseId: 'course-A');
      final bAttempts = await store.getAttempts(courseId: 'course-B');
      expect(aAttempts.map((a) => a.questionId),
          containsAll(['legacy-001', 'q-a1']));
      expect(aAttempts.map((a) => a.questionId), isNot(contains('q-b1')));
      expect(bAttempts.map((a) => a.questionId),
          containsAll(['legacy-001', 'q-b1']));
      expect(bAttempts.map((a) => a.questionId), isNot(contains('q-a1')));

      expect(
        (await store.getSessions(courseId: 'course-A')).map((s) => s.id),
        ['legacy-session'],
      );
      expect(
        (await store.getSessions(courseId: 'course-B')).map((s) => s.id),
        containsAll(['legacy-session', 'b-session']),
      );
    });
  });

  group('Pack version ledger', () {
    late LocalStore store;

    setUp(() async {
      final db = await openTestDatabase();
      store = LocalStore.withDatabase(db);
    });

    tearDown(() async {
      await store.close();
    });

    test('records applied pack version', () async {
      final pack = ContentPack.parse(_packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'az-900',
        questionIds: ['q-a1'],
      ));
      await store.applyContentPack(pack);
      expect(await store.getAppliedPackVersion('pack-a'), 1);
    });

    test('upgrade applies and updates ledger', () async {
      final v1 = ContentPack.parse(_packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'az-900',
        questionIds: ['q-a1'],
      ));
      final v2Json = _packJson(
        packId: 'pack-a',
        packVersion: 2,
        courseId: 'az-900',
        questionIds: ['q-a1', 'q-a2'],
      );
      final v2 = ContentPack.parse(v2Json);

      await store.applyContentPack(v1);
      await store.applyContentPack(v2);

      expect(await store.getAppliedPackVersion('pack-a'), 2);
      final questions = await store.getQuestions();
      expect(questions.map((q) => q.id), containsAll(['q-a1', 'q-a2']));
    });

    test('equal version is idempotent', () async {
      final pack = ContentPack.parse(_packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'az-900',
        questionIds: ['q-a1'],
      ));
      await store.applyContentPack(pack);
      await store.applyContentPack(pack);
      expect(await store.getAppliedPackVersion('pack-a'), 1);
      expect(await store.getQuestions(), hasLength(1));
    });

    test('downgrade is rejected and leaves content unchanged', () async {
      final v2Json = _packJson(
        packId: 'pack-a',
        packVersion: 2,
        courseId: 'az-900',
        questionIds: ['q-a1', 'q-a2'],
      );
      final v1Json = _packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'az-900',
        questionIds: ['q-a1'],
      );

      final successV2 =
          await ContentPackLoader.loadPackFromString(store, v2Json);
      expect(successV2, isTrue);
      expect(await store.getQuestions(), hasLength(2));

      final successV1 =
          await ContentPackLoader.loadPackFromString(store, v1Json);
      expect(successV1, isFalse);
      expect(await store.getAppliedPackVersion('pack-a'), 2);
      expect(await store.getQuestions(), hasLength(2));
    });
  });

  group('Per-pack withdrawal', () {
    late LocalStore store;

    setUp(() async {
      final db = await openTestDatabase();
      store = LocalStore.withDatabase(db);
    });

    tearDown(() async {
      await store.close();
    });

    test('withdraws exactly one pack, preserving history and other courses',
        () async {
      final packA = ContentPack.parse(_packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'az-900',
        questionIds: ['q-a1'],
      ));
      final packB = ContentPack.parse(_packJson(
        packId: 'pack-b',
        packVersion: 1,
        courseId: 'sc-900',
        questionIds: ['q-b1'],
      ));
      await store.applyContentPack(packA);
      await store.applyContentPack(packB);

      await store.recordAttempt(Attempt(
        questionId: 'q-a1',
        selectedOptionIndex: 0,
        correct: true,
        timestamp: DateTime.now(),
      ));
      await store.recordAttempt(Attempt(
        questionId: 'q-b1',
        selectedOptionIndex: 0,
        correct: false,
        timestamp: DateTime.now(),
      ));
      await store.saveSession(StudySession(
        id: 's-1',
        mode: 'exam',
        courseId: 'az-900',
        startedAt: DateTime.now().subtract(const Duration(minutes: 1)),
        finishedAt: DateTime.now(),
        questionCount: 1,
        correctCount: 1,
        scorePercent: 100,
      ));

      await store.withdrawPack('pack-a');

      expect(await store.getAppliedPackVersion('pack-a'), isNull);
      final remaining = await store.getQuestions();
      expect(remaining.map((q) => q.id), ['q-b1']);
      expect(await store.getCourses(), ['sc-900']);

      // Learner history is intact.
      expect(await store.getAttempts(), hasLength(2));
      expect(await store.getSessions(), hasLength(1));

      // Attempts on withdrawn questions are not attributable to any course,
      // so they stay visible in every course scope.
      expect(
        (await store.getAttempts(courseId: 'course-B')).map((a) => a.questionId),
        containsAll(['q-a1', 'q-b1']),
      );

      // Re-applying the withdrawn pack at its original version succeeds now
      // that the ledger entry has been removed.
      await store.applyContentPack(packA);
      expect(await store.getAppliedPackVersion('pack-a'), 1);
      expect(await store.getQuestions(courseId: 'az-900'), hasLength(1));
    });

    test('withdrawing an unknown pack is a no-op', () async {
      final pack = ContentPack.parse(_packJson(
        packId: 'pack-a',
        packVersion: 1,
        courseId: 'az-900',
        questionIds: ['q-a1'],
      ));
      await store.applyContentPack(pack);
      await store.withdrawPack('unknown');
      expect(await store.getQuestions(), hasLength(1));
      expect(await store.getAppliedPackVersion('pack-a'), 1);
    });
  });

  group('Bundled asset loading', () {
    test('bundled production pack loads into the store', () async {
      TestWidgetsFlutterBinding.ensureInitialized();
      final store = FakeLocalStore();
      final success =
          await ContentPackLoader.loadBundledPackIfPresent(store);
      expect(success, isTrue);
      final questions = await store.getQuestions();
      expect(questions, isNotEmpty);
      expect(questions.map((q) => q.courseId).toSet(),
          containsAll(['az-900', 'dp-900', 'ai-901']));
    });

    testWidgets('bundled content-pack asset is resolvable by the asset bundle',
        (tester) async {
      await expectLater(
        rootBundle.loadString(ContentPackLoader.defaultAssetPath),
        completes,
      );
    });
    });

    test('loadBundledPackIfPresent returns false for a missing asset path',
        () async {
      final db = await openTestDatabase();
      final store = LocalStore.withDatabase(db);
      final success = await ContentPackLoader.loadBundledPackIfPresent(
        store,
        assetPath: 'assets/this-pack-does-not-exist.json',
      );
      expect(success, isFalse);
      expect(await store.getQuestions(), isEmpty);
      await store.close();
    });
  });

  group('Schema migration v2 to v3', () {
    test('v2 database migrates to v3 and keeps existing rows', () async {
      final dbPath = await getDatabasesPath();
      final path = join(dbPath, 'v2_to_v3_migration_test.db');
      await deleteDatabase(path);

      final v2 = await openDatabase(
        path,
        version: 2,
        onCreate: (db, version) async {
          await LocalStore.createV1Schema(db);
          await LocalStore.migrateV1ToV2(db);
        },
        onUpgrade: (db, oldVersion, newVersion) async {
          if (oldVersion < 2) {
            await LocalStore.migrateV1ToV2(db);
          }
        },
      );
      await v2.insert('questions', {
        'id': 'legacy-q1',
        'text': 'Legacy question',
        'options': 'A\nB',
        'correctOptionIndex': 0,
        'domain': 'Legacy',
        'difficulty': 'easy',
        'source': 'legacy',
        'rightsBasis': 'legacy',
      });
      await v2.close();

      final v3 = await openDatabase(
        path,
        version: 3,
        onCreate: (db, version) => LocalStore.createSchema(db),
        onUpgrade: (db, oldVersion, newVersion) async {
          if (oldVersion < 2) {
            await LocalStore.migrateV1ToV2(db);
          }
          if (oldVersion < 3) {
            await LocalStore.migrateV2ToV3(db);
          }
        },
      );
      final rows = await v3.query('questions');
      expect(rows.length, 1);
      expect(rows.first['id'], 'legacy-q1');
      expect(rows.first['packId'], isNull);
      expect(rows.first['courseId'], isNull);

      final info = await v3.rawQuery('PRAGMA table_info(questions)');
      final names = info.map((r) => r['name'] as String).toSet();
      expect(names, containsAll(['packId', 'courseId']));

      final sessionInfo = await v3.rawQuery('PRAGMA table_info(sessions)');
      final sessionNames = sessionInfo.map((r) => r['name'] as String).toSet();
      expect(sessionNames, contains('courseId'));

      final tables =
          await v3.rawQuery("SELECT name FROM sqlite_master WHERE type='table'");
      final tableNames = tables.map((r) => r['name'] as String).toSet();
      expect(tableNames, containsAll(['pack_ledger', 'settings']));

      await v3.close();
      await deleteDatabase(path);
    });
  });
}
