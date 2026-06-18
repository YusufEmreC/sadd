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
      subtitle: 'Pentest, güvenlik araçları ve exploitler',
      topic: 'security',
      icon: Icons.security_rounded,
      accentColor: Color(0xFF00E676), // Neon Yeşil
    ),
    CategoryItem(
      title: 'Backend Geliştirme',
      subtitle: 'Sunucu mimarileri, Go, Rust ve Node.js',
      topic: 'backend',
      icon: Icons.dns_rounded,
      accentColor: Colors.deepPurpleAccent,
    ),
    CategoryItem(
      title: 'Frontend Geliştirme',
      subtitle: 'React, Vue, Next.js ve modern web sistemleri',
      topic: 'frontend',
      icon: Icons.web_rounded,
      accentColor: Colors.orangeAccent,
    ),
    CategoryItem(
      title: 'Yapay Zeka & LLM',
      subtitle: 'Makine öğrenmesi, PyTorch, Agent ve LLM modelleri',
      topic: 'artificial-intelligence',
      icon: Icons.psychology_rounded,
      accentColor: Colors.amberAccent,
    ),
    CategoryItem(
      title: 'DevOps & Bulut',
      subtitle: 'Docker, Kubernetes, AWS ve CI/CD otomasyonları',
      topic: 'devops',
      icon: Icons.cloud_done_rounded,
      accentColor: Colors.tealAccent,
    ),
    CategoryItem(
      title: 'Veri Bilimi',
      subtitle: 'Veri analitiği, Python, Pandas ve veri görselleştirme',
      topic: 'data-science',
      icon: Icons.bar_chart_rounded,
      accentColor: Colors.pinkAccent,
    ),
    CategoryItem(
      title: 'Oyun Geliştirme',
      subtitle: 'Unity, Unreal Engine, C# ve C++ mekanikleri',
      topic: 'game-development',
      icon: Icons.sports_esports_rounded,
      accentColor: Colors.redAccent,
    ),
    CategoryItem(
      title: 'Blokzincir & Web3',
      subtitle: 'Solidity, Rust, akıllı sözleşmeler ve dApps',
      topic: 'blockchain',
      icon: Icons.currency_bitcoin_rounded,
      accentColor: Colors.cyanAccent,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 24.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 20),
              Text(
                'Uzmanlık\nAlanını Seç',
                style: theme.textTheme.displayLarge?.copyWith(
                  height: 1.2,
                  fontSize: 28, // Liste büyüdüğü için başlığı biraz ufattık
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'İlgi alanına göre güncel GitHub repolarını, MCP sunucularını ve AI Agent araçlarını takip et.',
                style: theme.textTheme.bodyMedium,
              ),
              const SizedBox(height: 24),
              Expanded(
                child: ListView.separated(
                  itemCount: categories.length,
                  separatorBuilder: (context, index) => const SizedBox(height: 12),
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
                        padding: const EdgeInsets.all(16),
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
                              padding: const EdgeInsets.all(10),
                              decoration: BoxDecoration(
                                color: category.accentColor.withAlpha(26), // %10 opaklık
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Icon(
                                category.icon,
                                color: category.accentColor,
                                size: 24,
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    category.title,
                                    style: theme.textTheme.titleLarge?.copyWith(
                                      fontSize: 15,
                                    ),
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    category.subtitle,
                                    style: theme.textTheme.bodyMedium?.copyWith(
                                      fontSize: 12,
                                    ),
                                    maxLines: 1,
                                    overflow: TextOverflow.ellipsis,
                                  ),
                                ],
                              ),
                            ),
                            Icon(
                              Icons.arrow_forward_ios_rounded,
                              color: theme.textTheme.bodyMedium?.color?.withAlpha(128), // %50 opaklık
                              size: 14,
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
