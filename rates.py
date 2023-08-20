import time
import cv2
import threading
import ctypes
import mss
import mss.windows
import numpy as np
import config
import getDigits as gD
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from ctypes import wintypes
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

START_ANAYLSIS_TEMPLATE = cv2.imread('./templates/startanalysis.png', 0)
STOP_ANALYZING_TEMPLATE = cv2.imread('./templates/stopanalyzing.png', 0)

ED_WIDTH = 78
ED_HEIGHT = 79

class BattleAnalysis:
    """
    Class that keeps track of the battle analysis to see the enemies defeated
    per second
    """
    def __init__(self):

        self.frame = None
        self.ed_ratio = 1
        self.ed_sample = None
        self.sct = None
        self.window = {
            'left': 0,
            'top': 0,
            'width': 1366,
            'height': 768
        }
        self.ready = False
        self.calibrated = False
        self.thread = None
        self.model = None
        self.enemies_defeated = None

    def start(self):
        """Loads OCR and starts thread"""

        print("[~] Starting rates capture")
        print("[~] Loading model...")
        try:
            self.model = load_model('ocr/model')
        except Exception as e:
            print(f"[!] An error occured: {e}")
        print("[+] Model loaded!")

        if self.thread is None or not self.thread.is_alive():
            print('\n[~] Started rates capture')
            self.thread = threading.Thread(target=self.track, daemon=True)
            self.thread.start()
        else:
            print("Error, thread is already running")

    def track(self):

        mss.windows.CAPTUREBLT = 0

        # Create mss object that is a handle to the screen capture fuctionality as self.sct
        identifier = 0
        with mss.mss() as self.sct:
            while True:
                # Updates self.frame to be an image of the maplestory window
                self.getMapleFrame()

                if self.frame is None:
                    continue

                # Locates the bottom right pixel of the stop analyzing button
                _, br = single_match(self.frame, STOP_ANALYZING_TEMPLATE)    

                # Reconstruct enemies defeated area based on top left and bottom right
                ed_tl = (
                    br[0] - ED_WIDTH,
                    br[1] - ED_HEIGHT
                )
                ed_br = (
                    br[0],
                    br[1] - 58
                )

                # Ratio of width : height
                self.ed_ratio = (ed_br[0] - ed_tl[0]) / (ed_br[1] - ed_tl[1])

                # Image of enemies defeated
                self.ed_sample = self.frame[ed_tl[1]:ed_br[1], ed_tl[0]:ed_br[0]]

                # Get images and store into folder every 3 secs
                self.enemies_defeated = gD.getDigits(self.ed_sample, self.model)
                identifier+= 1

                config.enemies_defeated = self.enemies_defeated

                if not self.ready:
                    self.ready = True
                time.sleep(0.5)

    def screenshot(self, delay=1):
        try:
            return np.array(self.sct.grab(self.window))
        except mss.exception.ScreenShotError:
            print(f'\n[!] Error while taking screenshot, retrying in {delay} second'
                  + ('s' if delay != 1 else ''))
            time.sleep(delay)

    def getMapleFrame(self):
        """
        Takes a screenshot of entire screen and locates the Maplestory window
        Updates self.window to be the top left pixel and the width height of screen
        Updates self.frame to the image that self.window encapsulates
        """
        handle = user32.FindWindowW(None, 'MapleStory')       # Find the Maplestory window, none takes in any window class
        rect = wintypes.RECT()                                # (left, top, right, and bottom) of a rectangle in a Windows application.
        user32.GetWindowRect(handle, ctypes.pointer(rect))    
        rect = (rect.left, rect.top, rect.right, rect.bottom)
        rect = tuple(max(0, x) for x in rect)                 # No negative coords allowed

        self.window['left'] = rect[0]
        self.window['top'] = rect[1]
        self.window['width'] = rect[2]
        self.window['height'] = rect[3]


        with mss.mss() as self.sct:
            self.frame = self.screenshot()


def single_match(frame, template):
    """
    Finds the best match within FRAME.
    :param frame:       The image in which to search for TEMPLATE.
    :param template:    The template to match with.
    :return:            The top-left and bottom-right positions of the best match.
    """

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
    _, _, _, top_left = cv2.minMaxLoc(result)
    w, h = template.shape[::-1]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    return top_left, bottom_right


