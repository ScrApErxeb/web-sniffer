Phase 1 — Stabilisation

 Corriger duckduckgo_scraper.py pour utiliser ddgs.

 Vérifier que chaque scraper retourne {title, url, snippet}.

 Implémenter le cache avec TTL et gestion des doublons.

 Ajouter tests unitaires pour chaque scraper (pytest).

Phase 2 — Architecture

 Créer core/cache.py → lecture/écriture dans SQLite avec TTL.

 Créer core/fusion.py → fusion des résultats multi-sources + nettoyage URL.

 Créer core/utils.py → fonctions utilitaires (normalisation, logs, stats).

Phase 3 — Interface & monitoring

 Générer un rapport JSON/HTML après chaque run.

 Ajouter un indicateur de statut par scraper (OK, SKIPPED, ERROR).

 Ajouter logs détaillés pour debug et suivi.

Phase 4 — Scalabilité

 Paralléliser les scrapers via threading ou asyncio.

 Sauvegarder les résultats fusionnés dans une base (SQLite ou PostgreSQL).

 Option : préparer la migration vers un dashboard web.