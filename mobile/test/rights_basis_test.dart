import 'package:flutter_test/flutter_test.dart';
import 'package:study_app/legal/rights_basis.dart';

void main() {
  group('RightsBasis validation', () {
    test('accepts all permitted values without companion fields when not required',
        () {
      for (final basis in permittedRightsBases) {
        if (!RightsBasis.requiresLicenseRef(basis)) {
          expect(RightsBasis.validate(basis), isEmpty);
        }
      }
    });

    test('rejects an unknown rightsBasis value', () {
      final errors = RightsBasis.validate('made-up-basis');
      expect(errors, isNotEmpty);
      expect(errors.first, contains('not one of the permitted values'));
    });

    test('requires licenseRef for licensed-cc-by-4.0 and attributionText', () {
      final errors = RightsBasis.validate('licensed-cc-by-4.0');
      expect(errors, hasLength(2));
      expect(errors, everyElement(contains('requires')));
    });

    test('accepts licensed-cc-by-4.0 with both companion fields', () {
      final errors = RightsBasis.validate(
        'licensed-cc-by-4.0',
        licenseRef: 'https://example.com/license',
        attributionText: 'CC BY 4.0 — Example Author',
      );
      expect(errors, isEmpty);
    });

    test('requires licenseRef for licensed-commercial', () {
      final errors = RightsBasis.validate('licensed-commercial');
      expect(errors, hasLength(1));
      expect(errors.first, contains('licenseRef'));
    });

    test('accepts licensed-commercial with licenseRef', () {
      final errors = RightsBasis.validate(
        'licensed-commercial',
        licenseRef: 'Commercial licence #123',
      );
      expect(errors, isEmpty);
    });

    test('does not require licenseRef for original-human', () {
      expect(
        RightsBasis.validate('original-human', licenseRef: null),
        isEmpty,
      );
    });
  });
}
