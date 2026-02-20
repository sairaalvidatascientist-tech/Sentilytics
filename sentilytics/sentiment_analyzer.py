"""
Sentiment Analyzer Module
Uses VADER and TextBlob for real-time sentiment analysis
"""

import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import re
from typing import Dict, List

class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analysis tools"""
        # Download required NLTK data
        try:
            nltk.data.find('vader_lexicon')
        except LookupError:
            nltk.download('vader_lexicon', quiet=True)
        
        self.vader = SentimentIntensityAnalyzer()
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess text"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove mentions
        text = re.sub(r'@\w+', '', text)
        # Remove hashtags but keep the text
        text = re.sub(r'#(\w+)', r'\1', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of text
        Returns: dict with sentiment scores and classification
        """
        cleaned_text = self.clean_text(text)
        
        # VADER sentiment analysis
        vader_scores = self.vader.polarity_scores(cleaned_text)
        
        # TextBlob for additional analysis
        blob = TextBlob(cleaned_text)
        
        # Determine primary sentiment
        compound = vader_scores['compound']
        if compound >= 0.05:
            sentiment = 'positive'
        elif compound <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        # Determine emotion (simplified)
        emotion = self._detect_emotion(cleaned_text, vader_scores)
        
        return {
            'sentiment': sentiment,
            'emotion': emotion,
            'scores': {
                'positive': vader_scores['pos'],
                'negative': vader_scores['neg'],
                'neutral': vader_scores['neu'],
                'compound': vader_scores['compound']
            },
            'polarity': blob.sentiment.polarity,
            'subjectivity': blob.sentiment.subjectivity
        }
    
    def _detect_emotion(self, text: str, vader_scores: Dict) -> str:
        """Detect primary emotion from text"""
        text_lower = text.lower()
        
        # Simple keyword-based emotion detection
        joy_words = ['happy', 'excited', 'love', 'great', 'amazing', 'wonderful', 'fantastic']
        anger_words = ['angry', 'hate', 'furious', 'terrible', 'worst', 'awful']
        fear_words = ['scared', 'afraid', 'worried', 'concerned', 'anxious']
        sadness_words = ['sad', 'disappointed', 'depressed', 'unhappy']
        
        if any(word in text_lower for word in joy_words):
            return 'joy'
        elif any(word in text_lower for word in anger_words):
            return 'anger'
        elif any(word in text_lower for word in fear_words):
            return 'fear'
        elif any(word in text_lower for word in sadness_words):
            return 'sadness'
        elif vader_scores['compound'] >= 0.5:
            return 'joy'
        elif vader_scores['compound'] <= -0.5:
            return 'anger'
        else:
            return 'neutral'
    
    def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Analyze multiple texts"""
        return [self.analyze_sentiment(text) for text in texts]
    
    def get_sentiment_distribution(self, analyses: List[Dict]) -> Dict:
        """Calculate sentiment distribution from multiple analyses"""
        if not analyses:
            return {'positive': 0, 'negative': 0, 'neutral': 0}
        
        total = len(analyses)
        positive = sum(1 for a in analyses if a['sentiment'] == 'positive')
        negative = sum(1 for a in analyses if a['sentiment'] == 'negative')
        neutral = sum(1 for a in analyses if a['sentiment'] == 'neutral')
        
        return {
            'positive': round((positive / total) * 100, 1),
            'negative': round((negative / total) * 100, 1),
            'neutral': round((neutral / total) * 100, 1),
            'counts': {
                'positive': positive,
                'negative': negative,
                'neutral': neutral,
                'total': total
            }
        }
