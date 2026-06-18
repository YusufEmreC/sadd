class RepoModel {
  final int id;
  final String name;
  final String? description;
  final int stargazersCount;
  final String htmlUrl;
  final String ownerAvatarUrl;

  const RepoModel({
    required this.id,
    required this.name,
    this.description,
    required this.stargazersCount,
    required this.htmlUrl,
    required this.ownerAvatarUrl,
  });

  factory RepoModel.fromJson(Map<String, dynamic> json) {
    return RepoModel(
      id: json['id'] as int,
      name: json['name'] as String? ?? '',
      description: json['description'] as String?,
      stargazersCount: json['stargazers_count'] as int? ?? 0,
      htmlUrl: json['html_url'] as String? ?? '',
      ownerAvatarUrl: (json['owner'] as Map<String, dynamic>?)?['avatar_url'] as String? ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'stargazers_count': stargazersCount,
      'html_url': htmlUrl,
      'owner': {
        'avatar_url': ownerAvatarUrl,
      },
    };
  }
}
