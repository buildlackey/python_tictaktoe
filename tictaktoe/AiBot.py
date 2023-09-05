import logging

from tictaktoe import Model
from typing import List


class ScoredGameScenario:
    def __init__(self, score, list_of_moves):
        self.list_of_moves = list_of_moves
        self.score = score

"""
Uses brute force search through all possible solutions to discover best next move for Ai player 
"""
class AiNextMoveFactory:

    def __init__(self):
        self.players = [ Model.Player("one", True, 'x', None, True) , Model.Player("two", False, 'o', None, False) ]
        pass

    """
    Score a game play outcome as reflected in 'grid'.  If 'player' has the winning moves:1, else if opponent won: -1 
    """
    def score(self, grid: Model.Grid, player: Model.Player) -> ScoredGameScenario:
        if (grid.get_winner() == player.symbol):    # positive score for this move series if 'player' is winner
            return 1
        elif (grid.get_winner() != None):       # if winner is the other player, then negative score
            return -1
        elif (not grid.moves_left()):
            return None

    def all_game_outcomes(self,
                          g: Model.Grid,
                          desired_winner: Model.Player,
                          which_player_index: int,
                          moves_so_far) -> List[Model.Grid]:
        score = self.score(g, desired_winner)
        logging.debug(f"all_move_sequences. next_mover: {which_player_index}. moves_so_far:{moves_so_far}. score: {score}")
        if (score):
            logging.info(f"got scoreable grid with these moves: {moves_so_far}. grid: {g}")
            return [g]
        else:
            results = []
            cells_to_try = g.get_free_cells()
            who_moves = self.players[which_player_index]
            for cell in cells_to_try:
                updated_cell = cell.with_symbol(who_moves.symbol)  # free cell now marked with current player's symbol
                updated_grid = g.apply_move(updated_cell, who_moves)  # this grid will be scored in recursive calls
                logging.debug(f"player {who_moves} will try this grid in recursive call: {updated_grid}")
                result = self.all_game_outcomes(updated_grid, desired_winner, 1 - which_player_index, [updated_cell] + moves_so_far)
                results.append(result)
                logging.debug(f"unflattened results for cell {results}")
            flattened_result = self.flatten_list(results)
            return flattened_result

    def highest_scoring_sequence_of_moves(self, grid: Model.Grid, player: Model.Player):
        def select_best_score(self, candidates):
            winner = None
            for candidate in candidates:
                if (candidate.score):
                    #best_so_far =
                    winner = candidate



        candidates = self.all_game_outcomes(grid, player, [])
        best = select_best_score(candidates)



    def get_move(self, grid: Model.Grid, player: Model.Player):
        all_game_outcomes = self.all_game_outcomes(grid, player, [])
        for resultant_grid in all_game_outcomes:
            print(f"grid: {resultant_grid.render_as_string()}")


    def flatten_list(self, nested_list):
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(self.flatten_list(item))
            else:
                result.append(item)
        return result

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)  # Set the desired log level
    player1 = Model.Player("one", True, 'x', None, True)
    player2 = Model.Player("two", False, 'o', None, False)
    grid = Model.Grid(2)
    game_outcomes = AiNextMoveFactory().all_game_outcomes(grid, player2, 0, [])
    assert(len(game_outcomes) == 4 * 3 * 2 * 1)   # number of outcomes for cell grid is 4!
    assert all(grid.winner == player1.symbol for grid in game_outcomes)

