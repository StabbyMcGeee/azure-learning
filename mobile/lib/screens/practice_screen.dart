import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../data/local_store.dart';
import '../models/attempt.dart';
import '../models/question.dart';
import '../widgets/empty_state.dart';
import '../widgets/question_card.dart';

/// Free-form practice mode.
///
/// Questions come from the store, scoped to the learner's selected course. The
/// empty state is reached only when no pack is loaded or the selected course
/// has no items; this screen never seeds content of its own.
class PracticeScreen extends StatefulWidget {
  const PracticeScreen({super.key});

  @override
  State<PracticeScreen> createState() => _PracticeScreenState();
}

class _PracticeScreenState extends State<PracticeScreen> {
  LocalStore get _store => context.read<LocalStore>();
  List<Question> _questions = [];
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
    final questions = await _store.getQuestions(courseId: courseId);
    if (mounted) {
      setState(() {
        _questions = questions;
        _loaded = true;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Practice')),
      body: _body(),
    );
  }

  Widget _body() {
    if (!_loaded) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_questions.isEmpty) {
      return const EmptyState(
        icon: Icons.quiz,
        title: 'No practice questions yet',
        message:
            'Load rights-cleared questions to start practicing. '
            'No legacy desktop questions are imported.',
      );
    }
    final question = _questions[_index];
    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12.0, vertical: 8.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text('Question ${_index + 1} of ${_questions.length}'),
              Text(question.difficulty.toUpperCase()),
            ],
          ),
        ),
        Expanded(
          child: QuestionCard(
            question: question,
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
                  child: Text(_index < _questions.length - 1 ? 'Next' : 'Finish'),
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
    final question = _questions[_index];
    final correct = question.isCorrect(_selected!);
    await _store.recordAttempt(Attempt(
      questionId: question.id,
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
      if (_index < _questions.length - 1) {
        _index++;
        _selected = null;
        _showResult = false;
      } else {
        Navigator.pop(context);
      }
    });
  }
}
