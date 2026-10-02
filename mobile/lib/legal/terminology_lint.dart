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

    // 1. Retired or renamed product names.
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

    // 2. Bare ambiguous abbreviations where the register requires the
    //    course-qualified form.
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

    // 3. Known incorrect spellings / variants of official terms.
    for (final entry in TerminologyRegister.knownMisspellings.entries) {
      if (_contains(lower, entry.key)) {
        violations.add(TerminologyViolation(
          itemId: itemId,
          field: field,
          message: 'Incorrect spelling or variant "${entry.key}" found',
          expected: entry.value,
        ));
      }
    }

    // 4. Unverified product terms: product-like phrases that are not in the
    //    course's verified register and are not a retired/ambiguous pattern.
    //    A phrase starts at a known product-marker word (Azure, Microsoft,
    //    Entra, etc.) and extends over immediately following capitalised words.
    //    It stops at lowercase non-marker words, so ordinary prose such as
    //    "Microsoft Entra limits access" is not falsely flagged.
    final knownPatterns = _knownPatternsForCourse();
    final candidates = _extractProductCandidates(value);
    for (final candidate in candidates) {
      final candidateLower = candidate.toLowerCase();
      if (knownPatterns.contains(candidateLower)) continue;
      if (knownPatterns.any((p) => candidateLower.startsWith(p))) continue;
      if (knownPatterns.any((p) => p.startsWith(candidateLower))) continue;
      violations.add(TerminologyViolation(
        itemId: itemId,
        field: field,
        message: 'Unverified product term "$candidate" found',
        expected:
            'Use a current term from the azlegal-db-v1 register for $courseId',
      ));
    }

    return violations;
  }

  /// All known lowercase patterns for this course: verified terms, retired
  /// patterns, and ambiguous-acronym phrases.
  Set<String> _knownPatternsForCourse() {
    final patterns = <String>{};
    final verified = TerminologyRegister.verifiedTerms[courseId];
    if (verified != null) {
      for (final term in verified) {
        patterns.add(term.toLowerCase());
      }
    }
    for (final retired in TerminologyRegister.retiredTerms) {
      if (retired.courses.contains(courseId)) {
        patterns.add(retired.pattern.toLowerCase());
      }
    }
    for (final entry in TerminologyRegister.ambiguousAcronyms.entries) {
      final phrase = entry.value[courseId];
      if (phrase != null) patterns.add(phrase.toLowerCase());
      patterns.add(entry.key.toLowerCase());
    }
    return patterns;
  }

  /// Extracts candidate product phrases from [value]. A phrase starts at a
  /// product-marker word (e.g. Azure, Microsoft, Entra) and extends over
  /// immediately following capitalised words. It stops at lowercase words or
  /// punctuation, which prevents ordinary prose from being flagged.
  List<String> _extractProductCandidates(String value) {
    final candidates = <String>{};
    final words = value
        .split(RegExp(r"[^a-zA-Z0-9\-/()]+"))
        .where((w) => w.isNotEmpty)
        .toList();

    for (var i = 0; i < words.length; i++) {
      final word = words[i];
      if (!_isProductMarker(word)) continue;

      // Start a maximal phrase at this marker word.
      final phrase = [word];
      for (var j = i + 1; j < words.length; j++) {
        final next = words[j];
        if (_isCapitalised(next)) {
          phrase.add(next);
        } else {
          break;
        }
      }

      // Add the maximal phrase and each prefix. We keep the longest first so
      // that verified multi-word terms are checked before their prefixes.
      for (var len = phrase.length; len >= 1; len--) {
        final sub = phrase.sublist(0, len).join(' ');
        candidates.add(_normalizeCandidate(sub));
      }

      i += phrase.length - 1;
    }

    return candidates.toList();
  }

  bool _isProductMarker(String value) {
    final lower = value.toLowerCase();
    for (final marker in TerminologyRegister.productTermMarkers) {
      if (lower == marker || lower.contains(marker)) return true;
    }
    return false;
  }

  bool _isCapitalised(String value) {
    if (value.isEmpty) return false;
    final first = value.codeUnitAt(0);
    return first >= 65 && first <= 90; // 'A'-'Z'
  }

  /// Normalizes a candidate so that trivial parenthetical variants match the
  /// register (e.g. "Azure Virtual Machines" and "Azure Virtual Machines (VM)").
  String _normalizeCandidate(String value) {
    return value.replaceAll(RegExp(r'\s*\([^)]*\)\s*$'), '').trim();
  }

  bool _contains(String haystack, String needle) => haystack.contains(needle);
}
