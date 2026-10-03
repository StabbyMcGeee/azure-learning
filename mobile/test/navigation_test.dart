import 'package:flutter_test/flutter_test.dart';
import 'package:study_app/app.dart';
import 'package:study_app/data/question_bank.dart';
import 'package:study_app/navigation/app_router.dart';

import 'test_helpers.dart';

void main() {
  setUpAll(initTestDatabase);

  group('Navigation', () {
    testWidgets('dashboard shows study areas', (tester) async {
      await tester.pumpWidget(StudyApp(store: FakeLocalStore()));
      expect(find.text('Study App (placeholder)'), findsOneWidget);
      expect(find.text('Study'), findsOneWidget);
      expect(find.text('Practice'), findsOneWidget);
      expect(find.text('Exam'), findsOneWidget);
      expect(find.text('Review'), findsOneWidget);
      expect(find.text('Progress'), findsOneWidget);
    });

    testWidgets('tapping Study navigates to empty study screen', (tester) async {
      await tester.pumpWidget(StudyApp(store: FakeLocalStore()));
      await tester.tap(find.text('Study'));
      await tester.pumpAndSettle();
      expect(find.text('No study material yet'), findsOneWidget);
    });

    testWidgets('tapping Practice navigates to practice screen', (tester) async {
      final store = FakeLocalStore(QuestionBank.syntheticFixtures());
      await tester.pumpWidget(StudyApp(store: store));
      await tester.tap(find.text('Practice'));
      await tester.pumpAndSettle();
      expect(find.text('Practice'), findsWidgets);
    });

    testWidgets('direct route to progress screen renders', (tester) async {
      final store = FakeLocalStore();
      await tester.pumpWidget(
        StudyApp(
          store: store,
          initialRoute: AppRouter.progress,
        ),
      );
      await tester.pumpAndSettle();
      expect(find.text('Progress'), findsWidgets);
    });

    testWidgets('progress labels the selected course as its scope',
        (tester) async {
      final store = FakeLocalStore(QuestionBank.syntheticFixtures());
      await store.setSelectedCourseId('AZ-900');
      await tester.pumpWidget(
        StudyApp(store: store, initialRoute: AppRouter.progress),
      );
      await tester.pumpAndSettle();
      expect(find.text('Accuracy for AZ-900'), findsOneWidget);
      expect(find.textContaining('Recent attempts'), findsOneWidget);
    });

    testWidgets('progress labels the no-filter scope as all courses',
        (tester) async {
      final store = FakeLocalStore(QuestionBank.syntheticFixtures());
      await tester.pumpWidget(
        StudyApp(store: store, initialRoute: AppRouter.progress),
      );
      await tester.pumpAndSettle();
      expect(find.text('Accuracy for all courses'), findsOneWidget);
      expect(find.textContaining('Recent exam sessions'), findsOneWidget);
    });
  });
}
