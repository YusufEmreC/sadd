import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:sadd/core/network/github_api_service.dart';
import 'package:sadd/features/feed/logic/feed_state.dart';
import 'package:sadd/features/feed/data/repo_model.dart';

class FeedCubit extends Cubit<FeedState> {
  final GithubApiService _githubApiService;

  FeedCubit(this._githubApiService) : super(const FeedInitial());

  Future<void> fetchReposForCategory(String category) async {
    emit(const FeedLoading());
    try {
      // Canlı GitHub araması ve Raw JSON verisi çekme işlemleri paralel tetikleniyor.
      final results = await Future.wait([
        _githubApiService.fetchTrendingRepos(category),
        _githubApiService.fetchMcpAndAgents(),
      ]);

      final repos = results[0] as List<RepoModel>;
      final rawData = results[1] as Map<String, dynamic>;

      final mcps = rawData['mcp_list'] as List<dynamic>? ?? [];
      final agents = rawData['ai_agents'] as List<dynamic>? ?? [];

      emit(FeedLoaded(
        repos: repos,
        mcps: mcps,
        agents: agents,
      ));
    } catch (e) {
      emit(FeedError(e.toString()));
    }
  }
}
