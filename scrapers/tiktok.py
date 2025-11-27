# scrapers/tiktok.py
from scrapers.base import BaseScraper
from config import settings

class TiktokScraper(BaseScraper):
    async def scrape(self, keyword: str) -> str:
        print(f"[*] Scraping TikTok untuk: {keyword}")
        
        # Pergi ke halaman search TikTok
        url = f"https://www.tiktok.com/search?q={keyword}"
        await self.page.goto(url, timeout=settings.TIMEOUT)
        
        # Tunggu konten dimuat (bisa disesuaikan selectornya)
        try:
            await self.page.wait_for_selector('div[data-e2e="search_top-item"]', timeout=10000)
            elements = await self.page.locator('div[data-e2e="search_top-item"]').all_inner_texts()
            return "\n".join(elements)
        except:
            return "Konten TikTok tidak ditemukan atau butuh Login/Captcha handling."