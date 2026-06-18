import 'package:sadd/features/feed/data/repo_model.dart';

abstract class FeedState {
  const FeedState();
}

class FeedInitial extends FeedState {
  const FeedInitial();
}

class FeedLoading extends FeedState {
  const FeedLoading();
}

class FeedLoaded extends FeedState {
  final List<RepoModel> repos;
  final List<dynamic> mcps;
  final List<dynamic> agents;

  const FeedLoaded({
    required this.repos,
    required this.mcps,
    required this.agents,
  });
}

class FeedError extends FeedState {
  final String message;

  const FeedError(this.message);
}
