import logging

from tictaktoe import Model
from typing import List


class ScoredGameScenario:
    def __init__(self, score, grid, list_of_moves):
        self.score = score
        self.grid = grid
        self.list_of_moves = list_of_moves


    def __repr__(self):
        return f"score: {self.score}. moves: {self.list_of_moves}. grid: {self.grid}"

"""
Uses brute force search through all possible solutions to discover best next move for Ai player 
"""
class AiNextMoveFactory:

    def __init__(self):
        pass

    def set_players(self, first_player_to_move, second_player):
        self.players = [ first_player_to_move, second_player ]

    """
    Score a game play outcome as reflected in 'grid'.  If 'player' has the winning moves:1, else if opponent won: -1 
    """
    def score(self, grid: Model.Grid, desired_winner: Model.Player) -> int:
        if (grid.get_winner() == desired_winner.symbol):    # positive score for this move series if won by 'desired'
            return 1
        elif (grid.get_winner() != None):       # if winner is the other player, then negative score
            return -1
        elif (not grid.moves_left()):
            return None

    def all_game_outcomes(self,
                          g: Model.Grid,
                          desired_winner: Model.Player,
                          which_player_index: int,
                          moves_so_far) -> List[ScoredGameScenario]:
        score = self.score(g, desired_winner)
        logging.debug(f"all_move_sequences. next_mover: {which_player_index}. moves_so_far:{moves_so_far}. score: {score}")
        if (score):
            logging.info(f"got scoreable grid with these moves: {moves_so_far}. grid: {g}")
            return [ScoredGameScenario(score, g, moves_so_far)]
        else:
            results = []
            cells_to_try = g.get_free_cells()
            who_moves = self.players[which_player_index]
            for cell in cells_to_try:
                updated_cell = cell.with_symbol(who_moves.symbol)  # free cell now marked with current player's symbol
                updated_grid = g.apply_move(updated_cell, who_moves)  # this grid will be scored in recursive calls
                updated_moves = moves_so_far + [updated_cell]
                logging.debug(f"player {who_moves} GRID TO USE IN RECURSIVE CALL: {updated_grid}. mvs: {updated_moves}")
                result = self.all_game_outcomes(updated_grid, desired_winner, 1 - which_player_index, updated_moves)
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
            print(f"grid: {resultant_grid}")


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
    next_move_factory = AiNextMoveFactory()
    next_move_factory.set_players(player1, player2)
    game_outcomes = next_move_factory.all_game_outcomes(Model.Grid(2), player1, 0, [])
    print(f"outcomes: {game_outcomes}")
    assert(len(game_outcomes) == 4 * 3 * 2 * 1)   # number of outcomes for cell grid is 4!
    assert all(outcome.grid.winner == player1.symbol for outcome in game_outcomes)

