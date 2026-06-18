import 'dart:convert';
import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:sadd/features/feed/data/repo_model.dart';

class GithubApiService {
  final Dio _dio;

  GithubApiService()
      : _dio = Dio(
          BaseOptions(
            baseUrl: 'https://api.github.com',
            connectTimeout: const Duration(seconds: 10),
            receiveTimeout: const Duration(seconds: 10),
            headers: {
              'Accept': 'application/vnd.github+json',
              'User-Agent': 'Yazilimci-Hub-App', // GitHub API User-Agent başlığı zorunlu tutar.
            },
          ),
        );

  Future<List<RepoModel>> fetchTrendingRepos(String topic) async {
    try {
      final response = await _dio.get(
        '/search/repositories',
        queryParameters: {
          'q': 'topic:$topic pushed:>2026-05-01',
          'sort': 'stars',
          'order': 'desc',
          'per_page': 15,
        },
      );

      if (response.statusCode == 200) {
        final List<dynamic> items = response.data['items'] as List<dynamic>? ?? [];
        return items
            .map((item) => RepoModel.fromJson(item as Map<String, dynamic>))
            .toList();
      } else {
        throw DioException(
          requestOptions: response.requestOptions,
          response: response,
          message: 'GitHub API returned status code: ${response.statusCode}',
        );
      }
    } on DioException catch (e) {
      debugPrint('Dio Exception in fetchTrendingRepos: ${e.message}');
      if (e.response != null) {
        debugPrint('Response Data: ${e.response?.data}');
      }
      rethrow;
    } catch (e) {
      debugPrint('Generic Exception in fetchTrendingRepos: $e');
      rethrow;
    }
  }

  /// GitHub Actions ile üretilen data.json dosyasını raw URL üzerinden çeker.
  /// Hata alması durumunda uygulamanın tamamen çökmesini önlemek için boş liste döner.
  Future<Map<String, dynamic>> fetchMcpAndAgents() async {
    try {
      // Not: Kullanıcı adınızı ve depo ismini GitHub'a yükledikten sonra buradaki URL ile eşleştirin.
      const rawUrl = 'https://raw.githubusercontent.com/YusufEmreC/sadd/main/data.json';
      
      final response = await _dio.get(
        rawUrl,
        options: Options(
          headers: {
            'Accept': '*/*',
          },
        ),
      );

      if (response.statusCode == 200) {
        final data = response.data;
        if (data is Map<String, dynamic>) {
          return data;
        } else if (data is String) {
          final parsed = jsonDecode(data);
          if (parsed is Map<String, dynamic>) {
            return parsed;
          }
        }
      }
      return {'mcp_list': [], 'ai_agents': []};
    } catch (e) {
      // Hata durumunda (Örn: 404, internet olmaması vb.) boş veri dönerek 
      // uygulamanın diğer sekmelerinin (örneğin Trend Repolar) çalışmasını engellemiyoruz.
      debugPrint(' fetchMcpAndAgents raw verisi çekilemedi (404/Bağlantı Hatası). Boş liste ile devam ediliyor.');
      return {
        'mcp_list': [],
        'ai_agents': [],
      };
    }
  }
}
