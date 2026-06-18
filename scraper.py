import json
import os
import urllib.request
import urllib.parse
import re
import time

# Kürasyon için 9 ana kategorimiz ve anahtar kelimeleri
CATEGORIES_CONFIG = {
    "flutter": {
        "keywords": ["flutter", "dart", "mobile", "android", "ios", "app-store", "google-play"],
        "query": "topic:flutter topic:dart",
        "mcp_list": [],
        "ai_agents": []
    },
    "security": {
        "keywords": ["security", "pentest", "exploit", "cve", "hacking", "auth", "vulnerability", "cryptography", "sandbox"],
        "query": "topic:security topic:pentest topic:hacking",
        "mcp_list": [],
        "ai_agents": []
    },
    "backend": {
        "keywords": ["postgres", "redis", "database", "sql", "sqlite", "graphql", "server", "backend", "api", "fastapi", "django"],
        "query": "topic:backend topic:go topic:rust topic:nodejs",
        "mcp_list": [],
        "ai_agents": []
    },
    "frontend": {
        "keywords": ["react", "vue", "tailwind", "figma", "html", "css", "ui", "ux", "browser", "frontend", "nextjs", "angular"],
        "query": "topic:frontend topic:react topic:nextjs topic:vue",
        "mcp_list": [],
        "ai_agents": []
    },
    "artificial-intelligence": {
        "keywords": ["ai", "llm", "gpt", "agent", "rag", "ollama", "huggingface", "openai", "langchain", "prompt", "vector"],
        "query": "topic:artificial-intelligence topic:llm topic:langchain",
        "mcp_list": [],
        "ai_agents": []
    },
    "devops": {
        "keywords": ["docker", "kubernetes", "aws", "gcp", "azure", "ci/cd", "terraform", "ansible", "cloud", "devops", "monitoring"],
        "query": "topic:devops topic:docker topic:kubernetes topic:terraform",
        "mcp_list": [],
        "ai_agents": []
    },
    "data-science": {
        "keywords": ["data", "pandas", "jupyter", "spark", "numpy", "scikit", "notebook", "analytics", "science"],
        "query": "topic:data-science topic:python topic:pandas topic:dataset",
        "mcp_list": [],
        "ai_agents": []
    },
    "game-development": {
        "keywords": ["unity", "unreal", "blender", "game", "3d", "physics", "godot", "shader", "rendering"],
        "query": "topic:game-development topic:unity topic:unreal-engine",
        "mcp_list": [],
        "ai_agents": []
    },
    "blockchain": {
        "keywords": ["blockchain", "solidity", "web3", "crypto", "ethereum", "smart-contract", "bitcoin", "rust-blockchain", "defi"],
        "query": "topic:blockchain topic:ethereum topic:solidity topic:web3",
        "mcp_list": [],
        "ai_agents": []
    }
}

# Varsayılan başlangıç/baz küresi (İnternetten çekilemezse veya kategori boş kalırsa kullanılacak)
DEFAULT_MCPS = [
    {"name": "PostgreSQL-MCP", "description": "PostgreSQL veritabanlarında güvenli sorgulamalar ve şema analizi.", "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/postgres", "category": "backend"},
    {"name": "Docker-MCP", "description": "Docker konteynerlerini denetlemek ve logları okumak için.", "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/docker", "category": "devops"},
    {"name": "Dart-Analyzer-MCP", "description": "Dart ve Flutter kod analiz ve iyileştirme aracı.", "url": "https://github.com/example/dart-analyzer-mcp", "category": "flutter"},
    {"name": "Shodan-MCP", "description": "Shodan API ile internete açık cihazları ve portları tarar.", "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/shodan", "category": "security"},
    {"name": "Figma-API-MCP", "description": "Figma tasarımlarını LLM bağlamına çeken arayüz sunucusu.", "url": "https://github.com/example/figma-api-mcp", "category": "frontend"}
]

DEFAULT_AGENTS = [
    {"name": "AutoGPT", "description": "İnternet aramalı genel otonom görev yöneticisi.", "url": "https://github.com/Significant-Gravitas/AutoGPT", "category": "artificial-intelligence"},
    {"name": "BabyAGI", "description": "Görev oluşturma ve önceliklendirme süreçlerini yöneten yapay zeka ajanı.", "url": "https://github.com/yoheinakajima/babyagi", "category": "artificial-intelligence"},
    {"name": "Pentest-Agent", "description": "Sızma testleri gerçekleştiren otonom güvenlik ajanı.", "url": "https://github.com/example/pentest-agent", "category": "security"},
    {"name": "WidgetBuilder-Agent", "description": "Tasarımı otomatik olarak optimize Flutter widget'larına çeviren ajan.", "url": "https://github.com/example/widgetbuilder-agent", "category": "flutter"}
]

def fetch_content_from_url(url):
    """Verilen URL'in içeriğini çeker."""
    req = urllib.request.Request(url, headers={"User-Agent": "Yazilimci-Hub-Scraper"})
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                return response.read().decode("utf-8")
    except Exception as e:
        print(f"URL okunurken hata oluştu ({url}): {e}")
    return ""

def scrape_awesome_mcp_servers():
    """Awesome MCP listesini kazıyarak sunucuları çeker."""
    print("GitHub üzerinden Awesome MCP sunucuları taranıyor...")
    url = "https://raw.githubusercontent.com/punkpeye/awesome-mcp-servers/main/README.md"
    content = fetch_content_from_url(url)
    
    mcp_items = []
    if not content:
        return mcp_items
        
    pattern = re.compile(r'-\s+\[(.*?)\]\((.*?)\)\s+-\s+(.*)')
    for line in content.split("\n"):
        match = pattern.search(line)
        if match:
            name = match.group(1).strip()
            link = match.group(2).strip()
            desc = match.group(3).strip()
            
            # Badge'leri temizle (örneğin img.shields.io içeren markdown linkleri)
            desc = re.sub(r'!\[.*?\]\(.*?\)', '', desc).strip()
            
            if "github.com" in link and len(desc) > 5:
                mcp_items.append({
                    "name": name,
                    "description": desc,
                    "url": link
                })
    print(f"Awesome listesinden {len(mcp_items)} adet MCP sunucusu başarıyla çekildi.")
    return mcp_items

def scrape_awesome_ai_agents():
    """Awesome AI Agents listesini kazıyarak araçları çeker."""
    print("GitHub üzerinden Awesome AI Agents listesi taranıyor...")
    url = "https://raw.githubusercontent.com/kyrolabs/awesome-agents/master/README.md"
    content = fetch_content_from_url(url)
    
    agent_items = []
    if not content:
        return agent_items

    # kyrolabs/awesome-agents formatı: - [Name](URL): Description
    # veya - [Name](URL) Description
    pattern = re.compile(r'-\s+\[(.*?)\]\((.*?)\)(?::)?\s+(.*)')
    for line in content.split("\n"):
        match = pattern.search(line)
        if match:
            name = match.group(1).strip()
            link = match.group(2).strip()
            desc = match.group(3).strip()
            
            # Badge'leri temizle
            desc = re.sub(r'!\[.*?\]\(.*?\)', '', desc).strip()
            
            if "github.com" in link and len(desc) > 5:
                agent_items.append({
                    "name": name,
                    "description": desc,
                    "url": link
                })
    print(f"Awesome listesinden {len(agent_items)} adet AI Agent aracı başarıyla çekildi.")
    return agent_items

def classify_item(item, categories_config):
    """
    Öğeyi isim ve açıklamasındaki anahtar kelimelere göre 
    uygun kategorilere sınıflandırır.
    """
    text = (item["name"] + " " + item["description"]).lower()
    for cat_name, config in categories_config.items():
        for keyword in config["keywords"]:
            if keyword in text:
                return cat_name
    return None

def fetch_github_repos(query):
    """GitHub API'den en çok yıldız alan 15 repoyu çeker."""
    api_url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc&per_page=15"
    headers = {
        "User-Agent": "Yazilimci-Hub-Scraper",
        "Accept": "application/vnd.github+json"
    }
    
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
        
    req = urllib.request.Request(api_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                res_data = json.loads(response.read().decode("utf-8"))
                raw_items = res_data.get("items", [])
                
                repos = []
                for item in raw_items:
                    repos.append({
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "description": item.get("description"),
                        "stargazers_count": item.get("stargazers_count"),
                        "html_url": item.get("html_url"),
                        "owner": {
                            "avatar_url": item.get("owner", {}).get("avatar_url")
                        }
                    })
                return repos
    except Exception as e:
        print(f"GitHub API Arama hatası ({query}): {e}")
        time.sleep(2)
    return []

def main():
    curated_data = {}
    
    # 1. GitHub Awesome Listelerinden canlı veri çek
    scraped_mcps = scrape_awesome_mcp_servers()
    scraped_agents = scrape_awesome_ai_agents()

    # 2. Kategorileri hazırla
    for cat_name in CATEGORIES_CONFIG.keys():
        CATEGORIES_CONFIG[cat_name]["mcp_list"] = []
        CATEGORIES_CONFIG[cat_name]["ai_agents"] = []

    # 3. Canlı MCP'leri sınıflandırıp kategorilere dağıt
    for mcp in scraped_mcps:
        assigned_cat = classify_item(mcp, CATEGORIES_CONFIG)
        if assigned_cat:
            CATEGORIES_CONFIG[assigned_cat]["mcp_list"].append(mcp)

    # 4. Canlı Agent'ları sınıflandırıp kategorilere dağıt
    for agent in scraped_agents:
        assigned_cat = classify_item(agent, CATEGORIES_CONFIG)
        if assigned_cat:
            CATEGORIES_CONFIG[assigned_cat]["ai_agents"].append(agent)

    # 5. Varsayılan verileri ekle (Eğer kategori boş kaldıysa veya 3'ten azsa yedek doldur)
    for dmcp in DEFAULT_MCPS:
        cat = dmcp["category"]
        mcp_obj = {"name": dmcp["name"], "description": dmcp["description"], "url": dmcp["url"]}
        if mcp_obj not in CATEGORIES_CONFIG[cat]["mcp_list"]:
            CATEGORIES_CONFIG[cat]["mcp_list"].insert(0, mcp_obj)

    for dagent in DEFAULT_AGENTS:
        cat = dagent["category"]
        agent_obj = {"name": dagent["name"], "description": dagent["description"], "url": dagent["url"]}
        if agent_obj not in CATEGORIES_CONFIG[cat]["ai_agents"]:
            CATEGORIES_CONFIG[cat]["ai_agents"].insert(0, agent_obj)

    # 6. Her kategori için GitHub'dan repoları çekip JSON oluştur
    for category, content in CATEGORIES_CONFIG.items():
        print(f"'{category}' için trend repolar canlı olarak çekiliyor...")
        repos = fetch_github_repos(content["query"])
        
        curated_data[category] = {
            "repos": repos,
            "mcp_list": content["mcp_list"][:15], # Her kategori için en fazla 15 araç listele
            "ai_agents": content["ai_agents"][:15]
        }
        time.sleep(1)

    # 7. data.json Dosyasına Kaydet
    output_filename = "data.json"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(curated_data, f, indent=4, ensure_ascii=False)
        print(f"\nBaşarıyla dev veri tabanı (Canlı Repolar, MCP'ler, AI Agent'lar) '{output_filename}' dosyasına kaydedildi!")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    main()
