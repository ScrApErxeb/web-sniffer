from abc import ABC, abstractmethod
from core.http_client import fetch
from core.storage import save_data

class BaseScraper(ABC):
    def __init__(self, name: str):
        self.name = name

    def start(self, url: str):
        html = fetch(url)
        if not html:
            return
        data = self.parse(html)
        if data:
            save_data(self.name, data)

    @abstractmethod
    def parse(self, html: str) -> dict:
        pass
