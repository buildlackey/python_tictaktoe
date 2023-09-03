import logging
import copy


"""
Represents a human or AIbot player.   The constructor accepts a factory 
for generating this players next move. This enables us to allow a human 
to choose the move, or delegate this task to an AI bot
"""
class Player:
    def __init__(self, name, goes_first, symbol, move_factory_func):
        self.name = name
        self.goes_first = goes_first
        self.symbol = str(symbol).lower()
        self.gen_move_factory_func = move_factory_func

    def __str__(self):
        return f"Player: {self.name}. Goes first?: {self.goes_first}. Symbol: {self.symbol}"

    def move(self, grid):
        cell =  self.gen_move_factory_func(self, grid)
        logging.debug(f"moving to cell: {cell}")
        return cell


class Cell:
    def __init__(self, symbol, x, y, grid_size):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.grid_size = grid_size

    def __str__(self):
        return f"{self.symbol}"

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

    """
    Given a 'non corner' cell, this method returns two sequences of adjacent cells, one sequence for the 
    row that subsumes this cell, and another for the subsuming column.   If this is a 'corner cell' (e.g., 
    the cell at (0,0) could be considered to occupy the upper left 'corner' of the grid)  then 
    this method's return value will additionally include the sequence of cells that comprise the diagonal that
    subsumes this corner cell.
    """
    def get_adjoining_cells(self):
        other_indices_in_col = self.__get_sibling_indices__(self.x)
        col = [(self.x,y) for y in other_indices_in_col ]

        other_indices_in_row = self.__get_sibling_indices__(self.y)
        row = [(x,self.y) for x in other_indices_in_row ]

        adjoining_cells = [col, row]

        if (self.x % (self.grid_size - 1) == 0 and self.y % (self.grid_size - 1) == 0):
            logging.debug(f"Cell {self} identified as corner cell")
            adjoining_cells.append(self.__get_adjacent_cells_in_diagonal())

        return adjoining_cells



def cell_factory(x, y, max_index):
    return Cell('_', x, y, max_index)


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

    def __init__(self, max_index, object_factory=cell_factory):
        self.num_rows = max_index
        self.num_columns = max_index            # TODO - num_rows/cols not needed
        self.max_index = max_index
        self.object_factory = object_factory
        self.grid = {(x, y): self.object_factory(x,y,self.max_index) for y in range(max_index) for x in range(max_index)}
        self.winner = None


    def get_winner(self) -> Player:
        return self.winner


    def __validate_coords__(self, x, y):
        if not (0 <= x < self.max_index) or not (0 <= y < self.max_index):
            raise ValueError(f"Coordinates are out of bounds: ({x},{y})")

    """
    Determine if there are any remaining moves on board
    """
    def moves_left(self):
        if (self.winner != None):
            logging.debug("Already have a winner")
            return False                # we have a winner, not accepting any more moves
        remaining = False
        for x in range(self.max_index):
            for y in range(self.max_index):
                cell = self.fetch_cell(x, y)
                if cell.symbol == '_':
                    logging.debug(f"cell at ({x},{y}) is {cell.symbol}")
                    remaining = True
        return remaining

    def update_cell(self, cell):
        x = cell.x
        y = cell.y
        self.__validate_coords__( x, y)
        self.grid[(x, y)] = cell


    def fetch_cell(self, x, y) -> Cell:
        self.__validate_coords__( x, y)
        return self.grid.get((x, y), None)

    def clear(self):
        self.winner = None
        for x in range(self.max_index):
            for y in range(self.max_index):
                self.update_cell(Cell('_', x, y, self.max_index))


    """
    Applies the move indicated by the position of the input parameter 'cell' to the grid by creating a copy and 
    updating that copies corresponding x,y position to point to 'cell'.  The original grid state is not modified.
    The new copy is checked to see if this latest move is a winning move, and is marked accordingly.
    """
    def apply_move(self, cell, player_making_this_move):
        assert self.moves_left()        # shouldn't apply moves if no more available

        new_grid = copy.deepcopy(self)
        new_grid.update_cell(cell)

        if (new_grid.is_winning_move(cell, player_making_this_move)):
            new_grid.winner = cell.symbol                       # Yup - it's a winning move.  mark it !

        return new_grid


    """
        Detects if the move indicated by the position of the input parameter 'cell'  is a winning move.
        This determination is made by examining all columns, rows (and possibly diagonals in 
        the case of a corner cell) that intersect with 'cell'.  If we find any 'intersecting sequence' which 
        contains only one distinct letter for all cells in that sequence we indicate a winning move has been found.
    """
    def is_winning_move(self, cell, player_making_this_move):
        def is_cell_owned_by_curr_player(x_y_coords):
            cell = self.fetch_cell(x_y_coords[0], x_y_coords[1])
            logging.debug(f"fetched from coords {x_y_coords}: {cell}")
            return cell.symbol == player_making_this_move.symbol

        def all_cells_owned_by_curr_player(cell_coordinates_sequence):
            result =  all(is_cell_owned_by_curr_player(cell) for cell in cell_coordinates_sequence)
            logging.debug(f"processing intersection: {cell_coordinates_sequence} yields: {result}")
            return result

        intersections = cell.get_adjoining_cells()  # rows, columns, and maybe diagonals that intersect cell
        logging.debug(f"intersections: {intersections}")
        any_intersection_owned = any(all_cells_owned_by_curr_player(cell_coord_seq) for cell_coord_seq in intersections)
        logging.debug(f"for cell {cell} any_intersection_owned == {any_intersection_owned}")
        return any_intersection_owned
