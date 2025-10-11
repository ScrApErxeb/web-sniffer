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

## Installation

```bash
git clone (https://github.com/ScrApErxeb/web-sniffer.git)
cd web-sniffer
python -m venv scrap_env
source scrap_env/bin/activate  # ou `scrap_env\Scripts\activate` sur Windows
pip install -r requirements.txt

---
## Créer un fichier .env avec :

GOOGLE_API_KEY=ton_api_key
GOOGLE_CX_ID=ton_cx_id
DEFAULT_DATE_RANGE=w1
COUNTRIES=Burkina Faso,Cote d'Ivoire,Mali

## Usage

Lancer le scraping principal :

python multi_scrap.py


Les résultats sont sauvegardés dans results.db.

Le cache est stocké dans cache.db.

Les logs détaillés apparaissent dans la console.
