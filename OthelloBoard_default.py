import numpy as np

class OthelloBoard():
    
    # list of all 8 directions on the board, as (x,y) offsets
    directions = [(1,1),(1,0),(1,-1),(0,-1),(-1,-1),(-1,0),(-1,1),(0,1)]
    board_size = 8
    
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

    def current_mobi_eval(self, player):
        player_curr_mobi = len(self.get_legal_moves(player))
        opponent_curr_mobi = len(self.get_legal_moves(-player))

        if (player_curr_mobi + opponent_curr_mobi != 0):
            return 100 * (player_curr_mobi - opponent_curr_mobi) / (player_curr_mobi + opponent_curr_mobi) 
        else: 
            return 0

    def potential_mobi_eval(self, player):
        player_potent_mobi = 0
        opponent_potent_mobi = 0

        # Duyệt tất cả các cell
        for i in range(self.board_size):
            for j in range(self.board_size):
                # Nếu cell là empty
                if self.board[i][j] == 0:
                    check_player_done = False
                    check_opponent_done = False
                    # Kiểm tra tất cả các hướng
                    for dr, dc in OthelloBoard.directions:
                        if check_opponent_done and check_player_done:
                            break

                        r2, c2 = i + dr, j + dc
                        
                        if r2 < 0 or r2 >= self.board_size or c2 < 0 or c2 >= self.board_size:
                            continue
                        
                        if self.board[r2][c2] == player and not check_player_done:
                            player_potent_mobi += 1
                            check_player_done = True

                        if self.board[r2][c2] == -player and not check_opponent_done:
                            opponent_potent_mobi += 1
                            check_opponent_done = True

        if (player_potent_mobi + opponent_potent_mobi != 0):
            return 100 * (player_potent_mobi - opponent_potent_mobi) / (player_potent_mobi + opponent_potent_mobi) 
        else: 
            return 0


    def evaluate(self, player):
        opponent = -player
        
        player_count = np.sum(self.board == player)
        opponent_count = np.sum(self.board == opponent)
        
        # calculate the coin parity heuristic value
        coin_parity_value = 100 * (player_count - opponent_count) / (player_count + opponent_count)
        
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
            
        return coin_parity_value + corner_heuristic_value


    
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



    




