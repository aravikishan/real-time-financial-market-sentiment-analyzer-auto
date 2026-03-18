from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import sqlite3
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database setup
DATABASE = 'sentiment_analysis.db'

# Ensure the database and tables are created
if not os.path.exists(DATABASE):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Sentiment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_symbol TEXT NOT NULL,
        score REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Stock (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        sector TEXT NOT NULL
    )
    ''')
    # Seed data
    cursor.executemany('INSERT INTO Stock (symbol, name, sector) VALUES (?, ?, ?)', [
        ('AAPL', 'Apple Inc.', 'Technology'),
        ('GOOGL', 'Alphabet Inc.', 'Technology'),
        ('AMZN', 'Amazon.com Inc.', 'Consumer Discretionary'),
    ])
    conn.commit()
    conn.close()

# Data models
class Sentiment(BaseModel):
    stock_symbol: str
    score: float
    timestamp: datetime

class Stock(BaseModel):
    symbol: str
    name: str
    sector: str

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    return templates.TemplateResponse("index.html", {"request": {}})

@app.get("/sentiment", response_class=HTMLResponse)
async def get_sentiment_page():
    return templates.TemplateResponse("sentiment.html", {"request": {}})

@app.get("/api-docs", response_class=HTMLResponse)
async def get_api_docs():
    return templates.TemplateResponse("api_docs.html", {"request": {}})

@app.get("/about", response_class=HTMLResponse)
async def get_about_page():
    return templates.TemplateResponse("about.html", {"request": {}})

@app.get("/api/sentiment/{stock_symbol}", response_model=List[Sentiment])
async def get_sentiment(stock_symbol: str):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT stock_symbol, score, timestamp FROM Sentiment WHERE stock_symbol = ?', (stock_symbol,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Stock symbol not found")
    return [Sentiment(stock_symbol=row[0], score=row[1], timestamp=row[2]) for row in rows]

@app.post("/api/sentiment")
async def post_sentiment(sentiment: Sentiment):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Sentiment (stock_symbol, score) VALUES (?, ?)', (sentiment.stock_symbol, sentiment.score))
    conn.commit()
    conn.close()
    return {"message": "Sentiment data added successfully"}

@app.get("/api/stocks", response_model=List[Stock])
async def get_stocks():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT symbol, name, sector FROM Stock')
    rows = cursor.fetchall()
    conn.close()
    return [Stock(symbol=row[0], name=row[1], sector=row[2]) for row in rows]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
