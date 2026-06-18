import 'package:flutter/material.dart';
import 'package:sadd/core/theme/app_theme.dart';
import 'package:sadd/features/category_selection/category_selection_view.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Yazılımcı Hub',
      debugShowCheckedModeBanner: false,
      themeMode: ThemeMode.dark,
      darkTheme: AppTheme.darkTheme,
      home: const CategorySelectionView(),
    );
  }
}
