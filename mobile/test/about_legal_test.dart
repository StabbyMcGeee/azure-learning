import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:study_app/app.dart';
import 'package:study_app/models/content_pack.dart';

import 'test_helpers.dart';

ContentPack _packWithVerifiedDate() => ContentPack(
  formatVersion: 'azpack-v2',
  packId: 'com.example.test.about',
  packVersion: 1,
  title: 'About test pack',
  source: 'Test fixture',
  rightsBasis: 'original-human',
  lastVerifiedAt: '2026-10-02',
  questions: [
    PackQuestion(
      id: 'about-001',
      text: 'Sample question',
      options: const ['A', 'B'],
      correctOptionIndex: 0,
      domain: 'Test',
      difficulty: 'easy',
      source: 'Test fixture',
      rightsBasis: 'original-human',
      courseId: 'az-900',
    ),
  ],
);

void main() {
  testWidgets('About \u0026 Legal screen shows independence and trademark text',
      (tester) async {
    await tester.pumpWidget(StudyApp(store: FakeLocalStore()));
    await tester.tap(find.text('About \u0026 Legal'));
    await tester.pumpAndSettle();

    expect(find.text('About \u0026 Legal'), findsOneWidget);
    expect(
      find.textContaining('This app is an independent study aid'),
      findsOneWidget,
    );
    expect(
      find.textContaining('Microsoft, Azure, AZ-900'),
      findsOneWidget,
    );
  });

  testWidgets('About \u0026 Legal screen shows pack-sourced last verified date',
      (tester) async {
    final store = FakeLocalStore();
    await store.applyContentPack(_packWithVerifiedDate());

    await tester.pumpWidget(StudyApp(store: store));
    await tester.tap(find.text('About \u0026 Legal'));
    await tester.pumpAndSettle();

    expect(find.text('2026-10-02'), findsOneWidget);
  });

  testWidgets('About \u0026 Legal screen clears stale date when new pack omits it',
      (tester) async {
    final store = FakeLocalStore();
    await store.applyContentPack(_packWithVerifiedDate());
    expect(await store.getContentLastVerifiedAt(), '2026-10-02');

    // Apply a new version of the same pack without lastVerifiedAt.
    final clearedPack = ContentPack(
      formatVersion: 'azpack-v2',
      packId: 'com.example.test.about',
      packVersion: 2,
      title: 'About test pack v2',
      source: 'Test fixture',
      rightsBasis: 'original-human',
      questions: [
        PackQuestion(
          id: 'about-001',
          text: 'Sample question',
          options: const ['A', 'B'],
          correctOptionIndex: 0,
          domain: 'Test',
          difficulty: 'easy',
          source: 'Test fixture',
          rightsBasis: 'original-human',
          courseId: 'az-900',
        ),
      ],
    );
    await store.applyContentPack(clearedPack);
    expect(await store.getContentLastVerifiedAt(), isNull);

    await tester.pumpWidget(StudyApp(store: store));
    await tester.tap(find.text('About \u0026 Legal'));
    await tester.pumpAndSettle();

    expect(
      find.text('No verified content loaded yet.'),
      findsOneWidget,
    );
  });

  testWidgets('About \u0026 Legal screen shows fallback when no date loaded',
      (tester) async {
    await tester.pumpWidget(StudyApp(store: FakeLocalStore()));
    await tester.tap(find.text('About \u0026 Legal'));
    await tester.pumpAndSettle();

    expect(
      find.text('No verified content loaded yet.'),
      findsOneWidget,
    );
  });

  testWidgets('About \u0026 Legal screen has a license-viewing button',
      (tester) async {
    await tester.pumpWidget(StudyApp(store: FakeLocalStore()));
    await tester.tap(find.text('About \u0026 Legal'));
    await tester.pumpAndSettle();

    expect(find.byType(FilledButton), findsOneWidget);
    expect(find.text('View third-party licenses'), findsOneWidget);
  });
}
