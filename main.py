""" Runs all threads """
import time
from bot import Bot
from minimap import Minimap
from rates import BattleAnalysis
from clock import Clock

clock = Clock()
minimap = Minimap()
battle_analysis = BattleAnalysis()
bot = Bot()

clock.start()

minimap.start()
while not minimap.ready:
    time.sleep(0.01)

battle_analysis.start()
while not battle_analysis.ready:
    time.sleep(0.01)

bot.start(model="b1")
while not bot.ready:
    time.sleep(0.01)


print('\n[~] Successfully initialized main')
while True:
    time.sleep(100)
    print("100 seconds elapsed")
