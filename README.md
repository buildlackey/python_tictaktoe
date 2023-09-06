# Tic Tak Toe Game



## Overview

This repository holds code for a single player tic tak toe game where you 
play against a primitive AI Bot that uses brute force search to determine its moves.


## Running


You can run the program from the top level project folder as shown below. 
By specifying optional arguments you can run with  verbose logging 
(using the '-v' / --verbose flag), and/or with -m/--manual mode which 
turns off the AIBot's automated move discovery, instead allowing you 
to input the AIBot's moves.  (Both of these can be useful for 
testing/debugging).


    python Driver.py [-v] [-m] 


The program will prompt you for your name, desired game symbol, and other preferences.
When it is your turn to move, enter the coordinates of any free cell as two integers, separated by 
any non-integer characters, as shown below:


    Your move, JOE,  Enter x,y coordinates of free cell (each coord > 0 and < 3): 0 0

    o _ _

    _ _ _

    _ _ _



## Testing 

To run unit tests, execute these commands from the top level project folder:

   python3.11 -m venv game
   . game/bin/activate
   pip install pytest
    python -m pytest
