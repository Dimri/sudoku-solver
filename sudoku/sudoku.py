import re

NROWS = 9


class InvalidInputError(Exception):
    pass


class Sudoku:
    def __init__(self, board):
        self.ROWS = NROWS
        self.COLS = NROWS
        self.solvals = set()
        self.addvals = set()
        if self.valid_board(board):
            self.board = board
        else:
            raise InvalidInputError(f"Given input is not a valid input!")

    def valid_board(self, board):
        pattern = r"^[0-9]$"
        for rows in board:
            for elem in rows:
                if not re.match(pattern, elem):
                    return False

        return True

    def is_valid(self, target: str, pos: tuple) -> bool:

        # check row
        for i in range(self.COLS):
            if self.board[pos[0]][i] == target and pos[1] != i:
                return False

        # check col
        for i in range(self.ROWS):
            if self.board[i][pos[1]] == target and pos[0] != i:
                return False

        # check block
        block_x = pos[0] // 3
        block_y = pos[1] // 3

        for i in range(block_x * 3, block_x * 3 + 3):
            for j in range(block_y * 3, block_y * 3 + 3):
                if self.board[i][j] == target and (i, j) != pos:
                    return False

        return True

    def is_valid_solution(self) -> bool:
        for i in range(self.ROWS):
            for j in range(self.COLS):
                target = self.board[i][j]
                pos = (i, j)
                if not self.is_valid(target, pos):
                    return False

        return True

    def solve(self) -> bool:
        empty_cell = self.find_empty()

        if not empty_cell:
            return True
        else:
            row, col = empty_cell

        for i in range(1, self.ROWS + 1):

            if self.is_valid(str(i), empty_cell):
                self.board[row][col] = str(i)
                self.solvals.add((row, col))
                if self.solve():
                    return True

                self.board[row][col] = "0"
                self.solvals.remove((row, col))

        return False

    def find_empty(self):
        """
        function to find the first empty cell
        """
        for i in range(self.ROWS):
            for j in range(self.COLS):
                if self.board[i][j] == "0":
                    return (i, j)

        # if the board is full
        return None

    def print_board(self):
        print("\n" * 2)
        for i, row in enumerate(self.board):
            if i % 3 == 0:
                print("-" * 22)
            for j, col in enumerate(row):
                if j % 3 == 0:
                    print("|", end="")
                print(col, end=" ")
            print("|")
        print("\n" * 2)

    def add(self, data):
        """
        function to add user inserted data to board
        """
        for key, value in data.items():
            if key in ["solve-btn", "clear-btn"]:
                break
            idx = int(key.split("-")[1])

            rowidx = idx // self.ROWS
            colidx = idx % self.ROWS
            self.board[rowidx][colidx] = value
            self.addvals.add((rowidx, colidx))
