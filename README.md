# FastAPI Security Scanner

A professional REST API security scanner built with FastAPI and Python.

## What it does
- POST /scan — Full port scan with custom ports and API key auth
- GET /scan/{ip} — Quick scan with default ports
- GET /health — API health check
- Automatic Swagger UI documentation at /docs
- API key authentication — unauthorized requests blocked
- Pydantic validation on all inputs and outputs

## Tools used
- Python 3.12
- FastAPI
- Pydantic
- Uvicorn
- Socket
- ThreadPoolExecutor (50 concurrent workers)

## How to run
pip install fastapi uvicorn
uvicorn main:app --reload

## API endpoints
- GET  /health         → Check if API is running
- GET  /scan/{ip}      → Quick scan with default ports
- POST /scan           → Full scan with custom ports

## Authentication
All POST requests require API key in header:
x-api-key: secret-scanner-key-2026

## Author
Corazonpirate27
# fastapi-scanner
