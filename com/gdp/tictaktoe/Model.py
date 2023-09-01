import random
class Player:
    def __init__(self, name, goes_first, symbol):
        self.name = name
        self.goes_first = goes_first
        self.symbol = symbol

    def display(self):
        return f"Player: {self.name}. Goes first?: {self.goes_first}. Symbol: {self.symbol}"


class Cell:
    def __init__(self, symbol, x, y, grid_size):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.grid_size = grid_size

    def __str__(self):
        return f"Cell ({self.x},{self.y}): {self.symbol}"

    """
    Given a horizontal or vertical index position, return all the other indices in the row or column
    """
    def __get_sibling_indices__(self, index):
        return [i for i in range(self.grid_size) ]

    def __get_adjacent_cells_in_diagonal_for_dimension__(self,  dim):
        coords = [i for i in range(self.grid_size)]
        if (dim > 0):
            coords.reverse()
        print(f"__get_adjacent_cells_in_diagonal_for_dimension__ cell: {self}: dim: {dim}. result: {coords}")
        return coords

    def __get_adjacent_cells_in_diagonal(self):
        x_coords_for_adjacents = self.__get_adjacent_cells_in_diagonal_for_dimension__(self.x)
        y_coords_for_adjacents = self.__get_adjacent_cells_in_diagonal_for_dimension__(self.y)
        retval = list(zip(x_coords_for_adjacents, y_coords_for_adjacents))
        print(f"__get_adjacent_cells_in_diagonal cell: {self}: {retval}")
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
            print(f"Cell {self} identified as corner cell")
            adjoining_cells.append(self.__get_adjacent_cells_in_diagonal())


        return adjoining_cells



def cell_factory(x,y):
    return Cell('_', x, y)

class Grid:

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

    def __init__(self, max_index, object_factory=cell_factory):
        self.num_rows = max_index
        self.num_columns = max_index
        self.max_index = max_index
        self.object_factory = object_factory
        self.grid = {(x, y): self.object_factory(x,y) for y in range(max_index) for x in range(max_index)}

    def fetch(self, x, y):
        if not (0 <= x < self.max_index) or not (0 <= y < self.max_index):
            raise ValueError(f"Coordinates are out of bounds: ({x},{y})")
        return self.grid.get((x, y), None)


