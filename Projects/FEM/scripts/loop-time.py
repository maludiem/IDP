import os
import shutil
import time
from pathlib import Path
index = 0

def run_script():
    print("hand.txt file changed, replay main.py")
    os.system("python3 final_dumpling_compress.py")
    shutil.copy("output/main_model/model.obj","output/process/op_"+str(index)+".obj")
    os.system("python3 _fig1_final_dumpling.sh")

if __name__ == "__main__":
    file_to_watch = Path("../../../../../hand.txt")
    last_modified_time = file_to_watch.stat().st_mtime

    try:
        while True:
            current_modified_time = file_to_watch.stat().st_mtime
            if current_modified_time != last_modified_time:
                run_script()
                last_modified_time = current_modified_time
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped watching file")
