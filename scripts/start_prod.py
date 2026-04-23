import os
import subprocess
import sys

def run_command(command, cwd=None):
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        return False
    return True

def main():
    print("--- Starting Production Build Process ---")
    
    # 1. DB Setup
    print("\n[1/3] Initializing Database...")
    if not run_command("python setup_db.py", cwd="backend"):
        sys.exit(1)
        
    # 2. Start Backend
    print("\n[2/3] Starting Backend (Production Mode)...")
    # Using 4 workers for production-like load handling
    backend_cmd = "python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4"
    
    # Start in background
    p = subprocess.Popen(backend_cmd, shell=True, cwd="backend")
    print(f"Backend started with PID {p.pid}")
    
    # 3. Inform user about Frontend
    print("\n[3/3] System Ignition Complete.")
    print("Backend: http://localhost:8000")
    print("Search: http://localhost:8000/api/v1/search/semantic")
    
    # Keep script alive
    try:
        p.wait()
    except KeyboardInterrupt:
        p.terminate()
        print("System shutdown.")

if __name__ == "__main__":
    main()
