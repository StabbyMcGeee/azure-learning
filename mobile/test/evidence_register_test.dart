import 'package:flutter_test/flutter_test.dart';
import 'package:study_app/legal/evidence_register.dart';

Map<String, dynamic> _validItem() => {
  'itemId': 'az900-001',
  'courseId': 'az-900',
  'version': 1,
  'contentHash': 'sha256:abcdef',
  'objectiveId': 'az-900/AA.3/3.redundancy-options',
  'outlineSnapshot': {
    'url': 'https://example.com/az-900-outline',
    'retrievedAt': '2026-10-02',
    'skillsMeasuredAsOf': '2026-07-20',
    'contentHash': 'sha256:outline',
  },
  'factSheetId': 'fs-az900-001',
  'factSources': [
    {
      'url': 'https://example.com/source-a',
      'retrievedAt': '2026-10-02',
      'licenseClass': 'cc-by-4.0-repo',
    },
    {
      'url': 'https://example.com/source-b',
      'retrievedAt': '2026-10-02',
      'licenseClass': 'public-fact',
    },
  ],
  'termRefs': ['tr:redundancy-options'],
  'author': 'Author One',
  'authoredAt': '2026-10-02',
  'aiAssistance': 'none',
  'noExposureAttestation': {
    'authorId': 'author-one',
    'date': '2026-10-02',
    'examSat': [],
    'ndaBound': [],
  },
  'techReviewer': 'Reviewer A',
  'techReviewedAt': '2026-10-03',
  'rightsReviewer': 'Reviewer B',
  'rightsReviewedAt': '2026-10-03',
  'similarityReport': {
    'tool': 'internal-token-run',
    'version': '1',
    'thresholds': {'maxRunLen': 6},
    'comparedTo': ['https://example.com/source-a'],
    'resultHash': 'sha256:sim',
    'maxRunLen': 0,
  },
  'rightsBasis': 'original-human',
  'locale': 'en-US',
  'status': 'released',
  'lastVerifiedAt': '2026-10-02',
  'outlineVersionAtVerify': '2026-07-20',
};

void main() {
  group('EvidenceRegisterValidator', () {
    test('accepts a valid register list', () {
      final errors = EvidenceRegisterValidator.validateRegister([
        _validItem(),
      ]);
      expect(errors, isEmpty);
    });

    test('accepts a valid register object with items key', () {
      final errors = EvidenceRegisterValidator.validateRegister({
        'items': [_validItem()],
      });
      expect(errors, isEmpty);
    });

    test('rejects an unknown rightsBasis value', () {
      final item = _validItem();
      item['rightsBasis'] = 'unknown-basis';
      final errors = EvidenceRegisterValidator.validateItem(item);
      expect(errors, isNotEmpty);
      expect(errors, contains(contains('Invalid rightsBasis')));
    });

    test('requires licenseRef and attributionText for licensed-cc-by-4.0', () {
      final item = _validItem();
      item['rightsBasis'] = 'licensed-cc-by-4.0';
      item['licenseRef'] = null;
      item['attributionText'] = null;
      final errors = EvidenceRegisterValidator.validateItem(item);
      expect(errors, isNotEmpty);
      expect(
        errors,
        contains(contains('requires a non-empty licenseRef')),
      );
      expect(
        errors,
        contains(contains('requires a non-empty attributionText')),
      );
    });

    test('rejects a withdrawn item with invalid withdrawalReason', () {
      final item = _validItem();
      item['status'] = 'withdrawn';
      item['withdrawnAt'] = '2026-10-02';
      item['withdrawalReason'] = 'not-a-reason';
      final errors = EvidenceRegisterValidator.validateItem(item);
      expect(errors, isNotEmpty);
      expect(errors, contains(contains('Invalid withdrawalReason')));
    });

    test('rejects released item with fewer than two factSources', () {
      final item = _validItem();
      item['factSources'] = [
        {
          'url': 'https://example.com/source-a',
          'retrievedAt': '2026-10-02',
          'licenseClass': 'cc-by-4.0-repo',
        },
      ];
      final errors = EvidenceRegisterValidator.validateItem(item);
      expect(errors, contains(contains('at least 2 factSources')));
    });

    test('rejects released item where reviewers equal author', () {
      final item = _validItem();
      item['techReviewer'] = 'Author One';
      item['rightsReviewer'] = 'Author One';
      final errors = EvidenceRegisterValidator.validateItem(item);
      expect(errors, contains(contains('techReviewer must differ from author')));
      expect(
        errors,
        contains(contains('rightsReviewer must differ from author')),
      );
    });

    test('rejects invalid licenseClass in factSources', () {
      final item = _validItem();
      (item['factSources'] as List<dynamic>).first['licenseClass'] =
          'not-a-license';
      final errors = EvidenceRegisterValidator.validateItem(item);
      expect(errors, contains(contains('Invalid factSources[0].licenseClass')));
    });

    test('rejects duplicate itemIds in a register', () {
      final item = _validItem();
      final errors = EvidenceRegisterValidator.validateRegister([
        item,
        item,
      ]);
      expect(errors, contains(contains('duplicate itemId')));
    });

    test('validates a legacy withdrawn item with null evidence fields', () {
      final item = {
        'itemId': 'az900-000',
        'courseId': 'az-900',
        'version': 0,
        'contentHash': 'sha256:legacy',
        'objectiveId': 'az-900/DC.1/1.cloud',
        'outlineSnapshot': {
          'url': 'https://example.com/az-900-outline',
          'retrievedAt': '2026-10-02',
          'skillsMeasuredAsOf': '2026-07-20',
          'contentHash': 'sha256:outline',
        },
        'factSheetId': null,
        'factSources': null,
        'termRefs': [],
        'author': null,
        'authoredAt': null,
        'aiAssistance': null,
        'noExposureAttestation': null,
        'techReviewer': null,
        'techReviewedAt': null,
        'rightsReviewer': null,
        'rightsReviewedAt': null,
        'similarityReport': null,
        'rightsBasis': null,
        'locale': null,
        'status': 'withdrawn',
        'withdrawnAt': '2026-10-02',
        'withdrawalReason': 'rights-basis-failed',
        'lastVerifiedAt': null,
        'outlineVersionAtVerify': null,
      };
      final errors = EvidenceRegisterValidator.validateItem(item);
      // A legacy withdrawn item is accepted with null evidence fields because
      // the withdrawal reason documents why it cannot be released.
      expect(errors, isEmpty);
      expect(
        errors,
        isNot(contains(contains('Invalid withdrawalReason'))),
      );
    });
  });
}
