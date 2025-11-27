# scrapers/factory.py
from playwright.async_api import Page
from scrapers.google import GoogleScraper
from scrapers.tiktok import TiktokScraper
from scrapers.instagram import InstagramScraper
from scrapers.youtube import YoutubeScraper
from scrapers.twitter import TwitterScraper
from scrapers.facebook import FacebookScraper
from scrapers.threads import ThreadsScraper

class ScraperFactory:
    @staticmethod
    def get_scraper(platform: str, page: Page):
        platforms = {
            "google": GoogleScraper,
            "tiktok": TiktokScraper,
            "instagram": InstagramScraper,
            "youtube": YoutubeScraper,
            "twitter": TwitterScraper,
            "x": TwitterScraper,
            "facebook": FacebookScraper,
            "threads": ThreadsScraper   
        }
        
        scraper_class = platforms.get(platform.lower())
        if not scraper_class:
            raise ValueError(f"Platform '{platform}' belum didukung.")
        
        return scraper_class(page)