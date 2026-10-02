import 'terminology_register.dart';

/// A single terminology lint violation.
class TerminologyViolation {
  final String itemId;
  final String field;
  final String message;
  final String expected;

  const TerminologyViolation({
    required this.itemId,
    required this.field,
    required this.message,
    required this.expected,
  });

  @override
  String toString() => 'Question $itemId ($field): $message; expected: "$expected"';
}

/// Build-time terminology lint over pack question content.
///
/// The linter checks every question against the azlegal-db-v1 terminology
/// register (section 2). It reports all violations rather than stopping at
/// the first, and it checks course-scoped terms against the item's own
/// `courseId`.
class TerminologyLinter {
  final String courseId;
  final String itemId;

  const TerminologyLinter({
    required this.courseId,
    required this.itemId,
  });

  /// Lints a single question, returning every violation found in its text,
  /// explanation, and options.
  ///
  /// The `domain` field is intentionally skipped because it is an internal
  /// topic tag, not learner-facing terminology.
  List<TerminologyViolation> lint({
    required String text,
    required List<String> options,
    String? explanation,
  }) {
    final violations = <TerminologyViolation>[];

    final fields = <String, String>{
      'text': text,
      if (explanation != null && explanation.isNotEmpty) 'explanation': explanation,
    };
    for (var i = 0; i < options.length; i++) {
      fields['option $i'] = options[i];
    }

    for (final entry in fields.entries) {
      violations.addAll(_lintField(entry.key, entry.value));
    }

    return violations;
  }

  List<TerminologyViolation> _lintField(String field, String value) {
    final violations = <TerminologyViolation>[];
    final lower = value.toLowerCase();

    for (final retired in TerminologyRegister.retiredTerms) {
      if (!retired.courses.contains(courseId)) continue;
      if (_contains(lower, retired.pattern.toLowerCase())) {
        violations.add(TerminologyViolation(
          itemId: itemId,
          field: field,
          message: 'Retired or non-exam wording "${retired.pattern}" found',
          expected: retired.replacement,
        ));
      }
    }

    for (final entry in TerminologyRegister.ambiguousAcronyms.entries) {
      final acronym = entry.key;
      final coursePhrase = entry.value[courseId];
      if (coursePhrase == null) continue;
      if (_contains(lower, acronym.toLowerCase())) {
        // Accept the bare acronym only if the exact course-qualified phrase
        // appears in the same field.
        if (!_contains(lower, coursePhrase.toLowerCase())) {
          violations.add(TerminologyViolation(
            itemId: itemId,
            field: field,
            message: 'Bare ambiguous abbreviation "$acronym" must be qualified '
                'for $courseId',
            expected: coursePhrase,
          ));
        }
      }
    }

    return violations;
  }

  bool _contains(String haystack, String needle) => haystack.contains(needle);
}
