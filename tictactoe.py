"""
Tic Tac Toe Player
"""

import math
import copy

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
    
    options = set()

    for x in range(len(board)):

        for y in range(len(board[x])):

            if board[x][y] == None:
                options.add((x,y))
                
    return options


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    temp_b = copy.deepcopy(board)
    
    user = player(temp_b)
    
    x, y = action
    temp_b[x][y] = user
    
    return temp_b


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # across
    for row in board:
        if len(set(row)) == 1 and not None in row:
            return list(set(row))[0]

    
    # horizontal
    for x in range(len(board)):
        check = set()

        for y in range(len(board[x])):
            check.add(board[y][x])

        if len(check) == 1 and not None in check:
            return list(set(check))[0]
    
    # diagonal
    for x in range(1):
        i = 0
        
        check1 = list(set([board[i][i], board[i+1][i+1], board[i+2][i+2]]))
        check2 = list(set([board[i][i+2], board[i+1][i+1], board[i+2][i]]))
        
        if len(check1) == 1 and not None in check1:
            return check1[0]
        if len(check2) == 1 and not None in check2:
            return check2[0]
    
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
    
    if winner(board) == 'X':
        return 1
    if winner(board) == 'O':
        return -1
    if winner(board) == None:
        return 0
    
    return None


def minimax(board):
    
    options = actions(board)
    temp_b = copy.deepcopy(board)
    
    if player(board) == 'X':
        
        maxEval = float('-INF')
        bestmove = ''
    
        for child in options:
            temp_b = result(temp_b, child)
            evaluation = apply_minimax(temp_b)
            maxEval = max(maxEval, evaluation)
            
            if maxEval == evaluation:
                bestmove = child
                
        return bestmove
    
    
    if player(board) == 'O':
        
        minEval = float('INF')
        bestmove = ''
    
        for child in options:
            temp_b = result(temp_b, child)
            evaluation = apply_minimax(temp_b)
            minEval = min(minEval, evaluation)
            
            if minEval == evaluation:
                bestmove = child
                
        return bestmove


def apply_minimax(board_state):

    active = player(board_state)
    
    if terminal(board_state):
        return utility(board_state)
    
    if active == 'X':
        maxEval = float('-INF')
        
        options = actions(board_state)
        
        for child in options:
            temp_b = result(board_state, child)
            temp_p = player(temp_b)
            evaluation = apply_minimax(temp_b)
            maxEval = max(maxEval, evaluation)
        return maxEval
    
    else:
        minEval = float('INF')
        
        options = actions(board_state)
        
        for child in options:
            temp_b = result(board_state, child)
            temp_p = player(temp_b)
            evaluation = apply_minimax(temp_b)
            minEval = min(minEval, evaluation)
        return minEval
