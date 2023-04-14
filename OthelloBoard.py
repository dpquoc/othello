import numpy as np


class OthelloBoard():

    # list of all 8 directions on the board, as (x,y) offsets
    directions = [(1, 1), (1, 0), (1, -1), (0, -1),
                  (-1, -1), (-1, 0), (-1, 1), (0, 1)]
    board_size = 8

    def __init__(self, initial_state=None):
        if initial_state is not None:
            self.board = np.array(initial_state, dtype=np.int8)
        else:
            self.board = np.zeros(
                (self.board_size, self.board_size), dtype=np.int8)
            # Set the initial four cells
            center = self.board_size // 2
            self.board[center - 1:center + 1, center - 1:center +
                       1] = np.array([[-1, 1], [1, -1]], dtype=np.int8)

    def get_legal_moves(self, player):
        opponent = -player

        # create an array of all cells where the player has a piece
        player_cells = np.where(self.board == player, 1, 0)

        # create an array of all cells where the opponent has a piece
        opponent_cells = np.where(self.board == opponent, 1, 0)

        # create an array of all cells that are empty
        empty_cells = np.where(self.board == 0, 1, 0)

        legal_moves = []
        # check all directions for each player piece
        for r, c in zip(*np.where(player_cells)):
            for dr, dc in OthelloBoard.directions:
                r2, c2 = r + dr, c + dc
                if (r2 < 0 or r2 >= self.board_size or c2 < 0 or c2 >= self.board_size or
                        player_cells[r2, c2] or not opponent_cells[r2, c2]):
                    continue
                # found a potential legal move, keep following the direction
                while True:
                    r2, c2 = r2 + dr, c2 + dc
                    if r2 < 0 or r2 >= self.board_size or c2 < 0 or c2 >= self.board_size:
                        break
                    if empty_cells[r2, c2]:
                        legal_moves.append((r2, c2))
                        break
                    if player_cells[r2, c2]:
                        break

        return legal_moves

    def execute_move(self, move, player):
        # opponent = -player

        # create an array of all cells where the player has a piece
        player_cells = np.where(self.board == player, 1, 0)

        # # create an array of all cells where the opponent has a piece
        # opponent_cells = np.where(self.board == opponent, 1, 0)

        # create an array of all cells that are empty
        empty_cells = np.where(self.board == 0, 1, 0)

        # update the new board with the new piece
        r, c = move
        self.board[r][c] = player

        # flip opponent pieces as necessary
        for dr, dc in OthelloBoard.directions:
            r2, c2 = r + dr, c + dc
            if (r2 < 0 or r2 >= self.board_size or c2 < 0 or c2 >= self.board_size or
                    empty_cells[r2][c2] or player_cells[r2][c2]):
                continue
            # found a line of opponent pieces to flip
            to_flip = [(r2, c2)]
            while True:
                r2 += dr
                c2 += dc
                if (r2 < 0 or r2 >= self.board_size or c2 < 0 or c2 >= self.board_size or
                        empty_cells[r2][c2]):
                    break
                if player_cells[r2][c2]:
                    for fr, fc in to_flip:
                        self.board[fr][fc] = player
                    break
                to_flip.append((r2, c2))

        return self.board

    def evaluate(self, player):
        opponent = -player

        player_count = np.sum(self.board == player)
        opponent_count = np.sum(self.board == opponent)

        # calculate the coin parity heuristic value
        coin_parity_value = 100 * \
            (player_count - opponent_count) / (player_count + opponent_count)

        # calculate the corner heuristic value
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        max_corner_value = 0
        min_corner_value = 0

        for corner in corners:
            if self.board[corner] == player:
                max_corner_value += 1
            elif self.board[corner] == opponent:
                min_corner_value += 1

        if (max_corner_value + min_corner_value) != 0:
            corner_heuristic_value = 100 * \
                (max_corner_value - min_corner_value) / \
                (max_corner_value + min_corner_value)
        else:
            corner_heuristic_value = 0

        return coin_parity_value + corner_heuristic_value

    # STABILITY HEURISTIC FUNCTION PART
    def row_detector(self, i, j, cur_player):
        # True: Stable, False: Not stable
        size = self.board_size - 1
        left = j - 1
        right = j + 1
        while left > 0 and self.board[i][left] == cur_player:
            left -= 1
        while right < size  and self.board[i][right] == cur_player:
            right += 1
        if self.board[i][left] == -cur_player and self.board[i][right] == 0:
            return False
        elif self.board[i][left] == 0 and self.board[i][right] == -cur_player:
            return False
        else:
            return True

    def column_detector(self, i, j, cur_player):
        # True: Stable, False: Not stable
        size = self.board_size - 1
        up = i + 1
        down = i - 1
        while up > 0 and self.board[up][j] == cur_player:
            up -= 1
        while down < size and self.board[down][j] == cur_player:
            down += 1
        if self.board[up][j] == -cur_player and self.board[down][j] == 0:
            return False
        elif self.board[up][j] == 0 and self.board[down][j] == -cur_player:
            return False
        else:
            return True

    def diagonal_detector(self, i, j, cur_player):
        size = self.board_size - 1
        n = i - 1
        s = i + 1
        w = j - 1 
        e = j + 1
        while w > 0 and n > 0 and self.board[n][w] == cur_player:
            w -= 1
            n -= 1
        while s < size and e < size and self.board[s][e] == cur_player:
            s += 1
            e += 1
        if self.board[n][w] == -cur_player and self.board[s][e] == 0:
            return False
        elif self.board[n][w] == 0 and self.board[s][e] == -cur_player:
            return False
        
        n = i - 1
        s = i + 1
        w = j - 1
        e = j + 1
        while n > 0 and e < size and self.board[n][e] == cur_player:
            n -= 1
            e += 1
        while s < size and w > 0 and self.board[s][w] == cur_player:
            s += 1
            w -= 1
        if self.board[n][e] == -cur_player and self.board[s][w] == 0:
            return False
        elif self.board[n][e] == 0 and self.board[s][w] == -cur_player:
            return False
        else:
            return True
        
    def is_stable(self, i, j, cur_player):
        size = len(size.board_size) - 1
        corner_set = {(0, 0), (0, size - 1), (size - 1, 0),
                      (size - 1), (size - 1)}
        if (i, j) in corner_set:
            return True
        elif i == 0 or i == size:
            return self.row_detector(i, j, cur_player)
        elif j == 0 or j == size:
            return self.column_detector(i, i, cur_player)
        else:
            return self.row_detector(i, j, cur_player) and self.column_detector(i, j, cur_player) and self.diagonal_detector(i, j, cur_player)

    def is_unstable(self, i, j): pass

    def stability(self, cur_player):
        player = 0
        opponent = 0
        size = len(self.board_size)
        for i in range(size):
            for j in range(size):
                if self.board[i][j] == cur_player:
                    if self.is_stable(i, j, cur_player):
                        player += 1
                    else:
                        player -= 1
                else:
                    if self.is_stable(i, j, -cur_player):
                        opponent += 1
                    else:
                        opponent -= 1
        if player + opponent == 0:
            return 0
        else:
            return 100 * (player - opponent) / (player - opponent)
    # ----------- END ---------------

    def print_board(self):
        print("    ", end="")
        for i in range(self.board_size):
            print(i, end=" ")
        print()
        print("   +" + "--" * self.board_size + "+")
        for i in range(self.board_size):
            print(i, "|", end=" ")
            for j in range(self.board_size):
                if self.board[i][j] == 1:
                    print("X", end=" ")
                elif self.board[i][j] == -1:
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            print("|", i)
        print("   +" + "--" * self.board_size + "+")
        print("    ", end="")
        for i in range(self.board_size):
            print(i, end=" ")
        print()

# board = OthelloBoard()
# board.print_board()
# print(board.get_legal_moves(1))
# print(board.execute_move((2,3), 1))
