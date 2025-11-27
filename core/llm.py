# core/llm.py
import ollama
import json
import re
from config import settings

class LLMProcessor:
    def __init__(self):
        self.client = ollama.Client(host=settings.OLLAMA_URL)
        self.model = settings.OLLAMA_MODEL

    def analyze_content(self, raw_text: str, query: str) -> dict:
        """
        Mengembalikan Dict: {'summary': str, 'score': int}
        """
        prompt = f"""
        Kamu adalah analis data. Analisis data mentah berikut dari pencarian "{query}".
        
        Instruksi Wajib:
        1. Berikan ringkasan singkat (maks 2 kalimat).
        2. Berikan "Sentiment Score" (Skala 1-10) berdasarkan seberapa positif/populer tren tersebut.
        3. OUTPUT HARUS FORMAT JSON SAJA. Jangan ada teks lain.
        
        Format JSON:
        {{
            "summary": "Ringkasan kamu di sini...",
            "score": 8
        }}

        Data Mentah:
        {raw_text[:3000]}
        """
        
        try:
            response = self.client.chat(model=self.model, messages=[
                {'role': 'user', 'content': prompt},
            ])
            content = response['message']['content']
            
            # Bersihkan markdown jika LLM membungkus dengan ```json ... ```
            clean_json = re.sub(r'```json\n?|```', '', content).strip()
            
            return json.loads(clean_json)
        except json.JSONDecodeError:
            # Fallback jika LLM gagal return JSON murni
            return {"summary": content[:100] + "...", "score": 0}
        except Exception as e:
            return {"summary": f"Error: {str(e)}", "score": 0}