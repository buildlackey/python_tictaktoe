# Tic Tak Toe Game





## Running


You can run the program from the top level project folder --- 
with or without verbose logging (using the '-v' flag) -- as shown below: 


    python Driver.py [-v] 


The program will prompt you for your name, desired game symbol, and other preferences.
When it is your turn to move, enter the coordinates of any free cell as two integers, separated by 
any non-integer characters, as shown below:


    Your move, JOE,  Enter x,y coordinates of free cell (each coord > 0 and < 3): 0 0

    o _ _

    _ _ _

    _ _ _



## Testing 

To run unit tests, execute this command from the top level project folder:
    
    python -m pytest
