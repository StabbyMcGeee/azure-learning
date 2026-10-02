import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';

import '../models/content_pack.dart';
import 'local_store.dart';

/// Loads bounded, versioned offline content packs into a [LocalStore].
///
/// The loader is defensive: malformed, unsupported, or missing packs are
/// ignored so the app always falls back to the current empty question bank and
/// preserved user history.
class ContentPackLoader {
  static const String defaultAssetPath = 'assets/content-pack.json';

  ContentPackLoader._();

  /// Attempts to load a bundled pack from [assetPath].
  ///
  /// Returns `true` when a pack was found, parsed, validated, and applied.
  /// Returns `false` for any problem, including a missing asset, so the app
  /// keeps its existing empty bank.
  static Future<bool> loadBundledPackIfPresent(
    LocalStore store, {
    String assetPath = defaultAssetPath,
  }) async {
    try {
      final jsonString = await rootBundle.loadString(assetPath);
      return await ContentPackLoader.loadPackFromString(store, jsonString);
    } on FlutterError {
      // Asset not found or not registered. Keep the empty bank.
      return false;
    } on FormatException {
      return false;
    }
  }

  /// Parses, validates, and applies a pack from a raw JSON string.
  ///
  /// Returns `true` on success, `false` when the pack is invalid.
  static Future<bool> loadPackFromString(LocalStore store, String jsonString) async {
    late final ContentPack pack;
    try {
      pack = ContentPack.parse(jsonString);
    } on FormatException {
      return false;
    }

    final errors = ContentPackValidator(pack).validate();
    if (errors.isNotEmpty) {
      return false;
    }

    try {
      await store.applyContentPack(pack);
      return true;
    } on PackVersionTooLowException {
      return false;
    }
  }

  /// Parses a pack without applying it, returning validation errors.
  ///
  /// This is useful for diagnostics and tooling. An empty error list does not
  /// prove that rights are cleared.
  static List<String> dryRun(String jsonString) {
    try {
      final pack = ContentPack.parse(jsonString);
      return ContentPackValidator(pack).validate();
    } on FormatException catch (e) {
      return [e.message];
    }
  }
}
