import logging
import copy
from typing import List, Tuple

free_cell_symbol = '_'
x_symbol = 'x'
o_symbol = 'o'

class Intersection:
    def __init__(self, coords: List[Tuple[int,int]]):
        self.coords = sorted(coords)
        self.otherCoords = [(2,2)]

    def __repr__(self):
        return f"Intersection: {self.coords}"

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Intersection):
            return self.coords == other.coords
        return False

    """
    If Intersection contains one free cell, and all the other cells are owned by opposing player, returns the 
    free cell as the 'blocker' which -- if used in the next move, will prevent the opposing player from owning
    all the cells in the Intersection (thus preventing opponent from winning the game, at least via this Intersection).
    """
    def cell_to_block_opponent_win(self, opposing_player: 'Player', grid: 'Grid'):
        logging.debug(f"cell_to_block_opponent_win: {self}")

        free_cell = None
        num_owned_by_opponent = 0     # count of cells owned by opposing_player
        for coord_tuple in self.coords:
            logging.debug(f"checking coords: {coord_tuple}")
            cell = grid.get_cell(coord_tuple[0],coord_tuple[1])
            if (cell.is_free()):
                logging.debug(f"cell is free: {cell}")
                free_cell = cell
            elif (cell.symbol == opposing_player.symbol):
                logging.debug(f"cell is owned by opponent: {cell}")
                num_owned_by_opponent += 1
            else:
                assert cell.symbol == opposing_player.get_opponent_symbol()     # we should never get here

        logging.debug(f"num_owned_by_opponent: {num_owned_by_opponent}")
        if (free_cell and num_owned_by_opponent == grid.dimension - 1):  # if all but one owned by opponent
            return free_cell.with_symbol(opposing_player.get_opponent_symbol())  # return the free_cell if it was found
        else:
            return None


class Cell:
    def __init__(self, symbol, x: int, y: int, grid_size):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.grid_size = grid_size

    def __repr__(self):
        return f"({self.x},{self.y})->{self.symbol}"

    def with_symbol(self, new_symbol):
        new_cell = copy.deepcopy(self)
        new_cell.symbol = new_symbol
        return new_cell

    def is_free(self):
        return self.symbol == free_cell_symbol

    """
    Given a horizontal or vertical index position, return all the other indices in the row or column
    """
    def __get_sibling_indices__(self, index):
        return [i for i in range(self.grid_size) ]

    def __get_adjacent_cells_in_diagonal_for_dimension__(self,  dim):
        coords = [i for i in range(self.grid_size)]
        if (dim > 0):
            coords.reverse()
        logging.debug(f"__get_adjacent_cells_in_diagonal_for_dimension__ cell: {self}: dim: {dim}. result: {coords}")
        return coords

    def __get_adjacent_cells_in_diagonal(self):
        x_coords_for_adjacents = self.__get_adjacent_cells_in_diagonal_for_dimension__(self.x)
        y_coords_for_adjacents = self.__get_adjacent_cells_in_diagonal_for_dimension__(self.y)
        retval = list(zip(x_coords_for_adjacents, y_coords_for_adjacents))
        logging.debug(f"__get_adjacent_cells_in_diagonal cell: {self}: {retval}")
        return retval


    def __max_index__(self):
        return self.grid_size - 1

    def is_center_cell(self):
        mid_index = int(self.__max_index__())
        return self.x == mid_index and self.y == mid_index

    def is_edge_cell(self):
        return self.x == 0 or self.y == 0 or self.x == self.__max_index__() or self.y == self.__max_index__()

    def __right_to_left_diagonal__(self) -> List[Tuple[int,int]]:
        return [(self.__max_index__() - i, i) for i in range(self.grid_size)]

    def __left_to_right_diagonal__(self) -> List[Tuple[int,int]]:
        return  [(i,i) for i in range(self.grid_size)]

    """
    Given a cell that is not on a corner, and not along a diagonal in the grid,  this method returns two 
    Intersections (sequences of adjacent cell coordinates), one sequence for the row that subsumes this cell, 
    and another for the subsuming column.   

    If this cell is on a diagonal, then we return the upper-left to lower-right diagonal, plus the 'flipped' diagonal
    (which consists of the line running from upper right to lower left).
    """
    def get_intersections(self) -> List[Intersection]:
        if (self.grid_size == 1):       # trivial case of one cell grid
            return [(Intersection([(self.x, self.y)]))]

        indices_in_col = self.__get_sibling_indices__(self.x)
        col = [(self.x,y) for y in indices_in_col ]
        indices_in_row = self.__get_sibling_indices__(self.y)
        row = [(x,self.y) for x in indices_in_row ]

        intersections = [(Intersection(col)), (Intersection(row))]

        if (self.x == self.y):
            logging.debug(f"cell {self} is on left to right (and down) diagonal")
            intersections.append(Intersection(self.__left_to_right_diagonal__()))
        if (self.__max_index__() - self.x == self.y):
            logging.debug(f"cell {self} is on right to left (and down) diagonal")
            intersections.append(Intersection(self.__right_to_left_diagonal__()))

        return intersections


def cell_factory(x, y, max_index):
    return Cell(free_cell_symbol, x, y, max_index)


"""
Represents a human or AIbot player.   The constructor accepts a factory 
for generating this players next move. This enables us to allow a human 
to choose the move (useful for debugging), or delegate this task to an AI bot
"""
class Player:
    def __init__(self, name, goes_first, symbol, move_factory_func, is_internal_player):
        self.name = name
        self.goes_first = goes_first
        self.symbol = str(symbol).lower()
        self.move_factory_func = move_factory_func
        self.is_internal_player = is_internal_player

    def __repr__(self):
        return f"[Player: {self.name}. Goes first?: {self.goes_first}. Symbol: {self.symbol}]"

    def move(self, grid) -> Cell:
        cell =  self.move_factory_func(self, grid)
        logging.debug(f"move selected by {self}. cell: {cell}")
        return cell

    def get_opponent_symbol(self):
        if (self.symbol.lower() == o_symbol):
            return x_symbol
        elif (self.symbol.lower() == x_symbol):
            return o_symbol
        else:
            raise ValueError(f"illegal value for my symbol: {self.symbol}")

"""
A class representing an  MxM 2-D grid structure that stores arbitrary objects.

Attributes:
    max_dimension (int): The number of columns/rows in the grid.
    object_factory (callable): A callable that generates objects for grid cells.

Methods:
    fetch(x, y): Fetches the object at the specified grid coordinates.

Example:
    def random_number_factory():
        return random.randint(1, 100)
    grid = Grid(4, random_number_factory)
    element = grid.fetch(1, 2)
    print(element)  # Print the element at position (1, 2)
"""
class Grid:

    def __init__(self, dimension, object_factory=cell_factory):
        self.num_rows = dimension
        self.num_columns = dimension            # TODO - num_rows/cols not needed
        self.dimension = dimension
        self.object_factory = object_factory
        self.grid = {(x, y): self.object_factory(x, y, self.dimension) for y in range(dimension) for x in range(dimension)}
        self.winner = None


    def __calculate_max_printable_cell_width__(self) -> int:
        max_width = 0
        for y in range(self.dimension):
            for x in range(self.dimension):
                value = self.get_cell(x, y).symbol
                cell_width = len(str(value))
                max_width = max(max_width, cell_width)
        return max_width

    def __validate_coords__(self, x, y):
        if not (0 <= x < self.dimension) or not (0 <= y < self.dimension):
            raise ValueError(f"Coordinates are out of bounds: ({x},{y})")

    def __repr__(self):
        return f"winner: {self.winner}. cells: {self.render_as_string()}"

    def __max_index__(self):
        return self.dimension - 1

    def update_cell(self, cell):
        x = cell.x
        y = cell.y
        self.__validate_coords__( x, y)
        self.grid[(x, y)] = cell


    """
    Renders the state of the game board as a printable string
    """
    def render_as_string(self) -> str:
        cell_width = self.__calculate_max_printable_cell_width__()
        aligned_strings = []
        for y in range(self.dimension):
            row_values = []
            for x in range(self.dimension):
                cell = self.get_cell(x, y)
                row_values.append(str(cell.symbol).rjust(cell_width))
            aligned_strings.append(" ".join(row_values))
        result =  "\n\n".join(aligned_strings)
        #logging.debug(f"grid render result: {result}")
        return result

    def get_winner(self) -> Player:
        return self.winner

    def get_free_cells(self) -> List[Cell]:
        free_cells = []
        for y in range(self.dimension):
            for x in range(self.dimension):
                candidate = self.get_cell(x, y)
                if (candidate.is_free()):
                    free_cells.append(candidate)
        logging.debug(f"Free cells: {free_cells}")
        return free_cells

    """
    Determine if there are any remaining moves on board
    """
    def moves_left(self) -> bool:
        if (self.winner != None):
            logging.debug("Already have a winner")
            return False                # we have a winner, not accepting any more moves
        return self.get_free_cells()  != []


    def is_board_empty(self) -> bool:
        return (len(self.get_free_cells()) == self.dimension * self.dimension)

    def get_cell(self, x, y) -> Cell:
        self.__validate_coords__( x, y)
        return self.grid.get((x, y), None)

    def clear(self):
        self.winner = None
        for x in range(self.dimension):
            for y in range(self.dimension):
                self.update_cell(Cell(free_cell_symbol, x, y, self.dimension))


    """
    Applies the move indicated by the position of the input parameter 'cell' to the grid by creating a copy and 
    updating that copy's corresponding x,y position to point to 'cell'.  The original grid state is not modified.
    The new copy is checked to see if this latest move is a winning move, and is marked accordingly.
    """
    def apply_move(self, cell, player_making_this_move):
        assert self.moves_left()        # shouldn't apply moves if no more available

        new_grid = copy.deepcopy(self)
        new_grid.update_cell(cell)

        if (new_grid.is_winning_move(cell, player_making_this_move)):
            new_grid.winner = cell.symbol                       # Yup - it's a winning move.  mark it !

        logging.debug(f"{player_making_this_move}: SELECTS: {cell}. result -> {new_grid.render_as_string()}")
        return new_grid


    """
        Detects if the move indicated by the position of the input parameter 'cell'  is a winning move.
        This determination is made by examining all columns, rows (and possibly diagonals in 
        the case of a corner cell) that intersect with 'cell'.  If we find any 'intersecting sequence' which 
        contains only one distinct letter for all cells in that sequence we indicate a winning move has been found.
    """
    def is_winning_move(self, cell, player_making_this_move) -> bool:
        def is_cell_owned_by_curr_player(x_y_coords):
            cell = self.get_cell(x_y_coords[0], x_y_coords[1])
            logging.debug(f"result of fetch via coords {x_y_coords}: {cell}")
            return cell.symbol == player_making_this_move.symbol

        def all_cells_owned_by_curr_player(intersection):
            coords = intersection.coords
            result =  all(is_cell_owned_by_curr_player(cell) for cell in coords)
            logging.debug(f"processing intersection: {intersection} yields: {result}")
            return result

        intersections = cell.get_intersections()  # rows, columns, and maybe diagonals that intersect cell
        logging.debug(f"intersections: {intersections}")
        any_intersection_owned = any(all_cells_owned_by_curr_player(intersection) for intersection in intersections)
        logging.debug(f"for cell {cell} any_intersection_owned == {any_intersection_owned}")
        return any_intersection_owned
