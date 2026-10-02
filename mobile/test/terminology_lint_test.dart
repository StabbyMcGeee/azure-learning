import 'package:flutter_test/flutter_test.dart';
import 'package:study_app/legal/terminology_lint.dart';

void main() {
  group('TerminologyLinter', () {
    test('reports retired Azure AD in an AZ-900 item', () {
      final linter = TerminologyLinter(
        courseId: 'az-900',
        itemId: 'az900-022',
      );
      final violations = linter.lint(
        text: 'Which Azure AD feature provides single sign-on?',
        options: const ['SSO', 'MFA'],
      );
      expect(violations, isNotEmpty);
      final v = violations.first;
      expect(v.itemId, 'az900-022');
      expect(v.field, 'text');
      expect(v.message, contains('Azure AD'));
      expect(v.expected, 'Microsoft Entra ID');
    });

    test('reports bare RBAC in AZ-900 with expected qualified phrase', () {
      final linter = TerminologyLinter(
        courseId: 'az-900',
        itemId: 'az900-100',
      );
      final violations = linter.lint(
        text: 'Which RBAC role grants read access?',
        options: const ['Owner', 'Reader'],
      );
      expect(violations, hasLength(1));
      expect(violations.first.message, contains('RBAC'));
      expect(
        violations.first.expected,
        'Azure role-based access control (RBAC)',
      );
    });

    test('allows qualified RBAC phrase in AZ-900', () {
      final linter = TerminologyLinter(
        courseId: 'az-900',
        itemId: 'az900-101',
      );
      final violations = linter.lint(
        text:
            'Azure role-based access control (RBAC) assigns permissions to users.',
        options: const ['Reader', 'Contributor'],
      );
      expect(violations, isEmpty);
    });

    test('reports bare RBAC in SC-900 with expected qualified phrase', () {
      final linter = TerminologyLinter(
        courseId: 'sc-900',
        itemId: 'sc900-050',
      );
      final violations = linter.lint(
        text: 'RBAC in Microsoft Entra limits admin access.',
        options: const ['Global Administrator', 'User Administrator'],
      );
      expect(violations, hasLength(1));
      expect(
        violations.first.expected,
        'Microsoft Entra roles and role-based access control (RBAC)',
      );
    });

    test('reports geo redundant zones in any course', () {
      final linter = TerminologyLinter(
        courseId: 'az-900',
        itemId: 'az900-015',
      );
      final violations = linter.lint(
        text: 'Geo redundant zones replicate across regions.',
        options: const ['LRS', 'GRS'],
      );
      expect(violations, isNotEmpty);
      expect(violations.first.message, contains('geo redundant zones'));
    });

    test('flags Service Trust Portal in AZ-900 as course-scoped retired', () {
      final linter = TerminologyLinter(
        courseId: 'az-900',
        itemId: 'az900-126',
      );
      final violations = linter.lint(
        text: 'The Service Trust Portal shows compliance documents.',
        options: const ['Azure portal', 'Service Trust Portal'],
      );
      expect(violations, isNotEmpty);
      expect(violations.first.message, contains('Service Trust Portal'));
    });

    test('allows Service Trust Portal in SC-900', () {
      final linter = TerminologyLinter(
        courseId: 'sc-900',
        itemId: 'sc900-090',
      );
      final violations = linter.lint(
        text: 'The Microsoft Service Trust Portal helps with compliance.',
        options: const ['Microsoft Purview', 'Microsoft Service Trust Portal'],
      );
      expect(violations, isEmpty);
    });

    test('reports known misspellings of official terms', () {
      final linter = TerminologyLinter(
        courseId: 'az-900',
        itemId: 'az900-004',
      );
      final violations = linter.lint(
        text: 'Use defence-in-depth and multi-factor authentication.',
        options: const ['MFA', 'RBAC'],
      );
      final misspellings = violations
          .where((v) => v.message.contains('Incorrect spelling'))
          .toList();
      expect(misspellings, hasLength(2));
      expect(
        misspellings.map((v) => v.expected),
        containsAll([
          'defense-in-depth',
          'multifactor authentication (MFA)',
        ]),
      );
    });

    test('reports unverified product terms not in the register', () {
      final linter = TerminologyLinter(
        courseId: 'az-900',
        itemId: 'az900-zzz',
      );
      final violations = linter.lint(
        text: 'Deploy to the Azure Frobnicator service.',
        options: const ['Azure Frobnicator'],
      );
      final unverified = violations
          .where((v) => v.message.contains('Unverified product term'))
          .toList();
      expect(unverified, isNotEmpty);
      expect(
        unverified.first.message,
        contains('Azure Frobnicator'),
      );
    });

    test('allows current Azure product terms that are in the register', () {
      final linter = TerminologyLinter(
        courseId: 'az-900',
        itemId: 'az900-018',
      );
      final violations = linter.lint(
        text: 'Azure Virtual Machines run guest operating systems.',
        options: const ['Azure Virtual Machines'],
      );
      expect(violations, isEmpty);
    });

    test('does not flag retired AI-901 terms in AZ-900 content', () {
      final linter = TerminologyLinter(
        courseId: 'az-900',
        itemId: 'az900-ai',
      );
      final violations = linter.lint(
        text: 'LUIS and Anomaly Detector are not in this course.',
        options: const ['Language Understanding', 'Anomaly Detector'],
      );
      expect(violations, isEmpty);
    });

    test('flags retired AI-901 terms inside ai-901 content', () {
      final linter = TerminologyLinter(
        courseId: 'ai-901',
        itemId: 'ai901-001',
      );
      final violations = linter.lint(
        text: 'Use LUIS to build language understanding.',
        options: const ['LUIS'],
      );
      expect(violations, isNotEmpty);
      expect(violations.first.message, contains('LUIS'));
    });
  });
}
