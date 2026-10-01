/// A single study question.
///
/// The mobile v1 bank is intentionally empty at runtime. The legacy 133
/// desktop questions are NOT carried into this build because their rights are
/// unresolved. Synthetic fixtures may be injected in tests only.
class Question {
  final String id;
  final String text;
  final List<String> options;
  final int correctOptionIndex;
  final String? explanation;
  final String domain;
  final String difficulty;

  const Question({
    required this.id,
    required this.text,
    required this.options,
    required this.correctOptionIndex,
    this.explanation,
    required this.domain,
    required this.difficulty,
  });

  Map<String, dynamic> toMap() => {
        'id': id,
        'text': text,
        'options': options.join('\n'),
        'correctOptionIndex': correctOptionIndex,
        'explanation': explanation,
        'domain': domain,
        'difficulty': difficulty,
      };

  factory Question.fromMap(Map<String, dynamic> map) {
    final rawOptions = map['options'] as String?;
    return Question(
      id: map['id'] as String,
      text: map['text'] as String,
      options: rawOptions?.split('\n') ?? const [],
      correctOptionIndex: map['correctOptionIndex'] as int,
      explanation: map['explanation'] as String?,
      domain: map['domain'] as String,
      difficulty: map['difficulty'] as String,
    );
  }

  bool isCorrect(int selectedIndex) => selectedIndex == correctOptionIndex;
}
