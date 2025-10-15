from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseScraper(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def fetch_page(self, *args, **kwargs) -> str:
        """Récupérer la page HTML ou JSON."""
        pass

    @abstractmethod
    def parse(self, html: str) -> Any:
        """Extraire les données depuis le HTML ou JSON."""
        pass

    def run(self, max_pages: int = 1) -> Dict[str, Any]:
        """Exécute le scraper et retourne les résultats."""
        results: List[Any] = []
        for page in range(max_pages):
            html = self.fetch_page(page=page)
            parsed = self.parse(html)
            if parsed:
                results.append(parsed)
        return {self.name: results}
