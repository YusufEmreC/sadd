import 'package:flutter/material.dart';
import 'package:sadd/features/feed/presentation/feed_view.dart';

class CategoryItem {
  final String title;
  final String subtitle;
  final String topic;
  final IconData icon;
  final Color accentColor;

  const CategoryItem({
    required this.title,
    required this.subtitle,
    required this.topic,
    required this.icon,
    required this.accentColor,
  });
}

class CategorySelectionView extends StatelessWidget {
  const CategorySelectionView({super.key});

  static const List<CategoryItem> categories = [
    CategoryItem(
      title: 'Mobil Geliştirme',
      subtitle: 'Flutter, Dart ve mobil teknolojiler',
      topic: 'flutter',
      icon: Icons.phone_android_rounded,
      accentColor: Color(0xFF00B0FF), // Siber Mavi
    ),
    CategoryItem(
      title: 'Siber Güvenlik',
      subtitle: 'Pentest, güvenlik araçları ve scriptler',
      topic: 'security',
      icon: Icons.security_rounded,
      accentColor: Color(0xFF00E676), // Neon Yeşil
    ),
    CategoryItem(
      title: 'Backend',
      subtitle: 'Sunucu mimarileri, Go, Rust ve Node.js',
      topic: 'backend',
      icon: Icons.dns_rounded,
      accentColor: Colors.deepPurpleAccent,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 32.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 40),
              Text(
                'Uzmanlık\nAlanını Seç',
                style: theme.textTheme.displayLarge?.copyWith(
                  height: 1.2,
                ),
              ),
              const SizedBox(height: 12),
              Text(
                'İlgi alanına göre güncel GitHub repolarını, MCP sunucularını ve AI Agent araçlarını takip et.',
                style: theme.textTheme.bodyMedium,
              ),
              const SizedBox(height: 48),
              Expanded(
                child: ListView.separated(
                  itemCount: categories.length,
                  separatorBuilder: (context, index) => const SizedBox(height: 16),
                  itemBuilder: (context, index) {
                    final category = categories[index];
                    return GestureDetector(
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => FeedView(
                              categoryTitle: category.title,
                              selectedCategory: category.topic,
                            ),
                          ),
                        );
                      },
                      child: Container(
                        padding: const EdgeInsets.all(20),
                        decoration: BoxDecoration(
                          color: theme.cardColor,
                          borderRadius: BorderRadius.circular(16),
                          border: Border.all(
                            color: theme.dividerTheme.color ?? const Color(0xFF2C2C2E),
                            width: 1,
                          ),
                        ),
                        child: Row(
                          children: [
                            Container(
                              padding: const EdgeInsets.all(12),
                              decoration: BoxDecoration(
                                color: category.accentColor.withAlpha(26), // %10 opaklık
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Icon(
                                category.icon,
                                color: category.accentColor,
                                size: 28,
                              ),
                            ),
                            const SizedBox(width: 20),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    category.title,
                                    style: theme.textTheme.titleLarge?.copyWith(
                                      fontSize: 16,
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    category.subtitle,
                                    style: theme.textTheme.bodyMedium?.copyWith(
                                      fontSize: 13,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                            Icon(
                              Icons.arrow_forward_ios_rounded,
                              color: theme.textTheme.bodyMedium?.color?.withAlpha(128), // %50 opaklık
                              size: 16,
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
