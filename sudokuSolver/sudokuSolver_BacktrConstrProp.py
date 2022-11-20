import itertools
import time

import numpy as np
from read_sudoku import read_sudoku

domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # possible values for the cells


def print_sudoku(board):
    """
    Print the sudoku
    :param board: sudoku
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


def get_grid(board, i, j):
    """
    Get the 3x3 square the cell[i,j] belongs to
    :param board: sudoku
    :param i: row of the current cell
    :param j: column of the current cell
    :return:
    """
    grid = list(itertools.chain(row[j:j + 3] for row in board[i:i + 3]))
    return grid


def used_num_grid(board, i, j):
    """
    Get the values already present in the 3x3 square the cell [i,j] belongs to
    :param board: sudoku
    :param i: row of the current cell
    :param j: column of the current cell
    :return:
    """
    curr_grid = get_grid(board, i - i % 3, j - j % 3)
    used_num = list(itertools.chain(curr_grid[0], curr_grid[1], curr_grid[2]))
    return used_num


def used_num_row(board, i):
    """
    Get the values already present in the row the cell [i,j] belongs to
    :param board: sudoku
    :param i: row of the current cell
    :return:
    """
    used_num = []
    for j in range(9):
        if board[i][j] != 0:
            used_num.append(board[i][j])
    return used_num


def used_num_col(board, j):
    """
    Get the values already present in the column the cell [i,j] belongs to
    :param board: sudoku
    :param j: column of the current cell
    :return:
    """
    used_num = []
    for i in range(9):
        if board[i][j] != 0:
            used_num.append(board[i][j])
    return used_num


def get_possible_val(board, i, j):
    """
    Get the possible values of the cell [i,j] by removing those present in the row, column and 3x3 square it belongs to
    :param board: sudoku
    :param i: row of the current cell
    :param j: column of the current cell
    :return: list of the possible values
    """
    used_num = list(set(itertools.chain.from_iterable([used_num_col(board, j),
                                                       used_num_row(board, i),
                                                       used_num_grid(board, i, j)])))
    return [k for k in domain if k not in used_num]


def get_rows_ranked(board):
    """
    Heuristic.
    Sort the rows by number of empty/variable cells. The lower the better.
    :param board: sudoku
    :return:
    """
    rows_torank = []

    for rows in board:
        rows_torank.append(np.count_nonzero(rows == 0))
    rows_ranked = np.argsort(rows_torank)
    # print(rows_torank)
    # print(rows_ranked)

    return rows_ranked


def get_empty_cells(board):
    """
    Get the indexes of all the empty/variable cells sorted by the rows with less empty cells
    :param board: sudoku's board
    :return:
    """
    empty_cells = []
    for i in get_rows_ranked(board):
        for j in range(9):
            if board[i][j] == 0:
                empty_cells.append((i, j))
    return empty_cells


# def get_val_ranked(board, poss_val_mat, row, col):
#     """
#     Heuristic function,
#     rank possible values by checking the number of occurrences in other empty cells, the lower the better
#     :param board:
#     :param poss_val_mat:
#     :param row:
#     :param col:
#     :return:
#     """
#     # TODO this function slows the process but in the optimal situation helps doing less iterations
#     # but this is inefficient such that it's faster to not do this and do more iterations
#
#     val_torank = []
#     for val in poss_val_mat[row][col]:
#         # get the domain of occurrences of the sum in square, row and column
#         occ = 0
#         # check row
#         for j in range(9):
#             if board[row][j] == 0 and val in poss_val_mat[row][j]:
#                 occ = occ + 1
#         # check col
#         for i in range(9):
#             if board[i][col] == 0 and val in poss_val_mat[i][col]:
#                 occ = occ + 1
#         # check square
#         for offset_row in range(3):
#             for offset_col in range(3):
#                 curr_row = (row - row % 3) + offset_row
#                 curr_col = (col - col % 3) + offset_col
#                 if board[curr_row][curr_col] == 0 and val in poss_val_mat[curr_row][curr_col]:
#                     occ = occ + 1
#         val_torank.append(occ)
#     val_ranked_index = np.argsort(val_torank)
    # print(val_torank)
    # print(val_ranked_index)
    # print([poss_val_mat[row][col][i] for i in val_ranked_index])

    # return [poss_val_mat[row][col][i] for i in val_ranked_index]


# def try_values_heuristic(board, to_check, k):
#     """
#     Given a cell, try every possible values but using heuristic function.
#     After trying one value call the function on the next cell.
#     :param board:
#     :param to_check: list containing the coordinates of the empty/variable cells
#     :param k: index position of the coordinates of the current cell
#     :return:
#     """
#     i, j = to_check[k]
#     # try heuristic function by doing matrix before
#     poss_val_matrix = [[[] for _ in range(9)] for _ in range(9)]
#     for ii in range(9):
#         for jj in range(9):
#             if toSolve[ii][jj] == 0:
#                 poss_val_matrix[ii][jj] = list(get_possible_val(board, ii, jj))
#
#     for v in get_val_ranked(board, poss_val_matrix, i, j):
#         # try every possible values for each empty cell
#         board[i][j] = v
#         print("[{}] cell {},{} = {}".format(k, i, j, v))
#         if k < len(to_check) - 1:
#             try_values_heuristic(board, to_check, k + 1)
#         # check if sudoku is valid
#         if validate_sudoku(board, 9):
#             return
#     board[i][j] = 0


def try_values(board, to_check, k):
    """
    Given a cell, try every possible values.
    After trying one value call the function on the next cell.
    :param board:
    :param to_check: list containing the coordinates of the empty/variable cells
    :param k: index position of the coordinates of the current cell
    :return:
    """
    i, j = to_check[k]
    for v in list(get_possible_val(board, i, j)):
        board[i][j] = v
        # print("[{}] cell {},{} = {}".format(k, i, j, v))
        if k < len(to_check) - 1:
            try_values(board, to_check, k + 1)
        # check if sudoku is valid
        if validate_sudoku(board, 9):
            return
    board[i][j] = 0


def solver(board):
    """
    Solving function.
    :param board:
    :return:
    """
    empty_cell = get_empty_cells(board)

    # try_values_heuristic(board, empty_cell, 0)
    try_values(board, empty_cell, 0)

    if not validate_sudoku(board, 9):
        errmsg = 'There is no solution to this sudoku.'
        raise ValueError(errmsg)


def check_row(arr, row):
    """
    Checks if there is any duplicate in current row
    :param arr:
    :param row:
    :return:
    """
    st = set()
    for i in range(9):
        # If already encountered before, return false
        if arr[row][i] in st:
            return False
        # If it is not an empty cell, insert value at the current cell in the set
        if arr[row][i] != 0:
            st.add(arr[row][i])
    return len(st) == 9


def check_col(arr, col):
    """
    Checks if there is any duplicate in current column
    :param arr:
    :param col:
    :return:
    """
    st = set()
    for i in range(9):
        # If already encountered before, return false
        if arr[i][col] in st:
            return False
        # If it is not an empty cell, insert value at the current cell in the set
        if arr[i][col] != 0:
            st.add(arr[i][col])
    return len(st) == 9


def check_square(arr, start_row, start_col):
    """
    Checks if there is any duplicate in current 3x3 square
    :param arr:
    :param start_row:
    :param start_col:
    :return:
    """
    st = set()
    for row in range(3):
        for col in range(3):
            curr = arr[row + start_row][col + start_col]
            # If already encountered before, return false
            if curr in st:
                return False
            # If it is not an empty cell, insert value at current cell in set
            if curr != 0:
                st.add(curr)
    return len(st) == 9


def is_valid(arr, row, col):
    """
    Checks if current row, current column and current 3x3 square are valid
    :param arr:
    :param row:
    :param col:
    :return:
    """
    return check_row(arr, row) and check_col(arr, col) and check_square(arr, row - row % 3, col - col % 3)


def validate_sudoku(board, n):
    """
    Given a sudoku, check if it is valid.
    :param board:
    :param n:
    :return:
    """
    for i in range(n):
        for j in range(n):
            # If at least one of current row, column and 3x3 square are not valid, return false
            if not is_valid(board, i, j):
                return False
    return True


if __name__ == '__main__':
    for i in range(16):  # the last sudoku (15) test takes 90+ sec
        toSolve = read_sudoku(i)  # 0..14
        print_sudoku(toSolve)
        start = time.perf_counter()
        solver(toSolve)
        end = time.perf_counter()
        print_sudoku(toSolve)
        print(f"Sudoku N. {i} Time: {end - start:0.4f}")
