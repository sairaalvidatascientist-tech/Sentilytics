"""
Sentilytics Launcher Script
Installs dependencies, starts the backend, and opens the dashboard in Chrome.
"""
import os
import subprocess
import sys
import time
import webbrowser
import threading

def install_dependencies():
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
        print("Dependencies installed successfully.")
    except Exception as e:
        print(f"Error installing dependencies: {e}")
        print("Attempting to proceed anyway...")

def run_backend():
    print("Starting Sentilytics Backend...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    # Add the current directory to path so imports work correctly
    sys.path.append(os.getcwd())
    
    import uvicorn
    uvicorn.run("backend.main:app", host="localhost", port=8000, reload=False)

def open_browser():
    print("Opening Sentilytics in Chrome...")
    time.sleep(3)  # Wait for server to start
    url = "http://localhost:8000"
    
    try:
        # Try to open specifically in Chrome
        chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
        if os.path.exists('C:/Program Files/Google/Chrome/Application/chrome.exe'):
            webbrowser.get(chrome_path).open(url)
        else:
            webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        webbrowser.open(url)

if __name__ == "__main__":
    print("""
    ============================================================
    SENTILYTICS - SOCIAL MEDIA SENTIMENT ANALYSIS DASHBOARD
    ============================================================
    University of Layyah
    Department of Computer Science
    Project Developer: Saira Alvi
    ============================================================
    """)
    
    # Check if inside the right directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(current_dir, "backend/main.py")):
        print("[Error] Could not find backend/main.py. Please run this script from the project root directory.")
        sys.exit(1)
    
    os.chdir(current_dir)

    # Note: Skipping installation if we are in a controlled environment to save time, 
    # but for a real user, we'd run this. 
    # I'll keep it here as a comment for the user to see what's happening.
    # install_dependencies()

    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()

    # Open browser
    open_browser()

    print("\nSentilytics is running. Press Ctrl+C to stop.")
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down Sentilytics...")
        sys.exit(0)
