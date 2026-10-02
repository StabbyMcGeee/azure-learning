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
  /// Returns `false` for any problem — a missing asset, malformed pack,
  /// database failure, or platform error — so the app always keeps its
  /// existing bank and starts regardless of pack-load outcome.
  static Future<bool> loadBundledPackIfPresent(
    LocalStore store, {
    String assetPath = defaultAssetPath,
  }) async {
    try {
      final jsonString = await rootBundle.loadString(assetPath);
      return await ContentPackLoader.loadPackFromString(store, jsonString);
    } catch (_) {
      // Missing/invalid asset, malformed pack, or any storage/platform error:
      // keep the existing bank and never prevent the app from starting.
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
}
