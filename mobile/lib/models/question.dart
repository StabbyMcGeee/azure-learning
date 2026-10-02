/// A single study question.
///
/// The mobile v1 bank is intentionally empty at runtime. The legacy 133
/// desktop questions are NOT carried into this build because their rights are
/// unresolved. Synthetic fixtures may be injected in tests only.
///
/// Questions loaded from a [ContentPack] carry [source] and [rightsBasis]
/// provenance metadata; legacy rows may leave these null.
class Question {
  final String id;
  final String text;
  final List<String> options;
  final int correctOptionIndex;
  final String? explanation;
  final String domain;
  final String difficulty;
  final String? source;
  final String? rightsBasis;
  final String? packId;
  final String? courseId;

  const Question({
    required this.id,
    required this.text,
    required this.options,
    required this.correctOptionIndex,
    this.explanation,
    required this.domain,
    required this.difficulty,
    this.source,
    this.rightsBasis,
    this.packId,
    this.courseId,
  });

  Map<String, dynamic> toMap() => {
        'id': id,
        'text': text,
        'options': options.join('\n'),
        'correctOptionIndex': correctOptionIndex,
        'explanation': explanation,
        'domain': domain,
        'difficulty': difficulty,
        'source': source,
        'rightsBasis': rightsBasis,
        'packId': packId,
        'courseId': courseId,
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
      source: map['source'] as String?,
      rightsBasis: map['rightsBasis'] as String?,
      packId: map['packId'] as String?,
      courseId: map['courseId'] as String?,
    );
  }

  bool isCorrect(int selectedIndex) => selectedIndex == correctOptionIndex;
}
