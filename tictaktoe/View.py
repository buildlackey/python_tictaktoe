import re
import logging

from tictaktoe import Model

"""
Renders the state of the game board as a printable string
"""
class GridView:
    def __init__(self):
        pass

    def __calculate_cell_width__(self, grid):
        max_width = 0
        for y in range(grid.num_rows):
            for x in range(grid.num_columns):
                value = grid.fetch_cell(x, y)
                cell_width = len(str(value))
                max_width = max(max_width, cell_width)
        return max_width

    def render_as_string(self, grid):
        cell_width = self.__calculate_cell_width__(grid)
        aligned_strings = []
        for y in range(grid.num_rows):
            row_values = []
            for x in range(grid.num_columns):
                cell = grid.fetch_cell(x, y)
                row_values.append(str(cell).rjust(cell_width))
            aligned_strings.append(" ".join(row_values))
        return "\n\n".join(aligned_strings)

"""
This class is responsible for acquiring user input, displaying the game baord, and the status of the
game (announcing winning players, or draws, etc).
"""
class UI:
    def __init__(self):
        self.grid_view = GridView()

    def get_grid_view(self):
        return self.grid_view

    def announce_winner(self, grid):
        if grid.get_winner:
            print(f"\nGame has been won by player who wisely chose '{grid.winner}'. Congratulations!\n")
        else:
            print(f"\nGame resulted in a draw\n")
        self.display_game_grid(grid)

    def get_user_input(self, prompt, input_validator):
        while True:
            response = input(prompt).upper()
            if input_validator(response):
                break
            else:
                print(prompt)

        return response

    def get_restricted_input(self, prompt, valid_responses):
        def validator(string):
            return string in valid_responses
        return self.get_user_input(prompt, validator)

    def get_nonnull_input(self, prompt):
        def validator(string):
            return len(string) >  0
        return self.get_user_input(prompt, validator)

    def get_users_yes_no_response(self, prompt):
        def y_n_validator(string):
            return (str(string).upper() == 'Y' or str(string).upper() == 'N')

        return self.get_user_input(prompt, y_n_validator)



    def player_from_user_input(self, next_move_factory):
        player_name = self.get_nonnull_input("Please input player name: ")
        goes_first = self.get_restricted_input("Do you want to go first? (Y/N): ", ["Y", "N"])
        symbol = self.get_restricted_input("Please choose letter representing your moves ('X' or 'O'): ", ["X", "O"])
        return Model.Player(player_name, goes_first.upper() == 'Y', symbol, next_move_factory)



    def game_grid_from_user_input(self):
        def check_bounds(value):
            try:
                as_int = int(value)
                return 2 <= as_int and as_int <= 5
            except ValueError:
                return False

        max_index = self.get_user_input("How many cells for each row in grid? (pick between 2 and 5): ", check_bounds)
        return Model.Grid(int(max_index))

    def display_game_grid(self, grid):
        print(f"\n{self.grid_view.render_as_string(grid)}")

    def update_grid_with_player_move(self, grid: Model.Grid, player: Model.Player):
        """
        Prompts a player to enter the coordinates of their next move, and updates 'grid' to
        player's chosen letter ('X' or 'O').  Detects if this move is a winning move by
        examining all columns, rows (and possibly diagonals in the case of a corner cell) to
        check if any one contains only one distinct letter for all cells in the examined sequence.

        Args:
            grid:  the grid to update
            player: the player making the move.  If this is a winning move, said player may be declared winner
                    (by updating state in the grid that tracks if someone has already won)

        Returns:

        """
        def parse_input(input_str):
            # Define a regular expression pattern to match two integers separated by non-numeric characters
            pattern = r'[^0-9]*([0-9]+)[^0-9]+([0-9]+)[^0-9]*'

            match = re.match(pattern, input_str)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                if (x >= 0 and x < grid.max_index and y >= 0 and y < grid.max_index):
                    if grid.fetch_cell(x, y).symbol == '_':
                        return [x, y]
            return None

        def get_coords(string_input):
            return parse_input(string_input) is not None


        msg = f"\nYour move, {player.name},  Enter x,y coordinates of free cell (each coord > 0 and < {grid.max_index}): "
        input = self.get_user_input(msg, get_coords)
        coords = parse_input(input)
        logging.debug(f"coords: {coords}")

        cell = Model.Cell(player.symbol, coords[0], coords[1], grid.max_index)
        grid.update_cell(coords[0], coords[1], cell)
        if (grid.is_winning_move(cell, player)):
            grid.winner = cell.symbol