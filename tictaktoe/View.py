import re
import logging

from tictaktoe import Model


"""
Acquires user input, writes current state of game board to console, and annouces the status of the
game (announcing winning plays, draws, etc).
"""
class UI:
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
        return Model.Player(player_name, goes_first.upper() == 'Y', symbol, next_move_factory, False)



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
        print(f"\nGame Board:\n{grid.render_as_string()}")

    """
    Prompts player to enter the coordinates of a free cell where they wish to make their next move,

    Args:
        grid:  the grid where the move needs to be chosen
        player: the player making the move.

    Invariants:  the game grid must have available moves, and no established winner

    Returns: The cell with player's chosen coordinates.
    """
    def prompt_for_coords_of_next_move(self, grid: Model.Grid, player: Model.Player):
        def parse_input(input_str):
            # Define a regular expression pattern to match two integers separated by non-numeric characters
            pattern = r'[^0-9]*([0-9]+)[^0-9]+([0-9]+)[^0-9]*'

            match = re.match(pattern, input_str)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                if (x >= 0 and x < grid.dimension and y >= 0 and y < grid.dimension):
                    if grid.get_cell(x, y).is_free():
                        return [x, y]
            return None

        def get_coords(string_input):
            return parse_input(string_input) is not None


        assert grid.moves_left()

        msg = f"\nYour move, {player.name},  Enter x,y coordinates of free cell (each coord > 0 and < {grid.dimension}): "
        input = self.get_user_input(msg, get_coords)
        coords = parse_input(input)
        logging.debug(f"for next move position, human player {player} selected coords: {coords}")

        cell = Model.Cell(player.symbol, coords[0], coords[1], grid.dimension)
        return cell

    def announce_internal_player_move(self, player, cell, human_mode):
        if (human_mode or not player.is_internal_player):      #  if a human selected move then don't need a reminder
            return
        else:
            print(f"\nPlayer {player.name} selected cell at ({cell.x},{cell.y}) for next move")
