from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = '2fdfb5d074cf5056108bb0fc'

from sudoku import views
