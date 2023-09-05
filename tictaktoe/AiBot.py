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

    def set_players(self, first_player_to_move, second_player): # TODO: better consistency if done in in constructor
        self.players = [ first_player_to_move, second_player ]

    """
    Get the index of the player whose turn it is to move (so we can flip between players as their turn comes up)
    """
    def __get_index_of_player(self, player_who_most_move: Model.Player):
        if (player_who_most_move.symbol == self.players[0].symbol):
            return 0
        else:
            return 1

    def __flatten_list__(self, nested_list):
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(self.__flatten_list__(item))
            else:
                result.append(item)
        return result


    """
    Score a game play outcome as reflected in 'grid'.  If 'player' has the winning moves:1, else if opponent won: -1 
    """
    def __score__(self, grid: Model.Grid, desired_winner: Model.Player):
        if (grid.get_winner() == desired_winner.symbol):    # positive score for this move series if won by 'desired'
            return 1
        elif (grid.get_winner() != None):       # if winner is the other player, then negative score
            return -1
        elif (not grid.moves_left()):
            return None

    def __highest_scoring_outcome__(self, outcomes: List[ScoredGameScenario]) -> ScoredGameScenario:
        best_score_so_far = -999999
        best_candidate = None

        for candidate in outcomes:
            if (candidate.score > best_score_so_far):
                best_candidate = candidate
                best_score_so_far = candidate.score

        return best_candidate

    def all_game_outcomes(self,
                          g: Model.Grid,
                          desired_winner: Model.Player,
                          which_player_index: int,
                          moves_so_far) -> List[ScoredGameScenario]:
        score = self.__score__(g, desired_winner)
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
            flattened_result = self.__flatten_list__(results)
            return flattened_result
    def get_move(self, grid: Model.Grid, player_who_must_move: Model.Player) -> List[int]:
        index_of_player_with_current_turn  = self.__get_index_of_player(player_who_must_move)
        all_game_outcomes = self.all_game_outcomes(grid, player_who_must_move, index_of_player_with_current_turn, [])

        best = self.__highest_scoring_outcome__(all_game_outcomes)
        logging.debug(f"best score identified: {best}")
        last_move_cell = best.list_of_moves[0]
        return [ last_move_cell.x,last_move_cell.y ]


if __name__ == "__main__":      ## TODO - don't need .. delete
    logging.basicConfig(level=logging.DEBUG)  # Set the desired log level
    player1 = Model.Player("one", True, 'x', None, True)
    player2 = Model.Player("two", False, 'o', None, False)
    next_move_factory = AiNextMoveFactory()
    next_move_factory.set_players(player1, player2)
    game_outcomes = next_move_factory.all_game_outcomes(Model.Grid(2), player1, 0, [])
    print(f"outcomes: {game_outcomes}")
    assert(len(game_outcomes) == 4 * 3 * 2 * 1)   # number of outcomes for cell grid is 4!
    assert all(outcome.grid.winner == player1.symbol for outcome in game_outcomes)

