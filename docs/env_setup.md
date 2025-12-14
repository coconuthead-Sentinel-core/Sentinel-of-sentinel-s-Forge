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
- `QNF_API_KEY`: require an API key for REST/WS.
- `OPENAI_API_KEY`: enable AI endpoints in `backend/llm.py`.
- `OPENAI_MODEL`, `OPENAI_BASE_URL`, `OPENAI_EMBEDDING_MODEL`: optional tuning.

## ADHD-Friendly Ritual
- One card at a time, 25 min timer.
- Open only the files you are editing (pin them).
- Verify after each small change (server or tests).
- If stuck > 5 min, halve scope and continue.
