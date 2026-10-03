import 'package:flutter/material.dart';

import 'app.dart';
import 'data/content_pack_loader.dart';
import 'data/local_store.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final store = LocalStore();
  // If a content pack is bundled at assets/content-pack.json, load it. The
  // loader never throws: a missing, invalid, or unwritable pack leaves the
  // current bank and any existing attempt/session history intact.
  await ContentPackLoader.loadBundledPackIfPresent(store);

  runApp(StudyApp(store: store));
}
