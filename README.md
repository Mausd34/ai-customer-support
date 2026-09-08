# AI Customer Support

Professional AI-assisted customer support service with FAQ retrieval, intent detection, conversation context, and escalation.

## Features
- Natural-language FAQ matching
- Intent classification
- Conversation endpoint
- Human escalation workflow
- REST API with Swagger docs
- Docker-ready deployment

## Stack
Python · FastAPI · scikit-learn · Pydantic · Docker

## Quick start
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn api:app --reload
```
Open `http://127.0.0.1:8000/docs`.
