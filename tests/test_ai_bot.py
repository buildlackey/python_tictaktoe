
import pytest
import logging

from tictaktoe import Model
from tictaktoe import AiBot


@pytest.fixture
def configure_logging():
    # Set up logging configuration before the test
    logging.basicConfig(level=logging.INFO)  # Set the desired log level
    yield
    # Clean up logging configuration after the test (if needed)


def test_on_2by2_grid(configure_logging):
    player1 = Model.Player("one", True, 'x', None, True)
    player2 = Model.Player("two", False, 'o', None, False)
    grid = Model.Grid(2)

    next_move_factory = AiBot.AiNextMoveFactory()
    next_move_factory.set_players(player1, player2)
    game_outcomes = next_move_factory.all_game_outcomes(grid, player1, 0, [])

    assert(len(game_outcomes) == 4 * 3 * 2 * 1)   # number of outcomes for cell grid is 4!
    assert all(outcome.grid.winner == player1.symbol for outcome in game_outcomes)





def test_more(configure_logging):
    player1 = Model.Player("one", True, 'x', None, False)
    player2 = Model.Player("two", False, 'o', None, True)
    grid = Model.Grid(3)

    next_move_factory = AiBot.AiNextMoveFactory()
    next_move_factory.set_players(player1, player2)

    # 9! outcomes make the test run a little too slow... So occupy some board position to reduce the search space
    grid.update_cell(Model.Cell('x',1,1,3))

    print("THE GRID")
    print(grid.render_as_string())
    print("THE GRID")

    game_outcomes = next_move_factory.all_game_outcomes(grid, player1, 1, [])
    assert any(x.score == 1 and x.grid.winner == 'x' for x in game_outcomes)
    print(f"game_outcomes: {game_outcomes}")


def test_3by3_get_all_expected_outcomes(configure_logging):
    player1 = Model.Player("one", True, 'x', None, True)
    player2 = Model.Player("two", False, 'o', None, False)
    grid = Model.Grid(3)

    next_move_factory = AiBot.AiNextMoveFactory()
    next_move_factory.set_players(player1, player2)

    # 9! outcomes make the test run a little too slow... So occupy some board position to reduce the search space
    grid.update_cell(Model.Cell('x',2,1,3))
    grid.update_cell(Model.Cell('o',2,0,3))
    grid.update_cell(Model.Cell('o',0,1,3))

    print("THE GRID")
    print(grid.render_as_string())
    print("THE GRID")

    game_outcomes = next_move_factory.all_game_outcomes(grid, player1, 0, [])
    assert any(x.score == 1 and x.grid.winner == 'x' for x in game_outcomes)
    print(f"game_outcomes: {game_outcomes}")



def test_can_get_best_and_only_move_from_1by1_grid(configure_logging):

    next_move_factory = AiBot.AiNextMoveFactory()

    def next_move_from_ai_bot(player: Model.Player, grid: Model.Grid):  # next move factory using machine intelligence
        return next_move_factory.get_move(grid, player)

    player1 = Model.Player("one", True, 'x', next_move_from_ai_bot, True)
    player2 = Model.Player("two", False, 'o', next_move_from_ai_bot, False)
    grid = Model.Grid(1)

    next_move_factory.set_players(player1, player2)
    selected_move = player1.move(grid)
    assert(selected_move.symbol == 'x' and selected_move.x == 0 and selected_move.y == 0)
