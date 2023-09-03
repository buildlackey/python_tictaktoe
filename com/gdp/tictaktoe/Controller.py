import logging

from com.gdp.tictaktoe import Model
from com.gdp.tictaktoe import View




"""
Assists controller in determining which player is next to move. We key off the answer of our
external player to the question 'do you wish to go first' ? 
"""
class NextPlayerToMove():

    def __init__(self, player1: Model.Player, player2: Model.Player):
        self.moveCount = 0
        if (player1.goes_first):
            self.players = [player1, player2]
        else:
            self.players = [player2, player1]
    def get(self):
        index_of_next_player = self.moveCount % 2
        nextPlayer = self.players[index_of_next_player]
        logging.debug(f"players: {self.players}. count: {self.moveCount}. index: {index_of_next_player}: {nextPlayer}")
        self.moveCount += 1
        return nextPlayer

"""
Sets up the grid, identifies external player and prompts that player to choose their name, symbol, 
and whether or not to go first.   For each game will loop through process of getting players move until
a winning move or draw (no more positions open on board) is detected.  After each game concludes the
external player has the option of continuing for another round of play.
"""
class GameSessionController:
    def __init__(self):
        self.ui = View.UI()
        self.grid = self.ui.game_grid_from_user_input()
        self.opponent = self.ui.player_from_user_input()
        if self.opponent.symbol == 'X':
            my_player_symbol = 'O'
        else:
            my_player_symbol = 'X'
        self.my_player = Model.Player("SomeCheapAI", not self.opponent.goes_first, my_player_symbol)
        self.next_to_move = NextPlayerToMove(self.my_player, self.opponent)

    def get_grid(self):
        return self.grid


    def start(self):
        while True:
            self.grid.clear()

            while self.grid.winner == None :
                self.ui.display_game_grid(self.grid)
                player = self.next_to_move.get()
                self.ui.update_grid_with_player_move(self.grid, player)

                if not self.grid.moves_left():
                    self.ui.announce_winner(self.grid)
                    if (self.ui.get_users_yes_no_response("Play again? (y/n)") == 'N'):
                        return



if __name__ == "__main__":
    GameSessionController().start()
    logging.basicConfig(level=logging.DEBUG)  # Set the desired log level


