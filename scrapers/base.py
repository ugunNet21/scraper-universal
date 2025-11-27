# scrapers/base.py
from abc import ABC, abstractmethod
from playwright.async_api import Page

class BaseScraper(ABC):
    def __init__(self, page: Page):
        self.page = page

    @abstractmethod
    async def scrape(self, keyword: str) -> str:
        """Method ini wajib diimplementasikan oleh setiap platform scraper"""
        pass