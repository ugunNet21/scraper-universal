# utils/visualizer.py
"""
Enhanced Visualization Module
- Better ASCII Charts
- Multi-metric Dashboard
- Summary Report Generator
"""

from typing import Dict, List
from datetime import datetime


class Visualizer:
    """Enhanced Console Visualization"""
    
    # ANSI Color Codes
    COLORS = {
        'reset': '\033[0m',
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'bold': '\033[1m',
        'underline': '\033[4m'
    }
    
    @staticmethod
    def color(text: str, color: str) -> str:
        """Apply color to text"""
        return f"{Visualizer.COLORS.get(color, '')}{text}{Visualizer.COLORS['reset']}"
    
    
    @staticmethod
    def draw_bar_chart(label: str, value: float, max_value: float = 10, width: int = 30) -> str:
        """
        Draw horizontal bar chart
        Args:
            label: Chart label
            value: Current value
            max_value: Maximum scale value
            width: Bar width in characters
        """
        percentage = min(value / max_value, 1.0)
        filled_length = int(width * percentage)
        
        # Color coding
        if percentage >= 0.8:
            bar_color = 'green'
        elif percentage >= 0.5:
            bar_color = 'yellow'
        else:
            bar_color = 'red'
        
        bar = '█' * filled_length + '░' * (width - filled_length)
        colored_bar = Visualizer.color(bar, bar_color)
        
        return f"{label:20} |{colored_bar}| {value:.1f}/{max_value}"
    
    
    @staticmethod
    def draw_sentiment_gauge(sentiment_score: float, sentiment_label: str):
        """
        Visual sentiment gauge
        Score: 0-10
        """
        print("\n" + "="*60)
        print(Visualizer.color("📊 SENTIMENT ANALYSIS", 'bold'))
        print("="*60)
        
        # Gauge visualization
        gauge_width = 40
        position = int((sentiment_score / 10) * gauge_width)
        
        gauge = ['─'] * gauge_width
        gauge[position] = '█'
        
        # Color zones
        if sentiment_score >= 7:
            gauge_str = Visualizer.color(''.join(gauge), 'green')
            label_color = 'green'
        elif sentiment_score >= 4:
            gauge_str = Visualizer.color(''.join(gauge), 'yellow')
            label_color = 'yellow'
        else:
            gauge_str = Visualizer.color(''.join(gauge), 'red')
            label_color = 'red'
        
        print(f"Negative  {gauge_str}  Positive")
        print(f"    0                {sentiment_score:.1f}/10                10")
        print(f"\nLabel: {Visualizer.color(sentiment_label, label_color)}")
        print("="*60 + "\n")
    
    
    @staticmethod
    def draw_comprehensive_dashboard(data: Dict):
        """
        Full dashboard dengan multiple metrics
        
        Expected data structure:
        {
            'platform': str,
            'keyword': str,
            'score': float,
            'category': str,
            'trend_strength': str,
            'nlp_analysis': {...}
        }
        """
        print("\n" + Visualizer.color("╔" + "═"*78 + "╗", 'cyan'))
        print(Visualizer.color(f"║  {'COMPREHENSIVE TREND ANALYSIS':^76}  ║", 'cyan'))
        print(Visualizer.color("╚" + "═"*78 + "╝", 'cyan'))
        
        # Header Info
        print(f"\n🎯 Keyword: {Visualizer.color(data['keyword'], 'bold')}")
        print(f"📱 Platform: {Visualizer.color(data['platform'].upper(), 'bold')}")
        print(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📂 Category: {Visualizer.color(data.get('category', 'N/A'), 'yellow')}")
        print(f"🔥 Trend Strength: {Visualizer.color(data.get('trend_strength', 'N/A'), 'magenta')}")
        
        # Main Score Bar
        print(f"\n{Visualizer.draw_bar_chart('Overall Score', data['score'], 10)}")
        
        # NLP Analysis (jika ada)
        if data.get('nlp_analysis'):
            nlp = data['nlp_analysis']
            
            print(f"\n{Visualizer.color('─' * 80, 'cyan')}")
            print(Visualizer.color("🤖 NLP ANALYSIS DETAILS", 'bold'))
            print(Visualizer.color('─' * 80, 'cyan'))
            
            # Sentiment
            print(f"{Visualizer.draw_bar_chart('NLP Sentiment', nlp['sentiment_score'], 10)}")
            print(f"   Label: {Visualizer.color(nlp['sentiment_label'], 'green' if nlp['sentiment_label'] == 'Positive' else 'red')}")
            
            # Keywords
            if nlp.get('top_keywords'):
                keywords_str = ', '.join(nlp['top_keywords'])
                print(f"\n🔑 Top Keywords: {Visualizer.color(keywords_str, 'yellow')}")
            
            # Engagement
            if nlp.get('engagement'):
                eng = nlp['engagement']
                print(f"💬 Avg Engagement: {Visualizer.color(str(eng['avg_engagement']), 'magenta')}")
            
            # Lexical Diversity
            if 'lexical_diversity' in nlp:
                ld = nlp['lexical_diversity']
                print(f"📚 Lexical Diversity: {Visualizer.color(f'{ld:.2f}', 'cyan')} (uniqueness)")
        
        # Summary
        print(f"\n{Visualizer.color('─' * 80, 'cyan')}")
        print(Visualizer.color("📝 SUMMARY", 'bold'))
        print(Visualizer.color('─' * 80, 'cyan'))
        print(f"{data.get('summary', 'No summary available')}")
        
        print(f"\n{Visualizer.color('═' * 80, 'cyan')}\n")
    
    
    @staticmethod
    def generate_summary_report(all_results: List[Dict]) -> str:
        """
        Generate text summary report dari multiple results
        """
        if not all_results:
            return "No data to report."
        
        report = []
        report.append("\n" + "="*80)
        report.append("📊 TREND ANALYSIS SUMMARY REPORT")
        report.append("="*80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Total Analysis: {len(all_results)}")
        report.append("")
        
        # Group by keyword
        keywords = {}
        for result in all_results:
            kw = result['keyword']
            if kw not in keywords:
                keywords[kw] = []
            keywords[kw].append(result)
        
        for keyword, results in keywords.items():
            report.append(f"\n{'─'*80}")
            report.append(f"🎯 KEYWORD: {keyword.upper()}")
            report.append(f"{'─'*80}")
            
            # Statistics
            avg_score = sum(r['score'] for r in results) / len(results)
            max_score = max(results, key=lambda x: x['score'])
            
            report.append(f"\n📈 Statistics:")
            report.append(f"  • Average Score: {avg_score:.1f}/10")
            report.append(f"  • Best Platform: {max_score['platform']} ({max_score['score']}/10)")
            report.append(f"  • Total Platforms: {len(results)}")
            
            # Platform breakdown
            report.append(f"\n📱 Platform Breakdown:")
            for r in sorted(results, key=lambda x: x['score'], reverse=True):
                report.append(f"  • {r['platform']:12} → Score: {r['score']}/10 | {r.get('trend_strength', 'N/A')}")
        
        report.append("\n" + "="*80 + "\n")
        
        return "\n".join(report)
