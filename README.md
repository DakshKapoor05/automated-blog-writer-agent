# Automated Blog Writer — Minimal Multi-Agent Starter

**Goal:** Produce a short blog article from a topic using a 3-agent pipeline (Research → Outline → Writer). Ready for a 48-hour capstone submission.

## Features
- Multi-agent pipeline: ResearchAgent → OutlineAgent → WriterAgent
- Tools: small keyword extractor utility and a simple code-execution style helper (word counts)
- Sessions & Memory: In-memory session storage with simple JSON persistence
- Observability: Structured logging for each agent step
- Evaluation: compare single-call baseline vs multi-agent pipeline using simple metrics

## Quick start
1. Clone repo
2. Create `.env` from `.env.example` and add `OPENAI_API_KEY` (optional; without key the project uses mocks)
3. Install: `pip install -r requirements.txt`
4. Run FastAPI: `uvicorn main:app --reload`
5. Generate: `GET http://127.0.0.1:8000/generate_blog?topic=Impact%20of%20AI%20on%20Finance&style=concise`
6. Evaluate: `python eval/evaluate.py`


