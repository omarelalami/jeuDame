import numpy as np

board = np.zeros((8, 8), dtype=int)
for i in range(0, 8, 2):
        board[0, i+1] = 1  # ligne 1, colonnes impaires
        board[1, i] = 1    # ligne 2, colonnes paires
        board[2, i+1] = 1  # ligne 3, colonnes impaires



print(board)