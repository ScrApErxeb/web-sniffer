# Web Sniffer 🕵️‍♂️

**Web Sniffer** est un outil de scraping multi-sources conçu pour collecter des informations sur l'économie des pays à partir de Google, Bing, DuckDuckGo et Jeune Afrique. Il intègre un cache TTL, un reporting simplifié, et peut fonctionner en mode multithread pour accélérer les collectes.

---

## Fonctionnalités

- Scraping multi-sources : Google API, Bing HTML, DuckDuckGo (DDGS), Jeune Afrique.
- Cache SQLite avec TTL pour éviter de rescraper.
- Fusion automatique des résultats multi-sources.
- Gestion des doublons URL.
- Sauvegarde des résultats directement dans SQLite.
- Multithreading pour exécuter plusieurs scrapers en parallèle.
- Pause configurable pour éviter les erreurs 429.
- Logging complet avec statuts par source (OK, SKIPPED, ERROR).

---
---
## 🚀 Installation rapide

```bash
git clone https://github.com/ScrApErxeb/web-sniffer.git
cd web-sniffer
python -m venv venv
source venv/bin/activate  # sous Windows : venv\Scripts\activate
pip install -r requirements.txt

⚙️ Configuration

Créez un fichier .env à la racine :

GOOGLE_API_KEY=...
BING_COOKIE=...
CACHE_TTL=86400

▶️ Exécution

Lancer le scraper principal :

python main.py

🧩 Structure du projet
core/              # Composants communs : cache, fusion, parser, logger
scrapers/          # Scrapers par source (Google, Bing, DDG, Jeune Afrique)
config.py          # Gestion des variables d'environnement
main.py            # Point d'entrée principal
requirements.txt   # Dépendances
