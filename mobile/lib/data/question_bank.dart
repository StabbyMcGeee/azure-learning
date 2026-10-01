import '../models/question.dart';

/// The runtime question bank.
///
/// v1 intentionally starts empty. The legacy desktop 133-question bank is NOT
/// imported because content rights are unresolved. Real curriculum content must
/// be human-authored and rights-cleared before it is loaded here.
class QuestionBank {
  static const List<Question> productionBank = [];

  /// Synthetic fixtures for automated tests only. Never ship these as
  /// production curriculum.
  static List<Question> syntheticFixtures() => const [
        Question(
          id: 'fixture-001',
          text: 'Which cloud trait lets you pay only for resources you use?',
          options: [
            'High availability',
            'Fault tolerance',
            'Scalability',
            'Elasticity',
          ],
          correctOptionIndex: 3,
          explanation: 'Elasticity is the ability to scale resources up or down '
              'and pay for what you use.',
          domain: 'Cloud Concepts',
          difficulty: 'easy',
        ),
        Question(
          id: 'fixture-002',
          text: 'What is an example of capital expenditure (CapEx)?',
          options: [
            'Paying per hour for virtual machines',
            'Buying server hardware upfront',
            'A monthly SaaS subscription',
            'A per-API-call charge',
          ],
          correctOptionIndex: 1,
          explanation: 'CapEx is upfront spending on physical assets such as '
              'server hardware.',
          domain: 'Cloud Concepts',
          difficulty: 'easy',
        ),
        Question(
          id: 'fixture-003',
          text: 'Which service model provides the highest level of management '
              'by the cloud provider?',
          options: [
            'Infrastructure as a Service (IaaS)',
            'Platform as a Service (PaaS)',
            'Software as a Service (SaaS)',
            'Function as a Service (FaaS)',
          ],
          correctOptionIndex: 2,
          explanation: 'SaaS delivers fully managed applications.',
          domain: 'Cloud Architecture',
          difficulty: 'medium',
        ),
      ];
}
