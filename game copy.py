from functools import cache
import itertools

import numpy as np


def get_func_from_rate(rate_func):
    def rate(board, index):
        # new = board.copy()
        # new[index] = 1
        # return rate_func(new)
        return rate_func(updated_board(board, index))
    
    def func(board):
        # print(f'{board=}')
        return max((index for index, value in enumerate(board) if value == 0), key=lambda index: rate(board, index))
    return func


winningCombination = [
    [ 0, 1, 2 ],
    [ 3, 4, 5 ],
    [ 6, 7, 8 ],
    [ 0, 3, 6 ],
    [ 1, 4, 7 ],
    [ 2, 5, 8 ],
    [ 0, 4, 8 ],
    [ 2, 4, 6 ],
    ]


def execute(func1, func2):
    # print(func1)
    # print()
    board = [0] * 9

    while 1:
        if any(board[i1] + board[i2] + board[i3] == 3 for i1, i2, i3 in winningCombination):
            return (1, 0)
        if any(board[i1] + board[i2] + board[i3] == -3 for i1, i2, i3 in winningCombination):
            return (0, 1)
        if sum(map(abs, board)) == 9:
            return (0.5, 0.5)
        
        if sum(board) % 2 == 1:
            mirror_board = [-i for i in board]
            index = func2(mirror_board)
            # print('called', func2)
            board[index] = -1
        else:
            index = func1(board)
            # print('called', func1)
            board[index] = 1


def updated_board(board, i):
    return tuple(j if index != i else 1 for index, j in enumerate(board))


@cache
def best_result(board):
    if any(board[i1] + board[i2] + board[i3] == 3 for i1, i2, i3 in winningCombination):
        return 1
    if any(board[i1] + board[i2] + board[i3] == -3 for i1, i2, i3 in winningCombination):
        return -1
    if sum(map(abs, board)) == 9:
        return 0

    op = [best_result(tuple(-j for j in updated_board(board, i))) for i in range(9) if board[i] == 0]
    me = [-i for i in op]
    return max(me)

def rate_move(board1, board2):
    pass

def rate_func(func):
    rate = 0
    for board in itertools.product([0, 1, -1], repeat=9):
        br = best_result(board)
        rate += best_result(board) == -best_result(-j for j in tuple(updated_board(board, func(board))))
    return rate
        


if __name__ == '__main__':
    arr = [
        -1, 0, 1,
        1, 0, 0,
        -1, 0, -1
        ]
    print(best_result(tuple(arr)))

    f = get_func_from_rate(lambda x: best_result(tuple(x)))
    print(rate_func(f))