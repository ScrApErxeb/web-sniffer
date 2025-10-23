# 🌐 Web Sniffer

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Beta-orange.svg)

`web-sniffer` est un framework Python pour scraper et agréger automatiquement des données depuis plusieurs sources en ligne.  
Il prend en charge des moteurs de recherche et sites comme **Google**, **DuckDuckGo**, **Wikipedia**, et **JeuneAfrique**, avec **cache**, **retry**, et **multi-threading**.

---

## ⚡ Fonctionnalités principales

- Scraping multi-source et multi-pays.
- Cache JSON pour éviter les requêtes répétées.
- Gestion des erreurs, retry automatique et pause anti-429.
- Exécution parallèle via `ThreadPoolExecutor`.
- Rapport de performance détaillé par source.
- Facile à étendre avec de nouveaux scrapers.

---

## 🗂 Structure du projet

web-sniffer/
│
├─ core/
│ ├─ cache.py # Interface et implémentation JSONCache
│ ├─ config.py # Configuration globale (HTTP, cache, scraper runner)
│ ├─ http_client.py # Fonctions HTTP avec retry et logging
│ ├─ scraper_runner.py # Exécution parallèle des scrapers
│ └─ factory.py # Fabrique les instances de scrapers
│
├─ scrapers/
│ ├─ base_scraper.py # Classe de base pour tous les scrapers
│ ├─ google_search_scraper.py
│ ├─ duckduckgo_scraper.py
│ ├─ wikipedia_scraper.py
│ └─ jeune_afrique_scraper.py
│
├─ cache.json # Cache JSON généré automatiquement
├─ requirements.txt
└─ README.md

yaml
Copy code

---

## ⚙️ Installation

### 1. Cloner le projet
```bash
git clone https://github.com/ton-utilisateur/web-sniffer.git
cd web-sniffer
2. Créer un environnement virtuel
bash
Copy code
python -m venv sniffer_venv
# macOS / Linux
source sniffer_venv/bin/activate
# Windows
sniffer_venv\Scripts\activate
3. Installer les dépendances
bash
Copy code
pip install -r requirements.txt
4. Configurer les variables d'environnement
Créer un fichier .env à la racine du projet :

env
Copy code
GOOGLE_API_KEY=...
GOOGLE_CX_ID=...
DEFAULT_DATE_RANGE=w1
HTTP_TIMEOUT=10
HTTP_MAX_RETRIES=3
ANTI_429_MIN=4
ANTI_429_MAX=8
USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) ...
CACHE_FILE=cache.json
USE_CACHE=true
MAX_WORKERS=5
LOG_LEVEL=INFO
🚀 Utilisation
Lancer le scraping
bash
Copy code
python -m core.scraper_runner
Par défaut, le scraper utilise la liste de pays définie dans scraper_runner.py :

python
Copy code
countries_list = ["Burkina Faso", "Senegal", "Cote d'Ivoire", "Mali", "Niger"]
Résultats
Les données sont stockées dans le cache JSON (cache.json).

La console affiche le nombre de résultats par source et un rapport de performance.

Exemple de sortie JSON
json
Copy code
{
  "Burkina Faso": {
    "google": [
      {"title": "Économie du Burkina Faso", "url": "...", "snippet": "..."}
    ],
    "duckduckgo": [
      {"title": "Burkina Faso Economy", "url": "...", "snippet": "..."}
    ],
    "wikipedia": [
      {"title": "Burkina Faso", "url": "...", "snippet": "..."}
    ],
    "jeuneafrique": [
      {"title": "Burkina Faso : Actualités économiques", "url": "...", "snippet": ""}
    ]
  }
}
🛠 Ajouter un nouveau scraper
Créer une nouvelle classe dans scrapers/ héritant de BaseScraper.

Implémenter les méthodes fetch_page(), parse(), et run().

Ajouter la source dans ScraperFactory :

python
Copy code
elif source == "nouvelle_source":
    return NouveauScraper(**kwargs)
Ajouter la source dans ScraperRunner.SCRAPER_SOURCES si nécessaire.

🔧 Configuration globale
Toutes les options sont centralisées dans core/config.py :

HTTP : timeout, headers, retry, pause anti-429

Cache : fichier, activation

Scraper Runner : nombre de threads (max_workers)

📄 Licence
MIT License © 2025