Phase 1 – Stabilisation des scrapers existants
Objectif	Tâches	Statut
WikipediaScraper	- Nettoyer le texte (références, ponctuation, espaces)	✅ Scraping OK, nettoyage séparé
JeuneAfriqueScraper	- Récupération pages 1-2 Burkina Faso
- Gestion des URLs relatives	✅ Scraping OK
DemoScraper	- Garder pour tests rapides	✅


Phase 2 – Pipeline et stockage
Objectif	Tâches	Statut
Stockage JSON	- Sauvegarde des articles scrappés	✅ Fait
Tests unitaires	- Écrire tests pour Wikipedia et Jeune Afrique	⏳ À faire
Logs et reporting	- Ajouter logs pour chaque fetch / parse	⏳ À faire


Phase 3 – Extension multi-sites
Objectif	Tâches	Statut
Multi-pays Jeune Afrique	- Ajouter support de plusieurs pays	⏳ À faire
Pagination avancée	- Scraper toutes les pages disponibles	⏳ À faire
Autres sites	- Identifier 1 ou 2 sites supplémentaires pour le scraping	⏳ À faire


Phase 4 – Nettoyage & post-processing
Objectif	Tâches	Statut
Nettoyage texte	- Retirer références, HTML, caractères spéciaux	⏳ À faire
Normalisation	- Uniformiser titres, dates, liens	⏳ À faire
Préparation dataset	- Générer CSV ou JSON pour analyses	⏳ À faire


Phase 5 – Maintenance et évolutions
Objectif	Tâches	Statut
Surveillance	- Détecter changements structure HTML des sites	⏳ À faire
Ajout scrapers	- Nouveau site → nouveau scraper rapide	⏳ À faire
Documentation	- Compléter docs/ et Notion	⏳ À faire