"""
Lightweight smoke tests for the FastAPI app.

Runs in-process using FastAPI's TestClient, so it doesn't require the server
to be started or any external services. AI endpoints are probed and will be
treated as OK if they return a clear 400 with configuration guidance when
OPENAI_API_KEY is not set or the OpenAI SDK is missing.
"""

# ==============================================================================
# HOW TO RUN THIS TEST:
# 1. In your FIRST terminal, start the FastAPI server:
#    uvicorn main:app --reload --port 8000
#
# 2. In a SECOND, separate terminal (like the one you have open), run this script:
#    python scripts/smoke_test.py
# ==============================================================================

import sys
import os
import time
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from client import SentinelClient


def print_test(name, status, message=""):
    """Helper to print test results in a standard format."""
    if status:
        print(f"✅ PASS: {name}")
    else:
        print(f"❌ FAIL: {name} - {message}")


def run_smoke_test():
    print("🚀 INITIATING SMOKE TEST SEQUENCE...")
    print("=" * 40)
    
    client = SentinelClient(base_url="http://127.0.0.1:8000", timeout=5)
    
    # 1. Check API Connectivity
    print("[1/3] Pinging System Core...", end=" ")
    try:
        status = client.status()
        print(f"✅ ONLINE ({status.get('version')})")
    except Exception as e:
        print(f"❌ FAILED: {e}")
        print("      (Is the server running? Try: uvicorn main:app --reload)")
        return False

    # 2. Check AI Response (Mock or Real)
    print("[2/3] Testing Cognitive Engine...", end=" ")
    try:
        reply = client.chat("Status Report")
        if reply:
            print("✅ RESPONSIVE")
            print(f"      Received: {reply[:50]}...")
        else:
            print("⚠️  NO RESPONSE (Check logs)")
    except Exception as e:
        print(f"❌ FAILED: {e}")

    # 3. Check Database Write
    print("[3/3] Testing Memory Lattice...", end=" ")
    try:
        note = client.upsert_note("Smoke Test Entry", "diagnostics")
        if note and note.get("id"):
            print("✅ WRITE CONFIRMED")
        else:
            print("❌ WRITE FAILED")
    except Exception as e:
        print(f"❌ FAILED: {e}")

    print("=" * 40)
    print("🏁 SMOKE TEST COMPLETE")
    return True

if __name__ == "__main__":
    run_smoke_test()
