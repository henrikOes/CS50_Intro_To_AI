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
    x_placements = o_placements = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j] == X):
                x_placements += 1
            elif(board[i][j] == O):
                o_placements += 1
    
    if x_placements>o_placements:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    s = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j] != X and board[i][j] != O):
                s.append([i, j])
    
    return s


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    next_turn = player(board)
    
    new_board[action[0]][action[1]] = next_turn
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    w = None
    
    for row in board:
        if row[0] == row[1] == row[2]:
            w = row[0]

    # Check columns for three consecutive cells
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            w = board[0][col]

    # Check diagonal (top-left to bottom-right)
    if board[0][0] == board[1][1] == board[2][2]:
        w = board[0][0]

    # Check diagonal (top-right to bottom-left)
    if board[0][2] == board[1][1] == board[2][0]:
        w = board[0][2]

    return w
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    bool_val = True
    
    if (winner(board) == X or winner(board) == O):
        return True
        
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                bool_val = False
    
    return bool_val


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    char_winner = winner(board)
    
    if(char_winner == X):
        return 1
    elif(char_winner == O):
        return -1
    else: 
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    
    Sjekke hvem ai'en spiller for
    Hente alle mulig trekke og lage nye brett med disse trekkene
    Sjekke om spiller kan vinne neste gang på dette brettet
    returnere dersom spiller ikke kan vinne
    Hvor mange steg frem? 1 trekk foreløpig
    """
    if terminal(board):
        return None  # Ingen trekk om fullt brett eller vunnet

    current_player = player(board)  # Sjekker hvem sin tur
    best_action = None

    if current_player == 'X':  # Maximizing player "X"
        best_score = -math.inf
        for move in actions(board):
            new_board = result(board, move)
            score = minimax_value(new_board, False)  # Neste tur er minimiser O
            if score > best_score:
                best_score = score
                best_action = move
    else:  # Minimizing player (O)
        best_score = math.inf
        for move in actions(board):
            new_board = result(board, move)
            score = minimax_value(new_board, True)  # Neste tur er minimiser X
            if score < best_score:
                best_score = score
                best_action = move

    return best_action  # Returnerer beste trekk

def minimax_value(board, is_maximizing):
    if terminal(board):
        return utility(board)  # Om brett fullt returnerer vinner

    if is_maximizing:
        best_score = -math.inf
        for move in actions(board):
            new_board = result(board, move)
            score = minimax_value(new_board, False)  # Min
            best_score = max(best_score, score)
    else:
        best_score = math.inf
        for move in actions(board):
            new_board = result(board, move)
            score = minimax_value(new_board, True)  # Max
            best_score = min(best_score, score)

    return best_score