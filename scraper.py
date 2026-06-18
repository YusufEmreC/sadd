import json
import os

def generate_curation_data():
    # Kategori bazlı MCP ve AI Agent verileri
    data = {
        "flutter": {
            "mcp_list": [
                {
                    "name": "Dart-Analyzer-MCP",
                    "description": "Dart ve Flutter projelerini analiz eden, statik kod analiz hatalarını ve iyileştirme önerilerini raporlayan özelleştirilmiş MCP.",
                    "url": "https://github.com/example/dart-analyzer-mcp"
                },
                {
                    "name": "Flutter-Localization-MCP",
                    "description": "Uygulama içi dil dosyalarını (ARB) otomatik analiz eden ve eksik çevirileri tamamlayan yerelleştirme asistanı.",
                    "url": "https://github.com/example/flutter-localization-mcp"
                }
            ],
            "ai_agents": [
                {
                    "name": "AutoGPT-Mobile",
                    "description": "Mobil cihazlarda otonom görevler yürütebilen, uygulama içi aksiyonları simüle eden mobil AI ajanı.",
                    "url": "https://github.com/example/autogpt-mobile"
                },
                {
                    "name": "WidgetBuilder-Agent",
                    "description": "Ekran tasarımlarını analiz edip otomatik olarak optimize edilmiş Flutter Widget ağacı üreten kod asistanı.",
                    "url": "https://github.com/example/widgetbuilder-agent"
                }
            ]
        },
        "security": {
            "mcp_list": [
                {
                    "name": "Shodan-MCP",
                    "description": "Shodan API entegrasyonu ile internete açık cihazları, zafiyetleri ve portları sorgulamayı sağlayan güvenlik sunucusu.",
                    "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/shodan"
                },
                {
                    "name": "Hash-Cracker-MCP",
                    "description": "Çeşitli hash algoritmalarını (MD5, SHA256 vb.) kırmak için optimize edilmiş hesaplama motorlarını LLM'e bağlayan sunucu.",
                    "url": "https://github.com/example/hash-cracker-mcp"
                }
            ],
            "ai_agents": [
                {
                    "name": "Pentest-Agent",
                    "description": "Sızma testleri ve web zafiyet taramalarını otomatik gerçekleştiren otonom güvenlik ajanı.",
                    "url": "https://github.com/example/pentest-agent"
                },
                {
                    "name": "ThreatIntel-Agent",
                    "description": "Siber tehdit istihbarat kaynaklarını tarayıp sıfırıncı gün (0-day) açıklarını anlık raporlayan analiz ajanı.",
                    "url": "https://github.com/example/threatintel-agent"
                }
            ]
        },
        "backend": {
            "mcp_list": [
                {
                    "name": "PostgreSQL-MCP",
                    "description": "SQL veritabanlarında güvenli sorgulamalar ve şema incelemeleri yapmayı sağlayan resmi sunucu.",
                    "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/postgres"
                },
                {
                    "name": "Redis-Cli-MCP",
                    "description": "Redis bellek içi veritabanı komutlarını çalıştırma ve anahtar/değer durumlarını izleme sunucusu.",
                    "url": "https://github.com/example/redis-cli-mcp"
                }
            ],
            "ai_agents": [
                {
                    "name": "DB-Optimizer-Agent",
                    "description": "Yavaş çalışan veritabanı sorgularını analiz ederek indeksleme ve sorgu optimizasyon önerileri sunan veri tabanı ajanı.",
                    "url": "https://github.com/example/db-optimizer-agent"
                },
                {
                    "name": "SQL-Gen-Agent",
                    "description": "Doğal dilden karmaşık PostgreSQL, MySQL ve MongoDB sorguları üreten ve doğrulayan arka uç geliştirici asistanı.",
                    "url": "https://github.com/example/sql-gen-agent"
                }
            ]
        },
        "frontend": {
            "mcp_list": [
                {
                    "name": "TailwindCSS-Inspector-MCP",
                    "description": "HTML/React kodlarındaki Tailwind sınıflarını analiz eden ve çakışan CSS kodlarını raporlayan denetleyici.",
                    "url": "https://github.com/example/tailwindcss-inspector-mcp"
                },
                {
                    "name": "Figma-API-MCP",
                    "description": "Figma tasarımlarını doğrudan LLM bağlamına çekerek bileşen ve renk paleti analizleri yapmayı sağlayan arayüz sunucusu.",
                    "url": "https://github.com/example/figma-api-mcp"
                }
            ],
            "ai_agents": [
                {
                    "name": "UX-Audit-Agent",
                    "description": "Web sitelerinin ekran görüntülerini inceleyip erişilebilirlik (Accessibility) ve tasarım hatalarını raporlayan UX ajanı.",
                    "url": "https://github.com/example/ux-audit-agent"
                },
                {
                    "name": "Figma-to-React-Agent",
                    "description": "Figma tasarım token'larını okuyup doğrudan temiz Next.js ve Tailwind component'lerine dönüştüren frontend ajanı.",
                    "url": "https://github.com/example/figma-to-react-agent"
                }
            ]
        },
        "artificial-intelligence": {
            "mcp_list": [
                {
                    "name": "HuggingFace-Spaces-MCP",
                    "description": "HuggingFace üzerindeki açık kaynaklı ML modellerini ve Spaces demolarını sorgulayan entegrasyon sunucusu.",
                    "url": "https://github.com/example/huggingface-spaces-mcp"
                },
                {
                    "name": "Ollama-Local-MCP",
                    "description": "Yerel bilgisayarda çalışan Ollama modellerinin yük durumlarını ve çalışan model listelerini LLM'lere raporlayan araç.",
                    "url": "https://github.com/example/ollama-local-mcp"
                }
            ],
            "ai_agents": [
                {
                    "name": "AutoGPT",
                    "description": "Belirlenen hedeflere ulaşmak için kendi kendine internet araması yapan ve görevler oluşturan otonom AI ajanı.",
                    "url": "https://github.com/Significant-Gravitas/AutoGPT"
                },
                {
                    "name": "BabyAGI",
                    "description": "Görev oluşturma, önceliklendirme ve çalıştırma süreçlerini döngüsel olarak yöneten yapay zeka ajanı.",
                    "url": "https://github.com/yoheinakajima/babyagi"
                }
            ]
        },
        "devops": {
            "mcp_list": [
                {
                    "name": "Docker-MCP",
                    "description": "Docker konteynerlerini denetlemek, logları okumak ve yönetim komutları çalıştırmak için entegrasyon sunucusu.",
                    "url": "https://github.com/modelcontextprotocol/servers/tree/main/src/docker"
                },
                {
                    "name": "Kubernetes-Pod-Inspector-MCP",
                    "description": "K8s pod durumlarını, Kubernetes loglarını ve dağıtım şemalarını izlemeyi sağlayan altyapı sunucusu.",
                    "url": "https://github.com/example/k8s-pod-inspector-mcp"
                }
            ],
            "ai_agents": [
                {
                    "name": "KubeGuard-Agent",
                    "description": "Kubernetes cluster'larındaki anormal kaynak tüketimlerini ve çökme döngülerini (crashloopbackoff) izleyip otomatik düzelten ajan.",
                    "url": "https://github.com/example/kubeguard-agent"
                },
                {
                    "name": "CI-CD-Debugger-Agent",
                    "description": "Başarısız GitHub Actions ve GitLab CI hatlarını analiz ederek hata düzeltme önerileri üreten DevOps asistanı.",
                    "url": "https://github.com/example/cicd-debugger-agent"
                }
            ]
        },
        "data-science": {
            "mcp_list": [
                {
                    "name": "Pandas-Dataframe-MCP",
                    "description": "Büyük veri setlerini (CSV/Parquet) bellek üzerinde sorgulama ve filtreleme araçları sunan veri bilimi sunucusu.",
                    "url": "https://github.com/example/pandas-dataframe-mcp"
                },
                {
                    "name": "Jupyter-Notebook-MCP",
                    "description": "Jupyter Notebook dosyalarını (.ipynb) okuyan ve hücre çıktılarını analiz eden entegrasyon.",
                    "url": "https://github.com/example/jupyter-notebook-mcp"
                }
            ],
            "ai_agents": [
                {
                    "name": "AutoEDA-Agent",
                    "description": "Ham veriyi yükleyip otomatik olarak Keşifsel Veri Analizi (EDA) grafikleri ve istatistiksel raporlar üreten ajan.",
                    "url": "https://github.com/example/autoeda-agent"
                },
                {
                    "name": "FeatureEngineering-Agent",
                    "description": "Makine öğrenmesi modelleri için veri setinden otomatik olarak yeni öznitelikler (features) türeten veri mühendisi.",
                    "url": "https://github.com/example/featureengineering-agent"
                }
            ]
        },
        "game-development": {
            "mcp_list": [
                {
                    "name": "Unity-Profiler-MCP",
                    "description": "Unity oyun motorundaki bellek kaçaklarını, kare hızlarını (FPS) ve CPU tüketimini LLM'e raporlayan araç.",
                    "url": "https://github.com/example/unity-profiler-mcp"
                },
                {
                    "name": "Blender-Automation-MCP",
                    "description": "Blender Python API'sini kullanarak otonom olarak basit 3D modeller üreten tasarım sunucusu.",
                    "url": "https://github.com/example/blender-automation-mcp"
                }
            ],
            "ai_agents": [
                {
                    "name": "Playtest-Agent",
                    "description": "Oyun mekaniklerini test etmek için oyunu otonom oynayan ve çarpışma (collision) hatalarını raporlayan yapay zeka ajanı.",
                    "url": "https://github.com/example/playtest-agent"
                },
                {
                    "name": "BehaviorTree-Agent",
                    "description": "Düşman NPC'leri için optimize edilmiş yapay zeka davranış ağaçları (Behavior Trees) tasarlayan oyun geliştirme asistanı.",
                    "url": "https://github.com/example/behaviortree-agent"
                }
            ]
        },
        "blockchain": {
            "mcp_list": [
                {
                    "name": "Etherscan-API-MCP",
                    "description": "Ethereum akıllı sözleşme kodlarını, gas ücretlerini ve cüzdan işlemlerini sorgulayan zincir dışı arayüz sunucusu.",
                    "url": "https://github.com/example/etherscan-api-mcp"
                },
                {
                    "name": "Solidity-Compiler-MCP",
                    "description": "Solidity akıllı sözleşme kodlarındaki derleme hatalarını ve zafiyetleri analiz eden derleyici sunucusu.",
                    "url": "https://github.com/example/solidity-compiler-mcp"
                }
            ],
            "ai_agents": [
                {
                    "name": "ContractAuditor-Agent",
                    "description": "Akıllı sözleşmelerdeki güvenlik açıklarını (reentrancy, integer overflow vb.) tarayan otonom denetim ajanı.",
                    "url": "https://github.com/example/contractauditor-agent"
                },
                {
                    "name": "ArbitrageBot-Agent",
                    "description": "DeFi protokolleri arasında fiyat farklarını izleyerek otonom arbitraj fırsatları arayan Web3 ajanı.",
                    "url": "https://github.com/example/arbitragebot-agent"
                }
            ]
        }
    }

    # Dosyaya Yazma (data.json)
    output_filename = "data.json"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Başarıyla kategori bazlı veri üretildi ve '{output_filename}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    generate_curation_data()
