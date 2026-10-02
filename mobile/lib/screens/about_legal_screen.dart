import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../data/local_store.dart';

/// About and Legal screen.
///
/// Displays the app independence statement, a Microsoft trademark footnote, the
/// content-last-verified date sourced from the loaded content pack, and a
/// button to view the framework's own third-party licence registry.
class AboutLegalScreen extends StatefulWidget {
  const AboutLegalScreen({super.key});

  @override
  State<AboutLegalScreen> createState() => _AboutLegalScreenState();
}

class _AboutLegalScreenState extends State<AboutLegalScreen> {
  String? _lastVerifiedAt;
  int _licenseCount = 0;
  bool _loaded = false;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final store = context.read<LocalStore>();
    final courseId = await store.getSelectedCourseId();
    final lastVerified = await store.getContentLastVerifiedAt(
      courseId: courseId,
    );

    var count = 0;
    await for (final _ in LicenseRegistry.licenses) {
      count++;
    }

    if (mounted) {
      setState(() {
        _lastVerifiedAt = lastVerified;
        _licenseCount = count;
        _loaded = true;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    return Scaffold(
      appBar: AppBar(title: const Text('About & Legal')),
      body: _loaded
          ? ListView(
              padding: const EdgeInsets.all(16.0),
              children: [
                Text(
                  'Independence statement',
                  style: theme.textTheme.titleMedium,
                ),
                const SizedBox(height: 8),
                const Text(
                  'This app is an independent study aid. It is not endorsed by, '
                  'affiliated with, or sponsored by Microsoft Corporation. All '
                  'study content is authored or licensed separately and is '
                  'provided for exam preparation only.',
                ),
                const SizedBox(height: 16),
                Text(
                  'Trademark notice',
                  style: theme.textTheme.titleMedium,
                ),
                const SizedBox(height: 8),
                const Text(
                  'Microsoft, Azure, AZ-900, SC-900, AI-901, Microsoft Entra, '
                  'Microsoft Purview, Microsoft Defender, Microsoft Sentinel, '
                  'and other Microsoft product names are trademarks or '
                  'registered trademarks of Microsoft Corporation.',
                ),
                const SizedBox(height: 16),
                Text(
                  'Content last verified',
                  style: theme.textTheme.titleMedium,
                ),
                const SizedBox(height: 8),
                Text(
                  _lastVerifiedAt ?? 'No verified content loaded yet.',
                ),
                const SizedBox(height: 24),
                FilledButton.icon(
                  onPressed: () => _showLicenses(context),
                  icon: const Icon(Icons.description),
                  label: Text('View third-party licenses ($_licenseCount)'),
                ),
              ],
            )
          : const Center(child: CircularProgressIndicator()),
    );
  }

  void _showLicenses(BuildContext context) {
    showLicensePage(
      context: context,
      applicationName: 'Study App (placeholder)',
      applicationLegalese:
          'This app is an independent study aid and is not endorsed by '
          'Microsoft Corporation.',
    );
  }
}
