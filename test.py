import mss
import numpy as np
import cv2
import threading
import time


class Capture:
    def __init__(self):
        self.img = None
        self.thread = None
        self.window = {
            'left': 0,
            'top': 0,
            'width': 1366,
            'height': 768
        }

    def screenshot(self):
        with mss.mss() as sct:
            screenshot = sct.grab(self.window)
            self.img = np.array(screenshot)

    def start(self):
        self.thread = threading.Thread(target=self.screenshot, daemon=True)
        self.thread.start()

        # Wait for the thread to complete
        self.thread.join()

        # Display the image in the main thread after a short delay
        time.sleep(1) 
        cv2.imshow('test', self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

c = Capture()
c.start()