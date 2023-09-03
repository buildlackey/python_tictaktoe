
import pytest
import logging

from com.gdp.tictaktoe import Controller
from com.gdp.tictaktoe import View



def test_main_program(monkeypatch):
    responses = ["2", "joe", "y", "o", "0 0", "1 1", "0 1", "n"]

    def mock_input(prompt):
        nonlocal responses
        response = responses.pop(0)
        return response

    # Monkeypatch the input function with the mock_input function
    monkeypatch.setattr('builtins.input', mock_input)

    controller = Controller.GameSessionController()
    controller.start()

    grid = controller.get_grid()
    assert(grid.winner == 'o')

    grid_as_string = View.UI().grid_view.render_as_string(grid)
    assert grid_as_string == "o _\n\no x"
