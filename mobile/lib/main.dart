import 'package:flutter/material.dart';

import 'app.dart';
import 'data/content_pack_loader.dart';
import 'data/local_store.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final store = LocalStore();
  // If a content pack is bundled at assets/content-pack.json, load it.
  // The loader never throws: a missing/invalid pack, or any storage failure,
  // leaves the bank unchanged and the app still starts. The try/catch is a
  // belt-and-suspenders guard so an unexpected error cannot block first paint.
  try {
    await ContentPackLoader.loadBundledPackIfPresent(store);
  } catch (_) {
    // App starts regardless of pack-load outcome.
  }

  runApp(StudyApp(store: store));
}
