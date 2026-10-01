/// A practice or exam session result.
class StudySession {
  final String id;
  final String mode; // 'practice' | 'exam'
  final DateTime startedAt;
  final DateTime finishedAt;
  final int questionCount;
  final int correctCount;
  final int? scorePercent; // null for unscored practice, 0-100 for exams

  const StudySession({
    required this.id,
    required this.mode,
    required this.startedAt,
    required this.finishedAt,
    required this.questionCount,
    required this.correctCount,
    this.scorePercent,
  });

  Map<String, dynamic> toMap() => {
        'id': id,
        'mode': mode,
        'startedAt': startedAt.millisecondsSinceEpoch,
        'finishedAt': finishedAt.millisecondsSinceEpoch,
        'questionCount': questionCount,
        'correctCount': correctCount,
        'scorePercent': scorePercent,
      };

  factory StudySession.fromMap(Map<String, dynamic> map) => StudySession(
        id: map['id'] as String,
        mode: map['mode'] as String,
        startedAt: DateTime.fromMillisecondsSinceEpoch(map['startedAt'] as int),
        finishedAt:
            DateTime.fromMillisecondsSinceEpoch(map['finishedAt'] as int),
        questionCount: map['questionCount'] as int,
        correctCount: map['correctCount'] as int,
        scorePercent: map['scorePercent'] as int?,
      );
}
