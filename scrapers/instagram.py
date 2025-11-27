# scrapers/instagram.py
import asyncio
from scrapers.base import BaseScraper
from config import settings

class InstagramScraper(BaseScraper):
    async def scrape(self, keyword: str) -> str:
        # Ubah "Ide Bisnis AI" menjadi "IdeBisnisAI" untuk pencarian Hashtag
        hashtag = keyword.replace(" ", "")
        print(f"[*] Scraping Instagram Hashtag: #{hashtag}")
        
        url = f"https://www.instagram.com/explore/tags/{hashtag}/"
        
        try:
            await self.page.goto(url, timeout=settings.TIMEOUT)
            
            # Instagram sering minta login, kita coba tunggu konten muncul
            # Selector untuk grid gambar di explore page
            try:
                await self.page.wait_for_selector('article', timeout=10000)
            except:
                # Cek jika dialihkan ke halaman login
                if "login" in self.page.url:
                    return "GAGAL: Instagram meminta Login. (Perlu implementasi Cookies/Session)"
                return "KONTEN KOSONG: Tidak ada postingan untuk hashtag ini."

            # Ambil deskripsi dari atribut 'alt' pada gambar (karena caption ada di alt text img)
            # Kita ambil 15 postingan teratas
            images = await self.page.locator('article img').all()
            
            collected_text = []
            for i, img in enumerate(images[:15]): 
                alt_text = await img.get_attribute('alt')
                if alt_text:
                    collected_text.append(f"Post {i+1}: {alt_text}")
            
            if not collected_text:
                return "Data ditemukan tapi tidak ada teks deskripsi (Mungkin video tanpa alt text)."

            return "\n".join(collected_text)

        except Exception as e:
            return f"Error Instagram: {str(e)}"