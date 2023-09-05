
import pytest
import logging

from tictaktoe import Model
from tictaktoe import AiBot


@pytest.fixture
def configure_logging():
    # Set up logging configuration before the test
    logging.basicConfig(level=logging.DEBUG)  # Set the desired log level
    yield
    # Clean up logging configuration after the test (if needed)


def test_adjoining_cells(configure_logging):
    player1 = Model.Player("one", True, 'x', None, True)
    player2 = Model.Player("two", False, 'o', None, False)
    grid = Model.Grid(2)
    game_outcomes = AiBot.AiNextMoveFactory().all_game_outcomes(grid, player2, 0, [])
    assert(len(game_outcomes) == 4 * 3 * 2 * 1)   # number of outcomes for cell grid is 4!
    assert all(grid.winner == player1.symbol for grid in game_outcomes)
