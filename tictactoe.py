"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    
    actors = [x for x in board for x in x]
    
    # if no moves played yet, X gets first turn
    if set(actors) == None:
        return 'X'
    
    # if there are more O moves than X moves on the board, it is X's turn
    if actors.count('O') >= actors.count('X'):
        return 'X'
    
    return 'O'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    
    options = []

    for x in range(len(board)):

        for y in range(len(board[x])):

            if board[x][y] == None:
                options.append((x,y))
                
    return options


def result(board, action, user):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    x, y = action
    board[x][y] = user
    
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    for row in board:
        if len(set(row)) == 1 and not None in row:
            return list(set(row))[0]

        
    for x in range(len(board)):
        check = set()

        for y in range(len(board[x])):
            check.add(board[y][x])

        if len(check) == 1 and not None in check:
            return list(set(check))[0]
        
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    champion = winner(board)
    
    if champion:
        return champion
    
    if not champion:
        check = set([x for x in board for x in x])
        
        if None in check:
            return False
        if not None in check:
            return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError
