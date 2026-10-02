import '../models/question.dart';

/// The hardcoded question bank.
///
/// This list is intentionally empty. The app's runtime questions are loaded
/// from the bundled content pack (`assets/content-pack.json`) by
/// `ContentPackLoader`, not from this list. Every slot of the existing desktop
/// 133-question bank was rewritten from scratch; production content is authored
/// fresh in the pack with a recorded rights basis.
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
          courseId: 'AZ-900',
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
          courseId: 'AZ-900',
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
          courseId: 'AZ-900',
          difficulty: 'medium',
        ),
      ];
}
