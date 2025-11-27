# storage.py
import csv
import os
from datetime import datetime
from config import settings

class StorageManager:
    @staticmethod
    def save_to_csv(data: dict):
        """
        Menyimpan dictionary data ke CSV.
        Data diharapkan punya key: platform, keyword, summary, score, timestamp
        """
        file_exists = os.path.isfile(settings.CSV_FILE)
        
        with open(settings.CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "platform", "keyword", "score", "summary"])
            
            if not file_exists:
                writer.writeheader()  # Tulis header jika file baru
            
            # Tambahkan timestamp
            data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(data)
            print(f"[✔] Data tersimpan di {settings.CSV_FILE}")