# utils/auth_generator.py
import asyncio
from playwright.async_api import async_playwright

# Nama file tempat menyimpan session
SESSION_FILE = "session.json"

async def generate_session():
    print("🚀 Membuka Browser 'Stealth' untuk Login Manual...")
    
    async with async_playwright() as p:
        # --- PERUBAHAN PENTING DISINI ---
        # Kita tambahkan argumen khusus agar Google tidak tahu ini bot
        browser = await p.chromium.launch(
            headless=False,
            # Argumen untuk menyembunyikan identitas bot
            args=[
                "--disable-blink-features=AutomationControlled", # Matikan fitur kontrol otomatis
                "--no-sandbox",
                "--disable-infobars" 
            ],
            # Hapus banner "Chrome is being controlled by automated test software"
            ignore_default_args=["--enable-automation"]
        )
        
        # Gunakan User Agent Manusia Asli & Viewport standar laptop
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768}
        )
        
        page = await context.new_page()

        # --- TRIK EXTRA: Hapus property 'webdriver' via Javascript ---
        # Ini langkah kunci untuk menipu Google
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """)

        print("\n--- INSTRUKSI (MODE STEALTH) ---")
        print("1. Browser akan terbuka (tanpa banner 'automated').")
        print("2. Login ke akun-akun target (Sekarang Google harusnya mau menerima):")
        print("   - https://accounts.google.com (Login di sini dulu)")
        print("   - https://www.facebook.com")
        print("   - https://www.instagram.com")
        print("   - https://x.com")
        print("   - https://www.threads.net")
        print("3. Jika sudah semua, kembali ke terminal ini dan TEKAN ENTER.")
        print("-----------------\n")

        # Buka halaman login Google langsung
        await page.goto("https://accounts.google.com")

        input("👉 SUDAH SELESAI LOGIN SEMUA? Tekan Enter untuk menyimpan session...")

        await context.storage_state(path=SESSION_FILE)
        print(f"\n[✔] Session berhasil disimpan di: {SESSION_FILE}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(generate_session())