"""
Sentilytics - Real-Time Social Media Sentiment Analysis Dashboard
FastAPI Backend Server
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from datetime import datetime
from pathlib import Path
import uvicorn

from sentiment_analyzer import SentimentAnalyzer
from data_simulator import DataSimulator

# Initialize FastAPI app
app = FastAPI(title="Sentilytics", description="Real-Time Sentiment Analysis Dashboard")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize analyzers
sentiment_analyzer = SentimentAnalyzer()
data_simulator = DataSimulator()

# Store active WebSocket connections
active_connections: list[WebSocket] = []

# Global state for sentiment tracking
sentiment_history = []
emotion_counts = {'joy': 0, 'anger': 0, 'fear': 0, 'sadness': 0, 'neutral': 0}
total_posts_analyzed = 0
activity_log = []

# Mount static files
static_path = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")


@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    html_file = static_path / "index.html"
    return FileResponse(html_file)


@app.get("/api/stats")
async def get_stats():
    """Get current sentiment statistics"""
    global sentiment_history, total_posts_analyzed
    
    if not sentiment_history:
        return {
            'total_posts': 0,
            'sentiment_distribution': {'positive': 0, 'negative': 0, 'neutral': 0},
            'emotion_distribution': emotion_counts,
            'activity_log': []
        }
    
    # Calculate sentiment distribution
    recent_analyses = sentiment_history[-100:]  # Last 100 posts
    distribution = sentiment_analyzer.get_sentiment_distribution(recent_analyses)
    
    return {
        'total_posts': total_posts_analyzed,
        'sentiment_distribution': distribution,
        'emotion_distribution': emotion_counts,
        'activity_log': activity_log[-10:]  # Last 10 activities
    }


@app.get("/api/trending")
async def get_trending():
    """Get trending keywords"""
    keywords = data_simulator.generate_trending_keywords(sentiment_history)
    return {'keywords': keywords}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time data streaming"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Send initial data
        await websocket.send_json({
            'type': 'connection',
            'message': 'Connected to Sentilytics real-time stream',
            'timestamp': datetime.now().isoformat()
        })
        
        # Start streaming data
        while True:
            # Generate new post
            post = data_simulator.generate_post(keyword="Tesla")
            
            # Analyze sentiment
            analysis = sentiment_analyzer.analyze_sentiment(post['text'])
            
            # Update global state
            global sentiment_history, total_posts_analyzed, emotion_counts, activity_log
            sentiment_history.append(analysis)
            total_posts_analyzed += 1
            
            # Update emotion counts
            emotion = analysis['emotion']
            if emotion in emotion_counts:
                emotion_counts[emotion] += 1
            
            # Add to activity log
            activity_log.append({
                'timestamp': datetime.now().isoformat(),
                'message': f"Analyzed post from @{post['username']}: {analysis['sentiment']} sentiment",
                'sentiment': analysis['sentiment']
            })
            
            # Keep only last 1000 entries
            if len(sentiment_history) > 1000:
                sentiment_history = sentiment_history[-1000:]
            if len(activity_log) > 50:
                activity_log = activity_log[-50:]
            
            # Prepare data packet
            data_packet = {
                'type': 'sentiment_update',
                'timestamp': datetime.now().isoformat(),
                'post': {
                    'text': post['text'],
                    'username': post['username'],
                    'platform': post['platform']
                },
                'analysis': analysis,
                'stats': {
                    'total_posts': total_posts_analyzed,
                    'sentiment_distribution': sentiment_analyzer.get_sentiment_distribution(
                        sentiment_history[-100:]
                    ),
                    'emotion_distribution': emotion_counts
                }
            }
            
            # Send to all connected clients
            for connection in active_connections:
                try:
                    await connection.send_json(data_packet)
                except:
                    active_connections.remove(connection)
            
            # Wait before next update (simulate real-time stream)
            await asyncio.sleep(2)  # New post every 2 seconds
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)


@app.post("/api/analyze")
async def analyze_text(data: dict):
    """Analyze custom text input"""
    text = data.get('text', '')
    if not text:
        return {'error': 'No text provided'}
    
    analysis = sentiment_analyzer.analyze_sentiment(text)
    return {
        'text': text,
        'analysis': analysis,
        'timestamp': datetime.now().isoformat()
    }


@app.get("/api/crisis-simulation")
async def simulate_crisis():
    """Simulate a crisis scenario with negative sentiment spike"""
    global sentiment_history, activity_log
    
    # Generate crisis posts
    crisis_posts = data_simulator.generate_crisis_scenario()
    
    # Analyze all crisis posts
    for post in crisis_posts:
        analysis = sentiment_analyzer.analyze_sentiment(post['text'])
        sentiment_history.append(analysis)
    
    # Add crisis alert to activity log
    activity_log.append({
        'timestamp': datetime.now().isoformat(),
        'message': '🚨 CRISIS ALERT: Negative sentiment spike detected!',
        'sentiment': 'negative'
    })
    
    # Broadcast crisis alert to all connected clients
    alert_packet = {
        'type': 'crisis_alert',
        'timestamp': datetime.now().isoformat(),
        'message': 'Negative sentiment spike detected (-27%) in the last 10 minutes',
        'severity': 'high'
    }
    
    for connection in active_connections:
        try:
            await connection.send_json(alert_packet)
        except:
            pass
    
    return {'status': 'Crisis simulation triggered', 'posts_generated': len(crisis_posts)}


if __name__ == "__main__":
    print("🚀 Starting Sentilytics Server...")
    print("📊 Real-Time Sentiment Analysis Dashboard")
    print("🌐 Server will be available at: http://localhost:8000")
    print("\n" + "="*60)
    print("University of Layyah - Department of Computer Science")
    print("Developer: Saira Alvi")
    print("="*60 + "\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
