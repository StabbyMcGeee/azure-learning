import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../data/local_store.dart';
import '../navigation/app_router.dart';
import '../widgets/empty_state.dart';

/// Study mode landing screen.
///
/// Shows the empty-content state when no rights-cleared curriculum has been
/// loaded, and scopes any loaded study material to the selected course.
class StudyScreen extends StatefulWidget {
  const StudyScreen({super.key});

  @override
  State<StudyScreen> createState() => _StudyScreenState();
}

class _StudyScreenState extends State<StudyScreen> {
  LocalStore get _store => context.read<LocalStore>();
  String? _selectedCourseId;
  int _questionCount = 0;
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
        _selectedCourseId = courseId;
        _questionCount = questions.length;
        _loaded = true;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    if (!_loaded) {
      return Scaffold(
        appBar: AppBar(title: const Text('Study')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }
    if (_questionCount == 0) {
      return Scaffold(
        appBar: AppBar(title: const Text('Study')),
        body: EmptyState(
          icon: Icons.menu_book,
          title: 'Study material is empty',
          message: _selectedCourseId == null
              ? 'The first release curriculum has not been loaded. '
                  'Once human-authored, rights-cleared content is ready, '
                  'it will appear here for offline study.'
              : 'No study material is available for $_selectedCourseId yet.',
          actionLabel: 'Go to Practice',
          onAction: () => Navigator.pushNamed(context, AppRouter.practice),
        ),
      );
    }
    return Scaffold(
      appBar: AppBar(title: const Text('Study')),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                _selectedCourseId == null
                    ? 'Study material'
                    : 'Study material for $_selectedCourseId',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 8),
              Text('$_questionCount questions available offline'),
            ],
          ),
        ),
      ),
    );
  }
}
