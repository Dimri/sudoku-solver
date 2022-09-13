import re

class InvalidInputError(Exception):
    pass

class Sudoku:

    def __init__(self, board):
        self._NROWS = 9
        self._NCOLS = 9

        if self.valid(board):
            self.board = board
        else:
            raise InvalidInputError(f'{board} is not a valid input!')

    def valid(self, board):
        pattern = r'^[0-9\.]$'
        for rows in board:
            for elem in rows:
                if not re.match(pattern, elem):
                    return False

        return True

