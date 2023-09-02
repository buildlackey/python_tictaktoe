import sys

from com.gdp.tictaktoe import Model
from com.gdp.tictaktoe import View


class NextPlayerToMove():

    def __init__(self, player1: Model.Player, player2: Model.Player):
        self.moveCount = 0
        if (player1.goes_first):
            self.players = [player1, player2]
        else:
            self.players = [player2, player1]
    def get(self):
        nextPlayer = self.players[self.moveCount % 2]
        self.moveCount += 1
        return nextPlayer


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


    def start(self):
        while True:
            self.grid.clear()

            while self.grid.winner == None :
                self.ui.display_game_grid(self.grid)
                player = self.next_to_move.get()
                self.ui.update_grid_with_player_move(self.grid, player)

                if not self.grid.moves_left():
                    self.ui.announce_winner(self.grid)
                    if (self.ui.get_users_yes_no_response("Play again?") == 'Y'):
                        sys.exit(0)



if __name__ == "__main__":
    GameSessionController().start()


