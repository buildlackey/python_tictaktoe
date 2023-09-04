import logging

from tictaktoe import Model, View

"""
Uses brute force search through all possible solutions to discover best next move for Ai player 
"""
class AiNextMoveFactory():

    def __init__(self):
        pass

    def get_move(self, grid: Model.Grid, player: Model.Player):
        for x in range(grid.max_index):
            for y in range(grid.max_index):
                candidate_cell = grid.get_cell(x,y)
                if (candidate_cell.is_free()):
                    return candidate_cell


