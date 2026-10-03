import 'dart:math';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../data/local_store.dart';
import '../models/attempt.dart';
import '../models/question.dart';
import '../models/session.dart';
import '../navigation/app_router.dart';
import '../widgets/empty_state.dart';
import '../widgets/question_card.dart';

/// Exam simulation.
///
/// Presents a fixed-size exam set. Unanswered items are scored as wrong but
/// are not persisted as attempts or pushed into review scheduling.
class ExamScreen extends StatefulWidget {
  const ExamScreen({super.key});

  @override
  State<ExamScreen> createState() => _ExamScreenState();
}

class _ExamScreenState extends State<ExamScreen> {
  static const int _examSize = 3;
  LocalStore get _store => context.read<LocalStore>();
  List<Question> _questions = [];
  final Map<int, int> _answers = {};
  int _index = 0;
  bool _finished = false;
  bool _loaded = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final courseId = await _store.getSelectedCourseId();
    final questions = await _store.getQuestions(courseId: courseId);
    final selected = _pickExamSet(questions, _examSize);
    if (mounted) {
      setState(() {
        _questions = selected;
        _loaded = true;
      });
    }
  }

  List<Question> _pickExamSet(List<Question> source, int count) {
    if (source.length <= count) return List.unmodifiable(source);
    final random = Random();
    final shuffled = [...source]..shuffle(random);
    return List.unmodifiable(shuffled.take(count));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Exam Simulation'),
        actions: [
          if (!_finished)
            TextButton(
              onPressed: _finish,
              child: const Text('Finish', style: TextStyle(color: Colors.white)),
            ),
        ],
      ),
      body: _body(),
    );
  }

  Widget _body() {
    if (!_loaded) {
      return const Center(child: CircularProgressIndicator());
    }
    if (_questions.isEmpty) {
      return const EmptyState(
        icon: Icons.assignment,
        title: 'No exam questions available',
        message: 'No exam content is available. The bundled course content '
            'could not be loaded.',
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
              Text('Answered: ${_answers.length}/${_questions.length}'),
            ],
          ),
        ),
        Expanded(
          child: QuestionCard(
            question: question,
            selectedIndex: _answers[_index],
            showResult: _finished,
            onSelect: _finished ? null : _select,
          ),
        ),
        if (!_finished)
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                FilledButton(
                  onPressed: _index > 0 ? _previous : null,
                  child: const Text('Previous'),
                ),
                FilledButton(
                  onPressed: _index < _questions.length - 1 ? _next : _finish,
                  child: Text(_index < _questions.length - 1 ? 'Next' : 'Finish'),
                ),
              ],
            ),
          ),
      ],
    );
  }

  void _select(int index) {
    setState(() {
      _answers[_index] = index;
    });
  }

  void _previous() {
    setState(() {
      _index = max(_index - 1, 0);
    });
  }

  void _next() {
    setState(() {
      _index = min(_index + 1, _questions.length - 1);
    });
  }

  void _finish() {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Finish exam?'),
        content: Text(
          'You have answered ${_answers.length} of ${_questions.length} questions. '
          'Unanswered items will be scored as wrong.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          FilledButton(
            onPressed: () {
              Navigator.pop(context);
              _submitExam();
            },
            child: const Text('Finish'),
          ),
        ],
      ),
    );
  }

  Future<void> _submitExam() async {
    int correctCount = 0;
    final now = DateTime.now();
    for (var i = 0; i < _questions.length; i++) {
      final q = _questions[i];
      final selected = _answers[i];
      if (selected != null) {
        final correct = q.isCorrect(selected);
        if (correct) correctCount++;
        // Persist attempts only for answered items.
        await _store.recordAttempt(Attempt(
          questionId: q.id,
          courseId: q.courseId,
          selectedOptionIndex: selected,
          correct: correct,
          timestamp: now,
        ));
      }
      // Unanswered items are wrong but not persisted.
    }
    final courseIds = _questions
        .map((q) => q.courseId)
        .where((c) => c != null && c.isNotEmpty)
        .toSet();
    final sessionCourseId = courseIds.length == 1 ? courseIds.first : null;
    final sessionId = 'exam-${now.millisecondsSinceEpoch}';
    await _store.saveSession(StudySession(
      id: sessionId,
      mode: 'exam',
      courseId: sessionCourseId,
      startedAt: now.subtract(const Duration(minutes: 1)),
      finishedAt: now,
      questionCount: _questions.length,
      correctCount: correctCount,
      scorePercent: ((correctCount / _questions.length) * 100).round(),
    ));
    if (mounted) {
      setState(() {
        _finished = true;
      });
      Navigator.pushReplacementNamed(
        context,
        AppRouter.examResult,
        arguments: {
          'correctCount': correctCount,
          'questionCount': _questions.length,
          'sessionId': sessionId,
        },
      );
    }
  }
}
