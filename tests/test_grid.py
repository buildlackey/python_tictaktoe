
import pytest
from com.gdp.tictaktoe import Model
from com.gdp.tictaktoe import View


def test_grid_with_simple_cell_creation_factory():
    # Define a constant object factory that returns 1
    def sum_factory(x, y, dummy):
        return x+y

    # Create a 3x3 grid with the constant object factory
    grid = Model.Grid(3, sum_factory)

    # Iterate over all cells, fetching values and adding them to the total
    total = 0
    for y in range(3):
        for x in range(3):
            total += grid.fetch_cell(x, y)
    assert total == 18


def test_out_of_bounds_cell_reference():
    def constant_factory(x, y, dummy):
        return 1

    with pytest.raises(ValueError) as e:
        grid = Model.Grid(3, constant_factory)
        grid.fetch_cell(3, 4)
    assert "Coordinates are out of bounds: (3,4)" in str(e.value)

def test_grid_view():
    def times_factory(x,y, dummy):
        return x*y*3            # x 3 to get a mix of cell display lenghts to better test alignment

    # Create a 3x3 grid with the constant object factory
    grid = Model.Grid(3, times_factory)
    string_representation = View.GridView().render_as_string(grid)
    expected = " 0  0  0\n\n 0  3  6\n\n 0  6 12"
    assert string_representation == expected

