"""
Sentilytics Launcher
Automatically installs dependencies, starts server, and opens Chrome browser
"""

import subprocess
import sys
import time
import webbrowser
import os
from pathlib import Path

def print_banner():
    """Print startup banner"""
    print("\n" + "="*70)
    print(">> SENTILYTICS - Real-Time Sentiment Analysis Dashboard")
    print("="*70)
    print("Location: University of Layyah - Department of Computer Science")
    print("Developer: Saira Alvi")
    print("="*70 + "\n")

def check_python_version():
    """Ensure Python 3.7+"""
    if sys.version_info < (3, 7):
        print("[ERROR] Python 3.7 or higher is required")
        sys.exit(1)
    print(f"[OK] Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required packages"""
    print("\n[SETUP] Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"
        ])
        print("[OK] All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error installing dependencies: {e}")
        return False

def download_nltk_data():
    """Download required NLTK data"""
    print("\n[NLTK] Downloading NLTK data...")
    try:
        import nltk
        nltk.download('vader_lexicon', quiet=True)
        nltk.download('punkt', quiet=True)
        print("[OK] NLTK data downloaded")
        return True
    except Exception as e:
        print(f"[WARNING] Could not download NLTK data: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("\n[SERVER] Starting Sentilytics server...")
    print("[INFO] Server URL: http://localhost:8000")
    print("[INFO] Please wait while the server initializes...\n")
    
    # Start server in background
    try:
        if sys.platform == 'win32':
            # Windows
            process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Unix/Linux/Mac
            process = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        
        return process
    except Exception as e:
        print(f"[ERROR] Error starting server: {e}")
        return None

def open_browser():
    """Open Chrome browser to the application"""
    print("\n[BROWSER] Opening Chrome browser...")
    time.sleep(3)  # Wait for server to fully start
    
    url = "http://localhost:8000"
    
    try:
        # Try to open in Chrome specifically
        chrome_path = None
        
        if sys.platform == 'win32':
            # Windows Chrome paths
            possible_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    chrome_path = path
                    break
        elif sys.platform == 'darwin':
            # macOS
            chrome_path = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
        else:
            # Linux
            chrome_path = '/usr/bin/google-chrome'
        
        if chrome_path and os.path.exists(chrome_path):
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
            webbrowser.get('chrome').open(url)
            print(f"[OK] Chrome opened at {url}")
        else:
            # Fallback to default browser
            webbrowser.open(url)
            print(f"[OK] Browser opened at {url}")
            print("[WARNING] Chrome not found, using default browser")
        
        return True
    except Exception as e:
        print(f"[WARNING] Could not auto-open browser: {e}")
        print(f"[INFO] Please manually open: {url}")
        return False

def main():
    """Main launcher function"""
    print_banner()
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        print("\n[ERROR] Setup failed. Please install dependencies manually:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Download NLTK data
    download_nltk_data()
    
    # Start server
    server_process = start_server()
    if not server_process:
        print("\n[ERROR] Failed to start server")
        sys.exit(1)
    
    # Open browser
    open_browser()
    
    print("\n" + "="*70)
    print("[SUCCESS] SENTILYTICS IS NOW RUNNING!")
    print("="*70)
    print("\n[DASHBOARD] http://localhost:8000")
    print("[WEBSOCKET] ws://localhost:8000/ws")
    print("[API DOCS] http://localhost:8000/docs")
    print("\n[INFO] Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    try:
        # Keep script running
        server_process.wait()
    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Shutting down Sentilytics...")
        server_process.terminate()
        print("[OK] Server stopped. Goodbye!")

if __name__ == "__main__":
    main()
