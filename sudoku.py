from tkinter import *
from timeit import default_timer as timer
from easy_puzzles import easy1,easy2,easy3,easy4
from medium_puzzles import medium1,medium2,medium3,medium4
from hard_puzzles import hard1,hard2,hard3,hard4
from csp import *
MARGIN = 20  
SIDE = 50 
WIDTH_B = HEIGHT_B = MARGIN * 2 + SIDE * 9  
WIDTH = WIDTH_B + 180  

class SudokuUI(Frame):
    def __init__(self, parent):
        self.parent = parent
        self.original_board = [[0 for j in range(9)] for i in range(9)]
        self.current_board = [row[:] for row in self.original_board]
        Frame.__init__(self, parent)
        self.row, self.col = 0, 0
        self.__initUI()

    def __initUI(self):
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH_B, height=HEIGHT_B)
        self.canvas.pack(fill=BOTH, side=TOP)
        self.canvas.grid(row=0, column=0, rowspan=30, columnspan=60)

        self.level = IntVar(value=1)
        self.puzzle = IntVar(value=0)  

        self.time = StringVar()
        self.time.set("Time:                    ")

        self.make_menu()
        self.__change_level()

        self.clear_button = Button(self, text="Reset", command=self.__clear_board, width=15, height=5)
        self.clear_button.grid(row=8, column=61, padx=20, columnspan=3)
        self.solve_button = Button(self, text="Solve", command=self.solve_clicked, width=15, height=5)
        self.solve_button.grid(row=11, column=61, padx=20, columnspan=3)

        lbltime = Label(self, textvariable=self.time)
        Label(self, text="Algorithm:               ").grid(row=12, column=61)
        lbltime.grid(row=30, column=0)
        self.choice = StringVar(value="BK")

        self.radio = []
        self.radio.append(Radiobutton(self, text="Arc Consistency-3", variable=self.choice, value="AC3"))
        self.radio[0].grid(row=13, column=61)
        self.radio.append(Radiobutton(self, text="Backtracking                 ", variable=self.choice, value="BK"))
        self.radio[1].grid(row=14, column=61)

        lbltime.grid(row=30, column=0)
    
        Label(self, text="Choose Puzzle:               ").grid(row=16, column=61)
        self.radio_puzzles = []
        for i in range(4):
            self.radio_puzzles.append(Radiobutton(self, text=f"Puzzle {i+1}", variable=self.puzzle, value=i))
            self.radio_puzzles[i].bind("<Button-1>", lambda event, idx=i: self.change_puzzle(idx))
        for i, radio in enumerate(self.radio_puzzles):
            radio.grid(row=17 + i, column=61)

        self.__draw_grid()
        self.__draw_puzzle()

    def solve_clicked(self):
        self.solve_sudoku()

    def solve_sudoku(self):

        s = SudokuCSP(self.current_board)
        start = timer()
        if self.choice.get() == "BK":
            result = backtracking_search(s, select_unassigned_variable=mrv, order_domain_values=unordered_domain_values,
                                    inference=forward_checking)

        elif self.choice.get() == "AC3":
            if AC3(s):
                if all(len(s.curr_domains['CELL'+str(i)]) == 1 for i in range(81)):
                    result = {('CELL' + str(i)): s.curr_domains['CELL' + str(i)][0] for i in range(81)}
                else:
                    result = None
                    # result = backtracking_search(s, select_unassigned_variable=mrv, order_domain_values=unordered_domain_values,inference=mac)
                
        end = timer()
            
        if result:
            for i in range(9):
                for j in range(9):
                    index = i * 9 + j
                    self.current_board[i][j] = result.get("CELL" + str(index))
        else:
            print("Invalid sudoku Puzzle")

        self.__draw_puzzle()
        self.time.set("Time: "+str(round(end-start, 5))+" seconds")
        for rb in self.radio:
            rb.config(state=NORMAL)
        self.clear_button.config(state=NORMAL)
        self.solve_button.config(state=NORMAL)
        self.menu_bar.entryconfig("Level", state="normal")

    def make_menu(self):
        self.menu_bar = Menu(self.parent)
        self.parent.configure(menu=self.menu_bar)
        level_menu = Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Level", menu=level_menu)
        level_menu.add_radiobutton(label="Easy", variable=self.level, value=1, command=self.__change_level)
        level_menu.add_radiobutton(label="Medium", variable=self.level, value=2, command=self.__change_level)
        level_menu.add_radiobutton(label="Hard", variable=self.level, value=3, command=self.__change_level)

    def __draw_grid(self):
        for i in range(10):
            if i % 3 == 0:
                color = "black"
            else:
                color = "gray"
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT_B - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH_B - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        self.time.set("Time:                  ")
        for i in range(9):
            for j in range(9):
                cell = self.current_board[i][j]
                if cell != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    if str(cell) == str(self.original_board[i][j]):
                        self.canvas.create_text(x, y, text=cell, tags="numbers", fill="black")
                    else:
                        self.canvas.create_text(x, y, text=cell, tags="numbers", fill="red")

    def __clear_board(self):
        self.current_board = [row[:] for row in self.original_board]
        self.__draw_puzzle()

    def __change_level(self):
        level = self.level.get()
        if level == 1:
            if self.puzzle.get() == 0:
                self.original_board = easy1()
            elif self.puzzle.get() == 1:
                self.original_board = easy2()
            elif self.puzzle.get() == 2:
                self.original_board = easy3()
            elif self.puzzle.get() == 3:
                self.original_board = easy4()

        elif level == 2:
            if self.puzzle.get() == 0:
                self.original_board = medium1()
            elif self.puzzle.get() == 1:
                self.original_board = medium2()
            elif self.puzzle.get() == 2:
                self.original_board = medium3()
            elif self.puzzle.get() == 3:
                self.original_board = medium4()
        elif level == 3:
            if self.puzzle.get() == 0:
                self.original_board = hard1()
            elif self.puzzle.get() == 1:
                self.original_board = hard2()
            elif self.puzzle.get() == 2:
                self.original_board = hard3()
            elif self.puzzle.get() == 3:
                self.original_board = hard4()
        self.current_board = [row[:] for row in self.original_board]
        self.__draw_puzzle() 
    


    def change_puzzle(self, idx):
        if self.level.get() == 1:
            if idx == 0:
                self.original_board = easy1()
            elif idx == 1:
                self.original_board = easy2()
            elif idx == 2:
                self.original_board = easy3()
            elif idx == 3:
                self.original_board = easy4()

        elif self.level.get() == 2:
            if idx == 0:
                self.original_board = medium1()
            elif idx == 1:
                self.original_board = medium2()
            elif idx == 2:
                self.original_board = medium3()
            elif idx == 3:
                self.original_board = medium4()
        
        elif self.level.get() == 3:
            if idx == 0:
                self.original_board = hard1()
            elif idx == 1:
                self.original_board = hard2()
            elif idx == 2:
                self.original_board = hard3()
            elif idx == 3:
                self.original_board = hard4()
        self.current_board = [row[:] for row in self.original_board]
        self.__draw_puzzle()

class SudokuCSP(CSP):

    def __init__(self, board):

        self.domains = {}
        self.neighbors = {}
        for v in range(81):
            self.neighbors.update({'CELL' + str(v): {}})
        for i in range(9):
            for j in range(9):
                name = (i * 9 + j)
                var = "CELL"+str(name)
                self.add_neighbor(var, self.get_row(i) | self.get_column(j) | self.get_square(i, j))
                if board[i][j] != 0:
                    self.domains.update({var: str(board[i][j])})
                else:
                    self.domains.update({var: '123456789'})

        CSP.__init__(self, None, self.domains, self.neighbors, different_values_constraint)

    def get_square(self, i, j):
        if i < 3:
            if j < 3:
                return self.get_square_box(0)
            elif j < 6:
                return self.get_square_box(3)
            else:
                return self.get_square_box(6)
        elif i < 6:
            if j < 3:
                return self.get_square_box(27)
            elif j < 6:
                return self.get_square_box(30)
            else:
                return self.get_square_box(33)
        else:
            if j < 3:
                return self.get_square_box(54)
            elif j < 6:
                return self.get_square_box(57)
            else:
                return self.get_square_box(60)

    def get_square_box(self, index):
        tmp = set()
        tmp.add("CELL"+str(index))
        tmp.add("CELL"+str(index+1))
        tmp.add("CELL"+str(index+2))
        tmp.add("CELL"+str(index+9))
        tmp.add("CELL"+str(index+10))
        tmp.add("CELL"+str(index+11))
        tmp.add("CELL"+str(index+18))
        tmp.add("CELL"+str(index+19))
        tmp.add("CELL"+str(index+20))
        return tmp

    def get_column(self, index):
        return {'CELL'+str(j) for j in range(index, index+81, 9)}

    def get_row(self, index):
            return {('CELL' + str(x + index * 9)) for x in range(9)}

    def add_neighbor(self, var, elements):
        self.neighbors.update({var: {x for x in elements if x != var}})


root = Tk()
SudokuUI(root)
root.title("Sudoku")
root.mainloop()