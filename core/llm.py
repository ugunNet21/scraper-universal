# core/llm.py
"""
Enhanced LLM Processor dengan NLP Integration
Combines AI + Traditional NLP untuk hasil yang lebih akurat
"""

import ollama
import json
import re
from config import settings

# Import NLP Analyzer
try:
    from core.nlp_analyzer import NLPAnalyzer
    NLP_ENABLED = True
except ImportError as e:
    NLP_ENABLED = False
    print(f"[WARN] NLP Analyzer tidak tersedia: {e}")


class LLMProcessor:
    def __init__(self):
        self.client = ollama.Client(host=settings.OLLAMA_URL)
        self.model = settings.OLLAMA_MODEL
        
        # Initialize NLP Analyzer
        self.nlp_analyzer = None
        if NLP_ENABLED:
            try:
                self.nlp_analyzer = NLPAnalyzer()
                print("[✓] NLP Analyzer initialized successfully")
            except Exception as e:
                self.nlp_analyzer = None
                print(f"[!] NLP Analyzer failed to initialize: {e}")
        else:
            self.nlp_analyzer = None

    def analyze_content(self, raw_text: str, query: str) -> dict:
        """
        Enhanced Analysis: Combines LLM + NLP
        Returns: {
            'summary': str,
            'score': int,
            'nlp_analysis': dict,  # NEW
            'category': str,       # NEW
            'trend_strength': str  # NEW
        }
        """
        
        # ===== 1. NLP ANALYSIS FIRST =====
        nlp_result = None
        if self.nlp_analyzer:
            try:
                nlp_result = self.nlp_analyzer.comprehensive_analysis(raw_text)
                print(f"[NLP] Sentiment: {nlp_result['sentiment']['label']} "
                      f"(Score: {nlp_result['sentiment']['score']})")
            except Exception as e:
                print(f"[!] NLP Analysis error: {e}")
                nlp_result = None
        
        # ===== 2. LLM ANALYSIS =====
        llm_prompt = self._build_enhanced_prompt(raw_text, query, nlp_result)
        
        try:
            response = self.client.chat(model=self.model, messages=[
                {'role': 'user', 'content': llm_prompt},
            ])
            content = response['message']['content']
            
            # Enhanced JSON cleaning
            clean_json = re.sub(r'```json\n?|```', '', content).strip()
            
            # Handle multiple JSON objects atau invalid JSON
            try:
                llm_result = json.loads(clean_json)
            except json.JSONDecodeError:
                # Coba extract JSON dari teks
                llm_result = self._extract_json_from_text(clean_json)
                
        except Exception as e:
            print(f"[LLM] General Error: {e}")
            llm_result = {
                "summary": f"Analysis completed but with formatting issues",
                "score": 5,
                "category": "Unknown", 
                "trend_strength": "Medium"
            }
        
        # ===== 3. COMBINE RESULTS =====
        combined_result = self._combine_analysis(llm_result, nlp_result)
        
        return combined_result
    
    def _extract_json_from_text(self, text: str) -> dict:
        """Extract JSON from problematic text responses"""
        import re
        
        # Pattern untuk mencari JSON object
        json_pattern = r'\{[^{}]*"[^"]*"[^{}]*\}'
        matches = re.findall(json_pattern, text)
        
        if matches:
            # Ambil match terpanjang (kemungkinan JSON terbaik)
            best_match = max(matches, key=len)
            try:
                return json.loads(best_match)
            except:
                pass
        
        # Fallback: manual extraction
        summary_match = re.search(r'"summary":\s*"([^"]+)"', text)
        score_match = re.search(r'"score":\s*(\d+)', text)  
        category_match = re.search(r'"category":\s*"([^"]+)"', text)
        trend_match = re.search(r'"trend_strength":\s*"([^"]+)"', text)
        
        return {
            "summary": summary_match.group(1) if summary_match else "Analysis completed",
            "score": int(score_match.group(1)) if score_match else 5,
            "category": category_match.group(1) if category_match else "Unknown",
            "trend_strength": trend_match.group(1) if trend_match else "Medium"
        }

    def _build_enhanced_prompt(self, raw_text: str, query: str, nlp_result: dict = None) -> str:
        """Build smarter prompt dengan NLP context"""
        
        # Base prompt
        prompt = f"""
            Kamu adalah analis trend digital yang ahli. Analisis data berikut dari pencarian "{query}".

            INSTRUKSI:
            1. Buat ringkasan singkat & informatif (max 3 kalimat)
            2. Berikan skor popularitas (1-10) berdasarkan:
            - Volume konten/engagement
            - Sentiment publik
            - Trending indicators
            3. Tentukan kategori trend: Entertainment, Business, Technology, Social Issue, Sports, atau Other
            4. Tentukan kekuatan trend: Viral, Rising, Stable, atau Declining

        """
        
        # Add NLP context jika ada
        if nlp_result:
            sentiment_label = nlp_result['sentiment']['label']
            sentiment_score = nlp_result['sentiment']['score']
            top_keywords = ', '.join([kw[0] for kw in nlp_result['keywords'][:5]])
            
            prompt += f"""
                CONTEXT NLP ANALYSIS:
                - Sentiment: {sentiment_label} ({sentiment_score}/10)
                - Top Keywords: {top_keywords}
                - Engagement Metrics: {nlp_result['engagement']['avg_engagement']}

            """
        
        prompt += f"""
            OUTPUT FORMAT (JSON ONLY):
            {{
                "summary": "Ringkasan kamu...",
                "score": 8,
                "category": "Entertainment",
                "trend_strength": "Viral"
            }}

            DATA MENTAH:
            {raw_text[:3500]}
        """
        
        return prompt
    
    def _combine_analysis(self, llm_result: dict, nlp_result: dict = None) -> dict:
        """Combine LLM & NLP results"""
        
        combined = {
            'summary': llm_result.get('summary', ''),
            'score': llm_result.get('score', 5),
            'category': llm_result.get('category', 'Unknown'),
            'trend_strength': llm_result.get('trend_strength', 'Medium')
        }
        
        # Add NLP analysis jika ada
        if nlp_result:
            combined['nlp_analysis'] = {
                'sentiment_label': nlp_result['sentiment']['label'],
                'sentiment_score': nlp_result['sentiment']['score'],
                'top_keywords': [kw[0] for kw in nlp_result['keywords'][:5]],
                'engagement': nlp_result['engagement'],
                'lexical_diversity': nlp_result['text_stats']['lexical_diversity']
            }
            
            # Adjust score berdasarkan NLP sentiment jika berbeda signifikan
            nlp_score = nlp_result['sentiment']['score']
            llm_score = combined['score']
            
            # Average jika gap > 2
            if abs(nlp_score - llm_score) > 2:
                combined['score'] = round((nlp_score + llm_score) / 2)
                combined['score_adjusted'] = True
            else:
                combined['score_adjusted'] = False
        
        else:
            combined['nlp_analysis'] = None
        
        return combined
