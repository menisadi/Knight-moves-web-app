import chess
import numpy as np
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Variable to keep track of the last clicked square
last_clicked_square = None
last_square_was_toggled = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/square_click", methods=["POST"])
def square_click():
    global last_clicked_square, last_square_was_toggled
    data = request.get_json()
    print("Received JSON data:", data)
    col = data["col"]
    row = data["row"]
    square = chess.square(col, row)

    if 0 <= col < 8 and 0 <= row < 8:
        if square == last_clicked_square and last_square_was_toggled:
            # If the same square is clicked again and it was toggled, reset to black and white
            last_square_was_toggled = False
            return jsonify({"reset": True})
        else:
            distances_from_square = how_the_knight_move(square)
            last_clicked_square = square
            last_square_was_toggled = True
            return jsonify({"distances": distances_from_square.tolist()})
    else:
        return jsonify({"error": "Invalid Square"})


def how_the_knight_move(square1):
    distances = np.zeros((8, 8))
    for square2 in chess.SQUARES:
        distances[
            7 - chess.square_rank(square2), chess.square_file(square2)
        ] = chess.square_knight_distance(square1, square2)
    return distances


if __name__ == "__main__":
    app.run(debug=True)
