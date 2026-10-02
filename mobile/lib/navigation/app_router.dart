import 'package:flutter/material.dart';

import '../screens/about_legal_screen.dart';
import '../screens/dashboard_screen.dart';
import '../screens/exam_result_screen.dart';
import '../screens/exam_screen.dart';
import '../screens/practice_screen.dart';
import '../screens/progress_screen.dart';
import '../screens/review_screen.dart';
import '../screens/study_screen.dart';

class AppRouter {
  static const String dashboard = '/';
  static const String study = '/study';
  static const String practice = '/practice';
  static const String exam = '/exam';
  static const String examResult = '/exam/result';
  static const String review = '/review';
  static const String progress = '/progress';
  static const String aboutLegal = '/about-legal';

  static Route<dynamic>? onGenerateRoute(RouteSettings settings) {
    final name = settings.name;
    if (name == dashboard) {
      return MaterialPageRoute(builder: (_) => const DashboardScreen());
    }
    if (name == study) {
      return MaterialPageRoute(builder: (_) => const StudyScreen());
    }
    if (name == practice) {
      return MaterialPageRoute(builder: (_) => const PracticeScreen());
    }
    if (name == exam) {
      return MaterialPageRoute(builder: (_) => const ExamScreen());
    }
    if (name == examResult) {
      final args = settings.arguments as Map<String, dynamic>?;
      return MaterialPageRoute(
        builder: (_) => ExamResultScreen(
          correctCount: args?['correctCount'] as int? ?? 0,
          questionCount: args?['questionCount'] as int? ?? 0,
          sessionId: args?['sessionId'] as String? ?? '',
        ),
      );
    }
    if (name == review) {
      return MaterialPageRoute(builder: (_) => const ReviewScreen());
    }
    if (name == progress) {
      return MaterialPageRoute(builder: (_) => const ProgressScreen());
    }
    if (name == aboutLegal) {
      return MaterialPageRoute(builder: (_) => const AboutLegalScreen());
    }
    return null;
  }
}
