# scrapers/youtube.py
import asyncio
from scrapers.base import BaseScraper
from config import settings

class YoutubeScraper(BaseScraper):
    async def scrape(self, keyword: str) -> str:
        print(f"[*] Scraping YouTube untuk: {keyword}")
        
        # URL Search YouTube
        url = f"https://www.youtube.com/results?search_query={keyword}"
        
        try:
            await self.page.goto(url, timeout=settings.TIMEOUT)
            
            # Tunggu elemen video muncul
            # ytd-video-renderer adalah container utama per video di hasil search
            try:
                await self.page.wait_for_selector('ytd-video-renderer', timeout=10000)
            except:
                return "YouTube tidak memuat hasil (Timeout)."

            # Ambil judul dan metadata video
            videos = await self.page.locator('ytd-video-renderer').all()
            
            collected_data = []
            
            # Kita ambil 10 video teratas saja agar cepat
            for i, video in enumerate(videos[:10]):
                # Ambil Judul
                title_el = video.locator('#video-title')
                title = await title_el.inner_text()
                
                # Ambil Metadata (Views & Time) - biasanya ada di #metadata-line
                meta_el = video.locator('#metadata-line')
                meta = await meta_el.inner_text() if await meta_el.count() > 0 else "No metadata"
                
                # Bersihkan newline
                meta = meta.replace('\n', ' | ')
                
                collected_data.append(f"Video {i+1}: {title} ({meta})")
            
            if not collected_data:
                return "Elemen ditemukan tapi gagal mengekstrak teks."

            return "\n".join(collected_data)

        except Exception as e:
            return f"Error YouTube: {str(e)}"