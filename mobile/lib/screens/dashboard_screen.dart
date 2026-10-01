import 'package:flutter/material.dart';

import '../navigation/app_router.dart';

/// Main landing screen with navigation into the study, practice, exam, review,
/// and progress areas.
class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Study App (placeholder)'),
        centerTitle: true,
      ),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Welcome',
                style: theme.textTheme.headlineMedium,
              ),
              const SizedBox(height: 8),
              Text(
                'Offline study, practice, and exam simulation. '
                'No account, ads, or network required.',
                style: theme.textTheme.bodyMedium,
              ),
              const SizedBox(height: 24),
              Expanded(
                child: GridView.count(
                  crossAxisCount: _columns(context),
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                  childAspectRatio: 1.3,
                  children: [
                    _DashboardTile(
                      icon: Icons.menu_book,
                      label: 'Study',
                      onTap: () => Navigator.pushNamed(context, AppRouter.study),
                    ),
                    _DashboardTile(
                      icon: Icons.quiz,
                      label: 'Practice',
                      onTap: () => Navigator.pushNamed(context, AppRouter.practice),
                    ),
                    _DashboardTile(
                      icon: Icons.assignment,
                      label: 'Exam',
                      onTap: () => Navigator.pushNamed(context, AppRouter.exam),
                    ),
                    _DashboardTile(
                      icon: Icons.repeat,
                      label: 'Review',
                      onTap: () => Navigator.pushNamed(context, AppRouter.review),
                    ),
                    _DashboardTile(
                      icon: Icons.trending_up,
                      label: 'Progress',
                      onTap: () => Navigator.pushNamed(context, AppRouter.progress),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'Placeholder name and identifiers. Replace before release.',
                style: theme.textTheme.bodySmall,
              ),
            ],
          ),
        ),
      ),
    );
  }

  int _columns(BuildContext context) {
    final width = MediaQuery.of(context).size.width;
    return width > 600 ? 3 : 2;
  }
}

class _DashboardTile extends StatelessWidget {
  final IconData icon;
  final String label;
  final VoidCallback onTap;

  const _DashboardTile({
    required this.icon,
    required this.label,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 40, color: theme.colorScheme.primary),
              const SizedBox(height: 8),
              Text(label, style: theme.textTheme.titleMedium),
            ],
          ),
        ),
      ),
    );
  }
}
