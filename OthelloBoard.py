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
        new_board = np.copy(self.board)
        opponent = -player
        
        # create an array of all cells where the player has a piece
        player_cells = np.where(self.board == player, 1, 0)

        # create an array of all cells where the opponent has a piece
        opponent_cells = np.where(self.board == opponent, 1, 0)

        # create an array of all cells that are empty
        empty_cells = np.where(self.board == 0, 1, 0)

        # update the new board with the new piece
        r, c = move
        new_board[r][c] = player

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
                        new_board[fr][fc] = player
                    break
                to_flip.append((r2, c2))

        return new_board

    def evaluate(self, player):
        pass
    
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

board = OthelloBoard()
board.print_board()
print(board.get_legal_moves(1))
print(board.execute_move((2,3), 1))



