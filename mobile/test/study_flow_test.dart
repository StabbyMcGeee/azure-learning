import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:study_app/app.dart';
import 'package:study_app/models/content_pack.dart';
import 'package:study_app/models/question.dart';

import 'test_helpers.dart';

void main() {
  setUpAll(initTestDatabase);

  group('Study flow', () {
    testWidgets('shows product empty state when no content is loaded',
        (tester) async {
      final store = FakeLocalStore();
      await tester.pumpWidget(StudyApp(store: store));
      await tester.tap(find.text('Study'));
      await tester.pumpAndSettle();

      expect(find.text('No study material yet'), findsOneWidget);
      expect(find.text('Go to Practice'), findsNothing);
    });

    testWidgets('lists courses after content arrives', (tester) async {
      final store = FakeLocalStore();
      await tester.pumpWidget(StudyApp(store: store));

      await tester.tap(find.text('Study'));
      await tester.pumpAndSettle();
      expect(find.text('No study material yet'), findsOneWidget);

      await store.insertQuestions(_sampleQuestions());
      await tester.tap(find.byType(BackButton));
      await tester.pumpAndSettle();

      await tester.tap(find.text('Study'));
      await tester.pumpAndSettle();

      expect(find.text('AZ-900'), findsOneWidget);
      expect(find.text('AZ-104'), findsOneWidget);
    });

    testWidgets('only lists courses that have loaded content',
        (tester) async {
      final store = FakeLocalStore([
        const Question(
          id: 'partial-001',
          text: 'Sample',
          options: ['A', 'B'],
          correctOptionIndex: 0,
          explanation: 'A',
          domain: 'Governance',
          courseId: 'AZ-104',
          difficulty: 'easy',
        ),
      ]);
      await tester.pumpWidget(StudyApp(store: store));

      await tester.tap(find.text('Study'));
      await tester.pumpAndSettle();

      expect(find.text('AZ-104'), findsOneWidget);
      expect(find.text('AZ-900'), findsNothing);
    });

    testWidgets('course screen groups material by exact domain wording',
        (tester) async {
      final store = FakeLocalStore(_sampleQuestions());
      await tester.pumpWidget(StudyApp(store: store));

      await tester.tap(find.text('Study'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('AZ-900'));
      await tester.pumpAndSettle();

      expect(find.text('AZ-900'), findsWidgets);
      expect(find.text('Cloud Concepts'), findsOneWidget);
      expect(find.text('Cloud Architecture'), findsOneWidget);

      // Correct answer and explanation are visible for learning, not testing.
      expect(
        find.text('Elasticity scales resources and cost.'),
        findsOneWidget,
      );
      expect(find.text('Elasticity'), findsOneWidget);
    });

    testWidgets('marking seen updates status and coverage', (tester) async {
      final store = FakeLocalStore(_sampleQuestions());
      await tester.pumpWidget(StudyApp(store: store));

      await tester.tap(find.text('Study'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('AZ-900'));
      await tester.pumpAndSettle();

      expect(find.text('0 of 2 items seen'), findsOneWidget);
      expect(find.text('New'), findsOneWidget);

      await tester.ensureVisible(find.text('Mark seen').first);
      await tester.tap(find.text('Mark seen').first);
      await tester.pumpAndSettle();

      expect(find.text('Seen'), findsOneWidget);

      // Scroll back to the top so the course progress card is built again.
      await tester.fling(find.byType(ListView), const Offset(0, 300), 1000);
      await tester.pumpAndSettle();

      expect(find.text('1 of 2 items seen'), findsOneWidget);
    });

    testWidgets('marking needs more work updates status', (tester) async {
      final store = FakeLocalStore(_sampleQuestions());
      await tester.pumpWidget(StudyApp(store: store));

      await tester.tap(find.text('Study'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('AZ-104'));
      await tester.pumpAndSettle();

      expect(find.text('New'), findsOneWidget);
      await tester.ensureVisible(find.text('Needs more work').first);
      await tester.tap(find.text('Needs more work').first);
      await tester.pumpAndSettle();

      expect(find.text('Needs review'), findsOneWidget);
    });

    testWidgets('study actions never record scored attempts', (tester) async {
      final store = FakeLocalStore(_sampleQuestions());
      await tester.pumpWidget(StudyApp(store: store));

      await tester.tap(find.text('Study'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('AZ-900'));
      await tester.pumpAndSettle();

      await tester.ensureVisible(find.text('Mark seen').first);
      await tester.tap(find.text('Mark seen').first);
      await tester.pumpAndSettle();
      await tester.ensureVisible(find.text('Needs more work').first);
      await tester.tap(find.text('Needs more work').first);
      await tester.pumpAndSettle();

      expect(await store.getAttempts(), isEmpty);
    });

    testWidgets('coverage follows content that is replaced or withdrawn',
        (tester) async {
      final store = FakeLocalStore();
      await store.applyContentPack(
        _pack('pack-a', 'AZ-900', ['study-001', 'study-002']),
      );
      await tester.pumpWidget(StudyApp(store: store));

      await tester.tap(find.text('Study'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('AZ-900'));
      await tester.pumpAndSettle();
      expect(find.text('0 of 2 items seen'), findsOneWidget);

      await tester.ensureVisible(find.text('Mark seen').first);
      await tester.tap(find.text('Mark seen').first);
      await tester.pumpAndSettle();
      await tester.fling(find.byType(ListView), const Offset(0, 300), 1000);
      await tester.pumpAndSettle();
      expect(find.text('1 of 2 items seen'), findsOneWidget);

      // The course's pack is replaced by different material. The status stored
      // for the withdrawn item must not count toward the new total.
      await store.withdrawPack('pack-a');
      await store.applyContentPack(
        _pack('pack-b', 'AZ-900', ['study-009']),
      );
      await tester.fling(find.byType(ListView), const Offset(0, 300), 1000);
      await tester.pumpAndSettle();
      expect(find.text('0 of 1 items seen'), findsOneWidget);
      expect(find.text('New'), findsOneWidget);
    });

    testWidgets('a newer pack version retires items the learner already saw',
        (tester) async {
      final store = FakeLocalStore();
      await store.applyContentPack(
        _pack('pack-a', 'AZ-900', ['study-001', 'study-002'], packVersion: 1),
      );
      await tester.pumpWidget(StudyApp(store: store));

      await tester.tap(find.text('Study'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('AZ-900'));
      await tester.pumpAndSettle();
      expect(find.text('0 of 2 items seen'), findsOneWidget);

      await tester.ensureVisible(find.text('Mark seen').first);
      await tester.tap(find.text('Mark seen').first);
      await tester.pumpAndSettle();
      await tester.fling(find.byType(ListView), const Offset(0, 300), 1000);
      await tester.pumpAndSettle();
      expect(find.text('1 of 2 items seen'), findsOneWidget);

      // The course's pack ships a newer version that drops one of the two
      // items. The retired item must leave the bank, so it no longer counts
      // toward coverage and is no longer studyable.
      await store.applyContentPack(
        _pack('pack-a', 'AZ-900', ['study-001'], packVersion: 2),
      );
      await tester.fling(find.byType(ListView), const Offset(0, 300), 1000);
      await tester.pumpAndSettle();

      expect(find.text('1 of 1 items seen'), findsOneWidget);
      expect(find.text('Question study-002'), findsNothing);
    });

    testWidgets('lists only the selected course', (tester) async {
      final store = FakeLocalStore(_sampleQuestions());
      await tester.pumpWidget(StudyApp(store: store));
      await tester.pumpAndSettle();

      await tester.tap(find.text('All courses'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('AZ-900').last);
      await tester.pumpAndSettle();
      expect(await store.getSelectedCourseId(), 'AZ-900');

      await tester.tap(find.text('Study'));
      await tester.pumpAndSettle();

      expect(find.text('AZ-900'), findsWidgets);
      expect(find.text('AZ-104'), findsNothing);
    });

    testWidgets('a withdrawn course selection falls back to all content',
        (tester) async {
      final store = FakeLocalStore();
      await store.applyContentPack(
        _pack('pack-a', 'course-A', ['a-001', 'a-002']),
      );
      await store.applyContentPack(
        _pack('pack-b', 'course-B', ['b-001']),
      );
      await tester.pumpWidget(StudyApp(store: store));
      await tester.pumpAndSettle();

      await tester.tap(find.text('All courses'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('course-A').last);
      await tester.pumpAndSettle();
      expect(await store.getSelectedCourseId(), 'course-A');

      await store.withdrawPack('pack-a');
      await tester.tap(find.text('Practice'));
      await tester.pumpAndSettle();

      expect(await store.getSelectedCourseId(), isNull);
      expect(find.text('Question b-001'), findsOneWidget);
    });
  });
}

ContentPack _pack(
  String packId,
  String courseId,
  List<String> questionIds, {
  int packVersion = 1,
}) =>
    ContentPack(
      formatVersion: contentPackFormatVersion,
      packId: packId,
      packVersion: packVersion,
      title: 'Test pack',
      source: 'synthetic',
      rightsBasis: 'synthetic',
      questions: [
        for (final id in questionIds)
          PackQuestion(
            id: id,
            text: 'Question $id',
            options: const ['A', 'B'],
            correctOptionIndex: 0,
            explanation: 'A is correct.',
            domain: 'Cloud Concepts',
            difficulty: 'easy',
            source: 'synthetic',
            rightsBasis: 'synthetic',
            courseId: courseId,
          ),
      ],
    );

List<Question> _sampleQuestions() => const [
  Question(
    id: 'study-001',
    text: 'Which trait lets you pay only for resources you use?',
    options: [
      'Scalability',
      'Elasticity',
    ],
    correctOptionIndex: 1,
    explanation: 'Elasticity scales resources and cost.',
    domain: 'Cloud Concepts',
    courseId: 'AZ-900',
    difficulty: 'easy',
  ),
  Question(
    id: 'study-002',
    text: 'Which service model is fully managed by the provider?',
    options: [
      'IaaS',
      'PaaS',
      'SaaS',
    ],
    correctOptionIndex: 2,
    explanation: 'SaaS delivers fully managed applications.',
    domain: 'Cloud Architecture',
    courseId: 'AZ-900',
    difficulty: 'medium',
  ),
  Question(
    id: 'study-003',
    text: 'Which governance tool enforces standards?',
    options: [
      'Azure Policy',
      'Azure Advisor',
    ],
    correctOptionIndex: 0,
    explanation: 'Azure Policy defines and enforces standards.',
    domain: 'Governance',
    courseId: 'AZ-104',
    difficulty: 'medium',
  ),
];
