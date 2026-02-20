"""
Sentilytics - Main FastAPI Application
Real-Time Social Media Sentiment Analysis Dashboard
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Dict
import asyncio
import os
from datetime import datetime

from .config import config
from .sentiment_analyzer import SentimentAnalyzer
from .data_collector import DataCollector
from .alert_system import AlertSystem

# Initialize FastAPI app
app = FastAPI(
    title="Sentilytics API",
    description="Real-Time Social Media Sentiment Analysis Dashboard",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
sentiment_analyzer = SentimentAnalyzer()
data_collector = DataCollector()
alert_system = AlertSystem()

# Mount static files
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def serve_index():
    """Serve the index.html file"""
    from fastapi.responses import FileResponse
    return FileResponse(os.path.join(frontend_dir, "index.html"))

# Store active WebSocket connections
active_connections: List[WebSocket] = []

# Store analysis history
analysis_history = {}


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Sentilytics API",
        "version": "1.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/analyze")
async def analyze_sentiment(keyword: str = Query(..., description="Keyword to analyze")):
    """
    Analyze sentiment for a given keyword
    """
    try:
        # Collect posts related to the keyword
        posts = await data_collector.collect_posts(keyword, count=100)
        
        # Filter spam
        filtered_posts = data_collector.filter_spam(posts)
        
        # Extract text from posts
        texts = [post['text'] for post in filtered_posts]
        
        # Analyze sentiment
        analysis_result = sentiment_analyzer.analyze_batch(texts)
        
        # Check for alerts
        alert = alert_system.check_sentiment_spike(analysis_result['sentiment'])
        
        # Store in history
        if keyword not in analysis_history:
            analysis_history[keyword] = []
        
        analysis_history[keyword].append({
            'timestamp': datetime.now().isoformat(),
            'result': analysis_result
        })
        
        # Keep only last 50 entries
        if len(analysis_history[keyword]) > 50:
            analysis_history[keyword] = analysis_history[keyword][-50:]
        
        # Prepare response
        response = {
            'keyword': keyword,
            'sentiment': analysis_result['sentiment'],
            'emotions': analysis_result['emotions'],
            'keywords': analysis_result['keywords'],
            'timestamp': datetime.now().isoformat(),
            'alert': alert
        }
        
        return JSONResponse(content=response)
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                'error': str(e),
                'message': 'An error occurred during sentiment analysis'
            }
        )


@app.get("/api/history")
async def get_history(keyword: str = Query(..., description="Keyword to get history for")):
    """
    Get sentiment analysis history for a keyword
    """
    if keyword not in analysis_history:
        return JSONResponse(content={'history': []})
    
    return JSONResponse(content={'history': analysis_history[keyword]})


@app.get("/api/alerts")
async def get_alerts(limit: int = Query(10, description="Number of recent alerts to retrieve")):
    """
    Get recent alerts
    """
    alerts = alert_system.get_alert_history(limit)
    return JSONResponse(content={'alerts': alerts})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time updates
    """
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            keyword = data.get('keyword')
            
            if keyword:
                # Start streaming analysis
                async def send_update(posts):
                    texts = [post['text'] for post in posts]
                    result = sentiment_analyzer.analyze_batch(texts)
                    
                    await websocket.send_json({
                        'type': 'update',
                        'keyword': keyword,
                        'data': result,
                        'timestamp': datetime.now().isoformat()
                    })
                
                # This would stream in production
                # For now, send periodic updates
                await send_update(await data_collector.collect_posts(keyword, 20))
    
    except WebSocketDisconnect:
        active_connections.remove(websocket)


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'components': {
            'sentiment_analyzer': 'operational',
            'data_collector': 'operational',
            'alert_system': 'operational'
        }
    }


@app.on_event("startup")
async def startup_event():
    """
    Run on application startup
    """
    print("=" * 60)
    print("Sentilytics API Starting...")
    print("=" * 60)
    print(f"Sentiment Analysis Engine: Ready")
    print(f"Data Collector: Ready")
    print(f"Alert System: Ready")
    print(f"Server: http://{config.HOST}:{config.PORT}")
    print("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """
    Run on application shutdown
    """
    print("\n" + "=" * 60)
    print("Sentilytics API Shutting Down...")
    print("=" * 60)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG,
        log_level="info"
    )
