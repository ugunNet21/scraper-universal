# utils/storage.py
import csv
import os
from datetime import datetime
from config import settings


class StorageManager:
    # Enhanced CSV columns dengan NLP metrics
    FIELDNAMES = [
        "timestamp",
        "platform", 
        "keyword",
        "score",
        "category",      
        "trend_strength",
        "nlp_sentiment", 
        "nlp_score",     
        "top_keywords",  
        "summary"
    ]
    
    @staticmethod
    def save_to_csv(data: dict):
        """
        Save enhanced data to CSV dengan NLP metrics
        """
        file_exists = os.path.isfile(settings.CSV_FILE)
        
        with open(settings.CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=StorageManager.FIELDNAMES)
            
            if not file_exists:
                writer.writeheader()
            
            # Add timestamp
            data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Ensure all fields exist (fill missing with N/A)
            for field in StorageManager.FIELDNAMES:
                if field not in data:
                    data[field] = 'N/A'
            
            writer.writerow(data)
            print(f"[✔] Data saved to {settings.CSV_FILE}")
    
    
    @staticmethod
    def load_from_csv() -> list:
        """Load all data from CSV"""
        if not os.path.exists(settings.CSV_FILE):
            return []
        
        with open(settings.CSV_FILE, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    
    @staticmethod
    def get_statistics(keyword: str = None) -> dict:
        """
        Get statistical summary dari CSV data
        Args:
            keyword: Filter by specific keyword (optional)
        """
        data = StorageManager.load_from_csv()
        
        if not data:
            return {"error": "No data available"}
        
        # Filter by keyword if provided
        if keyword:
            data = [row for row in data if row['keyword'].lower() == keyword.lower()]
        
        if not data:
            return {"error": f"No data for keyword: {keyword}"}
        
        # Calculate statistics
        scores = [float(row['score']) for row in data if row['score'] != 'N/A']
        
        stats = {
            'total_records': len(data),
            'avg_score': sum(scores) / len(scores) if scores else 0,
            'max_score': max(scores) if scores else 0,
            'min_score': min(scores) if scores else 0,
            'platforms': list(set(row['platform'] for row in data)),
            'categories': list(set(row['category'] for row in data if row['category'] != 'N/A')),
            'latest_analysis': data[-1]['timestamp'] if data else None
        }
        
        return stats
