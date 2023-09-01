
import pytest
from com.gdp.tictaktoe import Model



def test_adjoining_cells():
    cell = Model.Cell('X', 0, 0, 3)
    assert cell.get_adjoining_cells() == [[(0, 0), (0, 1), (0, 2)], [(0, 0), (1, 0), (2, 0)], [(0, 0), (1, 1), (2, 2)]]

    cell = Model.Cell('X', 2, 2, 3)
    assert cell.get_adjoining_cells() == [[(2, 0), (2, 1), (2, 2)], [(0, 2), (1, 2), (2, 2)], [(2, 2), (1, 1), (0, 0)]]

    cell = Model.Cell('X', 1, 1, 3)
    assert cell.get_adjoining_cells() == [[(1, 0), (1, 1), (1, 2)], [(0, 1), (1, 1), (2, 1)]]
