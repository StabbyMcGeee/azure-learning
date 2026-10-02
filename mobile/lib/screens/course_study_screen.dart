import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../data/local_store.dart';
import '../models/question.dart';
import '../models/study_status.dart';
import '../widgets/empty_state.dart';
import '../widgets/question_card.dart';

/// Untimed, unscored study mode for a single course.
///
/// Material is grouped by the exact domain wording carried in the content.
/// The correct answer and explanation are visible for every item, and the
/// learner can mark each question as seen or needing more work.
class CourseStudyScreen extends StatefulWidget {
  final String courseId;

  const CourseStudyScreen({super.key, required this.courseId});

  @override
  State<CourseStudyScreen> createState() => _CourseStudyScreenState();
}

class _CourseStudyScreenState extends State<CourseStudyScreen> {
  LocalStore get _store => context.read<LocalStore>();
  final Map<String, GlobalKey> _itemKeys = {};
  List<Question> _questions = [];
  Map<String, StudyMaterialStatus> _statuses = {};
  bool _loaded = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final questions = await _store.getQuestions(courseId: widget.courseId);
    final statuses = await _store.getStudyStatusesForCourse(widget.courseId);
    if (mounted) {
      setState(() {
        _questions = questions;
        _statuses = statuses;
        _loaded = true;
      });
    }
  }

  Map<String, List<Question>> get _grouped {
    final groups = <String, List<Question>>{};
    for (final q in _questions) {
      groups.putIfAbsent(q.domain, () => []).add(q);
    }
    return groups;
  }

  StudyProgress get _progress {
    int seen = 0;
    int needsReview = 0;
    for (final q in _questions) {
      final status = _statuses[q.id];
      if (status == StudyMaterialStatus.seen) {
        seen++;
      } else if (status == StudyMaterialStatus.needsReview) {
        seen++;
        needsReview++;
      }
    }
    return StudyProgress(
      courseId: widget.courseId,
      total: _questions.length,
      seen: seen,
      needsReview: needsReview,
    );
  }

  Question? get _resumeQuestion {
    for (final q in _questions) {
      final status = _statuses[q.id];
      if (status == null || status == StudyMaterialStatus.needsReview) {
        return q;
      }
    }
    return null;
  }

  Future<void> _mark(String questionId, StudyMaterialStatus status) async {
    await _store.saveStudyStatus(
      courseId: widget.courseId,
      questionId: questionId,
      status: status,
    );
    await _load();
  }

  void _scrollToResume() {
    final target = _resumeQuestion;
    if (target == null) return;
    final key = _itemKeys[target.id];
    if (key == null) return;
    final context = key.currentContext;
    if (context == null) return;
    Scrollable.ensureVisible(
      context,
      duration: const Duration(milliseconds: 300),
      alignment: 0.1,
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.courseId),
        actions: [
          if (_resumeQuestion != null)
            TextButton(
              onPressed: _scrollToResume,
              child: const Text(
                'Resume',
                style: TextStyle(color: Colors.white),
              ),
            ),
        ],
      ),
      body: _body(theme),
    );
  }

  Widget _body(ThemeData theme) {
    if (!_loaded) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_questions.isEmpty) {
      return EmptyState(
        icon: Icons.menu_book,
        title: '${widget.courseId} has no material',
        message:
            'This course does not have any loaded study content yet. '
            'Content will appear here once it is available.',
      );
    }

    final progress = _progress;
    final children = _buildListChildren(theme, progress);

    return RefreshIndicator(
      onRefresh: _load,
      child: ListView.builder(
        padding: const EdgeInsets.only(bottom: 24.0),
        itemCount: children.length,
        itemBuilder: (context, index) => children[index],
      ),
    );
  }

  List<Widget> _buildListChildren(ThemeData theme, StudyProgress progress) {
    final List<Widget> children = [];

    children.add(
      Card(
        margin: const EdgeInsets.all(12.0),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Course progress', style: theme.textTheme.titleMedium),
              const SizedBox(height: 8),
              LinearProgressIndicator(
                value: progress.coverage,
                minHeight: 8,
                borderRadius: BorderRadius.circular(4.0),
              ),
              const SizedBox(height: 8),
              Text(
                '${progress.seen} of ${progress.total} items seen'
                '${progress.needsReview > 0 ? ' · ${progress.needsReview} marked for review' : ''}',
                style: theme.textTheme.bodyMedium,
              ),
            ],
          ),
        ),
      ),
    );

    final grouped = _grouped;
    for (final domain in grouped.keys) {
      final questions = grouped[domain]!;
      final domainSeen = questions.where((q) {
        final s = _statuses[q.id];
        return s == StudyMaterialStatus.seen ||
            s == StudyMaterialStatus.needsReview;
      }).length;

      children.add(
        Padding(
          padding: const EdgeInsets.fromLTRB(12.0, 16.0, 12.0, 4.0),
          child: Row(
            children: [
              Expanded(
                child: Text(
                  domain,
                  style: theme.textTheme.titleSmall?.copyWith(
                        color: theme.colorScheme.primary,
                        fontWeight: FontWeight.bold,
                      ),
                ),
              ),
              Text(
                '$domainSeen/${questions.length}',
                style: theme.textTheme.bodySmall,
              ),
            ],
          ),
        ),
      );

      for (final q in questions) {
        final key = _itemKeys[q.id] ??= GlobalKey();
        final status = _statuses[q.id];
        children.add(
          Padding(
            key: key,
            padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 6.0),
            child: _StudyItem(
              question: q,
              status: status,
              onMarkSeen: () => _mark(q.id, StudyMaterialStatus.seen),
              onMarkNeedsReview: () => _mark(q.id, StudyMaterialStatus.needsReview),
            ),
          ),
        );
      }
    }
    return children;
  }
}

class _StudyItem extends StatelessWidget {
  final Question question;
  final StudyMaterialStatus? status;
  final VoidCallback onMarkSeen;
  final VoidCallback onMarkNeedsReview;

  const _StudyItem({
    required this.question,
    required this.status,
    required this.onMarkSeen,
    required this.onMarkNeedsReview,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        QuestionCard(
          question: question,
          showResult: true,
          showDomain: false,
          onSelect: null,
        ),
        const SizedBox(height: 8),
        Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            _statusChip(theme),
            const Spacer(),
            OutlinedButton(
              onPressed: onMarkSeen,
              child: const Text('Mark seen'),
            ),
            const SizedBox(width: 8),
            OutlinedButton(
              onPressed: onMarkNeedsReview,
              child: const Text('Needs more work'),
            ),
          ],
        ),
      ],
    );
  }

  Widget _statusChip(ThemeData theme) {
    if (status == null) {
      return Chip(
        label: const Text('New'),
        backgroundColor: theme.colorScheme.surfaceContainerHighest,
      );
    }
    if (status == StudyMaterialStatus.needsReview) {
      return const Chip(
        label: Text('Needs review'),
        backgroundColor: Colors.orange,
        labelStyle: TextStyle(color: Colors.white),
      );
    }
    return const Chip(
      label: Text('Seen'),
      backgroundColor: Colors.green,
      labelStyle: TextStyle(color: Colors.white),
    );
  }
}
