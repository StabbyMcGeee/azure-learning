import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'data/local_store.dart';
import 'navigation/app_router.dart';

class StudyApp extends StatelessWidget {
  final LocalStore? store;
  final String? initialRoute;

  const StudyApp({super.key, this.store, this.initialRoute});

  @override
  Widget build(BuildContext context) {
    return Provider<LocalStore>(
      create: (_) => store ?? LocalStore(),
      dispose: (_, store) => store.close(),
      child: MaterialApp(
        title: 'Study App (placeholder)',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
          useMaterial3: true,
        ),
        darkTheme: ThemeData(
          colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.indigo,
            brightness: Brightness.dark,
          ),
          useMaterial3: true,
        ),
        themeMode: ThemeMode.system,
        initialRoute: initialRoute ?? AppRouter.dashboard,
        onGenerateRoute: AppRouter.onGenerateRoute,
        onUnknownRoute: (settings) => MaterialPageRoute(
          builder: (_) => const Scaffold(
            body: Center(child: Text('Page not found')),
          ),
        ),
      ),
    );
  }
}
