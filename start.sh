#!/bin/bash
set -e
echo "Starting Real-Time Financial Market Sentiment Analyzer..."
uvicorn app:app --host 0.0.0.0 --port 9147 --workers 1
