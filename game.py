import functools
import itertools
import random
import time
import timeit
import numpy as np


winningCombination = np.array([
    [ 0, 1, 2 ],
    [ 3, 4, 5 ],
    [ 6, 7, 8 ],
    [ 0, 3, 6 ],
    [ 1, 4, 7 ],
    [ 2, 5, 8 ],
    [ 0, 4, 8 ],
    [ 2, 4, 6 ],
    ])


def put_copy(arr, ind, v,):
    arr_copy = arr.copy()
    np.put(arr_copy, ind, v)
    return arr_copy


def move_from_evaluation_function(func):
    def move(board: np.array):
        return max(np.arange(9)[board == 0], key=lambda x: func(put_copy(board, x, 1)))
    return move


def is_valid(board: np.array):
    line_sums = board[winningCombination].sum(axis=1)
    w1 = any(i == 3 for i in line_sums)
    w2 = any(i == -3 for i in line_sums)

    return all([
        not (w1 and w2),
        0 <= np.count_nonzero(board == 1) - np.count_nonzero(board == -1) <= 1])


def game_output(board: np.array, check_valid=True):
    if check_valid and not is_valid(board):
        raise Exception(f'not valid: {board=}')
    line_sums = board[winningCombination].sum(axis=1)
    if 3 in line_sums:
        return 1
    if -3 in line_sums:
        return -1
    if np.count_nonzero(board) == 9:
        return 0


def execute(move1, move2, board=None):
    if board is None:
        board = np.zeros(9)
    while True:
        output = game_output(board)
        if output is None:
            if np.count_nonzero(board == 1) == np.count_nonzero(board == -1):
                index = move1(board.copy())
                board[index] = 1
            else:
                index = move2(-board.copy())
                board[index] = -1
        else:
            return output


@functools.cache
def best_result(board: tuple):
    board = np.array(board)
    output = game_output(board, check_valid=False)
    if output is None:
        op = [best_result(tuple(-put_copy(board, i, 1))) for i in range(9) if board[i] == 0]
        me = [-i for i in op]
        return max(me)
    else:
        return output


def execute_all_combs_one_side(move1, move2):
    rate = 0
    for board in itertools.product([0, 1, -1], repeat=9):
        board = np.array(board)
        if is_valid(board):
            rate += execute(move1, move2, board=board)
    return rate


def execute_all_combs(move1, move2):
    return execute_all_combs_one_side(move1, move2) - execute_all_combs_one_side(move2, move1)


def rate(move):
    return execute_all_combs(move, move_from_evaluation_function(lambda board: -best_result(tuple(-board))))


def develop():
    move1 = move_from_evaluation_function(lambda board: -best_result(tuple(-board)))

    def move2(board):
        return random.choice([i for i in range(9) if board[i] == 0])
    
    # # arr = (0,) * 9
    # arr = ( 0,  1,  0,
    #         1, -1, -1,
    #         0,  1, -1)
    # print(best_result(arr))

    # print(rate(move1, move1))
    # print(rate(move2, move2))
    print(rate(move2))


if __name__ == '__main__':
    accuracy = 1
    print(timeit.timeit(develop, number=accuracy) / accuracy)
