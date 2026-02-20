"""
Sentiment Analysis Engine for Sentilytics
Uses VADER and TextBlob for sentiment analysis
"""
import re
import string
from typing import Dict, List, Tuple
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import nltk

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

class SentimentAnalyzer:
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer()
        
        # Emoji to text mapping
        self.emoji_map = {
            '😊': 'happy', '😃': 'happy', '😄': 'happy', '😁': 'happy',
            '😢': 'sad', '😭': 'crying', '😔': 'sad',
            '😠': 'angry', '😡': 'angry', '🤬': 'angry',
            '😨': 'fearful', '😰': 'anxious', '😱': 'scared',
            '❤️': 'love', '💔': 'heartbroken',
            '👍': 'good', '👎': 'bad',
            '🔥': 'fire', '💯': 'perfect'
        }
    
    def preprocess_text(self, text: str) -> str:
        """
        Clean and preprocess text for sentiment analysis
        """
        if not text:
            return ""
        
        # Convert emojis to text
        for emoji, meaning in self.emoji_map.items():
            text = text.replace(emoji, f' {meaning} ')
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove mentions and hashtags (but keep the text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#(\w+)', r'\1', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text.strip()
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of a single text using VADER
        Returns sentiment scores and classification
        """
        cleaned_text = self.preprocess_text(text)
        
        if not cleaned_text:
            return {
                'positive': 0,
                'negative': 0,
                'neutral': 1,
                'compound': 0,
                'classification': 'neutral'
            }
        
        # VADER sentiment scores
        vader_scores = self.vader.polarity_scores(cleaned_text)
        
        # Classify sentiment
        compound = vader_scores['compound']
        if compound >= 0.05:
            classification = 'positive'
        elif compound <= -0.05:
            classification = 'negative'
        else:
            classification = 'neutral'
        
        return {
            'positive': vader_scores['pos'],
            'negative': vader_scores['neg'],
            'neutral': vader_scores['neu'],
            'compound': compound,
            'classification': classification
        }
    
    def analyze_emotion(self, text: str) -> Dict:
        """
        Analyze emotions in text
        Returns percentages for joy, anger, fear, sadness
        """
        cleaned_text = self.preprocess_text(text)
        
        if not cleaned_text:
            return {
                'joy': 0,
                'anger': 0,
                'fear': 0,
                'sadness': 0
            }
        
        # Emotion keywords
        joy_keywords = ['happy', 'joy', 'excited', 'love', 'great', 'awesome', 'amazing', 'wonderful', 'excellent']
        anger_keywords = ['angry', 'mad', 'furious', 'hate', 'terrible', 'awful', 'worst', 'disgusting']
        fear_keywords = ['scared', 'afraid', 'fearful', 'worried', 'anxious', 'nervous', 'terrified']
        sadness_keywords = ['sad', 'depressed', 'unhappy', 'disappointed', 'heartbroken', 'crying']
        
        text_lower = cleaned_text.lower()
        
        # Count emotion keywords
        joy_count = sum(1 for word in joy_keywords if word in text_lower)
        anger_count = sum(1 for word in anger_keywords if word in text_lower)
        fear_count = sum(1 for word in fear_keywords if word in text_lower)
        sadness_count = sum(1 for word in sadness_keywords if word in text_lower)
        
        total = joy_count + anger_count + fear_count + sadness_count
        
        if total == 0:
            # Use sentiment as fallback
            sentiment = self.analyze_sentiment(text)
            if sentiment['classification'] == 'positive':
                return {'joy': 70, 'anger': 10, 'fear': 10, 'sadness': 10}
            elif sentiment['classification'] == 'negative':
                return {'joy': 10, 'anger': 40, 'fear': 25, 'sadness': 25}
            else:
                return {'joy': 25, 'anger': 25, 'fear': 25, 'sadness': 25}
        
        return {
            'joy': int((joy_count / total) * 100),
            'anger': int((anger_count / total) * 100),
            'fear': int((fear_count / total) * 100),
            'sadness': int((sadness_count / total) * 100)
        }
    
    def extract_keywords(self, texts: List[str], top_n: int = 5) -> List[Dict]:
        """
        Extract top keywords from a list of texts
        """
        if not texts:
            return []
        
        # Combine all texts
        combined_text = ' '.join([self.preprocess_text(text) for text in texts])
        
        # Remove stopwords and punctuation
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
                    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                    'would', 'should', 'could', 'may', 'might', 'must', 'can', 'this',
                    'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'}
        
        words = combined_text.lower().split()
        words = [word.strip(string.punctuation) for word in words]
        words = [word for word in words if word and word not in stopwords and len(word) > 2]
        
        # Count word frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top N keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        return [{'word': word, 'count': count} for word, count in sorted_words]
    
    def analyze_batch(self, texts: List[str]) -> Dict:
        """
        Analyze sentiment for a batch of texts
        Returns aggregated results
        """
        if not texts:
            return {
                'sentiment': {'positive': 0, 'negative': 0, 'neutral': 0, 'total': 0},
                'emotions': {'joy': 0, 'anger': 0, 'fear': 0, 'sadness': 0},
                'keywords': []
            }
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        total_joy = 0
        total_anger = 0
        total_fear = 0
        total_sadness = 0
        
        for text in texts:
            sentiment = self.analyze_sentiment(text)
            if sentiment['classification'] == 'positive':
                positive_count += 1
            elif sentiment['classification'] == 'negative':
                negative_count += 1
            else:
                neutral_count += 1
            
            emotions = self.analyze_emotion(text)
            total_joy += emotions['joy']
            total_anger += emotions['anger']
            total_fear += emotions['fear']
            total_sadness += emotions['sadness']
        
        total_texts = len(texts)
        keywords = self.extract_keywords(texts)
        
        return {
            'sentiment': {
                'positive': positive_count,
                'negative': negative_count,
                'neutral': neutral_count,
                'total': total_texts
            },
            'emotions': {
                'joy': int(total_joy / total_texts),
                'anger': int(total_anger / total_texts),
                'fear': int(total_fear / total_texts),
                'sadness': int(total_sadness / total_texts)
            },
            'keywords': keywords
        }
