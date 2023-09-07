
import pytest
import logging

from tictaktoe import Model


@pytest.fixture
def configure_logging():
    # Set up logging configuration before the test
    logging.basicConfig(level=logging.DEBUG)  # Set the desired log level
    yield
    # Clean up logging configuration after the test (if needed)


def test_intersections(configure_logging):
    cell = Model.Cell('X', 0, 0, 3)                          # cell on diagonal -- in uppermost left-most position
    intersections = cell.get_intersections()
    assert intersections == \
           [
               Model.Intersection([(0, 1), (0, 0), (0, 2)]), # Down. (check order irrelevant for Intersection c-tor)
               Model.Intersection([(0, 0), (1, 0), (2, 0)]), # Across.
               Model.Intersection([(0, 0), (1, 1), (2, 2)])  # Left to right and down diagonal.
           ]

    cell = Model.Cell('X', 2, 2, 3)                          # cell on diagonal -- in lowermost right-most position
    assert cell.get_intersections() == \
           [
               Model.Intersection([(2, 0), (2, 1), (2, 2)]),
               Model.Intersection([(0, 2), (1, 2), (2, 2)]),
               Model.Intersection([(2, 2), (1, 1), (0, 0)])  # Left to right and down diagonal (coord order flipped)
           ]

    cell = Model.Cell('X', 1, 1, 3)             # test case of center cell - has two diagonal intersections, not just 1
    assert cell.get_intersections() == \
           [
               Model.Intersection([(1, 0), (1, 1), (1, 2)]),
               Model.Intersection([(0, 1), (1, 1), (2, 1)]),
               Model.Intersection([(0, 0), (1, 1), (2, 2)]), # Left to right and down diagonal.
               Model.Intersection([(2, 0), (1, 1), (0, 2)])  # Right to left and down diagonal
           ]

    cell = Model.Cell('X', 0, 1, 3)             # test non-diagonal cell: should only have row and column intersections
    assert cell.get_intersections() == \
           [
               Model.Intersection([(0, 0), (0, 1), (0, 2)]),    # column intersection
               Model.Intersection([(0, 1), (1, 1), (2, 1)])  # row intersection
           ]


def test_know_when_to_block_diag(configure_logging): # recognize need to apply blocking move if about to lose (diagonal)
    player1 = Model.Player("one", True, 'o', None, True)
    grid = Model.Grid(3)

    center_cell = Model.Cell('o', 1, 1, 3)

    # player 1 will win on diagonal in next move
    grid.update_cell(Model.Cell('o',2,1,3))
    grid.update_cell(Model.Cell('x',0,0,3))
    grid.update_cell(center_cell)

    print("THE GRID")
    print(grid.render_as_string())

    intersections = center_cell.get_intersections()
    blocker = None
    for i in intersections:
        logging.info(f"checking intersection for blocker: {i}")
        blocker = i.cell_to_block_opponent_win(player1, grid)
        if (blocker != None):
            logging.info(f"found blocking cell ${blocker} with in intersection: ${i}")
            break

    assert blocker.x == 0 and blocker.y == 1



def test_empty_grid(configure_logging):
    grid = Model.Grid(3)

    assert(grid.is_board_empty())

    grid.update_cell(Model.Cell('x',2,1,3))
    assert(not grid.is_board_empty())

