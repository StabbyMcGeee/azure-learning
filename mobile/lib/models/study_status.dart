/// Status a learner can assign to study material.
///
/// Studying is untimed and unscored, so these statuses are the only
/// per-question state recorded by the study flow.
enum StudyMaterialStatus {
  seen,
  needsReview,
}

extension StudyMaterialStatusX on StudyMaterialStatus {
  String get storageValue {
    switch (this) {
      case StudyMaterialStatus.seen:
        return 'seen';
      case StudyMaterialStatus.needsReview:
        return 'needs_review';
    }
  }

  static StudyMaterialStatus fromStorage(String value) {
    switch (value) {
      case 'seen':
        return StudyMaterialStatus.seen;
      case 'needs_review':
        return StudyMaterialStatus.needsReview;
      default:
        throw ArgumentError('Unknown study status: $value');
    }
  }
}

/// Per-course study coverage computed from the currently loaded question bank.
class StudyProgress {
  final String courseId;
  final int total;
  final int seen;
  final int needsReview;

  const StudyProgress({
    required this.courseId,
    required this.total,
    required this.seen,
    required this.needsReview,
  });

  int get remaining => total - seen;
  double get coverage => total == 0 ? 0.0 : seen / total;
  bool get complete => total > 0 && seen >= total;
}

/// A single persisted study status row.
class StudyStatusRecord {
  final String courseId;
  final String questionId;
  final StudyMaterialStatus status;
  final DateTime updatedAt;

  const StudyStatusRecord({
    required this.courseId,
    required this.questionId,
    required this.status,
    required this.updatedAt,
  });

  Map<String, dynamic> toMap() => {
        'courseId': courseId,
        'questionId': questionId,
        'status': status.storageValue,
        'updatedAt': updatedAt.millisecondsSinceEpoch,
      };

  factory StudyStatusRecord.fromMap(Map<String, dynamic> map) => StudyStatusRecord(
        courseId: map['courseId'] as String,
        questionId: map['questionId'] as String,
        status: StudyMaterialStatusX.fromStorage(map['status'] as String),
        updatedAt: DateTime.fromMillisecondsSinceEpoch(map['updatedAt'] as int),
      );
}
