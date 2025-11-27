# scrapers/threads.py
import asyncio
from scrapers.base import BaseScraper
from config import settings

class ThreadsScraper(BaseScraper):
    async def scrape(self, keyword: str) -> str:
        print(f"[*] Scraping Threads untuk: {keyword}")
        
        url = f"https://www.threads.net/search?q={keyword}"
        
        try:
            await self.page.goto(url, timeout=settings.TIMEOUT)
            await self.page.wait_for_timeout(3000) # Tunggu render

            # Cek Login
            if "login" in self.page.url:
                 return "GAGAL: Butuh Login (Jalankan auth_generator.py)."

            # Threads menggunakan div dengan style grid. 
            # Kita coba ambil teks dari div yang berisi konten thread.
            # Selector ini mungkin perlu update berkala.
            
            # Ambil semua text yang terlihat relevan
            # Threads biasanya membungkus konten di div yang punya style tertentu
            # Kita ambil container utama
            
            # Scroll dulu
            await self.page.evaluate("window.scrollBy(0, 1000)")
            await self.page.wait_for_timeout(1000)

            results = await self.page.locator('div[data-pressable-container="true"]').all_inner_texts()
            
            if not results:
                # Coba selector alternatif
                results = await self.page.locator('div[class*="Thread"]').all_inner_texts()

            clean_data = [r.replace('\n', ' ') for r in results[:10]]
            return "\n".join(clean_data)

        except Exception as e:
            return f"Error Threads: {str(e)}"