import 'package:flutter/material.dart';

import '../navigation/app_router.dart';
import '../widgets/empty_state.dart';

/// Study mode landing screen.
///
/// Shows an empty-content state because no rights-cleared curriculum has been
/// loaded yet.
class StudyScreen extends StatelessWidget {
  const StudyScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Study')),
      body: EmptyState(
        icon: Icons.menu_book,
        title: 'Study material is empty',
        message:
            'The first release curriculum has not been loaded. '
            'Once human-authored, rights-cleared content is ready, '
            'it will appear here for offline study.',
        actionLabel: 'Go to Practice',
        onAction: () => Navigator.pushNamed(context, AppRouter.practice),
      ),
    );
  }
}
