from flask import Flask, render_template, jsonify, request

from sudoku import Sudoku
from consistency import ForwardCheck

app = Flask(__name__)

sudoku = Sudoku()

@app.route("/")
def home():
    global sudoku
    sudoku = Sudoku()
    sudoku.generate(ForwardCheck(), difficulty = 0.03)
    return render_template("index.html", content = sudoku.board.cells)

@app.route('/new_board', methods=['GET'])
def new_board():
    global sudoku
    data = [ [0] * 9 for i in range(9) ]
    for i in range(9):
        for j in range(9):
            data[i][j] = sudoku.board.cells[i][j].value

    json_data = jsonify(data)
    
    return json_data

@app.route('/player_board', methods=['POST'])
def receive_data():
    board = request.json

    global sudoku
    for i in range(9):
        for j in range(9):
            sudoku.board.cells[i][j].value = board[i][j]

    response = {'status': sudoku.is_solved()}
    
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)