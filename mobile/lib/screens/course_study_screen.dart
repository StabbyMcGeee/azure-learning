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
  List<_StudyRow> _rows = const [];
  StudyProgress _progress = const StudyProgress(
    total: 0,
    seen: 0,
    needsReview: 0,
  );
  bool _loaded = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final questions = await _store.getQuestions(courseId: widget.courseId);
    final statuses = await _store.getStudyStatusesForCourse(widget.courseId);
    if (!mounted) return;
    setState(() {
      _rows = _planRows(questions, statuses);
      _progress = _coverage(questions, statuses);
      _loaded = true;
    });
  }

  static bool _countsAsSeen(StudyMaterialStatus? status) =>
      status == StudyMaterialStatus.seen ||
      status == StudyMaterialStatus.needsReview;

  /// Flattens the course into one row per progress card, domain header, and
  /// question so the list builder only has to build what is on screen.
  List<_StudyRow> _planRows(
    List<Question> questions,
    Map<String, StudyMaterialStatus> statuses,
  ) {
    final grouped = <String, List<Question>>{};
    for (final q in questions) {
      grouped.putIfAbsent(q.domain, () => <Question>[]).add(q);
    }

    final rows = <_StudyRow>[const _ProgressRow()];
    for (final entry in grouped.entries) {
      final items = entry.value;
      rows.add(_DomainRow(
        domain: entry.key,
        seen: items.where((q) => _countsAsSeen(statuses[q.id])).length,
        total: items.length,
      ));
      for (final q in items) {
        rows.add(_QuestionRow(
          question: q,
          status: statuses[q.id],
        ));
      }
    }
    return rows;
  }

  StudyProgress _coverage(
    List<Question> questions,
    Map<String, StudyMaterialStatus> statuses,
  ) {
    var seen = 0;
    var needsReview = 0;
    for (final q in questions) {
      final status = statuses[q.id];
      if (_countsAsSeen(status)) seen++;
      if (status == StudyMaterialStatus.needsReview) needsReview++;
    }
    return StudyProgress(
      total: questions.length,
      seen: seen,
      needsReview: needsReview,
    );
  }

  Future<void> _mark(String questionId, StudyMaterialStatus status) async {
    await _store.saveStudyStatus(
      courseId: widget.courseId,
      questionId: questionId,
      status: status,
    );
    await _load();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(widget.courseId)),
      body: _body(),
    );
  }

  Widget _body() {
    if (!_loaded) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_progress.total == 0) {
      return EmptyState(
        icon: Icons.menu_book,
        title: '${widget.courseId} has no material',
        message:
            'This course does not have any loaded study content yet. '
            'Content will appear here once it is available.',
      );
    }

    return RefreshIndicator(
      onRefresh: _load,
      child: ListView.builder(
        padding: const EdgeInsets.only(bottom: 24.0),
        itemCount: _rows.length,
        itemBuilder: (context, index) => _buildRow(context, _rows[index]),
      ),
    );
  }

  Widget _buildRow(BuildContext context, _StudyRow row) {
    final theme = Theme.of(context);
    return switch (row) {
      _ProgressRow() => _progressCard(theme, _progress),
      _DomainRow(:final domain, :final seen, :final total) =>
        _domainHeader(theme, domain: domain, seen: seen, total: total),
      _QuestionRow(:final question, :final status) => Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 6.0),
          child: _StudyItem(
            question: question,
            status: status,
            onMarkSeen: () => _mark(question.id, StudyMaterialStatus.seen),
            onMarkNeedsReview: () =>
                _mark(question.id, StudyMaterialStatus.needsReview),
          ),
        ),
    };
  }

  Widget _progressCard(ThemeData theme, StudyProgress progress) {
    return Card(
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
    );
  }

  Widget _domainHeader(
    ThemeData theme, {
    required String domain,
    required int seen,
    required int total,
  }) {
    return Padding(
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
            '$seen/$total',
            style: theme.textTheme.bodySmall,
          ),
        ],
      ),
    );
  }
}

sealed class _StudyRow {
  const _StudyRow();
}

class _ProgressRow extends _StudyRow {
  const _ProgressRow();
}

class _DomainRow extends _StudyRow {
  final String domain;
  final int seen;
  final int total;

  const _DomainRow({
    required this.domain,
    required this.seen,
    required this.total,
  });
}

class _QuestionRow extends _StudyRow {
  final Question question;
  final StudyMaterialStatus? status;

  const _QuestionRow({
    required this.question,
    required this.status,
  });
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
        Wrap(
          spacing: 8.0,
          runSpacing: 8.0,
          crossAxisAlignment: WrapCrossAlignment.center,
          children: [
            _statusChip(theme),
            OutlinedButton(
              onPressed: onMarkSeen,
              child: const Text('Mark seen'),
            ),
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
