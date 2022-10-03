from sudoku import app
from .sudoku import Sudoku, NROWS
from flask import render_template, request, flash, redirect, url_for
from sudoku import puzzles

SIZE = NROWS
CURRENT_PUZZLE = puzzles.PUZZLES['2']

@app.route('/')
def home_page():
    return render_template('index.html', board=stringit(CURRENT_PUZZLE))


@app.route('/solution', methods=['POST'])
def solution_page():

    # values submitted by user
    data = request.form
    print(data)

    # if user pressed 'solve'
    if 'solve-btn' in data:

        # if user entered data 
        if not is_empty(data):

            # if data is complete 
            if is_complete(data):

                # full board (user + puzzle)
                board = stringit(CURRENT_PUZZLE)
                S = Sudoku(board)
                S.add(data)

                # check for correct solution
                if S.is_valid_solution():
                    flash(f'Correct Solution!!', category='success')
                    return render_template('solved.html', board=S.board, vals=S.addvals)
                else:
                    flash(f'Incorrect Solution! Try again!', category='danger')
                    return redirect(url_for('home_page'))

            # if data is incomplete
            else:
                flash(f'Please fill all the cells!', category='danger')
                return redirect(url_for('home_page'))
                
        # no data entered
        else:
            S = Sudoku(stringit(CURRENT_PUZZLE))
            S.solve()
            return render_template('solved.html', board=S.board, vals=S.solvals)
    

    # if user pressed 'clear'
    elif 'clear-btn' in data:
        return redirect(url_for('home_page'))
    


def stringit(BOARD : list[list[int]]) -> list[list[str]]:
    STR_BOARD = [[str(x) for x in row] for row in BOARD]
    return STR_BOARD


def is_empty(data):
    for key, value in data.items():
        if key in ['solve-btn', 'clear-btn']:
            break
        if value != '':
            return False
    return True

def is_complete(data):
    for value in data.values():
        if value == '':
            return False
    return True