from flask import Flask
from sudoku import app

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')