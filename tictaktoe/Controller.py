import logging
import sys

from tictaktoe import Model, View

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

    def __str__(self):
        return f"player1: {self.players[0]}. player2: {self.players[1]}. count: {self.moveCount}"


    def get(self):
        index_of_next_player = self.moveCount % 2
        nextPlayer = self.players[index_of_next_player]
        logging.debug(f"nextTracker: {self}. index: {index_of_next_player}: {nextPlayer}")
        self.moveCount += 1
        return nextPlayer

"""
Sets up the grid, identifies external player and prompts that player to choose their name, symbol, 
and whether or not to go first.   For each game will loop through process of getting players move until
a winning move or draw (no more positions open on board) is detected.  After each game concludes the
external player has the option of continuing for another round of play.
"""
class GameSessionController:

    def __init_player_state(self, ui: View.UI,  human_mode):
        def next_move_factory(player: Model.Player, grid: Model.Grid):                # default factory for getting next move
            ui.update_grid_with_player_move(grid, player)

        self.opponent = self.ui.player_from_user_input(next_move_factory)
        if self.opponent.symbol == 'X':
            my_player_symbol = 'O'
        else:
            my_player_symbol = 'X'
        self.my_player = Model.Player("SomeCheapAI", not self.opponent.goes_first, my_player_symbol, next_move_factory)
        self.whose_turn = NextPlayerToMove(self.my_player, self.opponent)

    def __init__(self, human_mode=False):
        self.ui = View.UI()
        self.grid = self.ui.game_grid_from_user_input()
        self.grid_dimension = self.grid.max_index
        self.__init_player_state(self.ui, human_mode)


    def get_grid(self):
        return self.grid

    def clear_grid(self):
        self.grid = Model.Grid(int(self.grid_dimension))


    def start(self):
        while True:
            self.clear_grid()

            while self.grid.winner == None :
                self.ui.display_game_grid(self.grid)
                player = self.whose_turn.get()
                player.move(self.grid)

                if not self.grid.moves_left():
                    self.ui.announce_winner(self.grid)
                    if (self.ui.get_users_yes_no_response("\nPlay again? (y/n)") == 'N'):
                        return



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)  # Set the desired log level
    GameSessionController(True).start()


