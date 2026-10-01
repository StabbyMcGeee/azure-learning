import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../data/local_store.dart';
import '../models/attempt.dart';
import '../models/session.dart';

/// Progress and persistence screen.
///
/// Shows recorded attempts and exam sessions stored locally.
class ProgressScreen extends StatefulWidget {
  const ProgressScreen({super.key});

  @override
  State<ProgressScreen> createState() => _ProgressScreenState();
}

class _ProgressScreenState extends State<ProgressScreen> {
  LocalStore get _store => context.read<LocalStore>();
  List<Attempt> _attempts = [];
  List<StudySession> _sessions = [];
  bool _loaded = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final attempts = await _store.getAllAttempts();
    final sessions = await _store.getSessions();
    if (mounted) {
      setState(() {
        _attempts = attempts;
        _sessions = sessions;
        _loaded = true;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('Progress')),
      body: _loaded
          ? RefreshIndicator(
              onRefresh: _load,
              child: ListView(
                padding: const EdgeInsets.all(16.0),
                children: [
                  _statCard(theme),
                  const SizedBox(height: 16),
                  Text('Recent exam sessions', style: theme.textTheme.titleMedium),
                  const SizedBox(height: 8),
                  if (_sessions.isEmpty)
                    const Text('No exam sessions yet.')
                  else
                    ..._sessions.map((s) => ListTile(
                          title: Text('${s.mode.toUpperCase()} — ${s.scorePercent}%'),
                          subtitle: Text(
                            '${s.correctCount}/${s.questionCount} correct · '
                            '${s.finishedAt.toLocal()}',
                          ),
                        )),
                  const SizedBox(height: 16),
                  Text('Recent attempts', style: theme.textTheme.titleMedium),
                  const SizedBox(height: 8),
                  if (_attempts.isEmpty)
                    const Text('No attempts yet.')
                  else
                    ..._attempts.take(20).map((a) => ListTile(
                          leading: Icon(
                            a.correct ? Icons.check_circle : Icons.cancel,
                            color: a.correct ? Colors.green : Colors.red,
                          ),
                          title: Text(a.questionId),
                          subtitle: Text(a.timestamp.toLocal().toString()),
                        )),
                ],
              ),
            )
          : const Center(child: CircularProgressIndicator()),
    );
  }

  Widget _statCard(ThemeData theme) {
    final total = _attempts.length;
    final correct = _attempts.where((a) => a.correct).length;
    final accuracy = total == 0 ? 0 : ((correct / total) * 100).round();
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Lifetime accuracy', style: theme.textTheme.titleMedium),
            const SizedBox(height: 8),
            Text(
              '$accuracy%',
              style: theme.textTheme.displayMedium,
            ),
            Text('$correct correct out of $total attempts'),
          ],
        ),
      ),
    );
  }
}
