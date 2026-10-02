import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:study_app/app.dart';
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

      expect(await store.getAllAttempts(), isEmpty);
    });

    testWidgets('Resume action surfaces when there is unfinished material',
        (tester) async {
      final store = FakeLocalStore(_sampleQuestions());
      await tester.pumpWidget(StudyApp(store: store));

      await tester.tap(find.text('Study'));
      await tester.pumpAndSettle();
      await tester.tap(find.text('AZ-900'));
      await tester.pumpAndSettle();

      expect(find.text('Resume'), findsOneWidget);
    });
  });
}

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
