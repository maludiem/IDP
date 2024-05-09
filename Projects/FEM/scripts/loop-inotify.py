import os
import time
import inotify.adapters

def run_script():
    print("hand.txt file changed, replay main.py")
    os.system("python3 final_dumpling_compress.py")

if __name__ == "__main__":
    i = inotify.adapters.Inotify()
    i.add_watch("../../../../../rot1.txt")

    try:
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            if 'IN_MODIFY' in type_names:
                run_script()
    except KeyboardInterrupt:
        print("Stopped watching file")
