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
      // Sadece tek bir ağ isteği: GitHub CDN üzerinden derlenmiş tüm verileri (data.json) çeker.
      // Bu sayede mobil cihazlardan GitHub API limitine takılma sorunu tamamen çözülür.
      final rawData = await _githubApiService.fetchMcpAndAgents();

      // Aktif kategorinin verilerini alıyoruz
      final categoryData = rawData[category] as Map<String, dynamic>? ?? {};

      // data.json içinde hazır bulunan repo verilerini nesnelerimize dönüştürüyoruz
      final List<dynamic> rawRepos = categoryData['repos'] as List<dynamic>? ?? [];
      final repos = rawRepos
          .map((item) => RepoModel.fromJson(item as Map<String, dynamic>))
          .toList();

      final mcps = categoryData['mcp_list'] as List<dynamic>? ?? [];
      final agents = categoryData['ai_agents'] as List<dynamic>? ?? [];

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
