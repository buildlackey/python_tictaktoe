from com.gdp.tictaktoe import Model


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
                value = grid.fetch_cell(x, y)
                row_values.append(str(value).rjust(cell_width))
            aligned_strings.append(" ".join(row_values))
        return "\n".join(aligned_strings)


class UI:
    def __init__(self):
        self.grid_view = GridView()

    def get_restricted_input(self, prompt, valid_responses):
        while True:
            response = input(prompt).upper()
            if response in valid_responses:
                break
            else:
                print(f"Invalid choice. Please choose one of: {str(valid_responses)}")

    def get_nonnull_input(self, prompt):
        while True:
            response = input(prompt).upper()
            if len(response) > 0:
                break
            else:
                print(prompt)


    def player_from_user_input(self):
        player_name = self.get_nonnull_input("Please input player name: ")
        goes_first = self.get_restricted_input("Do you want to go first? (yes/no): ", ["Y", "N"])
        symbol = self.get_restricted_input("Please choose letter representing your moves ('X' or 'O'): ", ["X", "O"])
        return Model.Player(player_name, goes_first, symbol)

    def game_grid_from_user_input(self):
        while True:
            try:
                max_index = int(input("How many cells for each row in grid? (pick between 2 and 5): "))
                if 2 <= max_index <= 5:
                    break
                else:
                    print("Number is not in the range of 2 to 5. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        return Model.Grid(max_index)

    def display_game_grid(self, grid):
        print(f"\n{self.grid_view.render_as_string(grid)}")
