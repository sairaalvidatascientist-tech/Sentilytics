import subprocess
import os
import sys
import time
import webbrowser

def run():
    backend_path = os.path.join(os.getcwd(), "agropredict", "backend")
    
    # Check for requirements
    print("Checking dependencies...")
    # subprocess.run([sys.executable, "-m", "pip", "install", "-r", os.path.join(backend_path, "requirements.txt")])

    print("Starting AgroPredict Platform...")
    
    # Start the backend
    process = subprocess.Popen([sys.executable, os.path.join(backend_path, "main.py")], 
                              cwd=backend_path)
    
    # Give it a second to start
    time.sleep(3)
    
    # Open the browser
    webbrowser.open("http://localhost:8000")
    
    print("\n" + "="*50)
    print("AgroPredict is now running at http://localhost:8000")
    print("Close this terminal to stop the server.")
    print("="*50)
    
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        print("\nServer stopped.")

if __name__ == "__main__":
    run()
