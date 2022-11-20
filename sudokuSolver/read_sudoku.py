import numpy as np

input_folder = 'sudoku examples/'
examples = ['example0.txt', 'example1.txt', 'example2.txt', 'example3.txt',
            'example4.txt', 'example5.txt', 'example6.txt', 'example7.txt',
            'example8.txt', 'example9.txt', 'example10.txt', 'example11.txt',
            'example12.txt', 'example13.txt', 'example14.txt', 'example15.txt',
            ]


def read_sudoku(ex_num):
    try:
        board = []
        with open(input_folder + examples[ex_num], 'r') as file:
            for line in file:
                board.append(list(map(int, line.strip())))

        sudoku = np.array([[int(i) for i in line] for line in board])
        # print(sudoku)
        return sudoku
    except FileNotFoundError as _error:
        print(_error)
