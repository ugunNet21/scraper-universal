# scrapers/twitter.py
import asyncio
from scrapers.base import BaseScraper
from config import settings

class TwitterScraper(BaseScraper):
    async def scrape(self, keyword: str) -> str:
        print(f"[*] Scraping Twitter (X) untuk: {keyword}")
        
        # Gunakan src=typed_query agar hasil lebih relevan
        url = f"https://x.com/search?q={keyword}&src=typed_query"
        
        try:
            await self.page.goto(url, timeout=settings.TIMEOUT)
            
            # Cek apakah dilempar ke Login Wall
            # Twitter sering redirect url ke /login atau /i/flow/login
            await self.page.wait_for_timeout(3000) # Tunggu redirect sebentar
            if "login" in self.page.url:
                return "GAGAL: Twitter mewajibkan Login. (Sistem Session diperlukan nanti)"

            # Tunggu tweet muncul
            try:
                # Selector paling stabil di X adalah data-testid
                await self.page.wait_for_selector('[data-testid="tweet"]', timeout=10000)
            except:
                return "Tidak ada Tweet ditemukan atau Loading terlalu lama."

            # Ambil Tweet
            tweets = await self.page.locator('[data-testid="tweet"]').all()
            
            collected_data = []
            for i, tweet in enumerate(tweets[:10]):
                # Ambil teks di dalam tweet (biasanya di div[data-testid="tweetText"])
                text_el = tweet.locator('[data-testid="tweetText"]')
                
                if await text_el.count() > 0:
                    text = await text_el.inner_text()
                    collected_data.append(f"Tweet {i+1}: {text}")
            
            if not collected_data:
                return "Tweet elemen ada, tapi teks tidak terbaca (Mungkin hanya gambar/video)."

            return "\n".join(collected_data)

        except Exception as e:
            return f"Error Twitter: {str(e)}"