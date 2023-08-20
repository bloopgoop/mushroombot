import time
import threading
import ctypes
import ai
import config
import pickle
import os
import random
import automaple.vkeys as vk
from updater import Updater

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


class Bot():
    """
    Class that trains the AI and makes the moves
    """
    def __init__(self, save_interval=20, training_interval=4):

        self.ready = False
        self.calibrated = False
        self.thread = None
        self.updater = None
        self.file_path = None
        self.save_interval = save_interval
        self.training_interval = training_interval


        movements = ['left_fj', 'right_fj', 'down_j', 'ascend']
        skills = ['main_attack']

        self.actions = []

        for movement in movements:
            for skill in skills:
                self.actions.append((movement, skill))


        config.rates = 0
        


    def start(self, model):
        """ Checks if model exists, if not train one. Then starts this thread and the model update thread. """

        file_path = f"models/{model}.pkl"

        if self.thread is None or not self.thread.is_alive():

            if os.path.exists(file_path):
                print('\n[~] Started bot')
                self.thread = threading.Thread(target=self.use_model(file_path), daemon=True)
            else:
                print('\n[~] Started training bot')
                self.thread = threading.Thread(target=self.train, daemon=True)

                self.updater = Updater(file_path)
                self.updater.start()
                self.thread.start()

        else:
            print("Error, thread is already running")


    def train(self):
        """ Trains AI """
        model = ai.MapleAI()
        print('\n[~] Successfully initialized program')
        
        while True:
            state = getState(config.player_pos)
            action = model.choose_action(state)
            if action is None:
                print("NoneType,", state)

            old_defeated = config.enemies_defeated
            self.execute(action)
            time.sleep(self.training_interval + 0.3 * random.random())
            new_state = getState(config.player_pos)

            rates = config.enemies_defeated - old_defeated

            model.update(
                state,
                action,
                new_state,
                rates
            )


            if not self.ready:
                self.ready = True
            config.bot = model

            clear_console()
            print(f"\nStats\n\n"
                f"Time elapsed: "
                f"{config.time}\n"
                f"Character Position: {new_state}\n" 
                f"Action: {action}\n"
                f"Rates: {rates}\n"
                f"new: {config.enemies_defeated}\n"
                f"old: {old_defeated}\n"
                f"Time since last spawn: {config.time_since_spawn}\n"
                , end='\r')

    def use_model(self, model):

        with open(model, 'rb') as f:
            model = pickle.load(f)

        model.stop_training()

        print('\n[~] Successfully retrieved trained model')
        
        while True:
            state = getState(config.player_pos)
            action = model.choose_action(state)
            self.execute(action)

            clear_console()
            print(f"\nStats\n\n"
                f"Time elapsed: "
                f"{config.time}\n"
                f"Character Position: {state}\n" 
                f"Action: {action}\n"
                f"Time since last spawn: {config.time_since_spawn}\n"
                , end='\r')
            
            if not self.ready:
                self.ready = True
            config.bot = model
            time.sleep(0.2 + 0.3 * random.random())


    def execute(self, action):
        movement = action[0]
        skill = action[1]

        if movement == 'left_fj':
            vk.press("left")
            vk.press("alt", 2, up_time=0.05)
        elif movement == 'right_fj':
            vk.press("right")
            vk.press("alt", 2, up_time=0.05)
        elif movement == 'down_j':
            vk.key_down("down")
            vk.press("alt")
            vk.key_up("down")
        else:
            vk.press("alt", up_time=0.05)
            vk.press("a")
        
        if skill == 'main_attack':
            vk.press("shift")
        
        time.sleep(0.1 + 0.4 * random.random())



def getState(pos):
    """ Takes in config.player_pos and returns the state tuple of pos, time """
    x = round(pos[0], 1)
    y = round(pos[1], 1)

    state = (x, y)

    return state


