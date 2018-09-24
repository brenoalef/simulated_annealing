import time
from tkinter import *
from math import floor
from functools import partial
from simulated_annealing import simulated_annealing

class EightQueen:
    board = set(range(0, 64))

    def __init__(self, initial_state=[0, 1, 2, 3, 4, 5, 6, 7]):
        self.initial_state = initial_state

    def __attacked_positions(self, state):
        others = set(state)
        positions = set()
        for p in state[0:8]:
            l = floor(p / 8)
            c = p % 8
            others = others - {p}
            positions = positions.union(set(range(l*8, (l+1)*8, 1)))
            positions = positions.union(set(range(p - min(l, c)*9, p + (7 - max(l, c))*9 + 1, 9)))
            positions = positions.union(set(range(p - (min(l, 7 - c))*7, p + min(7 - l, c)*7 + 1, 7)))
        return positions

    def actions(self, state):
        return [x for x in self.board if x not in state and x not in self.__attacked_positions(state)]

    def result(self, state, action):      
        new_state = [a for a in state]
        new_state[action%8] = action
        return new_state

    def value(self, state):
        return 28 - len(self.__attacked_positions(state).intersection(set(state)))


def raw_exec_time(problem):
    start_time = time.clock()
    simulated_annealing(problem)
    print("SA: " + format(time.clock() - start_time, '.5f') + " seconds")


if __name__ == '__main__':
    problem = EightQueen()
    
    #raw_exec_time(problem)

    solution = simulated_annealing(problem)
    print("SA: ", solution)
    
    root = Tk()
    root.title('8-queens')
    canvas = Canvas(root,bg='white',height=500,width=500)
    canvas.pack(side=TOP,padx=10,pady=10)
    queen = PhotoImage(file="queen.gif")
    queen = queen.subsample(8, 8)
    board_rows=8
    board_cols=8
    x=1
    y=1
    square_size= 500/8
    for rows in range(board_rows):
        color_white = not (rows%2)
        for columns in range(board_cols):
            color="lightgray"
            if not color_white:
                color="red"
            x=columns*square_size
            y=rows*square_size
            canvas.create_rectangle(x, y, x+square_size, y+square_size, fill=color)
            if rows*8 + columns in solution:
                canvas.create_image(x, y, anchor = NW, image=queen)
            color_white = not color_white

    bou1 = Button(root,text='Close',width=25,command=root.quit)
    bou1.pack(side=RIGHT,padx=10,pady=10)

    root.mainloop()
    