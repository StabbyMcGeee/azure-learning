import 'package:flutter/material.dart';

import '../models/question.dart';

/// Displays a question prompt and its answer options.
class QuestionCard extends StatelessWidget {
  final Question question;
  final int? selectedIndex;
  final bool showResult;
  final ValueChanged<int>? onSelect;

  const QuestionCard({
    super.key,
    required this.question,
    this.selectedIndex,
    this.showResult = false,
    this.onSelect,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      elevation: 2,
      margin: const EdgeInsets.all(12.0),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              question.domain,
              style: theme.textTheme.labelLarge?.copyWith(
                    color: theme.colorScheme.primary,
                    fontWeight: FontWeight.bold,
                  ),
            ),
            const SizedBox(height: 8),
            Text(
              question.text,
              style: theme.textTheme.titleMedium,
            ),
            const SizedBox(height: 16),
            ...question.options.asMap().entries.map((entry) {
              final index = entry.key;
              final text = entry.value;
              final bool correct = index == question.correctOptionIndex;
              Color? tileColor;
              Widget? trailing;
              if (showResult) {
                if (correct) {
                  tileColor = Colors.green.withAlpha((0.15 * 255).toInt());
                  trailing = const Icon(Icons.check_circle, color: Colors.green);
                } else if (index == selectedIndex) {
                  tileColor = Colors.red.withAlpha((0.15 * 255).toInt());
                  trailing = const Icon(Icons.cancel, color: Colors.red);
                }
              }
              return Padding(
                padding: const EdgeInsets.symmetric(vertical: 4.0),
                child: ListTile(
                  title: Text(text),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(8.0),
                  ),
                  tileColor: tileColor,
                  trailing: trailing,
                  selected: selectedIndex == index,
                  selectedTileColor:
                      theme.colorScheme.primaryContainer.withAlpha((0.3 * 255).toInt()),
                  onTap: onSelect == null ? null : () => onSelect!(index),
                ),
              );
            }),
            if (showResult && question.explanation != null) ...[
              const SizedBox(height: 16),
              Text(
                'Explanation:',
                style: theme.textTheme.titleSmall,
              ),
              const SizedBox(height: 4),
              Text(question.explanation!),
            ],
          ],
        ),
      ),
    );
  }
}
