import threading
import webbrowser
import time
import os
import sys
import uvicorn
import tkinter as tk
from tkinter import messagebox

def show_error_popup(title, message):
    """Displays a native Windows dialog box with the exact crash logs."""
    root = tk.Tk()
    root.withdraw()  # Hide the main tiny black window
    messagebox.showerror(title, message)
    root.destroy()

# Fix environment paths so internal packages can see each other
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
    internal_path = os.path.join(base_path, "_internal")
    sys.path.insert(0, internal_path)
    sys.path.insert(0, base_path)
    os.chdir(base_path)

try:
    # Attempt to import the server app
    from app import app
except Exception as e:
    import traceback
    error_details = traceback.format_exc()
    show_error_popup("Backend Import System Fault", f"Failed to import core application layers:\n\n{error_details}")
    sys.exit(1)

def start_backend():
    """Launches the FastAPI backend core server securely and catches crashes."""
    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        show_error_popup("Server Boot Runtime Crash", f"The background server crashed while starting:\n\n{error_details}")

def launch_interface():
    """Waits for the backend server to spin up, then opens the dashboard."""
    time.sleep(3.0)  # Give the server 3 full seconds to bind to port 8000
    
    if getattr(sys, 'frozen', False):
        current_dir = sys._MEIPASS
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
    ui_path = os.path.join(current_dir, "index.html")
    
    if os.path.exists(ui_path):
        webbrowser.open(f"file:///{ui_path}")
    else:
        show_error_popup("UI Resolution Error", f"Missing interface assets. index.html not found at:\n{ui_path}")

if __name__ == "__main__":
    # 1. Start backend server in a safe diagnostic thread
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()
    
    # 2. Launch interface natively via default browser
    launch_interface()
    
    # 3. Keep main execution stream open
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass