import time
import config
import threading


class Clock():
    def __init__(self):

        self.thread = None

    def start(self):
        """Starts thread"""

        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.count, daemon=True)
            self.thread.start()
            print("[~] Started clock")
        else:
            print("Error, thread is already running")

    def count(self):
        start_time = time.time()
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            hours = int(elapsed_time // 3600)
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)

            config.time = f"{hours:02}:{minutes:02}:{seconds:02}"
            config.time_since_spawn = (config.time_since_spawn + 1) % 8
            time.sleep(1)
            