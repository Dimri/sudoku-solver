import os
import json
import numpy as np

from sudoku import app, ALLOWED_EXTENSIONS
from .sudoku import Sudoku, NROWS
from flask import render_template, request, flash, redirect, url_for, jsonify
from sudoku import puzzles

from werkzeug.utils import secure_filename
from sudoku.image import digit_matrix


def allowed_file(filename):
    """check if the file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def stringit(BOARD):
    """convert board with integer entries to string entries"""
    return [[str(x) for x in row] for row in BOARD]


def is_empty(data):
    """checks if the board submitted was empty"""
    # print(f"data : {data}")
    for key, value in data.items():
        if key in ["solve-btn", "clear-btn"]:
            break
        if value:
            return False
    return True


def is_complete(data):
    """checks if all the sudoku cells were filled"""
    for value in data.values():
        if not value:
            return False
    return True


def str_to_arr(board):
    board = board.replace(" ", "")
    board = board.replace("'", "")
    board = board.replace("[", "")
    board = board.replace("]", "")
    board = board.replace(",", "")
    new_board = []
    for i in range(9):
        row = []
        for j in range(9):
            row.append(board[i * 9 + j])
        new_board.append(row)
    return new_board


def solve(data, board):
    board = str_to_arr(board)
    S = Sudoku(stringit(board))
    # if the data is empty
    # we solve the puzzle using algo
    if is_empty(data):
        S.solve()
        flash(f"Solved!!", category="success")
        # show solved puzzle
        return render_template(
            "solved.html", board=S.board, vals=S.solvals, is_solved=True
        )

    # if data is not empty
    # prompt incomplete puzzle error
    if not is_complete(data):
        flash(f"Please fill all the cells!", category="danger")
        return redirect(url_for("play_page"))

    # if data is complete
    # we check if the puzzle is correct or not
    S.add(data)
    # check for correct solution
    if S.is_valid_solution():
        flash(f"Correct Solution!!", category="success")
        return render_template(
            "solved.html", board=S.board, vals=S.addvals, is_solved=True
        )
    else:
        flash(f"Incorrect Solution! Try again!", category="danger")
        return redirect(url_for("play_page"))


main_puzzle = Sudoku(stringit(puzzles.puzzles_dict["1"]))
last_visited_page = 0  # 1 = upload page, 0 = otherwise


@app.route("/")
def home_page():
    global last_visited_page
    last_visited_page = 0
    return render_template("home.html")


@app.route("/play")
@app.route("/play/<show_puzzle>")
def play_page(show_puzzle=None):
    if show_puzzle:
        puzzle = Sudoku(stringit(str_to_arr(show_puzzle)))
    else:
        puzzle = main_puzzle
    return render_template("index.html", board=puzzle.orig_board)


@app.route("/puzzle/<filename>", methods=["POST"])
def puzzle_page(filename):
    puzzle_from_image = stringit(digit_matrix(app.config["UPLOAD_FOLDER"] + filename))
    puzzle = Sudoku(puzzle_from_image)
    return render_template("index.html", board=puzzle.orig_board, filename=filename)


@app.route("/solution/<board>", methods=["POST"])
def solution_page(board):
    # values submitted by user
    data = request.form
    # pressed 'solve'
    if "solve-btn" in data:
        return solve(data, board)

    # pressed 'clear'
    elif "clear-btn" in data:
        if last_visited_page == 1:
            return redirect(url_for("play_page", show_puzzle=board))
        else:
            return redirect(url_for("play_page"))


@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    global last_visited_page
    last_visited_page = 1
    if request.method != "POST":
        return render_template("uploadfile.html")

    # check if the post request has the file part
    if "file" not in request.files:
        flash("No file part", category="danger")
        return redirect(url_for("upload_page"))

    file = request.files["file"]
    # if user does not select file
    # submit an empty part without filename
    if file.filename == "":
        flash("No selected file", category="danger")
        return redirect(url_for("upload_page"))

    # if file exists and filename is allowed
    # save file locally
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        flash("Image successfully uploaded", category="success")
        return render_template("uploadfile.html", filename=filename)


@app.route("/display/<filename>")
def display_image(filename):
    return redirect(url_for("static", filename="uploads/" + filename), code=301)
