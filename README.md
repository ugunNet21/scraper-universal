# 🌐 Universal Scraper (AI + Auth + Multi-Platform)

Universal Scraper adalah sistem scraping cerdas yang dapat:
- 🔎 Scrape banyak platform (TikTok, YouTube, Instagram, Twitter/X, Google, Threads, Facebook)
- 🤖 Menganalisis hasil menggunakan LLM (AI)
- 📊 Menampilkan grafik ASCII (Sentiment & Popularity Score)
- 📁 Menyimpan hasil ke CSV
- 🔐 Mendukung **login session** via `session.json` (Anti Bot Detection)

Sistem ini cocok untuk:
- Riset trend digital
- Analisis sentimen
- Social listening
- Riset kompetitor
- Pengumpulan data konten

---

## 🚀 **Features**
- ✔ Async Playwright Scraper  
- ✔ Auto-detect login session  
- ✔ Human-like browser fingerprint  
- ✔ LLM content analyzer (JSON output)  
- ✔ CSV export  
- ✔ Multi-platform & multi-keyword support  
- ✔ Anti-bot bypass (`AutomationControlled` disabled)  

---

## Struktur
```bash
universal_scraper/
├── .env
├── requirements.txt
├── main.py
├── config.py
├── core/
│   ├── llm.py
│   └── browser.py
├── scrapers/
│   ├── base.py
│   ├── google.py
│   ├── tiktok.py
│   ├── youtube.py
│   ├── instagram.py
│   ├── twitter.py
│   ├── facebook.py
│   ├── threads.py
│   └── factory.py
└── utils/
    ├── logger.py
    ├── storage.py
    └── auth_generator.py


```

## Membuat Venv
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Run
```bash
pyhton utils/auth_generator.py
python main.py
ollama serve
```

## Output
```bash
[INFO] Menggunakan session.json (Login Mode)
[*] Scraping TikTok untuk: Tren framework web 2025
[*] Menganalisis data tiktok dengan AI...

📊 CHART ANALISIS: TIKTOK - Tren framework web 2025
Sentiment/Popularity Score: 8/10
|████████████████----| 80%

[✔] Data tersimpan di hasil_scraping.csv

```