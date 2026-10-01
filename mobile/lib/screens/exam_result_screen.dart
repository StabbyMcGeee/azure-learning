import 'package:flutter/material.dart';

import '../navigation/app_router.dart';

/// Result screen shown after an exam finishes.
class ExamResultScreen extends StatelessWidget {
  final int correctCount;
  final int questionCount;
  final String sessionId;

  const ExamResultScreen({
    super.key,
    required this.correctCount,
    required this.questionCount,
    required this.sessionId,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final percent = questionCount == 0
        ? 0
        : ((correctCount / questionCount) * 100).round();
    return Scaffold(
      appBar: AppBar(title: const Text('Exam Result')),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(
                'Exam complete',
                style: theme.textTheme.headlineSmall,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 24),
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(24.0),
                  child: Column(
                    children: [
                      Text(
                        '$percent%',
                        style: theme.textTheme.displayLarge,
                      ),
                      const SizedBox(height: 8),
                      Text(
                        '$correctCount / $questionCount correct',
                        style: theme.textTheme.titleMedium,
                      ),
                      const SizedBox(height: 8),
                      Text('Session: $sessionId'),
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 16),
              Text(
                'This is a study estimate only and does not guarantee '
                'performance on any official certification exam.',
                style: theme.textTheme.bodySmall,
                textAlign: TextAlign.center,
              ),
              const Spacer(),
              FilledButton(
                onPressed: () => Navigator.pushNamedAndRemoveUntil(
                  context,
                  AppRouter.dashboard,
                  (route) => false,
                ),
                child: const Text('Back to Dashboard'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
