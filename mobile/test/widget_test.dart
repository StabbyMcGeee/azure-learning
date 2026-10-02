import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:study_app/app.dart';

import 'test_helpers.dart';

void main() {
  setUpAll(initTestDatabase);

  testWidgets('App launches and dashboard is accessible', (tester) async {
    await tester.pumpWidget(StudyApp(store: FakeLocalStore()));
    expect(find.text('Study App (placeholder)'), findsOneWidget);
    expect(find.byType(MaterialApp), findsOneWidget);
  });

  testWidgets('Empty state displays action when questions are absent',
      (tester) async {
    await tester.pumpWidget(StudyApp(store: FakeLocalStore()));
    await tester.tap(find.text('Study'));
    await tester.pumpAndSettle();
    expect(find.text('Study material is empty'), findsOneWidget);
    expect(find.text('Go to Practice'), findsOneWidget);
  });

  testWidgets('Unknown routes do not crash', (tester) async {
    final store = FakeLocalStore();
    await tester.pumpWidget(StudyApp(store: store));
    final BuildContext context = tester.element(find.byType(Scaffold).first);
    Navigator.of(context).pushNamed('/nonexistent');
    await tester.pumpAndSettle();
    expect(find.text('Page not found'), findsOneWidget);
  });
}
