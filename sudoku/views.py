import os

from sudoku import app, ALLOWED_EXTENSIONS
from .sudoku import Sudoku, NROWS
from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
)
from sudoku import puzzles

from werkzeug.utils import secure_filename
from sudoku.image import digit_matrix

SIZE = NROWS
PUZZLE = puzzles.PUZZLES["2"]


@app.route("/")
def home_page():
    return render_template("home.html", board=stringit(PUZZLE))


@app.route("/play")
def play_page():
    return render_template("index.html", board=stringit(PUZZLE))


@app.route("/puzzle/<filename>", methods=["POST"])
def puzzle_page(filename):
    PUZZLE = stringit(digit_matrix(app.config["UPLOAD_FOLDER"] + filename))
    return render_template("index.html", board=PUZZLE)


@app.route("/solution", methods=["POST"])
def solution_page():
    # values submitted by user
    data = request.form
    # pressed 'solve'
    if "solve-btn" in data:
        return solve(data)

    # pressed 'clear'
    elif "clear-btn" in data:
        return redirect(url_for("home_page"))


@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    if request.method != "POST":
        return render_template("uploadfile.html")

    # check if the post request has the file part
    if "file" not in request.files:
        flash("No file part", category="danger")
        return redirect(url_for("upload_page"))

    file = request.files["file"]
    # if user does not select file
    # submit a empty part without filename
    if file.filename == "":
        flash("No selected file", category="danger")
        return redirect(url_for("upload_page"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        flash("Image successfully uploaded", category="success")
        return render_template("uploadfile.html", filename=filename)


@app.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for("static", filename="uploads/" + filename), code=301)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def stringit(BOARD):
    return [[str(x) for x in row] for row in BOARD]


def is_empty(data):
    for key, value in data.items():
        if key in ["solve-btn", "clear-btn"]:
            break
        if value:
            return False
    return True


def is_complete(data):
    for value in data.values():
        if not value:
            return False
    return True


def solve(data):
    # if the data is empty
    if is_empty(data):
        S = Sudoku(stringit(PUZZLE))
        S.solve()
        flash(f"Solved!!", category="success")
        return render_template("solved.html", board=S.board, vals=S.solvals)

    # if data is not empty
    if not is_complete(data):
        flash(f"Please fill all the cells!", category="danger")
        return redirect(url_for("home_page"))

    # if data is complete
    S = Sudoku(stringit(PUZZLE))
    S.add(data)

    # check for correct solution
    if S.is_valid_solution():
        flash(f"Correct Solution!!", category="success")
        return render_template("solved.html", board=S.board, vals=S.addvals)
    else:
        flash(f"Incorrect Solution! Try again!", category="danger")
        return redirect(url_for("home_page"))
