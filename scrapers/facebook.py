# scrapers/facebook.py
import asyncio
from scrapers.base import BaseScraper
from config import settings

class FacebookScraper(BaseScraper):
    async def scrape(self, keyword: str) -> str:
        print(f"[*] Scraping Facebook untuk: {keyword}")
        
        # URL Search Postingan Publik
        url = f"https://www.facebook.com/search/posts/?q={keyword}"
        
        try:
            await self.page.goto(url, timeout=settings.TIMEOUT)
            
            # Cek login: Jika ada tombol "Log In" di header, berarti session gagal/expired
            if "login" in self.page.url:
                return "GAGAL: Session tidak valid. Harap jalankan auth_generator.py lagi."

            # Facebook butuh waktu load yang agak lama (CSR)
            await self.page.wait_for_timeout(5000)

            # Selector Facebook sangat sulit (obfuscated). 
            # Kita gunakan pendekatan generik: Ambil semua teks dalam container feed.
            # Biasanya feed ada di role="feed" atau main role="main"
            
            try:
                # Scroll sedikit agar konten loading
                await self.page.evaluate("window.scrollBy(0, 1000)")
                await self.page.wait_for_timeout(2000)
                
                # Ambil text dari elemen role="article" (Postingan biasanya berupa article)
                posts = await self.page.locator('[role="article"]').all_inner_texts()
            except:
                return "Tidak ada postingan ditemukan atau layout Facebook berubah."

            if not posts:
                 # Fallback extreme: Ambil body text jika selector spesifik gagal
                 body = await self.page.locator('body').inner_text()
                 return body[:3000] # Ambil sebagian saja

            # Bersihkan data (Facebook banyak teks tombol seperti 'Like', 'Comment')
            clean_posts = []
            for p in posts[:5]: # Ambil 5 post teratas
                # Hapus baris baru berlebih
                clean_p = " ".join(p.split())
                clean_posts.append(f"Post: {clean_p[:300]}") # Potong biar gak kepanjangan
            
            return "\n---\n".join(clean_posts)

        except Exception as e:
            return f"Error Facebook: {str(e)}"