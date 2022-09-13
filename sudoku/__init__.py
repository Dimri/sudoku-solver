from flask import Flask

app = Flask(__name__)

from sudoku import views
