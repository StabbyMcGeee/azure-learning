import 'package:flutter/material.dart';

import 'app.dart';
import 'data/content_pack_loader.dart';
import 'data/local_store.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final store = LocalStore();
  // If a content pack is bundled at assets/content-pack.json, load it.
  // If the asset is absent or invalid, the app starts with the empty v1 bank
  // and any existing attempt/session history remains intact.
  await ContentPackLoader.loadBundledPackIfPresent(store);

  runApp(StudyApp(store: store));
}
