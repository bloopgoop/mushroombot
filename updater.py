import pickle
import threading
import os
import config
import time

class Updater():
    """
    Class that trains the AI and makes the moves
    """
    def __init__(self, file_path):

        self.ready = False
        self.thread = None
        self.file_path = file_path

    def start(self):
        """ Checks if model exists, if not train one. Then starts this thread and the model update thread. """

        if self.thread is None or not self.thread.is_alive():

            if not os.path.exists(self.file_path):
                print('\n[~] Started bot saving')
                self.thread = threading.Thread(target=self.save, daemon=True)
                self.thread.start()
            else:
                print("[X] Loading trained model...")
                time.sleep(1)
                
        else:
            print("Error, thread is already running")


    def save(self):
        """ Save the model every 20 seconds """
        os.makedirs('models', exist_ok=True)

        time.sleep(5)
        print("while true loop for updater running")
        while True:
            # Write binary
            with open(self.file_path, 'wb') as f:
                pickle.dump(config.bot, f)

            print("pickle dumped")
            if self.ready == False:
                self.ready = True

            print("save success")
            time.sleep(5)

        