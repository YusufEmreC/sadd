import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:sadd/core/network/github_api_service.dart';
import 'package:sadd/features/feed/logic/feed_cubit.dart';
import 'package:sadd/features/feed/logic/feed_state.dart';
import 'package:sadd/features/feed/data/repo_model.dart';

class FeedView extends StatelessWidget {
  final String categoryTitle;
  final String selectedCategory;

  const FeedView({
    super.key,
    required this.categoryTitle,
    required this.selectedCategory,
  });

  Future<void> _launchUrl(BuildContext context, String urlString) async {
    final Uri? url = Uri.tryParse(urlString);
    if (url != null) {
      try {
        await launchUrl(url, mode: LaunchMode.externalApplication);
      } catch (e) {
        if (context.mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Link açılamadı: $urlString')),
          );
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return BlocProvider(
      create: (context) => FeedCubit(GithubApiService())
        ..fetchReposForCategory(selectedCategory),
      child: DefaultTabController(
        length: 3,
        child: Scaffold(
          appBar: AppBar(
            title: Text(categoryTitle),
            bottom: TabBar(
              indicatorColor: theme.colorScheme.primary,
              labelColor: theme.colorScheme.primary,
              unselectedLabelColor: theme.textTheme.bodyMedium?.color?.withAlpha(150),
              indicatorSize: TabBarIndicatorSize.tab,
              labelStyle: theme.textTheme.labelLarge?.copyWith(fontSize: 13),
              unselectedLabelStyle: theme.textTheme.labelLarge?.copyWith(fontSize: 13),
              tabs: const [
                Tab(text: '🔥 Trend Repolar'),
                Tab(text: '🔌 MCP\'ler'),
                Tab(text: '🤖 AI Agent\'lar'),
              ],
            ),
          ),
          body: BlocBuilder<FeedCubit, FeedState>(
            builder: (context, state) {
              if (state is FeedLoading) {
                return Center(
                  child: CircularProgressIndicator(
                    color: theme.colorScheme.primary,
                  ),
                );
              } else if (state is FeedError) {
                return Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.error_outline_rounded, color: Colors.redAccent, size: 48),
                        const SizedBox(height: 16),
                        Text(
                          'Hata oluştu:\n${state.message}',
                          textAlign: TextAlign.center,
                          style: theme.textTheme.bodyMedium,
                        ),
                        const SizedBox(height: 16),
                        ElevatedButton(
                          style: ElevatedButton.styleFrom(
                            backgroundColor: theme.colorScheme.primary,
                            foregroundColor: Colors.black,
                          ),
                          onPressed: () {
                            context.read<FeedCubit>().fetchReposForCategory(selectedCategory);
                          },
                          child: const Text('Tekrar Dene'),
                        ),
                      ],
                    ),
                  ),
                );
              } else if (state is FeedLoaded) {
                return TabBarView(
                  children: [
                    // 1. Sekme: Trend Repolar (Canlı API)
                    state.repos.isEmpty
                        ? Center(
                            child: Text(
                              'Henüz veri bulunamadı',
                              style: theme.textTheme.bodyMedium,
                            ),
                          )
                        : ListView.separated(
                            padding: const EdgeInsets.all(16),
                            itemCount: state.repos.length,
                            separatorBuilder: (context, index) => const SizedBox(height: 12),
                            itemBuilder: (context, index) {
                              return _buildRepoCard(context, theme, state.repos[index]);
                            },
                          ),

                    // 2. Sekme: MCP Listesi (Raw GitHub JSON)
                    state.mcps.isEmpty
                        ? Center(
                            child: Text(
                              'Henüz veri bulunamadı',
                              style: theme.textTheme.bodyMedium,
                            ),
                          )
                        : ListView.separated(
                            padding: const EdgeInsets.all(16),
                            itemCount: state.mcps.length,
                            separatorBuilder: (context, index) => const SizedBox(height: 12),
                            itemBuilder: (context, index) {
                              final mcp = state.mcps[index] as Map<String, dynamic>;
                              return _buildMockCard(
                                context,
                                theme,
                                title: mcp['name']?.toString() ?? '',
                                description: mcp['description']?.toString() ?? '',
                                url: mcp['url']?.toString() ?? '',
                                accentColor: theme.colorScheme.secondary,
                              );
                            },
                          ),

                    // 3. Sekme: AI Agents Listesi (Raw GitHub JSON)
                    state.agents.isEmpty
                        ? Center(
                            child: Text(
                              'Henüz veri bulunamadı',
                              style: theme.textTheme.bodyMedium,
                            ),
                          )
                        : ListView.separated(
                            padding: const EdgeInsets.all(16),
                            itemCount: state.agents.length,
                            separatorBuilder: (context, index) => const SizedBox(height: 12),
                            itemBuilder: (context, index) {
                              final agent = state.agents[index] as Map<String, dynamic>;
                              return _buildMockCard(
                                context,
                                theme,
                                title: agent['name']?.toString() ?? '',
                                description: agent['description']?.toString() ?? '',
                                url: agent['url']?.toString() ?? '',
                                accentColor: Colors.deepPurpleAccent,
                              );
                            },
                          ),
                  ],
                );
              }
              return const SizedBox.shrink();
            },
          ),
        ),
      ),
    );
  }

  Widget _buildRepoCard(BuildContext context, ThemeData theme, RepoModel repo) {
    return Card(
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: () => _launchUrl(context, repo.htmlUrl),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: CachedNetworkImage(
                      imageUrl: repo.ownerAvatarUrl,
                      width: 36,
                      height: 36,
                      fit: BoxFit.cover,
                      placeholder: (context, url) => Container(
                        color: theme.colorScheme.surface,
                        width: 36,
                        height: 36,
                        child: const Center(
                          child: SizedBox(
                            width: 16,
                            height: 16,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          ),
                        ),
                      ),
                      errorWidget: (context, url, error) => const Icon(Icons.account_circle, size: 36),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      repo.name,
                      style: theme.textTheme.titleLarge?.copyWith(fontSize: 15),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ),
                  const SizedBox(width: 8),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(
                      color: theme.colorScheme.primary.withAlpha(26),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.star_rounded,
                          color: theme.colorScheme.primary,
                          size: 14,
                        ),
                        const SizedBox(width: 4),
                        Text(
                          '${repo.stargazersCount}',
                          style: theme.textTheme.labelLarge?.copyWith(
                            fontSize: 11,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              if (repo.description != null && repo.description!.isNotEmpty) ...[
                const SizedBox(height: 12),
                Text(
                  repo.description!,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: theme.textTheme.bodyMedium?.copyWith(
                    fontSize: 13,
                    height: 1.4,
                  ),
                ),
              ],
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Text(
                    'Detayları Gör',
                    style: theme.textTheme.labelLarge?.copyWith(
                      color: theme.colorScheme.primary,
                      fontSize: 12,
                    ),
                  ),
                  const SizedBox(width: 4),
                  Icon(
                    Icons.open_in_new_rounded,
                    size: 14,
                    color: theme.colorScheme.primary,
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildMockCard(
    BuildContext context,
    ThemeData theme, {
    required String title,
    required String description,
    required String url,
    required Color accentColor,
  }) {
    return Card(
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: () => _launchUrl(context, url),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    width: 6,
                    height: 24,
                    decoration: BoxDecoration(
                      color: accentColor,
                      borderRadius: BorderRadius.circular(4),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      title,
                      style: theme.textTheme.titleLarge?.copyWith(fontSize: 15),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 12),
              Text(
                description,
                maxLines: 3,
                overflow: TextOverflow.ellipsis,
                style: theme.textTheme.bodyMedium?.copyWith(
                  fontSize: 13,
                  height: 1.4,
                ),
              ),
              const SizedBox(height: 12),
              Row(
                mainAxisAlignment: MainAxisAlignment.end,
                children: [
                  Text(
                    'İncele',
                    style: theme.textTheme.labelLarge?.copyWith(
                      color: accentColor,
                      fontSize: 12,
                    ),
                  ),
                  const SizedBox(width: 4),
                  Icon(
                    Icons.open_in_new_rounded,
                    size: 14,
                    color: accentColor,
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
