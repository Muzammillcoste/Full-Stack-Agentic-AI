import subprocess
import sys
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_EXTENSIONS = {'.py'}  # Only restart on Python file changes
WATCHED_DIRS = ['.']  # Watch all files under current directory

class RestartHandler(FileSystemEventHandler):
    def __init__(self, restart_callback):
        super().__init__()
        self.restart_callback = restart_callback

    def on_any_event(self, event):
        if event.is_directory:
            return
        _, ext = os.path.splitext(event.src_path)
        if ext in WATCHED_EXTENSIONS:
            print(f"Detected change in {event.src_path}, restarting processes...")
            self.restart_callback()

def start_processes():
    server = subprocess.Popen([sys.executable, "main.py"])
    worker = subprocess.Popen([
        "rq", "worker", "--worker-class", "rq.worker.SimpleWorker"
    ])
    return server, worker

def stop_processes(server, worker):
    for proc in (server, worker):
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    processes = {'server': None, 'worker': None}
    def start_all():
        server, worker = start_processes()
        processes['server'] = server
        processes['worker'] = worker

    def stop_all():
        stop_processes(processes['server'], processes['worker'])

    def restart():
        stop_all()
        start_all()

    start_all()
    event_handler = RestartHandler(restart)
    observer = Observer()
    for path in WATCHED_DIRS:
        observer.schedule(event_handler, path, recursive=True)
    observer.start()
    print("Watching for file changes. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        observer.stop()
        observer.join()
        stop_all()
