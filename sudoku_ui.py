from tkinter import *
from tkinter.font import *
from tkinter import messagebox

from sudoku import Sudoku
from consistency import ForwardCheck   
from board_export import txt_exporter

root = Tk()
root.title('Sudoku')

sudoku = Sudoku()

# selected number
global selected
global btn_cells

class BTN(Button):
    xy: list[int]
    value: int

    def select(self) -> None:
        global selected
        self['bg'] = '#1e738f'
        self['activebackground'] = '#185a70'
        if selected != None:
            selected['bg'] = 'white'
            selected['activebackground'] = '#e3e3e3'
        selected = self
        selected['bg'] = '#1e738f'
        selected['activebackground'] = '#185a70'
        selected.value = 1
        self.update_btns()
    
    def update(self) -> None:
        global selected
        if selected == None:
            return
        if selected.value == 0:
            self['text'] = " "
            sudoku.board.cells[self.xy[0]][self.xy[1]].value = 0
            self.update_btns()
            return
        self['text'] = selected['text']
        sudoku.board.cells[self.xy[0]][self.xy[1]].value = selected['text']
        self.update_btns()

    def update_btns(self) -> None:
        global selected
        global btn_cells
        for i in range(9):
            for j in range(9):
                if selected.value == 1 and btn_cells[i][j]['text'] == selected['text']:
                    btn_cells[i][j]['bg'] = '#bfd2d9'
                    btn_cells[i][j]['activebackground'] = '#9eb3ba'
                elif btn_cells[i][j]['text'] != selected['text'] or selected.value == 0:
                    btn_cells[i][j]['bg'] = 'white'
                    btn_cells[i][j]['activebackground'] = '#e3e3e3'

class UI():
    numbers: list[int]

    def __init__(self, btn_cells: list[list[BTN]] = [[]], numbers: list[int] = [None for x in range(9)]) -> None:
            self.numbers = numbers
            self.create_menu()

    def draw_board(self) -> None:
        grids = [[None for y in range(3)] for x in range(3)] 
        for i in range(3):
            for j in range(3):
                grids[i][j] = Frame(root, highlightbackground = 'azure3',
                                        highlightcolor = 'azure3', highlightthickness=2)
                grids[i][j].grid(row = i, column = j, sticky = 'nsew')

        global btn_cells
        btn_cells = [[None for y in range(9)] for x in range(9)]
        for i in range(9):
            for j in range(9):
                frm_cell = Frame(grids[i // 3][j // 3])
                frm_cell.grid(row = (i % 3), column = (j % 3))
                frm_cell.rowconfigure(0, minsize = 65)
                frm_cell.columnconfigure(0, minsize = 65)
                value = sudoku.board.cells[i][j].value
                btn = BTN(frm_cell, state = DISABLED if value !=  0 else NORMAL, 
                            font = ("Helvetica", 20, NORMAL) if value == 0 else ("Helvetica", 20, BOLD),
                            text = " " if value == 0 else value,
                            relief = 'groove', bg = 'white', activebackground="#e3e3e3")
                btn.xy = [i, j]
                btn['command'] = btn.update
                btn.grid(sticky='nsew')
                btn_cells[i][j] = btn

    def draw_labels(self) -> None:
        global selected
        blocks = [] 
        for i in range(3):
            block = Frame(root)
            block.grid(row = 10, column = i)
            blocks.append(block)

        for i in range(9):
            frm_cell = Frame(blocks[i // 3])
            frm_cell.grid(row = 0, column = i)
            frm_cell.rowconfigure(0, minsize = 65)
            frm_cell.columnconfigure(0, minsize = 65)
            self.numbers[i] = BTN(frm_cell, relief = 'groove', bg = 'white', text = i + 1, font = ("Helvetica", 20))
            self.numbers[i]['command'] = self.numbers[i].select
            self.numbers[i].grid(sticky = 'nsew')

        selected = self.numbers[0]
        selected.value = 1
        self.numbers[0]['bg'] = '#1e738f'
        self.numbers[0]['activebackground'] = '#185a70'
        selected.update_btns()

    def draw_sudoku(self) -> None:
        self.draw_board()
        self.draw_labels()

    def check(self) -> None:
        if sudoku.is_solved():
            messagebox.showinfo("Sudoku", "Sudoku is solved!")
        else:
            messagebox.showinfo("Sudoku", "Try again!")

    def solve(self) -> None:
        try:
            solved = sudoku.solve(ForwardCheck());
            if solved:
                self.draw_board()
            else:
                messagebox.showwarning("Sudoku", "No solution found.")
        except:
            messagebox.showwarning("Sudoku", "No solution found.")

    def generate(self, difficulty: float) -> None:
        global sudoku
        sudoku = Sudoku()
        sudoku.generate(ForwardCheck(), difficulty = difficulty) 

    def new_game(self, difficulty: float) -> None:
        self.generate(difficulty)
        self.draw_board()
        global selected
        selected.update_btns()
        #print("---------------------------")

    def erase(self) -> None:
        global selected
        selected.value = 0
        selected.update_btns()
        for btn in self.numbers:
            btn['bg'] = 'white'
            btn['activebackground'] = '#e3e3e3'

    def create_menu(self) -> None:
        my_menu = Menu(root)
        root.config(menu=my_menu)

        new_game_menu = Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label="New Game", menu=new_game_menu)
        new_game_menu.add_command(label="Very easy", command=lambda: self.new_game(0.01))
        new_game_menu.add_command(label="Easy", command=lambda: self.new_game(0.4))
        new_game_menu.add_command(label="Medium", command=lambda: self.new_game(0.6))
        new_game_menu.add_command(label="Hard", command=lambda: self.new_game(0.7))
        my_menu.add_command(label="Check", command=self.check)
        my_menu.add_command(label="Solve", command=self.solve)
        my_menu.add_command(label="Erase", command=self.erase)

ui = UI()
ui.draw_sudoku()

root.mainloop()