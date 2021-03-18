# Optimal Rocket League Bot
This is a bot designed to utilize numerical optimization techniques in order to
optimally play the game Rocket League.

## Requirements
Install Rocket League
https://www.epicgames.com/store/en-US/p/rocket-league

Install RLBot GUI
https://www.youtube.com/watch?v=oXkbizklI2U

Install Python 3
https://www.python.org/downloads/
- recommended version 3.9.2

Install NumPy
https://numpy.org/install/
- recommended using pip installation

## Setup
Once all of the prerequisite requirements are met (above) you run the RLBot GUI.
In order to enable this bot you must load the folder where you clone this
repository using the RLBot GUI. I would recommend cloning the repository into
the default RLBot bot folder which can be found by clicking the button labeled
"Manage bot folders" and copying the path ending with the folder "MyBots".

Some match settings that are recommended would be enabling rendering, skip
replays, and instant start. One setting which must remain off is enabling
lockstep as this leads to improper packet timestamps.

## File Information
appearance.cfg : controls the bot appearances (mostly unimportant except for car type)

config.cfg : stores metadata about the bot and developers (mostly unimportant)

src : contains all source code

src/hive.py : is the code responsible for controlling the bots

src/drone.py : dummy file required by RLBot API to control the bots (mostly unimportant)

src/utils : contains all source code for utility classes/functions/values

src/utils/constants.py : contains all constant variables and settings

src/utils/state.py : contains utilities for interacting and storing game state data

src/utils/predictor.py : contains code for managing state predictors

src/utils/scorer.py : contains code for managing state scorers

src/utils/decision.py : contains code implementing an arbitrary decision tree algorithm
