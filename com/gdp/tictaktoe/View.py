from com.gdp.tictaktoe import Model

class GridView:
    def __init__(self, grid):
        self.grid = grid

    def calculate_cell_width(self):
        max_width = 0
        for y in range(self.grid.num_rows):
            for x in range(self.grid.num_columns):
                value = self.grid.fetch(x, y)
                cell_width = len(str(value))
                max_width = max(max_width, cell_width)
        return max_width

    def print_aligned(self):
        cell_width = self.calculate_cell_width()
        aligned_strings = []
        for y in range(self.grid.num_rows):
            row_values = []
            for x in range(self.grid.num_columns):
                value = self.grid.fetch(x, y)
                row_values.append(str(value).rjust(cell_width))
            aligned_strings.append(" ".join(row_values))
        return "\n".join(aligned_strings)


class UI:
    def __init__(self):
        pass

    def playerFromUserInput(self):
        player_name = input("Please input player name: ")
        goes_first = input("Do you want to go first? (yes/no): ").lower() == "yes"

        while True:
            symbol = input("Please choose the letter which will represent your moves (either 'X' or 'O'): ").upper()
            if symbol in ['X', 'O']:
                break
            else:
                print("Invalid choice. Please choose 'X' or 'O'.")

        return Model.Player(player_name, goes_first, symbol)


    def gameGridFromUserInput(self):
        while True:
            try:
                num = int(input("How many cells for each row in grid? (pick between 2 and 5): "))
                if 2 <= num <= 5:
                    break
                else:
                    print("Number is not in the range of 2 to 5. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        return Model.Grid(player_name, symbol)







