import re
from tracemalloc import start

class InvalidInputError(Exception):
    pass

class Sudoku:

    def __init__(self, board):
        self._NROWS = 9
        self._NCOLS = 9

        if self.valid(board):
            self.board = board
        else:
            raise InvalidInputError(f'Given input is not a valid input!')

    def valid(self, board):
        pattern = r'^[0-9\.]$'
        for rows in board:
            for elem in rows:
                if not re.match(pattern, elem):
                    return False

        return True


    def check_row_repeat(self, r : int, c : int) -> bool:
        '''
            function to check if target value repeats in row
            r : target row index
            c : target col index

            returns 'True' if target repeats else 'False'
        '''
        target = self.board[r][c]

        for i in range(self._NROWS):
            # if row is same as target row
            if i == r:
                continue

            # check for target
            if self.board[i][c] == target:
                return True
        
        return False


    def check_col_repeat(self, r : int, c : int) -> bool:
        '''
            function to check if target value repeats in col
            r : target row index
            c : target col index

            returns 'True' if target repeats else 'False'
        '''
        target = self.board[r][c]

        for j in range(self._NCOLS):
            # if column is same as target column
            if j == c:
                continue

            # check for target
            if self.board[r][j] == target:
                return True
        
        return False

    
    def check_block_repeat(self, r : int, c : int) -> bool:
        '''
            function to check if target value repeats in the block
            r : target row index
            c : target col index

            returns 'True' if target repeats else 'False'
        '''
        target = self.board[r][c]

        # starting indices of block
        start_x = (r // 3) * 3
        start_y = (c // 3) * 3

        for i in range(start_x, start_x + 3):
            for j in range(start_y, start_y + 3):
                # if current element indices is same as target indices
                if i == r and j == c:
                    continue

                # check for target
                if self.board[i][j] == target:
                    return True

        return False


    def valid_solution(self):
        
        for i in range(self._NROWS):
            for j in range(self._NCOLS):
                if self.board[i][j] == '.':
                    continue

                # if any of the following is true, solution is not valid    
                if self.check_block_repeat(i,j) or self.check_col_repeat(i,j) or self.check_row_repeat(i,j):
                    return False

        return True