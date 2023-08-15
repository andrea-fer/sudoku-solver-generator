from flask import Flask, render_template

from sudoku import Sudoku
from consistency import ForwardCheck

app = Flask(__name__)

@app.route("/")
def home():
    sudoku = Sudoku()
    sudoku.generate(ForwardCheck(), difficulty = 0.5)
    return render_template("index.html", content = sudoku.board.cells)

if __name__ == "__main__":
    app.run(debug=True)