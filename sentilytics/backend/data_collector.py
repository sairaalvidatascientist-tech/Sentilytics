"""
Data Collection Module for Sentilytics
Handles social media data collection and simulation
"""
import random
import asyncio
from typing import List, Dict
from datetime import datetime

class DataCollector:
    def __init__(self):
        self.simulated_mode = True
        
        # Sample posts for simulation
        self.sample_posts = {
            'positive': [
                "This is absolutely amazing! Love it! 😊",
                "Great product, highly recommend to everyone!",
                "Best experience ever! Will definitely come back ❤️",
                "Incredible service and fantastic quality 👍",
                "So happy with this purchase! Exceeded expectations 😄",
                "Outstanding! This is exactly what I needed 💯",
                "Wonderful experience from start to finish!",
                "Absolutely love this! Can't stop using it 🔥",
                "Perfect! Everything I hoped for and more",
                "Excellent quality and amazing customer service"
            ],
            'negative': [
                "Terrible experience, very disappointed 😠",
                "Worst purchase I've ever made. Don't waste your money!",
                "Absolutely awful. Would not recommend 👎",
                "Very frustrating and poor quality",
                "Horrible service, never again 😡",
                "Complete waste of time and money",
                "Extremely disappointed with this product",
                "Not worth it at all. Save your money!",
                "Poor quality and terrible customer support",
                "Regret buying this. Total disappointment 😔"
            ],
            'neutral': [
                "It's okay, nothing special but works fine",
                "Average product, does what it says",
                "Not bad, not great. Just okay",
                "Decent quality for the price",
                "It works as expected, nothing more",
                "Standard product, meets basic requirements",
                "Fair enough, gets the job done",
                "Acceptable quality, no complaints",
                "It's fine, does what I need it to do",
                "Normal experience, nothing to write home about"
            ]
        }
    
    async def collect_posts(self, keyword: str, count: int = 50) -> List[Dict]:
        """
        Collect posts related to a keyword
        In production, this would call actual social media APIs
        For now, returns simulated data
        """
        if self.simulated_mode:
            return await self._generate_simulated_posts(keyword, count)
        else:
            # TODO: Implement actual API calls
            return await self._collect_from_apis(keyword, count)
    
    async def _generate_simulated_posts(self, keyword: str, count: int) -> List[Dict]:
        """
        Generate simulated social media posts
        """
        posts = []
        
        # Simulate some delay
        await asyncio.sleep(0.5)
        
        for i in range(count):
            # Random sentiment distribution (weighted towards positive)
            sentiment_type = random.choices(
                ['positive', 'negative', 'neutral'],
                weights=[0.5, 0.25, 0.25]
            )[0]
            
            # Select a random post template
            post_template = random.choice(self.sample_posts[sentiment_type])
            
            # Add keyword to post
            post_text = f"{keyword}: {post_template}"
            
            # Create post object
            post = {
                'id': f'post_{i}_{datetime.now().timestamp()}',
                'text': post_text,
                'author': f'user_{random.randint(1000, 9999)}',
                'timestamp': datetime.now().isoformat(),
                'platform': random.choice(['Twitter', 'Reddit', 'Facebook']),
                'likes': random.randint(0, 1000),
                'retweets': random.randint(0, 500)
            }
            
            posts.append(post)
        
        return posts
    
    async def _collect_from_apis(self, keyword: str, count: int) -> List[Dict]:
        """
        Collect posts from actual social media APIs
        TODO: Implement Twitter, Reddit, etc. API calls
        """
        # Placeholder for future implementation
        posts = []
        
        # Twitter API call would go here
        # Reddit API call would go here
        # etc.
        
        return posts
    
    async def stream_posts(self, keyword: str, callback):
        """
        Stream posts in real-time
        Calls the callback function with new posts as they arrive
        """
        while True:
            # Generate a batch of new posts
            new_posts = await self._generate_simulated_posts(keyword, random.randint(5, 15))
            
            # Call the callback with new posts
            await callback(new_posts)
            
            # Wait before next batch (simulate real-time streaming)
            await asyncio.sleep(random.randint(3, 8))
    
    def filter_spam(self, posts: List[Dict]) -> List[Dict]:
        """
        Filter out spam and bot-generated content
        """
        filtered_posts = []
        
        spam_keywords = ['buy now', 'click here', 'limited offer', 'act now', 'free money']
        
        for post in posts:
            text_lower = post['text'].lower()
            is_spam = any(spam_word in text_lower for spam_word in spam_keywords)
            
            if not is_spam:
                filtered_posts.append(post)
        
        return filtered_posts
