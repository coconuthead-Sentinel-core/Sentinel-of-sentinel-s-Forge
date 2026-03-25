# Environment Setup (Fast, Repeatable)

This guide gets the backend running locally in a few commands. It’s optimized for VS Code and short, repeatable rituals.

## 1) Create and Activate Virtual Environment

VS Code profile (recommended)
- Open the integrated terminal. It auto-activates `.venv` or `venv` via the workspace profile.
- Profile reference: `.vscode/settings.json` uses “PowerShell (venv auto)”.

Manual PowerShell (Windows)
```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process Bypass
. .\.venv\Scripts\Activate.ps1
```

Manual CMD (Windows)
```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

Manual macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 2) Install Dependencies
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3) Run the Server
```bash
uvicorn main:app --reload
```

Open:
- Docs: http://127.0.0.1:8000/docs
- Root banner: http://127.0.0.1:8000/
- Optional UI (if present): http://127.0.0.1:8000/ui

## 4) WebSocket Quick Check
- Connect to `ws://127.0.0.1:8000/ws/sync` (add `?api_key=...` if configured).
- In a Python REPL, publish a test event:
```python
from backend.eventbus import bus
bus.publish({"type": "test.event", "data": {"ok": 1}})
```

## 5) Run Tests
```bash
pytest -q
```

## Optional Environment
- `API_KEY`: require an API key for REST/WS and production compose startup.
- `JWT_SECRET_KEY`: required for production auth tokens.
- `CORS_ORIGINS`: comma-separated HTTPS origins allowed by the API.
- `STRIPE_SECRET_KEY`: Stripe account secret used to leave mock billing mode.
- `STRIPE_WEBHOOK_SECRET`: Stripe webhook signing secret for `/api/billing/webhook`.
- `STRIPE_PRICE_ID_STARTER`, `STRIPE_PRICE_ID_PRO`, `STRIPE_PRICE_ID_ENTERPRISE`: recurring Stripe Price IDs for the three plans.
- `OPENAI_API_KEY`: enable AI endpoints in `backend/llm.py`.
- `OPENAI_MODEL`, `OPENAI_BASE_URL`, `OPENAI_EMBEDDING_MODEL`: optional tuning.

## Docker Compose Runtime
The production `docker-compose.yml` now forwards billing secrets at container runtime instead of relying on a baked `.env` file inside the image. Export the variables in your shell or define them in a local compose `.env` file before running:

```powershell
$env:API_KEY="replace-me"
$env:JWT_SECRET_KEY="replace-me"
$env:CORS_ORIGINS="https://your-domain.com"
$env:STRIPE_SECRET_KEY="sk_test_or_live_..."
$env:STRIPE_WEBHOOK_SECRET="whsec_..."
$env:STRIPE_PRICE_ID_STARTER="price_..."
$env:STRIPE_PRICE_ID_PRO="price_..."
$env:STRIPE_PRICE_ID_ENTERPRISE="price_..."
docker compose up --build
```

## ADHD-Friendly Ritual
- One card at a time, 25 min timer.
- Open only the files you are editing (pin them).
- Verify after each small change (server or tests).
- If stuck > 5 min, halve scope and continue.
