import random
import time

import numpy as np
import math
from random import choice
from sudokuSolver_BacktrConstrProp import validate_sudoku
from read_sudoku import read_sudoku


def print_sudoku(board):
    """
    Print the sudoku
    :param board:
    :return:
    """
    print("\n-------------------------")
    for i in range(9):
        for j in range(9):
            if board[i][j] is not None:
                if j == 0:
                    print("|", end=" ")
                print(f"{board[i][j]} ", end="")
            if (j + 1) % 3 == 0:
                print("|", end=" ")
        if (i + 1) % 3 == 0:
            print("\n-------------------------", end=" ")
        print()


def swap_cells(current_sudoku, toswap):
    """
    Swap two cells
    :param current_sudoku:
    :param toswap: list containing the two cells to swap
    :return:
    """
    new_sudoku = np.copy(current_sudoku)
    tmp = new_sudoku[toswap[0][0]][toswap[0][1]]
    new_sudoku[toswap[0][0]][toswap[0][1]] = new_sudoku[toswap[1][0]][toswap[1][1]]
    new_sudoku[toswap[1][0]][toswap[1][1]] = tmp
    return new_sudoku


def get_random_cells(empty_cells, block):
    """
    Randomly choose two cells from the random 3x3 square
    :param empty_cells:
    :param block: random 3x3 square
    :return:
    """
    while 1:
        first = random.choice(block)
        second = choice([box for box in block if box != first])

        if empty_cells[first[0]][first[1]] == 0 and empty_cells[second[0]][second[1]] == 0:
            return [first, second]


def get_new_state(current_sudoku, empty_cells, block_list):
    """
    Generate the new sudoku from the current one by randomly choosing a 3x3 square and swapping two random cells
    :param current_sudoku:
    :param empty_cells: starting sudoku board used to keep track of variable cells
    :param block_list: list of the 3x3 square coordinates
    :return:
    """
    random_block = random.choice(block_list)
    random_cells = get_random_cells(empty_cells, random_block)
    new_sudoku = swap_cells(current_sudoku, random_cells)
    return new_sudoku, random_cells


def choose_new_state(current_sudoku, empty_cells, block_list, temp):
    """
    Compare the costs of the current sudoku and the new sudoku, and return the new one if it has a lower cost.
    If the new sudoku has a higher cost, return it with a certain probability. Otherwise keep the current.
    :param current_sudoku:
    :param empty_cells: starting sudoku board used to keep track of variable cells
    :param block_list: list of the 3x3 square coordinates
    :param temp: temperature
    :return:
    """
    new_sudoku, swapped = get_new_state(current_sudoku, empty_cells, block_list)

    # current_cost = calculate_cost(current_sudoku)
    # new_cost = calculate_cost(new_sudoku)
    current_cost = calculate_rowcol_cost(swapped[0][0], swapped[0][1], current_sudoku) + \
                   calculate_rowcol_cost(swapped[1][0], swapped[1][1], current_sudoku)
    new_cost = calculate_rowcol_cost(swapped[0][0], swapped[0][1], new_sudoku) + \
               calculate_rowcol_cost(swapped[1][0], swapped[1][1], new_sudoku)
    cost_diff = new_cost - current_cost

    if cost_diff < 0:
        return new_sudoku, cost_diff
    else:
        if np.random.uniform(0, 1, 1) < math.exp(-cost_diff / temp):
            return new_sudoku, cost_diff
    return current_sudoku, 0


def calculate_cost(board):
    """
    Cost Function
    Sum of the number of duplicates in each rows and columns. The lower the better.
    Ideally, cost is 0 if the sudoku is solved.
    The board is already filled with value from 1 to 9.
    :param board:
    :return:
    """
    errors = 0
    # present_values = []
    # for i in range(9):
    #     for j in range(9):
    #         present_values.append(board[j][i])
    #     errors = errors + (9 - len(set(present_values)))
    #     present_values = []
    # for i in range(9):
    #     for j in range(9):
    #         present_values.append(board[i][j])
    #     errors = errors + (9 - len(set(present_values)))
    #     present_values = []
    for i in range(9):
        errors = errors + calculate_rowcol_cost(i, i, board)
    return errors


def calculate_rowcol_cost(row, col, board):
    """
    Calculate the number of duplicates in the given row and column.
    :param row:
    :param col:
    :param board:
    :return:
    """
    errors = 0
    errors = errors + (9 - len(np.unique(board[:, col])))
    errors = errors + (9 - len(np.unique(board[row, :])))
    return errors


def get_empty_cells(board):
    """
    Counts the number of the empty cells/variable cells
    :param board:
    :return:
    """
    empty_cells = 0
    for i in range(9):
        for j in range(9):
            if board[i, j] == 0:
                empty_cells += 1
    return empty_cells


def get_grid_val(board, block):
    """
    Get the values of a given 3x3 square
    :param board:
    :param block: coordinates of a 3x3 square
    :return:
    """
    present_val = []
    for row, col in block:
        if board[row][col] != 0:
            present_val.append(board[row][col])
    return present_val


def generate_random_state(board, block_list):
    """
    Fill the starting board with random numbers from 1 to 9.
    The constraint where the numbers in each 3x3 square are unique from 1 to 9 is considered.
    :param board:
    :param block_list: list of the 3x3 square coordinates
    :return:
    """
    for block in block_list:
        for row, col in block:
            if board[row][col] == 0:
                board[row][col] = choice([i for i in range(1, 10) if i not in get_grid_val(board, block)])
    return board


def get_3x3blocks():
    """
    Get the coordinates of the nine 3x3 squares in a 9x9 sudoku
    :return:
    """
    blocks_list = []
    for k in range(0, 9):
        tmp_list = []
        rows = [i + 3 * (k % 3) for i in range(0, 3)]
        cols = [i + 3 * math.trunc(k / 3) for i in range(0, 3)]
        for x in rows:
            for y in cols:
                tmp_list.append((x, y))
        blocks_list.append(tmp_list)
    return blocks_list


def solves_sudoku(board):
    """
    Solves the sudoku using Simulated Annealing.
    Define a starting temperature and a temperature decrease rate for the Simulated Annealing.
    :param board:
    :return:
    """
    # the starting board is used to track the empty/variable cells, those with 0
    working_board = np.copy(board)
    solution_found = 0
    temp = 1
    temp_decrease_rate = 0.9999
    blocks = get_3x3blocks()  # get blocks' cells' coordinates
    curr_sudoku = generate_random_state(working_board, blocks)
    score = calculate_cost(curr_sudoku)

    itertns = get_empty_cells(board)  # number of iterations before decreasing the temperature
    k = 0  # for debugging

    if score == 0:
        return curr_sudoku

    while solution_found == 0:
        for i in range(0, itertns):
            # if too many iterations, it will frequently go up/down since the temperature is the same here
            # if too few, the temperature falls too quickly so it will rarely go up
            k += 1
            curr_sudoku, score_diff = choose_new_state(curr_sudoku, board, blocks, temp)
            score += score_diff
            # print("[{}-{}] Temp: {} Score: {} Stuck Count: {}".format(k, i, temp, score, local_minima))

            if score <= 0:
                solution_found = 1
                break
        if score <= 0:
            solution_found = 1

        temp *= temp_decrease_rate

    return curr_sudoku, k


if __name__ == '__main__':
    for i in range(14):  # the last 2 sudoku (14, 15) test are not included because they take too long 20+ mins
        # i = 6
        sudoku = read_sudoku(i)
        print_sudoku(sudoku)
        start = time.perf_counter()
        solution, tot_iter = solves_sudoku(sudoku)
        end = time.perf_counter()
        print_sudoku(solution)
        print(validate_sudoku(solution, 9))
        print(f"Sudoku N. {i} Iterations: {tot_iter} Time: {end - start:0.4f}")
