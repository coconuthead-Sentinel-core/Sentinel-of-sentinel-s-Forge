import subprocess
import time
import sys
import os
import socket
from pathlib import Path

# --- Unicode Patch for Windows Consoles ---
# Ensures emojis (🚀, ✅, etc.) don't crash the script on legacy terminals.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Fallback for older Python versions or environments
        pass

def wait_for_port(port, timeout=30):
    """Wait until the port is open."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            result = sock.connect_ex(('127.0.0.1', port))
            if result == 0:
                return True
        time.sleep(1)
    return False

def main():
    # Ensure we are in the project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    print("🚀 Starting Sentinel Forge Evaluation Pipeline...")
    print("=" * 60)

    # 1. Start the API Server in the background
    print("\n[1/3] Starting API Server...")
    server_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for port 8000 to be ready
    print("      Waiting for server to be ready (max 30s)...")
    if wait_for_port(8000):
        print("      ✅ Server is listening on port 8000")
    else:
        print("❌ Server failed to start within timeout. Logs:")
        # Read whatever output we have
        out, err = server_process.communicate(timeout=5)
        print(err.decode() if err else "No error output captured.")
        server_process.terminate()
        return

    try:
        # 2. Run the Collection Script
        print("\n[2/3] Collecting Responses...")
        collect_result = subprocess.run(
            [sys.executable, "evaluation/collect_responses.py"],
            capture_output=False 
        )
        
        if collect_result.returncode != 0:
            print("❌ Collection failed.")
        else:
            # 3. Run the Evaluation Script
            print("\n[3/3] Running Evaluation...")
            subprocess.run(
                [sys.executable, "evaluation/run_evaluation.py"],
                capture_output=False
            )

    finally:
        # 4. Cleanup: Stop the server
        print("\n🛑 Shutting down server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print("✅ Pipeline Complete.")

if __name__ == "__main__":
    main()
