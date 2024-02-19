# mushroombot

This project attempts to simulate grinding in maplestory using computer vision and machine-learning techniques<br><br>

The bot uses screen capture methods and computer vision to find in-game feature such as character position and mobs defeated. 
It is intended to be used for any map and for any class, given a set of defined actions that the user provides the bot.
It does this by utilizing the Q-learning algorithm, a reinforced learning algorithm that gives a state and an action pair a corresponding Q-value.
<br><br>
Libraries like user32 are used to simulate key presses, making this bot undetectable

# Q-learning
This algorithm uses a state, action pair and links it to a corresponding q-value so that the bot can make intelligent decisions.
The states are the (x, y) positions of the character. The actions are the set of actions that the user defines for the bot (default is
'left', 'up', 'right', 'down'). The rewards/q-value is the mobs defeated by an action. Because the mobs defeated count can not be negative, 
I added a default bias of -4 so that the bot may be punished when performing non-optimal movements.

# Screen Capture
To get a reward/punsihment system for the bot, I used several computer vision techniques to capture the in-game battle analysis.
The battle analysis keeps track of farming metrics that I needed to extract to use in the program.
Libraries like cv2, mss, and numpy helped to detect, screenshot, and manipulate images for processing. 
After processing, I created an OCR using a convolutional neural network with a custom data set to read and extract numbers from the battle analysis.

# Acknowledgements / Disclaimers
Training the bot is very slow, it takes more than an hour to get it to figure out a routine for farming. The battle analysis capture may generate wrong
answers and may mess up the q-learning process. Runes detection and solving is not implemented. <br><br>

Credits go out to [auto-maple](https://github.com/tanjeffreyz/auto-maple) for the code to simulate key presses and for minimap positional capture.<br><br>
This bot was made for educational purposes only. 
