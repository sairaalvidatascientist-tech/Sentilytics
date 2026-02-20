"""
Configuration settings for Sentilytics backend
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Server settings
    HOST = "localhost"
    PORT = 8000
    DEBUG = True
    
    # CORS settings
    CORS_ORIGINS = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
        "file://"
    ]
    
    # API Keys (optional - for production use)
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
    
    # Sentiment analysis settings
    SENTIMENT_THRESHOLD_POSITIVE = 0.05
    SENTIMENT_THRESHOLD_NEGATIVE = -0.05
    
    # Alert settings
    NEGATIVE_SENTIMENT_ALERT_THRESHOLD = 0.4  # 40%
    
    # Data collection settings
    MAX_POSTS_PER_REQUEST = 100
    SIMULATED_DATA_MODE = True  # Set to False when API keys are available

config = Config()
