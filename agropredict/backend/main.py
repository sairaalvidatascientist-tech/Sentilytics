from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pandas as pd
import numpy as np
import os
import json
import sqlite3
from typing import List, Optional
from pydantic import BaseModel
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import io
import base64

app = FastAPI(title="AgroPredict")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
MODELS_DIR = os.path.join(BASE_DIR, "models")
DB_PATH = os.path.join(BASE_DIR, "agropredict.db")

for d in [DATA_DIR, REPORTS_DIR, MODELS_DIR]:
    os.makedirs(d, exist_ok=True)

# Plotting style
plt.style.use('ggplot')
sns.set_theme(style="whitegrid", palette="muted")

# Database setup
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS platform_settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contributors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            profile_link TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS variables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            unit TEXT,
            is_visible BOOLEAN DEFAULT 1
        )
    ''')
    
    # Initialize default settings
    default_settings = {
        "platform_name": "AgroPredict",
        "institutional_host": "University of Layyah",
        "department": "Plant Production and Biotechnology",
        "faculty": "Faculty of Agricultural Sciences and Technology (FAST)",
        "default_model": "Random Forest",
        "accuracy_threshold": "0.65",
        "target_r2": "0.75"
    }
    for key, val in default_settings.items():
        cursor.execute("INSERT OR IGNORE INTO platform_settings (key, value) VALUES (?, ?)", (key, val))
        
    # Default contributors
    default_contributors = [
        ("Dr. Zeshan Hassan", "Senior Professor, Supervisor", "https://scholar.google.com"),
        ("Abdullah Afzal Alvi", "Researcher & Platform Developer", "https://scholar.google.com"),
        ("Muzzamil Hussain", "Researcher & Platform Developer", ""),
        ("Sadia Noureen", "Researcher & Platform Developer", "")
    ]
    cursor.execute("SELECT COUNT(*) FROM contributors")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO contributors (name, role, profile_link) VALUES (?, ?, ?)", default_contributors)
        
    # Default variables
    default_vars = [
        ("Plant height", "Phenotyping", "cm", 1),
        ("Number of leaves", "Phenotyping", "count", 1),
        ("Leaf area", "Phenotyping", "cm2", 1),
        ("Temperature Min", "Environmental", "C", 1),
        ("Temperature Max", "Environmental", "C", 1),
        ("Rainfall", "Environmental", "mm", 1),
        ("Soil moisture", "Environmental", "%", 1)
    ]
    cursor.execute("SELECT COUNT(*) FROM variables")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO variables (name, category, unit, is_visible) VALUES (?, ?, ?, ?)", default_vars)
        
    conn.commit()
    conn.close()

init_db()

# Models
class Contributor(BaseModel):
    id: Optional[int] = None
    name: str
    role: str
    profile_link: str

class Variable(BaseModel):
    id: Optional[int] = None
    name: str
    category: str
    unit: str
    is_visible: bool

class Settings(BaseModel):
    platform_name: str
    institutional_host: str
    department: str
    faculty: str
    default_model: str
    accuracy_threshold: float

# API Endpoints
@app.get("/api/settings")
def get_settings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT key, value FROM platform_settings")
    settings = dict(cursor.fetchall())
    conn.close()
    return settings

@app.get("/api/contributors")
def get_contributors():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, role, profile_link FROM contributors")
    results = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "role": r[2], "profile_link": r[3]} for r in results]

@app.get("/api/variables")
def get_variables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, unit, is_visible FROM variables")
    results = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "category": r[2], "unit": r[3], "is_visible": bool(r[4])} for r in results]

@app.post("/api/predict")
async def predict(data: dict):
    # This is a simulation for the demo
    return {
        "status": "success",
        "predicted_height": 15.5,
        "yield_estimate": 4.2,
        "metrics": {
            "r2": 0.72,
            "rmse": 0.15,
            "mae": 0.12
        },
        "feature_importance": {
            "Temperature": 0.8,
            "Rainfall": 0.15,
            "Soil Moisture": 0.05
        }
    }

@app.post("/api/upload")
async def upload_dataset(file: UploadFile = File(...)):
    file_path = os.path.join(DATA_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"status": "success", "filename": file.filename}

@app.post("/api/train")
async def train_model(filename: str, algorithm: str = "Random Forest"):
    file_path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    df = pd.read_csv(file_path) if filename.endswith('.csv') else pd.read_excel(file_path)
    
    # Simple heuristic: target is the last column
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.linear_model import LinearRegression
    from xgboost import XGBRegressor
    from sklearn.metrics import r2_score, mean_squared_error
    
    if algorithm == "Random Forest":
        model = RandomForestRegressor(n_estimators=100)
    elif algorithm == "XGBoost":
        model = XGBRegressor()
    else:
        model = LinearRegression()
        
    model.fit(X, y)
    y_pred = model.predict(X)
    r2 = r2_score(y, y_pred)
    
    # Save model
    import joblib
    joblib.dump(model, os.path.join(MODELS_DIR, "latest_model.joblib"))
    
    return {
        "status": "trained",
        "r2": r2,
        "rmse": np.sqrt(mean_squared_error(y, y_pred))
    }

@app.get("/api/plots/{plot_type}")
def get_plot(plot_type: str):
    plt.figure(figsize=(10, 6))
    # Dummy data for plot generation demo
    data = np.random.randn(100)
    
    if plot_type == "scatter":
        plt.scatter(range(100), data, color='#2d5a27', alpha=0.6)
        plt.title("Observed vs Predicted Values")
    elif plot_type == "boxplot":
        sns.boxplot(data=data, color='#8bc34a')
        plt.title("Variety-to-Variety Comparison")
    elif plot_type == "heatmap":
        corr = np.random.rand(5, 5)
        sns.heatmap(corr, annot=True, cmap="Greens")
        plt.title("Correlation Matrix")
        
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    plt.close()
    return {"image": img_str}

# Mount static files
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
