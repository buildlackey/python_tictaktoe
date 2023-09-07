# Tic Tak Toe Game



## Overview

This repository holds code for a single player tic tak toe game where you 
play against a primitive AI Bot that uses brute force search to determine its moves.


## Caveats

Pure brute force approach leads to 9! combinations of moves being score if the AI player goes first, 
so to speed things up we use some heurestics.  For example, if the AI player goes first we grab the middle 
cell without any scoring or searching.  BUT, if the human opponent player goes first the AI move generator 
is still slow. So please give it about a minute for that second move.


## Installation

Before running, install the zip file as shown below:

    # download the zip file to some directory: /tmp/zip.tar.gz
    # make a workspace folder and cd to it
    rm -rf /tmp/junk
    mkdir /tmp/junk
    cd  /tmp/junk
    tar xvzf /tmp/zip.tar.gz


## Running


After following the steps in the preceding section you 
can run the program from the top level project folder as shown below. 
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

To run unit tests, execute these command from the top level project folder:

   python3.11 -m venv game
   . game/bin/activate
   pip install pytest
    python -m pytest
