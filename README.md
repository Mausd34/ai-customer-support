# AI Customer Support

AI-assisted support application combining FAQ retrieval, intent detection, confidence scoring, and human escalation guidance.

## Features
- Natural-language FAQ matching
- Intent and confidence detection
- Browser chat interface at `/`
- FAQ catalog endpoint
- Human escalation flag for low confidence
- Swagger/OpenAPI at `/docs`
- Automated API tests
- Docker-ready deployment

## Stack
Python · FastAPI · Pydantic · scikit-learn-ready NLP architecture · Docker

## Run locally
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn api:app --reload
```
Open `http://127.0.0.1:8000/`.

## Docker
```bash
docker build -t ai-customer-support .
docker run -p 8000:8000 ai-customer-support
```

> The assistant is designed to support agents, not replace human review for sensitive cases.
