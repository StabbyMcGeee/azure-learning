import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../data/local_store.dart';
import '../models/attempt.dart';
import '../widgets/empty_state.dart';
import '../widgets/question_card.dart';

/// Spaced-repetition review screen showing questions that are due.
class ReviewScreen extends StatefulWidget {
  const ReviewScreen({super.key});

  @override
  State<ReviewScreen> createState() => _ReviewScreenState();
}

class _ReviewScreenState extends State<ReviewScreen> {
  LocalStore get _store => context.read<LocalStore>();
  List<ReviewItem> _due = [];
  int _index = 0;
  int? _selected;
  bool _showResult = false;
  bool _loaded = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final courseId = await _store.getSelectedCourseId();
    final due = await _store.getDueReviewItems(courseId: courseId);
    if (mounted) {
      setState(() {
        _due = due;
        _loaded = true;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Review')),
      body: _body(),
    );
  }

  Widget _body() {
    if (!_loaded) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_due.isEmpty) {
      return const EmptyState(
        icon: Icons.repeat,
        title: 'Nothing to review',
        message:
            'You have no due questions. Come back after practicing or taking an exam.',
      );
    }
    final item = _due[_index];
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('Review ${_index + 1} of ${_due.length}'),
              Text('Streak: ${item.consecutiveCorrect}'),
            ],
          ),
        ),
        Expanded(
          child: QuestionCard(
            question: item.question,
            selectedIndex: _selected,
            showResult: _showResult,
            onSelect: _showResult ? null : _select,
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(16.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              if (_showResult)
                FilledButton(
                  onPressed: _next,
                  child: Text(_index < _due.length - 1 ? 'Next' : 'Done'),
                )
              else
                FilledButton(
                  onPressed: _selected == null ? null : _submit,
                  child: const Text('Submit'),
                ),
            ],
          ),
        ),
      ],
    );
  }

  void _select(int index) {
    setState(() {
      _selected = index;
    });
  }

  Future<void> _submit() async {
    final item = _due[_index];
    final correct = item.question.isCorrect(_selected!);
    await _store.recordAttempt(Attempt(
      questionId: item.question.id,
      courseId: item.question.courseId,
      selectedOptionIndex: _selected!,
      correct: correct,
      timestamp: DateTime.now(),
    ));
    if (mounted) {
      setState(() {
        _showResult = true;
      });
    }
  }

  void _next() {
    setState(() {
      if (_index < _due.length - 1) {
        _index++;
        _selected = null;
        _showResult = false;
      } else {
        Navigator.pop(context);
      }
    });
  }
}
