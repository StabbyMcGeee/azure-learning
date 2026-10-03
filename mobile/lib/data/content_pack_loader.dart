import 'package:flutter/services.dart';

import '../models/content_pack.dart';
import 'local_store.dart';

/// Loads bounded, versioned offline content packs into a [LocalStore].
///
/// The loader is total: every problem - a missing asset, malformed JSON, an
/// unsupported or invalid pack, a rejected downgrade, or a storage failure -
/// leaves the question bank and user history untouched instead of throwing, so
/// callers can always fall back to the current bank.
class ContentPackLoader {
  static const String defaultAssetPath = 'assets/content-pack.json';

  ContentPackLoader._();

  /// Attempts to load a bundled pack from [assetPath].
  ///
  /// Returns `true` when a pack was found, parsed, validated, and applied.
  /// Returns `false` for any problem, including a missing asset, so the app
  /// keeps its existing bank.
  static Future<bool> loadBundledPackIfPresent(
    LocalStore store, {
    String assetPath = defaultAssetPath,
  }) async {
    try {
      final jsonString = await rootBundle.loadString(assetPath);
      return await loadPackFromString(store, jsonString);
    } on Object {
      return false;
    }
  }

  /// Parses, validates, and applies a pack from a raw JSON string.
  ///
  /// Returns `true` on success, `false` when the pack is invalid or could not
  /// be applied.
  static Future<bool> loadPackFromString(LocalStore store, String jsonString) async {
    final ContentPack pack;
    try {
      pack = ContentPack.parse(jsonString);
    } on FormatException {
      return false;
    }

    if (ContentPackValidator(pack).validate().isNotEmpty) {
      return false;
    }

    try {
      await store.applyContentPack(pack);
    } on Object {
      return false;
    }
    return true;
  }
}
