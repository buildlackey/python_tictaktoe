
import pytest
import logging

from tictaktoe import Model


@pytest.fixture
def configure_logging():
    # Set up logging configuration before the test
    logging.basicConfig(level=logging.DEBUG)  # Set the desired log level
    yield
    # Clean up logging configuration after the test (if needed)


def test_adjoining_cells(configure_logging):
    cell = Model.Cell('X', 0, 0, 3)
    assert cell.get_adjoining_cells() == [[(0, 0), (0, 1), (0, 2)], [(0, 0), (1, 0), (2, 0)], [(0, 0), (1, 1), (2, 2)]]

    cell = Model.Cell('X', 2, 2, 3)
    assert cell.get_adjoining_cells() == [[(2, 0), (2, 1), (2, 2)], [(0, 2), (1, 2), (2, 2)], [(2, 2), (1, 1), (0, 0)]]

    cell = Model.Cell('X', 1, 1, 3)
    assert cell.get_adjoining_cells() == [[(1, 0), (1, 1), (1, 2)], [(0, 1), (1, 1), (2, 1)], [(2, 2), (1, 1), (0, 0)]]



def test_empty_grid(configure_logging):
    grid = Model.Grid(3)

    assert(grid.is_board_empty())

    grid.update_cell(Model.Cell('x',2,1,3))
    assert(not grid.is_board_empty())
