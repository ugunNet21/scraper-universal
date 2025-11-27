# main.py
import os
import asyncio
from playwright.async_api import async_playwright

from config import settings
from scrapers.factory import ScraperFactory
from core.llm import LLMProcessor
from utils.storage import StorageManager


# ================================
#  CHART CONSOLE
# ================================
def draw_chart(platform, keyword, score):
    """Menggambar bar chart ASCII sederhana"""
    bar_length = 20
    filled_length = int(bar_length * score / 10)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)

    color_reset = "\033[0m"
    color_green = "\033[92m"
    color_cyan = "\033[96m"

    print(f"\n{color_cyan}📊 CHART ANALISIS: {platform.upper()} - {keyword}{color_reset}")
    print(f"Sentiment/Popularity Score: {score}/10")
    print(f"{color_green}|{bar}| {score * 10}%{color_reset}\n")


# ================================
#  TASK SCRAPER
# ================================
async def run_task(platform: str, keyword: str, llm: LLMProcessor):

    async with async_playwright() as p:

        # ---- AUTH SUPPORT ----
        session_file = "session.json"

        if not os.path.exists(session_file):
            print("[WARN] session.json tidak ditemukan! Mode Anonymous dipakai.")
            print("      → Jalankan utils/auth_generator.py untuk login dan simpan sesi!")
            context_options = {
                "user_agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }
        else:
            print("[INFO] Menggunakan session.json (Login Mode)")
            context_options = {
                "storage_state": session_file,
                "user_agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            }

        # ---- Launch browser ----
        browser = await p.chromium.launch(
            headless=settings.HEADLESS,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context(**context_options)
        page = await context.new_page()

        try:
            # ---- 1. SCRAPE ----
            scraper = ScraperFactory.get_scraper(platform, page)
            raw_data = await scraper.scrape(keyword)

            if isinstance(raw_data, str) and "TERDETEKSI BOT" in raw_data:
                print(f"[!] BOT DETECTED PADA {platform}, skip.")
                return

            # ---- 2. ANALISIS LLM ----
            print(f"[*] Menganalisis data {platform} dengan AI...")
            result = llm.analyze_content(raw_data, keyword)

            # ---- 3. OUTPUT ----
            print(f"\n--- HASIL: {keyword} ({platform.upper()}) ---")
            print(f"Ringkasan: {result.get('summary')}")

            # ---- 4. CHART ----
            score = result.get("score", 0)
            draw_chart(platform, keyword, score)

            # ---- 5. SAVE CSV ----
            save_data = {
                "platform": platform,
                "keyword": keyword,
                "summary": result.get("summary"),
                "score": score,
            }
            StorageManager.save_to_csv(save_data)

        except Exception as e:
            print(f"[X] ERROR di platform {platform}: {e}")

        finally:
            await browser.close()


# ================================
#  MAIN LOOP
# ================================
async def main():
    llm = LLMProcessor()

    platforms = [
        "tiktok", "youtube", "instagram", "twitter",
        "google", "threads", "facebook"
    ]

    for keyword in settings.KEYWORDS:
        for platform in platforms:
            await run_task(platform, keyword, llm)


# ================================
#  ENTRY POINT
# ================================
if __name__ == "__main__":
    print("🚀 Mulai Universal Scraper dengan Auth + LLM + Chart...")
    print(f"🎯 Target Keywords: {settings.KEYWORDS}")
    asyncio.run(main())
