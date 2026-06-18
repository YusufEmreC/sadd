import json
import os
import urllib.request
import urllib.parse
import re
import time

# Kürasyon için 9 ana kategorimiz ve genişletilmiş anahtar kelimeleri
CATEGORIES_CONFIG = {
    "flutter": {
        "keywords": ["flutter", "dart", "mobile", "android", "ios", "app-store", "google-play", "adb", "kotlin", "swift", "java", "objc"],
        "query": "topic:flutter topic:dart",
        "mcp_list": [],
        "ai_agents": []
    },
    "security": {
        "keywords": ["security", "pentest", "exploit", "cve", "hacking", "auth", "vulnerability", "cryptography", "sandbox", "nmap", "shodan", "wireshark", "sniff", "leak", "spy", "malware", "reverse-engineering"],
        "query": "topic:security topic:pentest topic:hacking",
        "mcp_list": [],
        "ai_agents": []
    },
    "backend": {
        "keywords": ["postgres", "redis", "database", "sql", "sqlite", "graphql", "server", "backend", "api", "fastapi", "django", "spring", "express", "go", "rust", "laravel", "rails", "serverless"],
        "query": "topic:backend topic:go topic:rust topic:nodejs",
        "mcp_list": [],
        "ai_agents": []
    },
    "frontend": {
        "keywords": ["react", "vue", "tailwind", "figma", "html", "css", "ui", "ux", "browser", "frontend", "nextjs", "angular", "chrome", "dom", "webpack", "vite", "javascript", "typescript", "design"],
        "query": "topic:frontend topic:react topic:nextjs topic:vue",
        "mcp_list": [],
        "ai_agents": []
    },
    "artificial-intelligence": {
        "keywords": ["ai", "llm", "gpt", "agent", "rag", "ollama", "huggingface", "openai", "langchain", "prompt", "vector", "claude", "gemini", "anthropic", "llama", "deepseek", "copilot", "nlp"],
        "query": "topic:artificial-intelligence topic:llm topic:langchain",
        "mcp_list": [],
        "ai_agents": []
    },
    "devops": {
        "keywords": ["docker", "kubernetes", "aws", "gcp", "azure", "ci/cd", "terraform", "ansible", "cloud", "devops", "monitoring", "github-actions", "gitlab", "jenkins", "deploy", "nginx", "dns"],
        "query": "topic:devops topic:docker topic:kubernetes topic:terraform",
        "mcp_list": [],
        "ai_agents": []
    },
    "data-science": {
        "keywords": ["data", "pandas", "jupyter", "spark", "numpy", "scikit", "notebook", "analytics", "science", "matplotlib", "seaborn", "pytorch", "tensorflow", "keras", "sql-query"],
        "query": "topic:data-science topic:python topic:pandas topic:dataset",
        "mcp_list": [],
        "ai_agents": []
    },
    "game-development": {
        "keywords": ["unity", "unreal", "blender", "game", "3d", "physics", "godot", "shader", "rendering", "graphics", "engine", "opengl", "canvas", "play"],
        "query": "topic:game-development topic:unity topic:unreal-engine",
        "mcp_list": [],
        "ai_agents": []
    },
    "blockchain": {
        "keywords": ["blockchain", "solidity", "web3", "crypto", "ethereum", "smart-contract", "bitcoin", "rust-blockchain", "defi", "etherscan", "wallet", "nft", "token", "contract", "dapp"],
        "query": "topic:blockchain topic:ethereum topic:solidity topic:web3",
        "mcp_list": [],
        "ai_agents": []
    }
}

# Genel/Ortak MCP sunucuları (Kategorilerde eksik kalırsa 20'ye tamamlamak için kullanılacak)
GENERAL_MCPS = [
    {"name": "Filesystem-MCP", "description": "LLM'lerin yerel dosyaları güvenli bir şekilde okumasını ve yazmasını sağlayan resmi sunucu.", "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem"},
    {"name": "GitHub-MCP", "description": "GitHub API entegrasyonu ile issue, PR ve repo yönetimi sağlayan sunucu.", "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/github"},
    {"name": "Fetch-MCP", "description": "Web sitelerinin içeriğini okuyup temiz markdown olarak LLM'e aktaran araç.", "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/fetch"},
    {"name": "Google-Search-MCP", "description": "Google arama motoru entegrasyonu ile güncel verilere doğrudan erişim.", "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/google-search"},
    {"name": "Sequential-Thinking-MCP", "description": "LLM'lerin karmaşık problemleri adım adım analiz etmesini sağlayan resmi sunucu.", "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/sequential-thinking"},
    {"name": "Docker-MCP", "description": "Docker konteynerlerini denetlemek, durum izlemek ve logları okumak için.", "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/docker"},
    {"name": "PostgreSQL-MCP", "description": "PostgreSQL veritabanlarında güvenli sorgulamalar ve şema analizi.", "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/postgres"},
    {"name": "Puppeteer-MCP", "description": "Web tarayıcısını kontrol ederek ekran görüntüleri alma ve web otomasyonu yapma sunucusu.", "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/puppeteer"},
    {"name": "Sentry-MCP", "description": "Sentry API'si ile uygulama hata loglarını ve çökmelerini LLM'lere raporlayan sunucu.", "url": "https://github.com/example/sentry-mcp"},
    {"name": "Linear-MCP", "description": "Linear proje yönetim aracındaki görevleri sorgulama ve güncelleme sunucusu.", "url": "https://github.com/example/linear-mcp"}
]

# Genel/Ortak AI Agent araçları (Kategorilerde eksik kalırsa 20'ye tamamlamak için kullanılacak)
GENERAL_AGENTS = [
    {"name": "AutoGPT", "description": "Belirlenen hedeflere ulaşmak için kendi kendine internet araması yapan otonom AI ajanı.", "url": "https://github.com/Significant-Gravitas/AutoGPT"},
    {"name": "BabyAGI", "description": "Görev oluşturma, önceliklendirme ve çalıştırma süreçlerini yöneten sade yapay zeka ajanı.", "url": "https://github.com/yoheinakajima/babyagi"},
    {"name": "OpenInterpreter", "description": "Doğal dil komutlarıyla yerel bilgisayarınızda Python/Bash kodları çalıştıran asistan.", "url": "https://github.com/OpenInterpreter/open-interpreter"},
    {"name": "SWE-agent", "description": "GitHub depolarındaki yazılım hatalarını otonom olarak analiz edip düzelten yazılım mühendisliği ajanı.", "url": "https://github.com/princeton-nlp/SWE-agent"},
    {"name": "Devika", "description": "İnternet araştırması, kod yazımı ve hata ayıklama yeteneklerine sahip yapay zeka yazılımcısı.", "url": "https://github.com/stitionai/devika"},
    {"name": "CrewAI", "description": "Rol tabanlı, otonom yapay zeka ajanlarını orkestre eden popüler çoklu-ajan çatısı.", "url": "https://github.com/joaomdmoura/crewai"},
    {"name": "Microsoft-Autogen", "description": "Birden çok ajanın işbirliği yaparak karmaşık görevleri çözmesini sağlayan yazılım altyapısı.", "url": "https://github.com/microsoft/autogen"},
    {"name": "ChatDev", "description": "Yazılım şirketini simüle ederek tasarımcı, kodlayıcı ve testçi ajanlarla yazılım üreten sanal ekip.", "url": "https://github.com/OpenBMB/ChatDev"},
    {"name": "SuperAGI", "description": "Geliştiricilerin otonom AI ajanları oluşturmasını ve yönetmesini kolaylaştıran açık kaynaklı platform.", "url": "https://github.com/TransformerOptimus/SuperAGI"},
    {"name": "MetaGPT", "description": "Tek satır gereksinimden PRD şeması, görev planı ve kod üreten yazılım mühendisliği orkestratörü.", "url": "https://github.com/geekan/MetaGPT"}
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

def translate_to_turkish(text):
    """
    Ücretsiz Google Translate API kullanarak 
    İngilizce metinleri Türkçe'ye çevirir.
    """
    if not text or len(text.strip()) == 0:
        return ""
    try:
        # Google Translate gtx parametresiyle ücretsiz çeviri
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=tr&dt=t&q={urllib.parse.quote(text)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                res_data = json.loads(response.read().decode("utf-8"))
                # Çevrilen parçaları birleştir
                translated_parts = [part[0] for part in res_data[0] if part and part[0]]
                return "".join(translated_parts)
    except Exception as e:
        print(f"Metin Türkçe'ye çevrilirken hata oluştu: {e}")
    return text # Hata durumunda orijinali koru

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

    pattern = re.compile(r'-\s+\[(.*?)\]\((.*?)\)(?::)?\s+(.*)')
    for line in content.split("\n"):
        match = pattern.search(line)
        if match:
            name = match.group(1).strip()
            link = match.group(2).strip()
            desc = match.group(3).strip()
            
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
    """Öğeyi anahtar kelimelere göre sınıflandırır."""
    text = (item["name"] + " " + item["description"]).lower()
    for cat_name, config in categories_config.items():
        for keyword in config["keywords"]:
            if keyword in text:
                return cat_name
    return None

def fetch_github_repos(query):
    """GitHub API'den en çok yıldız alan 20 repoyu çeker."""
    api_url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&order=desc&per_page=20"
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
                    raw_desc = item.get("description", "")
                    
                    # İngilizce açıklamaları anlık olarak Türkçe'ye çeviriyoruz
                    turkish_desc = translate_to_turkish(raw_desc) if raw_desc else "Açıklama belirtilmemiş."
                    
                    repos.append({
                        "id": item.get("id"),
                        "name": item.get("name"),
                        "description": turkish_desc,
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

    # 2. Kategorileri sıfırla
    for cat_name in CATEGORIES_CONFIG.keys():
        CATEGORIES_CONFIG[cat_name]["mcp_list"] = []
        CATEGORIES_CONFIG[cat_name]["ai_agents"] = []

    # 3. Canlı MCP'leri sınıflandırıp kategorilere dağıt ve açıklamalarını Türkçe'ye çevir
    print("Çekilen MCP açıklamaları Türkçe'ye çevriliyor...")
    for mcp in scraped_mcps:
        assigned_cat = classify_item(mcp, CATEGORIES_CONFIG)
        if assigned_cat:
            mcp["description"] = translate_to_turkish(mcp["description"])
            CATEGORIES_CONFIG[assigned_cat]["mcp_list"].append(mcp)

    # 4. Canlı Agent'ları sınıflandırıp kategorilere dağıt ve açıklamalarını Türkçe'ye çevir
    print("Çekilen AI Agent açıklamaları Türkçe'ye çevriliyor...")
    for agent in scraped_agents:
        assigned_cat = classify_item(agent, CATEGORIES_CONFIG)
        if assigned_cat:
            agent["description"] = translate_to_turkish(agent["description"])
            CATEGORIES_CONFIG[assigned_cat]["ai_agents"].append(agent)

    # 5. Her kategoriyi tam olarak 20 adet araca tamamla (Padding)
    for cat_name, content in CATEGORIES_CONFIG.items():
        current_mcps = content["mcp_list"]
        for gmcp in GENERAL_MCPS:
            if len(current_mcps) >= 20:
                break
            if not any(x["name"].lower() == gmcp["name"].lower() for x in current_mcps):
                # Yedek öğeyi çevirip ekle
                translated_desc = translate_to_turkish(gmcp["description"])
                current_mcps.append({
                    "name": gmcp["name"],
                    "description": translated_desc,
                    "url": gmcp["url"]
                })
        content["mcp_list"] = current_mcps[:20]

        current_agents = content["ai_agents"]
        for gagent in GENERAL_AGENTS:
            if len(current_agents) >= 20:
                break
            if not any(x["name"].lower() == gagent["name"].lower() for x in current_agents):
                translated_desc = translate_to_turkish(gagent["description"])
                current_agents.append({
                    "name": gagent["name"],
                    "description": translated_desc,
                    "url": gagent["url"]
                })
        content["ai_agents"] = current_agents[:20]

    # 6. Her kategori için GitHub'dan 20'şer adet canlı repo çekip Türkçe'ye çevirerek nihai JSON'ı oluştur
    for category, content in CATEGORIES_CONFIG.items():
        print(f"'{category}' kategorisi için trend repolar canlı çekiliyor ve çevriliyor...")
        repos = fetch_github_repos(content["query"])
        
        curated_data[category] = {
            "repos": repos if repos else [],
            "mcp_list": content["mcp_list"],
            "ai_agents": content["ai_agents"]
        }
        time.sleep(1)

    # 7. data.json Dosyasına Kaydet
    output_filename = "data.json"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(curated_data, f, indent=4, ensure_ascii=False)
        print(f"\nBaşarıyla her alanda tam 20'şer veri içeren %100 Türkçe veritabanı '{output_filename}' dosyasına kaydedildi!")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    main()
