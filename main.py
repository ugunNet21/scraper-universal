# main.py - ENHANCED VERSION dengan NLP Integration
import os
import asyncio
from playwright.async_api import async_playwright

from config import settings
from scrapers.factory import ScraperFactory
from core.llm import LLMProcessor
from utils.storage import StorageManager

# Import Enhanced Visualizer
try:
    from utils.visualizer import Visualizer
    VIZ_ENABLED = True
except ImportError:
    VIZ_ENABLED = False
    print("[WARN] Enhanced visualizer not available. Using basic charts.")


# ================================
#  FALLBACK BASIC CHART (jika visualizer.py tidak ada)
# ================================
def draw_basic_chart(platform, keyword, score):
    """Simple fallback chart"""
    bar_length = 20
    filled_length = int(bar_length * score / 10)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    print(f"\n📊 {platform.upper()} - {keyword}")
    print(f"Score: {score}/10")
    print(f"|{bar}| {score * 10}%\n")


# ================================
#  TASK SCRAPER (Enhanced)
# ================================
async def run_task(platform: str, keyword: str, llm: LLMProcessor):
    async with async_playwright() as p:
        # ---- AUTH SUPPORT ----
        session_file = "session.json"

        if not os.path.exists(session_file):
            print("[WARN] session.json tidak ditemukan! Mode Anonymous.")
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
                print(f"[!] BOT DETECTED di {platform}, skip.")
                return None

            # ---- 2. ANALISIS LLM + NLP ----
            print(f"[*] Menganalisis {platform} dengan AI + NLP...")
            result = llm.analyze_content(raw_data, keyword)
            
            # Add platform & keyword ke result
            result['platform'] = platform
            result['keyword'] = keyword

            # ---- 3. ENHANCED VISUALIZATION ----
            if VIZ_ENABLED:
                viz = Visualizer()
                viz.draw_comprehensive_dashboard(result)
            else:
                # Fallback ke basic chart
                print(f"\n--- HASIL: {keyword} ({platform.upper()}) ---")
                print(f"Summary: {result.get('summary')}")
                print(f"Category: {result.get('category')}")
                print(f"Trend: {result.get('trend_strength')}")
                draw_basic_chart(platform, keyword, result['score'])

            # ---- 4. SAVE CSV ----
            save_data = {
                "platform": platform,
                "keyword": keyword,
                "summary": result.get("summary", ""),
                "score": result.get("score", 0),
                "category": result.get("category", "Unknown"),
                "trend_strength": result.get("trend_strength", "Unknown")
            }
            
            # Add NLP metrics jika ada
            if result.get('nlp_analysis'):
                nlp = result['nlp_analysis']
                save_data['nlp_sentiment'] = nlp.get('sentiment_label', 'N/A')
                save_data['nlp_score'] = nlp.get('sentiment_score', 0)
                save_data['top_keywords'] = ', '.join(nlp.get('top_keywords', []))
            
            StorageManager.save_to_csv(save_data)
            
            return result

        except Exception as e:
            print(f"[X] ERROR di {platform}: {e}")
            return None

        finally:
            await browser.close()


# ================================
#  MAIN LOOP (Enhanced)
# ================================
async def main():
    llm = LLMProcessor()
    
    platforms = [
        "tiktok", "youtube", "instagram", "twitter",
        "google", "threads", "facebook"
    ]
    
    all_results = []
    
    print("\n" + "="*80)
    print("🚀 UNIVERSAL SCRAPER - ENHANCED NLP VERSION")
    print("="*80)
    print(f"🎯 Keywords: {settings.KEYWORDS}")
    print(f"📱 Platforms: {', '.join(platforms)}")
    print(f"🤖 AI Model: {settings.OLLAMA_MODEL}")
    print(f"🔬 NLP: {'ENABLED ✓' if llm.nlp_analyzer else 'DISABLED ✗'}")
    print("="*80 + "\n")

    for keyword in settings.KEYWORDS:
        print(f"\n{'═'*80}")
        print(f"Processing Keyword: {keyword.upper()}")
        print(f"{'═'*80}\n")
        
        for platform in platforms:
            result = await run_task(platform, keyword, llm)
            if result:
                all_results.append(result)
            
            # Small delay between platforms
            await asyncio.sleep(2)
    
    # ---- FINAL SUMMARY REPORT ----
    if VIZ_ENABLED and all_results:
        viz = Visualizer()
        summary = viz.generate_summary_report(all_results)
        print(summary)
        
        # Save summary to file
        with open("analysis_summary.txt", "w", encoding="utf-8") as f:
            f.write(summary)
        print("[✓] Summary report saved to: analysis_summary.txt")


# ================================
#  ENTRY POINT
# ================================
if __name__ == "__main__":
    asyncio.run(main())