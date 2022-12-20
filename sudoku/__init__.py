import os
from flask import Flask

app = Flask(__name__)

UPLOAD_FOLDER = 'sudoku/static/uploads/'
ALLOWED_EXTENSIONS = set(["png", "jpeg", "jpg"])

app.config["MAX_CONTENT_LENGTH"] = (
    16 * 1024 * 1024
)  # allow only 16MB or less size files
app.config["SECRET_KEY"] = "2fdfb5d074cf5056108bb0fc"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

from sudoku import views
