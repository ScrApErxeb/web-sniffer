# JOURNAL_DEV - web-sniffer

## 06/10/2025
**Action :** Création du projet `web-sniffer`  
**Résultat / Statut :** Structure initiale créée (`core/`, `scrapers/`, `data/`, `tests/`)  
**Remarques / Problèmes :** N/A  
**Prochaine étape :** Ajouter `.gitignore` et commit initial

## 06/10/2025
**Action :** Ajout DemoScraper  
**Résultat / Statut :** Test sur httpbin.org → OK  
**Remarques / Problèmes :** `example.com` inutile pour scraping réel  
**Prochaine étape :** Ajouter WikipediaScraper

## 06/10/2025
**Action :** Ajout WikipediaScraper  
**Résultat / Statut :** Page Python récupérée → OK  
**Remarques / Problèmes :** Premier paragraphe vide → nécessité de parser `mw-parser-output`  
**Prochaine étape :** Nettoyage du texte séparé

## 06/10/2025
**Action :** Création `.gitignore` et commit initial  
**Résultat / Statut :** Repo GitHub propre  
**Remarques / Problèmes :** N/A  
**Prochaine étape :** Ajouter scraper Jeune Afrique

## 06/10/2025
**Action :** Ajout JeuneAfriqueCountryScraper pages 1-2  
**Résultat / Statut :** 90 articles récupérés  
**Remarques / Problèmes :** URLs relatives → prévoir normalisation si besoin  
**Prochaine étape :** Ajouter support multi-pays ou multi-pages

## 06/10/2025
**Action :** Pipeline final  
**Résultat / Statut :** Scraping → parsing → stockage JSON → OK  
**Remarques / Problèmes :** N/A  
**Prochaine étape :** Ajouter tests unitaires et nettoyage / post-processing


## [2025-10-08]
- ✅ Intégration Google Custom Search terminée
- ✅ 10 résultats trouvés pour “Burkina Faso économie”
- 🧩 Prochaine étape : multi-pays et sauvegarde auto
- [2025-10-10 15:44:05] burkina faso | burkina faso économie | fusionné 94 | stats: {'google': 10, 'bing': 10, 'duckduckgo': 0, 'jeuneafrique': 90}
- [2025-10-10 15:44:15] cote-divoire | cote-divoire économie | fusionné 93 | stats: {'google': 10, 'bing': 10, 'duckduckgo': 0, 'jeuneafrique': 90}
- [2025-10-10 15:44:22] mali | mali économie | fusionné 88 | stats: {'google': 10, 'bing': 10, 'duckduckgo': 0, 'jeuneafrique': 90}
