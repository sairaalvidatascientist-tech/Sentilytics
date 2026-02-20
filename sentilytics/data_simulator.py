"""
Data Simulator Module
Simulates real-time social media posts for sentiment analysis
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict
import time

class DataSimulator:
    def __init__(self):
        """Initialize data simulator with sample content"""
        self.keywords = {
            'Tesla': {
                'positive': [
                    "Just bought a Tesla Model 3! Best car I've ever owned! #Tesla #ElectricVehicle",
                    "Tesla's autopilot is absolutely amazing! The future is here!",
                    "Love my Tesla! The acceleration is mind-blowing!",
                    "Tesla stock is soaring! Great investment decision!",
                    "The new Tesla factory is creating thousands of jobs. Fantastic news!",
                    "Tesla's battery technology is revolutionary. Game changer!",
                    "Elon Musk is a visionary. Tesla is changing the world!",
                ],
                'negative': [
                    "Tesla quality control is terrible. My car has so many issues.",
                    "Tesla service centers are the worst. Waiting months for repairs!",
                    "Overpriced and overhyped. Tesla is not worth the money.",
                    "Tesla's autopilot is dangerous. Too many accidents!",
                    "Tesla stock is crashing. Should have sold earlier.",
                    "Tesla's customer service is non-existent. Very disappointed.",
                ],
                'neutral': [
                    "Tesla announced new factory in Texas. Production starts next year.",
                    "Tesla Model Y specifications released. Check the website for details.",
                    "Tesla earnings report coming next week. Analysts predict mixed results.",
                    "Tesla charging stations expanding to 50 new locations.",
                    "Tesla software update version 11.0 now available for download.",
                ]
            },
            'AI': {
                'positive': [
                    "AI is revolutionizing healthcare! Amazing breakthroughs in diagnosis.",
                    "ChatGPT is incredible! AI assistants are the future!",
                    "AI-powered tools are making my work so much easier!",
                    "Excited about AI advancements in education. Students will benefit greatly!",
                    "AI art generators are mind-blowing! Creativity unleashed!",
                ],
                'negative': [
                    "AI is taking our jobs. This is getting scary.",
                    "AI-generated content is ruining creative industries.",
                    "Concerned about AI privacy issues. Our data is not safe.",
                    "AI bias is a serious problem that needs addressing.",
                    "AI regulation is too slow. We need action now!",
                ],
                'neutral': [
                    "New AI research paper published on machine learning algorithms.",
                    "AI conference scheduled for next month in San Francisco.",
                    "AI market expected to reach $500B by 2028, report says.",
                    "Google announces new AI research division.",
                ]
            },
            'default': {
                'positive': [
                    "Great news! This is exactly what we needed!",
                    "Absolutely amazing! Love this so much!",
                    "Best decision ever! Highly recommend!",
                    "Fantastic results! Very impressed!",
                ],
                'negative': [
                    "This is terrible. Very disappointed.",
                    "Worst experience ever. Not recommended.",
                    "Completely unacceptable. Needs improvement.",
                    "Very frustrated with this situation.",
                ],
                'neutral': [
                    "New update released today. Check it out.",
                    "Event scheduled for next week.",
                    "Report shows mixed results this quarter.",
                    "Announcement coming soon. Stay tuned.",
                ]
            }
        }
        
        self.usernames = [
            "TechEnthusiast", "DataScientist", "AIResearcher", "SocialMediaGuru",
            "TrendWatcher", "DigitalNomad", "InnovationHub", "FutureThinker",
            "CodeMaster", "AnalyticsExpert", "MarketAnalyst", "BrandMonitor"
        ]
    
    def generate_post(self, keyword: str = "Tesla", sentiment_bias: str = None) -> Dict:
        """
        Generate a simulated social media post
        
        Args:
            keyword: Topic keyword for the post
            sentiment_bias: Force specific sentiment ('positive', 'negative', 'neutral', or None for random)
        
        Returns:
            Dict with post data
        """
        # Get keyword-specific content or use default
        content_pool = self.keywords.get(keyword, self.keywords['default'])
        
        # Determine sentiment
        if sentiment_bias and sentiment_bias in ['positive', 'negative', 'neutral']:
            sentiment = sentiment_bias
        else:
            # Random distribution: 60% positive, 20% negative, 20% neutral
            rand = random.random()
            if rand < 0.6:
                sentiment = 'positive'
            elif rand < 0.8:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
        
        # Select random post from sentiment category
        post_text = random.choice(content_pool[sentiment])
        
        # Generate metadata
        post = {
            'id': f"post_{int(time.time() * 1000)}_{random.randint(1000, 9999)}",
            'text': post_text,
            'username': random.choice(self.usernames),
            'timestamp': datetime.now().isoformat(),
            'likes': random.randint(0, 1000),
            'retweets': random.randint(0, 500),
            'keyword': keyword,
            'platform': random.choice(['Twitter', 'Reddit', 'Facebook'])
        }
        
        return post
    
    def generate_batch(self, count: int = 10, keyword: str = "Tesla") -> List[Dict]:
        """Generate multiple posts"""
        return [self.generate_post(keyword) for _ in range(count)]
    
    def generate_crisis_scenario(self, keyword: str = "Tesla") -> List[Dict]:
        """Generate posts simulating a crisis (sudden negative sentiment spike)"""
        posts = []
        # 80% negative posts
        for _ in range(8):
            posts.append(self.generate_post(keyword, sentiment_bias='negative'))
        # 20% neutral/positive
        for _ in range(2):
            posts.append(self.generate_post(keyword, sentiment_bias=random.choice(['neutral', 'positive'])))
        
        return posts
    
    def generate_trending_keywords(self, analyses: List[Dict]) -> List[Dict]:
        """Generate trending keywords from analyzed posts"""
        keywords = [
            {'word': 'Innovation', 'frequency': random.randint(50, 100)},
            {'word': 'Technology', 'frequency': random.randint(40, 90)},
            {'word': 'Future', 'frequency': random.randint(30, 80)},
            {'word': 'Quality', 'frequency': random.randint(25, 70)},
            {'word': 'Price', 'frequency': random.randint(20, 60)},
            {'word': 'Service', 'frequency': random.randint(15, 50)},
        ]
        
        # Sort by frequency
        keywords.sort(key=lambda x: x['frequency'], reverse=True)
        return keywords[:6]
