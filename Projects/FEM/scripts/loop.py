import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
path_to_watch = "../../../../../rot1.txt"

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("rot1.txt"):
            print("file changed,replay main.py")
            os.system("python3 final_dumpling_compress.py")
            observer.schedule(event_handler, path=path_to_watch, recursive=False)

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=False)
    observer.start()

    try:
        print("start loop!")
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
