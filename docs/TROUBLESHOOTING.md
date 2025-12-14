# Sentinel Forge Troubleshooting Guide

## 🚨 Quick Fixes

### 1. Connection Refused (`WinError 10061`)
**Error:** `Max retries exceeded with url... [WinError 10061] No connection could be made...`
**Fix:** The server is not running.
1. Open a terminal.
2. Run: `python scripts/run_full_eval.py` (This handles server startup automatically).
3. OR manually run: `uvicorn main:app --reload --port 8000`

### 2. Missing Dependencies (`ModuleNotFoundError`)
**Error:** `No module named 'gradio'` or `No module named 'azure'`
**Fix:**
1. Ensure your virtual environment is active (`.venv`).
2. Run: `pip install -r requirements.txt`

### 3. Syntax Errors in `api.py`
**Error:** `SyntaxError: invalid syntax` pointing to `REM` or `run_in threadpool`.
**Fix:**
- **Line 1:** Change `REM filepath:...` to `# filepath:...`
- **Function calls:** Change `run_in threadpool` to `run_in_threadpool` (add the underscore).

### 4. Azure OpenAI / Cosmos DB Errors
**Error:** `AOAI_ENDPOINT not set` or `401 Unauthorized`.
**Fix:**
1. Check if `.env` exists. If not, copy `.env.example`.
2. Edit `.env` and add your keys:
   ```dotenv
   API_KEY=your-secret
   AOAI_ENDPOINT=https://...
   COSMOS_ENDPOINT=https://...
   ```

## 🧪 Verification
To verify fixes, run the test suite:
```bash
pytest tests/test_vectors.py
```
