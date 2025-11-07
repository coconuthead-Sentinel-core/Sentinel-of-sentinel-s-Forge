# Sentinel-of-sentinel-s-Forge

## FastAPI Backend

This repo now includes a FastAPI backend and a service (middle) layer wrapping the Quantum Nexus Forge engine.

### Structure
- `quantum_nexus_forge_v5_2_enhanced.py` — core engine (import-safe; runs demo only when executed directly)
- `sentinel_cognition.py` — cognitive graph built from the blueprint (Sentinel Processor, Cognitive Neural Overlay, Symbolic Array, Reflective Pool, Gemini Stack, Cube Core)
- `backend/` — backend package
  - `backend/service.py` — service layer (thread-safe wrapper, background job support)
  - `backend/schemas.py` — Pydantic request/response models
  - `backend/api.py` — FastAPI router/endpoints
- `main.py` — ASGI application entrypoint (`FastAPI` app)
- `requirements.txt` — backend dependencies
- `frontend/` — static browser UI served at `/ui`

### Endpoints (prefix `/api`)
- `GET /status` — system status
- `POST /process` — process data: `{ "data": any, "pool_id": "optional" }`
- `POST /pools` — create pool: `{ "pool_id": str, "initial_size": int }`
- `POST /teardown` — complete system teardown
- `POST /rebuild` — rebuild from foundation: `{ "default_pools": int, "pool_size": int }`
- `POST /stress` — stress test: `{ "iterations": int, "concurrent": bool, "async_mode": bool }`
- `GET /jobs/{job_id}` — background stress job status
- `GET /cog/status` — status of the cognitive graph
- `POST /cog/process` — run the image-inspired cognition pipeline: `{ "data": any }`
- `GET /cog/rules` — get symbolic rules
- `PUT /cog/rules` — set rules: `{ "rules": { substring: tag } }`
- `GET /cog/memory` — snapshot reflective memory
- `DELETE /cog/memory` — clear reflective memory
- `GET /cog/prime` — Shannon Prime information-theoretic metrics
- `GET /cog/suggest` — Metatron Engine rule suggestions

### Run locally
1. Create/activate a virtual environment.
2. Install deps: `pip install -r requirements.txt`
3. Start server: `uvicorn main:app --reload`
4. Open docs: `http://127.0.0.1:8000/docs`
5. Open UI: `http://127.0.0.1:8000/ui`
6. Click "Connect WS" in the Tri-Node section to receive live updates.

### Connect to OpenAI (ChatGPT)
- Set your key in the environment before starting the server:
  - PowerShell:
    - `$env:OPENAI_API_KEY = "sk-..."`
    - Optional: `$env:OPENAI_BASE_URL = "https://api.openai.com/v1"` (defaults)  
    - Optional: `$env:OPENAI_MODEL = "gpt-4o-mini"`, `$env:OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"`
- Test via UI “Chat (OpenAI)” panel or API:
  - `POST /api/ai/chat` with `{ "messages": [{"role":"user","content":"hello"}] }`
  - `POST /api/ai/embeddings` with `{ "input": ["hello world"] }`

### Persistence
- State is saved under `data/state.json`. It includes symbolic rules and a small reflective memory preview. On startup, the service loads these into the cognition graph.

### Notes
- The service layer serializes access to core operations and provides a simple background job mechanism for long-running stress tests.
- The cognitive graph implements a lightweight neuro-symbolic-reflective pipeline modeled on the diagram. It enriches inputs with a pseudo-embedding, rule tags, short-term memory references, a dual-path feature merge, and a compact signature from the Cube Core.
- New components from the diagrams:
  - Shannon Prime Core tracks token entropy and stability to monitor structure.
  - Metatron Engine proposes symbolic rules from frequent tokens.
  - Emotional Analyzer provides a tiny lexicon-based valence score.
  - Ethical Guard flags simple categories (demo only; not a substitute for safety tooling).
  - SentinelPrimeSync models the tri‑node network (Sentinel, Sora, Architect) with a glyphic protocol and shared session state.
- If you need CORS for a browser-based frontend, we can add it via FastAPI middleware.
  - Configure allowed origins with env var `QNF_CORS_ORIGINS` (comma-separated), default `*`.

### Docker

- Build image: docker build -t qnf-api .`r
- Run container: docker run --rm -p 8000:8000 qnf-api`r
- Open: http://127.0.0.1:8000/docs and http://127.0.0.1:8000/ui`r

The container uses Gunicorn with Uvicorn workers and listens on port 8000 (exposed). For Azure App Service (Containers), set app setting WEBSITES_PORT=8000.
