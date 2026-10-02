import 'rights_basis.dart';

/// Build-time validator for the azlegal-db-v1 per-item evidence register.
///
/// This validates a private provenance register (section 3) against the schema
/// and permitted values in the report. It does **not** validate question
/// expression itself; that is handled by the terminology lint and the
/// content-pack validator.
class EvidenceRegisterValidator {
  const EvidenceRegisterValidator._();

  static const List<String> permittedLicenseClasses = [
    'cc-by-4.0-repo',
    'learn-tou',
    'marketing-site',
    'product-behaviour',
    'public-fact',
  ];

  static const List<String> permittedStatuses = [
    'draft',
    'fact-checked',
    'rights-reviewed',
    'approved',
    'released',
    'withdrawn',
  ];

  static const List<String> permittedLocales = [
    'en-US',
  ];

  static const List<String> permittedWithdrawalReasons = [
    'source-license-revoked',
    'objective-removed',
    'factual-error',
    'rights-basis-failed',
    'duplicate',
  ];

  static const List<String> permittedAiAssistance = [
    'none',
    'review-only',
  ];

  /// Validates a complete register object.
  ///
  /// The register may be either a list of items or an object with an `items`
  /// key. Returns all validation errors found; an empty list means the register
  /// is structurally valid.
  static List<String> validateRegister(dynamic register) {
    final errors = <String>[];
    final List<dynamic> items;

    if (register is List<dynamic>) {
      items = register;
    } else if (register is Map<String, dynamic>) {
      final rawItems = register['items'];
      if (rawItems is! List<dynamic>) {
        errors.add('Register must be a list or an object with an "items" array');
        return errors;
      }
      items = rawItems;
    } else {
      errors.add('Register must be a list or an object with an "items" array');
      return errors;
    }

    final seenIds = <String>{};
    for (var i = 0; i < items.length; i++) {
      final item = items[i];
      if (item is! Map<String, dynamic>) {
        errors.add('Item $i is not an object');
        continue;
      }
      final itemId = item['itemId'];
      final prefix = 'Item $i (${itemId is String ? itemId : 'no id'})';
      errors.addAll(validateItem(item).map((e) => '$prefix: $e'));

      if (itemId is String && itemId.isNotEmpty) {
        if (seenIds.contains(itemId)) {
          errors.add('$prefix: duplicate itemId "$itemId"');
        } else {
          seenIds.add(itemId);
        }
      }
    }

    return errors;
  }

  /// Validates a single evidence-register item.
  static List<String> validateItem(Map<String, dynamic> item) {
    final errors = <String>[];

    void requireString(String key) {
      final value = item[key];
      if (value is! String || value.trim().isEmpty) {
        errors.add('Missing or invalid required string field "$key"');
      }
    }

    void requireInt(String key) {
      final value = item[key];
      if (value is! int) {
        errors.add('Missing or invalid required integer field "$key"');
      }
    }

    void requireDate(String key) {
      final value = item[key];
      if (value is! String || !_isIsoDate(value)) {
        errors.add('Missing or invalid ISO-8601 date field "$key"');
      }
    }

    void requireArray(String key) {
      final value = item[key];
      if (value is! List<dynamic>) {
        errors.add('Missing or invalid required array field "$key"');
      }
    }

    void requireObject(String key) {
      final value = item[key];
      if (value is! Map<String, dynamic>) {
        errors.add('Missing or invalid required object field "$key"');
      }
    }

    // Core identity fields are always required.
    requireString('itemId');
    requireString('courseId');
    requireInt('version');
    requireString('status');

    final status = item['status'];

    // Withdrawn legacy items may carry no evidence chain. Only the
    // withdrawal record and the basis/status enums are checked.
    if (status == 'withdrawn') {
      requireDate('withdrawnAt');
      requireString('withdrawalReason');
      _checkEnum(
        item,
        'withdrawalReason',
        permittedWithdrawalReasons,
        errors,
      );
      _checkEnum(item, 'rightsBasis', permittedRightsBases, errors);
      return errors;
    }

    requireString('contentHash');
    requireString('objectiveId');
    requireObject('outlineSnapshot');
    requireString('factSheetId');
    requireArray('factSources');
    requireArray('termRefs');
    requireString('author');
    requireDate('authoredAt');
    requireString('aiAssistance');
    requireObject('noExposureAttestation');
    requireString('techReviewer');
    requireDate('techReviewedAt');
    requireString('rightsReviewer');
    requireDate('rightsReviewedAt');
    requireObject('similarityReport');
    requireString('rightsBasis');
    requireString('locale');
    requireDate('lastVerifiedAt');
    requireString('outlineVersionAtVerify');

    // Enum checks.
    _checkEnum(item, 'rightsBasis', permittedRightsBases, errors);
    _checkEnum(item, 'locale', permittedLocales, errors);
    _checkEnum(item, 'status', permittedStatuses, errors);
    _checkEnum(item, 'aiAssistance', permittedAiAssistance, errors);

    final rightsBasis = item['rightsBasis'];
    if (rightsBasis is String && RightsBasis.isValid(rightsBasis)) {
      final licenseRef = item['licenseRef'];
      final attributionText = item['attributionText'];
      errors.addAll(
        RightsBasis.validate(
          rightsBasis,
          licenseRef: licenseRef is String ? licenseRef : null,
          attributionText: attributionText is String ? attributionText : null,
        ).map((e) => 'rightsBasis companion: $e'),
      );
    }

    // Status-machine checks for released/approved items.
    if (status == 'released' || status == 'approved') {
      final factSources = item['factSources'];
      if (factSources is List<dynamic> && factSources.length < 2) {
        errors.add('Status "$status" requires at least 2 factSources');
      }

      final attestation = item['noExposureAttestation'];
      if (attestation is! Map<String, dynamic> ||
          attestation['authorId'] is! String ||
          attestation['date'] is! String) {
        errors.add('Status "$status" requires a signed noExposureAttestation');
      }

      final author = item['author'];
      final techReviewer = item['techReviewer'];
      final rightsReviewer = item['rightsReviewer'];
      if (techReviewer is String && author is String && techReviewer == author) {
        errors.add('techReviewer must differ from author');
      }
      if (rightsReviewer is String &&
          author is String &&
          rightsReviewer == author) {
        errors.add('rightsReviewer must differ from author');
      }

      final similarityReport = item['similarityReport'];
      if (similarityReport is! Map<String, dynamic> ||
          similarityReport['tool'] is! String ||
          similarityReport['resultHash'] is! String) {
        errors.add('Status "$status" requires a similarityReport');
      }
    }

    // factSources licenseClass enum check.
    final factSources = item['factSources'];
    if (factSources is List<dynamic>) {
      for (var i = 0; i < factSources.length; i++) {
        final source = factSources[i];
        if (source is Map<String, dynamic>) {
          _checkEnum(
            source,
            'licenseClass',
            permittedLicenseClasses,
            errors,
            prefix: 'factSources[$i]',
          );
          if (source['url'] is! String || source['retrievedAt'] is! String) {
            errors.add('factSources[$i] requires url and retrievedAt');
          }
        } else {
          errors.add('factSources[$i] is not an object');
        }
      }
    }

    return errors;
  }

  static void _checkEnum(
    Map<String, dynamic> container,
    String key,
    List<String> permitted,
    List<String> errors, {
    String prefix = '',
  }) {
    final value = container[key];
    if (value is! String) return;
    if (!permitted.contains(value)) {
      final label = prefix.isEmpty ? key : '$prefix.$key';
      errors.add(
        'Invalid $label "$value"; permitted values are: '
        '${permitted.join(', ')}',
      );
    }
  }

  static bool _isIsoDate(String value) {
    // Require a full ISO-8601 calendar date (YYYY-MM-DD); reject partial or
    // lenient values such as "2026" or "2026-02-31" that DateTime.parse might
    // otherwise accept (the latter rolls over to 2026-03-03).
    if (!RegExp(r'^\d{4}-\d{2}-\d{2}$').hasMatch(value)) return false;
    try {
      final parsed = DateTime.parse(value);
      final year = int.parse(value.substring(0, 4));
      final month = int.parse(value.substring(5, 7));
      final day = int.parse(value.substring(8, 10));
      return parsed.year == year &&
          parsed.month == month &&
          parsed.day == day;
    } on FormatException {
      return false;
    }
  }
}
