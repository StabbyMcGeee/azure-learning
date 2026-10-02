import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../data/local_store.dart';
import '../models/question.dart';
import '../navigation/app_router.dart';
import '../widgets/empty_state.dart';

/// Study mode landing screen.
///
/// Shows the empty-content state when nothing is loaded in the bank, scopes
/// loaded study material to the selected course, and lets learners choose a
/// course to browse its material grouped by domain. Studying is untimed and
/// unscored and does not record attempts.
class StudyScreen extends StatefulWidget {
  const StudyScreen({super.key});

  @override
  State<StudyScreen> createState() => _StudyScreenState();
}

class _StudyScreenState extends State<StudyScreen> {
  LocalStore get _store => context.read<LocalStore>();
  List<Question> _questions = [];
  bool _loaded = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final questions = await _store.getQuestions();
    if (mounted) {
      setState(() {
        _questions = questions;
        _loaded = true;
      });
    }
  }

  List<String> get _courses {
    final courses = _questions
        .map((q) => q.courseId)
        .where((c) => c != null && c.isNotEmpty)
        .cast<String>()
        .toSet()
        .toList();
    courses.sort();
    return courses;
  }

  Map<String, int> get _courseTotals {
    final totals = <String, int>{};
    for (final q in _questions) {
      final courseId = q.courseId;
      if (courseId != null && courseId.isNotEmpty) {
        totals[courseId] = (totals[courseId] ?? 0) + 1;
      }
    }
    return totals;
  }

  Map<String, Set<String>> get _courseDomains {
    final domains = <String, Set<String>>{};
    for (final q in _questions) {
      final courseId = q.courseId;
      if (courseId != null && courseId.isNotEmpty) {
        domains.putIfAbsent(courseId, () => {}).add(q.domain);
      }
    }
    return domains;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Study')),
      body: _body(),
    );
  }

  Widget _body() {
    if (!_loaded) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_questions.isEmpty) {
      return const EmptyState(
        icon: Icons.menu_book,
        title: 'No study material yet',
        message:
            'Your courses will appear here once content is loaded. '
            'Study offline at your own pace—no timer, no score.',
      );
    }

    final courses = _courses;
    final totals = _courseTotals;
    final domains = _courseDomains;

    return RefreshIndicator(
      onRefresh: _load,
      child: ListView.builder(
        padding: const EdgeInsets.all(12.0),
        itemCount: courses.length,
        itemBuilder: (context, index) {
          final courseId = courses[index];
          return _CourseCard(
            courseId: courseId,
            totalQuestions: totals[courseId] ?? 0,
            domainCount: domains[courseId]?.length ?? 0,
            onTap: () => Navigator.pushNamed(
              context,
              AppRouter.courseStudy,
              arguments: {'courseId': courseId},
            ),
          );
        },
      ),
    );
  }
}

class _CourseCard extends StatelessWidget {
  final String courseId;
  final int totalQuestions;
  final int domainCount;
  final VoidCallback onTap;

  const _CourseCard({
    required this.courseId,
    required this.totalQuestions,
    required this.domainCount,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                courseId,
                style: theme.textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
              ),
              const SizedBox(height: 8),
              Text(
                '$totalQuestions study items · $domainCount domain${domainCount == 1 ? '' : 's'}',
                style: theme.textTheme.bodyMedium,
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Text(
                    'Browse material',
                    style: theme.textTheme.labelLarge?.copyWith(
                          color: theme.colorScheme.primary,
                        ),
                  ),
                  const SizedBox(width: 4),
                  Icon(
                    Icons.arrow_forward,
                    color: theme.colorScheme.primary,
                    size: 18,
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
