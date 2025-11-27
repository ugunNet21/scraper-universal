# core/nlp_analyzer.py
"""
Enhanced NLP & ML Module untuk Analisis Mendalam
- Sentiment Analysis dengan TextBlob & VADER
- Text Preprocessing & Feature Extraction
- Topic Modeling
- Keyword Extraction
- Statistical Analysis
"""

import re
from collections import Counter
from typing import Dict, List, Tuple
import json

# Install: pip install textblob vaderSentiment scikit-learn
try:
    from textblob import TextBlob
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    from sklearn.feature_extraction.text import TfidfVectorizer
    
    NLP_AVAILABLE = True
except ImportError as e:
    NLP_AVAILABLE = False
    print(f"[WARN] NLP libraries not installed: {e}")


class NLPAnalyzer:
    """Advanced NLP Analyzer dengan Custom Tokenizer (No NLTK)"""
    
    def __init__(self):
        if not NLP_AVAILABLE:
            raise ImportError("NLP libraries required. Run: pip install textblob vaderSentiment scikit-learn")
        
        self.vader = SentimentIntensityAnalyzer()
        
        # Comprehensive stopwords list (Indonesian + English)
        self.stop_words = set([
            # Indonesian stopwords
            'yang', 'untuk', 'pada', 'adalah', 'ini', 'itu', 'dengan', 'dari', 'di', 'dan', 'atau', 
            'dalam', 'juga', 'bisa', 'ada', 'akan', 'dia', 'kamu', 'kita', 'mereka', 'saya', 'tak', 
            'tidak', 'ya', 'telah', 'untuk', 'waktu', 'orang', 'saat', 'nama', 'hari', 'baru', 'lagi', 
            'tahun', 'bulan', 'minggu', 'jam', 'menit', 'detik', 'sebagai', 'oleh', 'karena', 'jika',
            'ke', 'para', 'amat', 'agar', 'ataupun', 'bahwa', 'demi', 'dengan', 'hingga', 'jangan',
            'lagi', 'melainkan', 'memang', 'mengingat', 'meski', 'mungkin', 'nantinya', 'oleh',
            'pula', 'sambil', 'sampai', 'saja', 'saling', 'sangat', 'sebab', 'sebagai', 'sebelum',
            'sebuah', 'secara', 'sedang', 'segera', 'sehingga', 'sejak', 'sekali', 'sekaligus',
            'selama', 'selanjutnya', 'semua', 'semula', 'sendiri', 'seolah', 'seorang', 'seperti',
            'seraya', 'sering', 'serta', 'sesuatu', 'sesungguhnya', 'setelah', 'setiap', 'seusai',
            'suatu', 'sudah', 'supaya', 'tadi', 'tahu', 'tahun', 'tapi', 'tepat', 'terhadap',
            'terus', 'tetap', 'tetapi', 'tiap', 'tidak', 'tidaklah', 'tinggal', 'to', 'tuju',
            'ujar', 'umumnya', 'untuk', 'usah', 'usai', 'waduh', 'wah', 'waktu', 'walau', 'wong',
            
            # English stopwords  
            'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us',
            'them', 'my', 'your', 'his', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours',
            'theirs', 'what', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why', 'how',
            'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no',
            'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'now'
        ])
    
    
    def preprocess_text(self, text: str) -> str:
        """Text Cleaning & Normalization"""
        if not text or not isinstance(text, str):
            return ""
            
        # Lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        
        # Remove mentions & hashtags (tapi keep textnya)
        text = re.sub(r'@(\w+)', r'\1', text)  # Keep username tanpa @
        text = re.sub(r'#(\w+)', r'\1', text)  # Keep hashtag text tanpa #
        
        # Remove special characters (keep letters, numbers, spaces, basic punctuation)
        text = re.sub(r'[^a-zA-Z0-9\s.,!?]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    
    def robust_tokenize(self, text: str) -> List[str]:
        """
        Robust tokenization menggunakan regex (No NLTK dependency)
        Handles multiple languages including Indonesian
        """
        text = self.preprocess_text(text)
        if not text:
            return []
            
        # Advanced regex tokenization
        # Pattern: words (including Indonesian characters), numbers, and some special cases
        tokens = re.findall(r'[a-zA-ZÀ-ÿ0-9]+(?:\'[a-zA-ZÀ-ÿ]+)?|[a-zA-ZÀ-ÿ]+|[0-9]+', text)
        
        # Filter stopwords & short words, apply stemming-like simplification
        filtered = []
        for word in tokens:
            # Skip stopwords and very short words
            if word.lower() in self.stop_words or len(word) < 2:
                continue
                
            # Simple stemming for common suffixes (Indonesian & English)
            word_simple = self._simple_stem(word.lower())
            
            filtered.append(word_simple)
        
        return filtered
    
    def _simple_stem(self, word: str) -> str:
        """Simple stemming untuk kata umum (Indonesian & English)"""
        # Indonesian suffixes
        id_suffixes = ['nya', 'lah', 'kah', 'pun', 'ku', 'mu']
        for suffix in id_suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                word = word[:-len(suffix)]
                break
        
        # English suffixes
        en_suffixes = ['ing', 'ed', 'es', 's', 'ly']
        for suffix in en_suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                word = word[:-len(suffix)]
                break
        
        return word
    
    
    def sentiment_analysis_vader(self, text: str) -> Dict:
        """
        Sentiment Analysis menggunakan VADER
        Returns: {'compound': float, 'pos': float, 'neu': float, 'neg': float}
        """
        if not text:
            return {'scores': {'compound': 0, 'pos': 0, 'neu': 0, 'neg': 0}, 'label': 'Neutral', 'confidence': 0}
            
        scores = self.vader.polarity_scores(text)
        
        # Interpretasi
        compound = scores['compound']
        if compound >= 0.05:
            label = "Positive"
        elif compound <= -0.05:
            label = "Negative"
        else:
            label = "Neutral"
        
        return {
            'scores': scores,
            'label': label,
            'confidence': abs(compound)
        }
    
    
    def sentiment_analysis_textblob(self, text: str) -> Dict:
        """
        Sentiment Analysis menggunakan TextBlob
        Returns: {'polarity': float, 'subjectivity': float}
        """
        if not text:
            return {'polarity': 0, 'subjectivity': 0, 'label': 'Neutral'}
            
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            if polarity > 0.1:
                label = "Positive"
            elif polarity < -0.1:
                label = "Negative"
            else:
                label = "Neutral"
            
            return {
                'polarity': polarity,
                'subjectivity': subjectivity,
                'label': label
            }
        except:
            return {'polarity': 0, 'subjectivity': 0, 'label': 'Neutral'}
    
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """Extract Top Keywords by Frequency"""
        tokens = self.robust_tokenize(text)
        if not tokens:
            return []
            
        counter = Counter(tokens)
        keywords = counter.most_common(top_n)
        
        # Filter hanya kata yang meaningful (minimal 2 karakter dan muncul minimal 1 kali)
        return [(word, count) for word, count in keywords if len(word) >= 2]
    
    
    def extract_tfidf_keywords(self, texts: List[str], top_n: int = 10) -> List[str]:
        """
        Extract Keywords using TF-IDF
        texts: List of documents
        """
        if len(texts) < 2:
            return []
        
        # Custom tokenizer untuk TF-IDF
        def custom_tokenizer(text):
            return self.robust_tokenize(text)
        
        vectorizer = TfidfVectorizer(
            max_features=top_n,
            tokenizer=custom_tokenizer,
            token_pattern=None,  # Use custom tokenizer
            ngram_range=(1, 2)  # unigram + bigram
        )
        
        try:
            vectorizer.fit_transform(texts)
            return vectorizer.get_feature_names_out().tolist()
        except Exception as e:
            print(f"[TF-IDF] Error: {e}")
            return []
    
    
    def analyze_engagement_metrics(self, text: str) -> Dict:
        """
        Analisis Metrik Engagement dari Teks
        - Deteksi angka (views, likes, dll)
        - Hitung rata-rata engagement
        """
        if not text:
            return {'avg_engagement': 0, 'total_metrics': 0}
            
        # Extract numbers dengan berbagai pattern
        patterns = [
            r'(\d+(?:\.\d+)?)\s*(?:rb|ribu)\b',
            r'(\d+(?:\.\d+)?)\s*(?:jt|juta)\b', 
            r'(\d+(?:\.\d+)?)\s*k\b',
            r'(\d+(?:\.\d+)?)\s*m\b',
            r'(\d+(?:\.\d+)?)\s*(?:views|likes|share|comments|subscribers|followers)\b',
            r'(\d+(?:,\d+)+)\b',  # numbers with commas
            r'(\d+)\s*(?:x|times)\b'  # engagement multipliers
        ]
        
        all_numbers = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            all_numbers.extend(matches)
        
        if not all_numbers:
            return {'avg_engagement': 0, 'total_metrics': 0}
        
        # Convert ke angka
        total = 0
        count = 0
        
        for num in all_numbers:
            try:
                # Clean number (remove commas)
                num_clean = num.replace(',', '')
                val = float(num_clean)
                
                # Apply multipliers berdasarkan konteks
                if any(x in text.lower() for x in ['rb', 'ribu']):
                    val *= 1000
                elif any(x in text.lower() for x in ['jt', 'juta']):
                    val *= 1000000
                elif 'k' in text.lower():
                    val *= 1000
                elif 'm' in text.lower():
                    val *= 1000000
                    
                total += val
                count += 1
                print(f"[ENGAGEMENT] Found number: {num} -> {val}")
            except Exception as e:
                print(f"[ENGAGEMENT] Error converting {num}: {e}")
                pass
        
        avg = total / count if count > 0 else 0
        
        return {
            'avg_engagement': round(avg, 2),
            'total_metrics': count
        }
    
    
    def comprehensive_analysis(self, text: str) -> Dict:
        """
        Full NLP Analysis Pipeline
        Combines all methods above
        """
        if not text:
            return self._get_empty_analysis()
            
        try:
            print(f"[NLP] Analyzing text length: {len(text)}")
            
            # Sentiment Analysis (2 methods)
            vader_sentiment = self.sentiment_analysis_vader(text)
            textblob_sentiment = self.sentiment_analysis_textblob(text)
            
            # Keyword Extraction
            keywords = self.extract_keywords(text, top_n=10)
            print(f"[NLP] Extracted {len(keywords)} keywords")
            
            # Engagement Metrics
            engagement = self.analyze_engagement_metrics(text)
            print(f"[NLP] Engagement: {engagement}")
            
            # Text Stats
            tokens = self.robust_tokenize(text)
            word_count = len(tokens)
            unique_words = len(set(tokens))
            
            # Combined Sentiment Score (Average dari VADER & TextBlob)
            # Normalize to 1-10 scale
            vader_score = (vader_sentiment['scores']['compound'] + 1) / 2  # 0-1
            textblob_score = (textblob_sentiment['polarity'] + 1) / 2  # 0-1
            
            combined_score = ((vader_score + textblob_score) / 2) * 10  # 1-10 scale
            
            # Determine final label
            if combined_score >= 6:
                final_label = "Positive"
            elif combined_score <= 4:
                final_label = "Negative"
            else:
                final_label = "Neutral"
            
            result = {
                'sentiment': {
                    'score': round(combined_score, 2),
                    'label': final_label,
                    'vader': vader_sentiment,
                    'textblob': textblob_sentiment
                },
                'keywords': keywords,
                'engagement': engagement,
                'text_stats': {
                    'word_count': word_count,
                    'unique_words': unique_words,
                    'lexical_diversity': round(unique_words / word_count, 2) if word_count > 0 else 0
                }
            }
            
            print(f"[NLP] Analysis completed: {result['sentiment']['label']} ({result['sentiment']['score']}/10)")
            return result
            
        except Exception as e:
            print(f"[NLP] Comprehensive analysis error: {e}")
            return self._get_empty_analysis()
    
    def _get_empty_analysis(self) -> Dict:
        """Return empty analysis when error occurs"""
        return {
            'sentiment': {
                'score': 5.0,
                'label': 'Neutral',
                'vader': {'scores': {'compound': 0}, 'label': 'Neutral', 'confidence': 0},
                'textblob': {'polarity': 0, 'subjectivity': 0, 'label': 'Neutral'}
            },
            'keywords': [],
            'engagement': {'avg_engagement': 0, 'total_metrics': 0},
            'text_stats': {
                'word_count': 0,
                'unique_words': 0,
                'lexical_diversity': 0
            }
        }