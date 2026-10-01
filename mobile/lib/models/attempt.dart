import 'question.dart';

/// A recorded answer attempt, used for progress and spaced-repetition review.
class Attempt {
  final String questionId;
  final int selectedOptionIndex;
  final bool correct;
  final DateTime timestamp;

  const Attempt({
    required this.questionId,
    required this.selectedOptionIndex,
    required this.correct,
    required this.timestamp,
  });

  Map<String, dynamic> toMap() => {
        'questionId': questionId,
        'selectedOptionIndex': selectedOptionIndex,
        'correct': correct ? 1 : 0,
        'timestamp': timestamp.millisecondsSinceEpoch,
      };

  factory Attempt.fromMap(Map<String, dynamic> map) => Attempt(
        questionId: map['questionId'] as String,
        selectedOptionIndex: map['selectedOptionIndex'] as int,
        correct: map['correct'] == 1,
        timestamp: DateTime.fromMillisecondsSinceEpoch(map['timestamp'] as int),
      );
}

/// Convenience pairing of a question and its latest review state.
class ReviewItem {
  final Question question;
  final DateTime? nextReview;
  final int consecutiveCorrect;

  const ReviewItem({
    required this.question,
    required this.nextReview,
    required this.consecutiveCorrect,
  });
}
