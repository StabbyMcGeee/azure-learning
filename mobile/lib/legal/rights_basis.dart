/// Permitted values for a content pack's `rightsBasis` field.
///
/// These values come from the azlegal-db-v1 per-item evidence schema
/// (section 3.1). Any other value is rejected at build/load time.
const List<String> permittedRightsBases = [
  'original-human',
  'original-human-ai-assisted',
  'licensed-cc-by-4.0',
  'licensed-commercial',
  'public-domain',
];

/// Shared rights-basis validation helpers.
///
/// Companion fields `licenseRef` and `attributionText` are required only when
/// the chosen basis demands them, keeping the fail-closed behavior localised.
class RightsBasis {
  const RightsBasis._();

  static bool isValid(String value) => permittedRightsBases.contains(value);

  static bool requiresLicenseRef(String value) => value.startsWith('licensed-');

  static bool requiresAttribution(String value) => value == 'licensed-cc-by-4.0';

  /// Validates a single rights-basis value and its companion fields.
  ///
  /// Returns a list of human-readable error strings. An empty list means the
  /// basis is permitted and its companion fields are present when required.
  static List<String> validate(
    String value, {
    String? licenseRef,
    String? attributionText,
  }) {
    final errors = <String>[];
    if (!isValid(value)) {
      errors.add(
        'rightsBasis "$value" is not one of the permitted values: '
        '${permittedRightsBases.join(', ')}',
      );
      return errors;
    }

    if (requiresLicenseRef(value) &&
        (licenseRef == null || licenseRef.trim().isEmpty)) {
      errors.add('rightsBasis "$value" requires a non-empty licenseRef');
    }

    if (requiresAttribution(value) &&
        (attributionText == null || attributionText.trim().isEmpty)) {
      errors.add(
        'rightsBasis "$value" requires a non-empty attributionText',
      );
    }

    return errors;
  }
}
