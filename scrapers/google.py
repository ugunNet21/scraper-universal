# scrapers/google.py
from scrapers.base import BaseScraper
from config import settings
import asyncio

class GoogleScraper(BaseScraper):
    async def scrape(self, keyword: str) -> str:
        print(f"[*] Scraping Google untuk: {keyword}")
        
        # Gunakan URL dengan parameter 'hl=id' (Bahasa Indonesia) & 'gl=id' (Lokasi Indo)
        url = f"https://www.google.com/search?q={keyword}&hl=id&gl=id"
        
        try:
            await self.page.goto(url, timeout=settings.TIMEOUT)
            
            # Cek apakah terkena CAPTCHA/Consent page
            if "google_abuse" in self.page.url or "sorry" in self.page.url:
                return "TERDETEKSI BOT: Google memblokir request ini (Captcha)."

            # Tunggu elemen hasil pencarian (div.g atau div[data-header-feature])
            # Kita gunakan try/except untuk selector
            try:
                await self.page.wait_for_selector("div#search", timeout=10000)
            except:
                pass # Lanjut saja siapa tau konten sudah load

            # Ambil semua teks body sebagai fallback jika selector spesifik gagal
            body_text = await self.page.locator("body").inner_text()
            
            # Potong agar tidak terlalu panjang (hemat token LLM)
            return body_text[:5000] 

        except Exception as e:
            return f"Error Google Scraping: {str(e)}"