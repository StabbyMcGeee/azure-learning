import 'dart:convert';
import 'dart:io';

import 'package:study_app/legal/evidence_register.dart';

/// Build-time validator for the private evidence register.
///
/// Run from the mobile package root:
///
///     dart run tool/validate_evidence_register.dart
///
/// Reads `data/evidence-register.json` and prints all validation errors.
/// Exits with a non-zero status when the register is invalid, so it can be
/// wired into CI as a build-time gate.
void main() async {
  const path = 'data/evidence-register.json';
  final file = File(path);
  if (!file.existsSync()) {
    stderr.writeln('Evidence register not found: $path');
    exit(1);
  }

  final dynamic decoded;
  try {
    decoded = jsonDecode(await file.readAsString());
  } on FormatException catch (e) {
    stderr.writeln('Invalid JSON in $path: $e');
    exit(1);
  }

  final errors = EvidenceRegisterValidator.validateRegister(decoded);
  if (errors.isEmpty) {
    stdout.writeln('Evidence register is valid.');
    return;
  }

  stderr.writeln('Evidence register validation failed:');
  for (final error in errors) {
    stderr.writeln('  - $error');
  }
  exit(1);
}
