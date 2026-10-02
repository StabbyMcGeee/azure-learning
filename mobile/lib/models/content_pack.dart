import 'dart:convert';

import '../legal/rights_basis.dart';
import '../legal/terminology_lint.dart';
import '../legal/terminology_register.dart';
import 'question.dart';

/// Offline content pack format version identifier.
///
/// The mobile app only accepts packs that declare this exact version. Bump it
/// only when the schema makes an incompatible change and ship a matching
/// migration path.
const String contentPackFormatVersion = 'azpack-v2';

/// Maximum number of questions a single pack may contain.
///
/// This bound protects the app from unbounded memory use and abuse. It is a
/// policy constant, not a legal guarantee.
const int contentPackMaxQuestions = 10000;

/// A bounded, versioned offline content pack.
///
/// A pack carries both pack-level and per-question provenance metadata.
/// The presence of metadata is required by validation; it does not, by itself,
/// prove that rights are cleared.
class ContentPack {
  final String formatVersion;
  final String packId;
  final int packVersion;
  final String title;
  final String source;
  final String rightsBasis;
  final String? licenseRef;
  final String? attributionText;
  final String? lastVerifiedAt;
  final List<PackQuestion> questions;

  const ContentPack({
    required this.formatVersion,
    required this.packId,
    required this.packVersion,
    required this.title,
    required this.source,
    required this.rightsBasis,
    this.licenseRef,
    this.attributionText,
    this.lastVerifiedAt,
    required this.questions,
  });

  /// Parses a pack from a decoded JSON string.
  ///
  /// Throws [FormatException] when the JSON is invalid or required fields are
  /// missing/typed incorrectly. Semantic validation is performed separately by
  /// [ContentPackValidator].
  factory ContentPack.parse(String source) {
    final dynamic decoded = jsonDecode(source);
    if (decoded is! Map<String, dynamic>) {
      throw const FormatException('Content pack must be a JSON object');
    }
    return ContentPack.fromJson(decoded);
  }

  factory ContentPack.fromJson(Map<String, dynamic> json) {
    final formatVersion = _requireString(json, 'formatVersion');
    final packId = _requireString(json, 'packId');
    final packVersion = _requireInt(json, 'packVersion');
    final title = _requireString(json, 'title');
    final source = _requireString(json, 'source');
    final rightsBasis = _requireString(json, 'rightsBasis');
    final licenseRef = json['licenseRef'] as String?;
    final attributionText = json['attributionText'] as String?;
    final lastVerifiedAt = json['lastVerifiedAt'] as String?;

    final rawQuestions = json['questions'];
    if (rawQuestions is! List<dynamic>) {
      throw const FormatException('Missing or invalid "questions" array');
    }

    final questions = <PackQuestion>[];
    for (var i = 0; i < rawQuestions.length; i++) {
      final item = rawQuestions[i];
      if (item is! Map<String, dynamic>) {
        throw FormatException('Question at index $i must be an object');
      }
      questions.add(PackQuestion.fromJson(item));
    }

    return ContentPack(
      formatVersion: formatVersion,
      packId: packId,
      packVersion: packVersion,
      title: title,
      source: source,
      rightsBasis: rightsBasis,
      licenseRef: licenseRef,
      attributionText: attributionText,
      lastVerifiedAt: lastVerifiedAt,
      questions: questions,
    );
  }

  static String _requireString(Map<String, dynamic> json, String key) {
    final value = json[key];
    if (value is! String) {
      throw FormatException('Missing or invalid required string field "$key"');
    }
    return value;
  }

  static int _requireInt(Map<String, dynamic> json, String key) {
    final value = json[key];
    if (value is! int) {
      throw FormatException('Missing or invalid required integer field "$key"');
    }
    return value;
  }
}

/// A single question entry inside a [ContentPack].
class PackQuestion {
  final String id;
  final String text;
  final List<String> options;
  final int correctOptionIndex;
  final String? explanation;
  final String domain;
  final String difficulty;
  final String source;
  final String rightsBasis;
  final String? licenseRef;
  final String? attributionText;
  final String courseId;

  const PackQuestion({
    required this.id,
    required this.text,
    required this.options,
    required this.correctOptionIndex,
    this.explanation,
    required this.domain,
    required this.difficulty,
    required this.source,
    required this.rightsBasis,
    this.licenseRef,
    this.attributionText,
    required this.courseId,
  });

  factory PackQuestion.fromJson(Map<String, dynamic> json) {
    final id = ContentPack._requireString(json, 'id');
    final text = ContentPack._requireString(json, 'text');
    final domain = ContentPack._requireString(json, 'domain');
    final difficulty = ContentPack._requireString(json, 'difficulty');
    final source = ContentPack._requireString(json, 'source');
    final rightsBasis = ContentPack._requireString(json, 'rightsBasis');
    final licenseRef = json['licenseRef'] as String?;
    final attributionText = json['attributionText'] as String?;
    final courseId = ContentPack._requireString(json, 'courseId');

    final rawOptions = json['options'];
    if (rawOptions is! List<dynamic>) {
      throw const FormatException('Missing or invalid question "options"');
    }
    final options = rawOptions.map((o) {
      if (o is! String) {
        throw const FormatException('Question options must be strings');
      }
      return o;
    }).toList();

    final correctOptionIndex = ContentPack._requireInt(json, 'correctOptionIndex');

    final explanation = json['explanation'];
    if (explanation != null && explanation is! String) {
      throw const FormatException('Question "explanation" must be a string');
    }

    return PackQuestion(
      id: id,
      text: text,
      options: options,
      correctOptionIndex: correctOptionIndex,
      explanation: explanation as String?,
      domain: domain,
      difficulty: difficulty,
      source: source,
      rightsBasis: rightsBasis,
      licenseRef: licenseRef,
      attributionText: attributionText,
      courseId: courseId,
    );
  }

  Question toQuestion({required String packId}) => Question(
        id: id,
        text: text,
        options: options,
        correctOptionIndex: correctOptionIndex,
        explanation: explanation,
        domain: domain,
        difficulty: difficulty,
        source: source,
        rightsBasis: rightsBasis,
        packId: packId,
        courseId: courseId,
      );
}

/// Semantic validator for [ContentPack].
///
/// Returns a list of human-readable error strings. An empty list means the pack
/// is structurally and semantically valid; it does not mean the pack's legal
/// rights are proven.
class ContentPackValidator {
  final ContentPack pack;

  /// Whether to run the azlegal-db-v1 terminology lint over question content.
  ///
  /// Terminology checking is a build-time gate and is enabled by default. It
  /// can be disabled for tests that exercise only structural validation.
  final bool lintTerminology;

  const ContentPackValidator(
    this.pack, {
    this.lintTerminology = true,
  });

  List<String> validate() {
    final errors = <String>[];
    _validateTopLevel(errors);
    _validateQuestions(errors);
    return errors;
  }

  void _validateTopLevel(List<String> errors) {
    if (pack.formatVersion != contentPackFormatVersion) {
      errors.add(
        'Unsupported formatVersion "${pack.formatVersion}" '
        '(expected "$contentPackFormatVersion")',
      );
    }
    if (pack.packId.trim().isEmpty) {
      errors.add('Missing or empty packId');
    }
    if (pack.packVersion < 1) {
      errors.add('packVersion must be >= 1');
    }
    if (pack.title.trim().isEmpty) {
      errors.add('Missing or empty title');
    }
    if (pack.source.trim().isEmpty) {
      errors.add('Missing or empty pack-level source');
    }
    if (pack.rightsBasis.trim().isEmpty) {
      errors.add('Missing or empty pack-level rightsBasis');
    } else {
      errors.addAll(
        RightsBasis.validate(
          pack.rightsBasis,
          licenseRef: pack.licenseRef,
          attributionText: pack.attributionText,
        ).map((e) => 'Pack-level: $e'),
      );
    }

    if (pack.lastVerifiedAt != null &&
        !_isIsoDate(pack.lastVerifiedAt!)) {
      errors.add(
        'Pack-level lastVerifiedAt "${pack.lastVerifiedAt}" is not a valid '
        'ISO-8601 date',
      );
    }
  }

  void _validateQuestions(List<String> errors) {
    if (pack.questions.length > contentPackMaxQuestions) {
      errors.add(
        'Pack contains ${pack.questions.length} questions; '
        'maximum is $contentPackMaxQuestions',
      );
    }

    final seenIds = <String>{};
    for (var i = 0; i < pack.questions.length; i++) {
      final q = pack.questions[i];
      final prefix = 'Question $i (${q.id.isEmpty ? 'no id' : q.id})';

      if (q.id.trim().isEmpty) {
        errors.add('$prefix: missing or empty id');
      } else if (!seenIds.add(q.id)) {
        errors.add('$prefix: duplicate id "${q.id}"');
      }

      if (q.text.trim().isEmpty) {
        errors.add('$prefix: missing or empty text');
      }

      if (q.options.length < 2) {
        errors.add('$prefix: must have at least two options');
      }

      if (q.correctOptionIndex < 0 || q.correctOptionIndex >= q.options.length) {
        errors.add(
          '$prefix: correctOptionIndex ${q.correctOptionIndex} is out of range '
          '(0..${q.options.length - 1})',
        );
      }

      if (q.domain.trim().isEmpty) {
        errors.add('$prefix: missing or empty domain');
      }

      if (q.difficulty.trim().isEmpty) {
        errors.add('$prefix: missing or empty difficulty');
      }

      if (q.source.trim().isEmpty) {
        errors.add('$prefix: missing or empty source');
      }

      if (q.rightsBasis.trim().isEmpty) {
        errors.add('$prefix: missing or empty rightsBasis');
      } else {
        errors.addAll(
          RightsBasis.validate(
            q.rightsBasis,
            licenseRef: q.licenseRef,
            attributionText: q.attributionText,
          ).map((e) => '$prefix: $e'),
        );
      }

      if (q.courseId.trim().isEmpty) {
        errors.add('$prefix: missing or empty courseId');
      } else if (!TerminologyRegister.isKnownCourse(q.courseId)) {
        errors.add(
          '$prefix: courseId "${q.courseId}" is not a registered course; '
          'permitted values are: ${TerminologyRegister.allCourses.join(', ')}',
        );
      }

      if (lintTerminology && TerminologyRegister.isKnownCourse(q.courseId)) {
        final linter = TerminologyLinter(
          courseId: q.courseId,
          itemId: q.id,
        );
        final violations = linter.lint(
          text: q.text,
          options: q.options,
          explanation: q.explanation,
        );
        for (final v in violations) {
          errors.add('$prefix: ${v.message}; expected: "${v.expected}"');
        }
      }
    }
  }
}

bool _isIsoDate(String value) {
  try {
    DateTime.parse(value);
    return true;
  } on FormatException {
    return false;
  }
}
