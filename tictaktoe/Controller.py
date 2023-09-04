import logging

from tictaktoe import Model, View, AiBot

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
        logging.debug(f"nextTracker: {self}. index: {index_of_next_player}: NextUp: {nextPlayer}")
        self.moveCount += 1
        return nextPlayer

"""
Sets up the grid, prompts the external player for their name, prefered game symbol ('x' or 'o'), 
and whether or not to go first.   For each game round the controller will loop through process of getting players 
moves until a winning move or draw (no more positions open on board) is detected.  Upon conclusion of each game
the external player has the option of continuing for another round of play.
"""
class GameSessionController:
    def __init_player_state(self, ui: View.UI, use_human_input_for_all_players, ai_next_move_factory):
        def next_move_from_ui_input(player: Model.Player, grid: Model.Grid): # factory for getting next move from human
            return ui.prompt_for_coords_of_next_move(grid, player)

        def next_move_from_ai_bot(player: Model.Player, grid: Model.Grid): # next move factory using machine intelligence
            return ai_next_move_factory.get_move(grid, player)

        self.external_player = self.ui.player_from_user_input(next_move_from_ui_input)

        # set up state that drives behavior of internal player
        if self.external_player.symbol == 'X':
            symbol = 'O'        # internal player symbol is 'o'
        else:
            symbol = 'X'        # internal player symbol is 'x'
        goes_first =  not self.external_player.goes_first
        if (use_human_input_for_all_players):
            self.internal_player = Model.Player("SomeCheapAI", goes_first, symbol, next_move_from_ui_input, True)
        else:
            self.internal_player = Model.Player("SomeCheapAI", goes_first, symbol, next_move_from_ai_bot, True)

        self.whose_turn = NextPlayerToMove(self.internal_player, self.external_player)

    def __init__(self, human_mode=False):
        self.ui = View.UI()
        self.grid = self.ui.game_grid_from_user_input()
        self.grid_dimension = self.grid.max_index
        self.human_mode = human_mode
        self.__init_player_state(self.ui, human_mode, AiBot.AiNextMoveFactory())


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
                cell = player.move(self.grid)
                self.ui.announce_internal_player_move(player, cell, self.human_mode)
                self.grid = self.grid.apply_move(cell, player)  # get new grid copy updated with this move

                if not self.grid.moves_left():
                    self.ui.announce_winner(self.grid)
                    if (self.ui.get_users_yes_no_response("\nPlay again? (y/n)") == 'N'):
                        return



if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)  # Set the desired log level
    GameSessionController(False).start()


