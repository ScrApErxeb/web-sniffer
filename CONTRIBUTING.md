# 🤝 Contribution au projet Web Sniffer

Merci de votre intérêt pour contribuer à **web-sniffer** !  
Que ce soit pour corriger un bug, ajouter un nouveau scraper ou améliorer la documentation, votre aide est la bienvenue.  

---

## 1. Règles générales

- Suivre le **PEP8** pour le code Python.
- Les nouvelles fonctionnalités doivent **passer les tests locaux** avant soumission.
- Utiliser **des messages de commit clairs** et explicites.
- Créer une branche spécifique pour chaque nouvelle fonctionnalité ou correction :

```bash
git checkout -b feature/nom-de-la-fonctionnalité
2. Comment contribuer
a) Signaler un bug
Vérifier que le bug n’a pas déjà été signalé dans les issues.

Créer une nouvelle issue détaillant :

Le problème rencontré.

La version de Python et des dépendances.

Les étapes pour reproduire le bug.

b) Ajouter un nouveau scraper
Créer une nouvelle classe dans scrapers/ héritant de BaseScraper.

Implémenter les méthodes :

fetch_page()

parse()

run()

Ajouter la source dans core/factory.py (ScraperFactory) :

python
Copy code
elif source == "nouvelle_source":
    return NouveauScraper(**kwargs)
Ajouter la source dans ScraperRunner.SCRAPER_SOURCES si nécessaire.

Tester le scraper localement avec quelques pays avant de soumettre.

c) Améliorer le code ou la documentation
Pour le code, soumettre des Pull Requests (PR) avec tests ou validation locale.

Pour la documentation, corriger ou compléter les fichiers .md existants.

Ajouter des exemples clairs et complets dans le README si nécessaire.

3. Tests
Avant de soumettre une PR, tester les scrapers sur au moins 2 pays.

Vérifier que le cache fonctionne correctement (cache.json).

4. Pull Requests
Forker le dépôt.

Créer votre branche (git checkout -b feature/nom-de-la-fonctionnalité).

Faire vos changements.

Commit et push :

bash
Copy code
git add .
git commit -m "Ajout du scraper ExempleScraper"
git push origin feature/nom-de-la-fonctionnalité
Ouvrir une Pull Request vers la branche principale du dépôt.

5. Code Review
Chaque PR sera examinée par l’équipe ou le mainteneur.

Les suggestions de modification doivent être appliquées avant fusion.

Les PR approuvées seront fusionnées dans main.

6. Bonnes pratiques
Respecter les noms des variables et classes existants.

Commenter les parties complexes du code.

Garder le code modulaire et réutilisable.

Limiter les requêtes HTTP inutiles pour éviter le blocage des sites.

Ajouter des messages de log clairs et informatifs.

Merci encore pour votre contribution !
Ensemble, nous rendons web-sniffer plus robuste et complet 🚀