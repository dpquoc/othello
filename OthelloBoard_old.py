import numpy as np

class OthelloBoard():
    
    # list of all 8 directions on the board, as (x,y) offsets
    directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]
    board_size = 8
    
    __POINT_MAP = [
    [120, -20, 20, 5, 5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20, 5, 5, 20, -20, 120],
    ]


    def __init__(self, initial_state=None):
        if initial_state is not None:
            self.board = np.array(initial_state, dtype=np.int8)
        else:
            self.board = np.zeros((self.board_size, self.board_size), dtype=np.int8)
            # Set the initial four cells
            center = self.board_size // 2
            self.board[center - 1:center + 1, center - 1:center + 1] = np.array([[-1, 1], [1, -1]], dtype=np.int8)
        
        
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
        
        player_front_tile = opponent_front_tile = 0
        player_point = opponent_point = 0
        player_unstable = opponent_unstable = 0
        player_mobi = opponent_mobi = 0

        # main loop
        for i in range(8):
            for j in range(8):
                
                if self.board[i][j] == player:
                    player_point += OthelloBoard.__POINT_MAP[i][j]

                if self.board[i][j] == opponent:
                    opponent_point += OthelloBoard.__POINT_MAP[i][j]
                
                is_check_front_tile = False
                if self.board[i][j] != 0:
                    for dr, dc in OthelloBoard.directions:
                        r2, c2 = dr + i, dc + j
                        
                        if (r2 < 0 or r2 >= 8 or c2 < 0 or c2 >= 8):
                            continue

                        if (self.board[r2][c2] == 0 and not is_check_front_tile):
                            if self.board[i][j] == player:
                                player_front_tile += 1
                            else:
                                opponent_front_tile += 1
                            is_check_front_tile = True
                            continue

                        if (self.board[r2][c2] == self.board[i][j]):
                            continue

                        can_flip = 0
                        while True:
                            if (r2 < 0 or r2 >= 8 or c2 < 0 or c2 >= 8 or
                                    self.board[r2][c2] == 0 or self.board[r2][c2] == self.board[i][j]):
                                break

                            can_flip += 1
                            r2 = r2 + dr
                            c2 = c2 + dc

                        if r2 < 0 or r2 >= 8 or c2 < 0 or c2 >= 8 or self.board[r2][c2] == self.board[i][j]:
                            continue

                        if self.board[i][j] == player:
                            player_mobi += 1
                            opponent_unstable += can_flip
                        else:
                            opponent_mobi += 1
                            player_unstable += can_flip
        
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
            corner_heuristic_value = 100 * (max_corner_value - min_corner_value) / (max_corner_value + min_corner_value)
        else:
            corner_heuristic_value = 0

        if (player_point + opponent_point) != 0:
            point_map_score = 100 * (player_point - opponent_point) / (player_point + opponent_point)
        else:
            point_map_score = 0

        if (player_front_tile + opponent_front_tile) != 0:
            front_tile_score = 100 * (player_front_tile - opponent_front_tile) / (player_front_tile + opponent_front_tile)
        else:
            front_tile_score = 0

        if (player_mobi + opponent_mobi) != 0:
            mobi_score = 100 * (player_mobi - opponent_mobi) / (player_mobi + opponent_mobi)
        else:
            mobi_score = 0

        if (player_unstable + opponent_unstable) != 0:
            unstable_score = -100 * (player_unstable - opponent_unstable) / (player_unstable + opponent_unstable)
        else:
            unstable_score = 0

        return corner_heuristic_value + point_map_score + front_tile_score + mobi_score + unstable_score


    
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



    




