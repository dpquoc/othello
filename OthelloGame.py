import numpy as np
from OthelloBoard import OthelloBoard
import time

class OthelloGame():
    def __init__(self, player1, player2, time=60):
        self.player1 = player1
        self.player2 = player2
        self.time = time
    
    def start_game(self):
        player1_time = self.time * 1.0
        player2_time = self.time * 1.0
        board = OthelloBoard()
        player1_can_move = True
        player2_can_move = True
        
        while True:
            # Player 1's turn
            start_time = time.time()
            player1_action = self.player1.play(board.board, 1, player1_time)
            end_time = time.time()
            player1_time -= (end_time - start_time)
            
            if player1_action != None :
                board.execute_move(player1_action, 1)
                player1_can_move = True
                print(f"Player 1 ({type(self.player1).__name__}) chose move {player1_action} in {round(end_time - start_time, 2)} seconds.", end=" | ")
            else:
                player1_can_move = False
            
            
            # Player 2's turn
            start_time = time.time()
            player2_action = self.player2.play(board.board, -1, player2_time)
            end_time = time.time()
            player2_time -= (end_time - start_time)
            
            if player2_action != None :
                board.execute_move(player2_action, -1)
                player2_can_move = True
                print(f"Player 2 ({type(self.player2).__name__}) chose move {player2_action} in {round(end_time - start_time, 2)} seconds.")
            else:
                player2_can_move = False
            
            if not player1_can_move and not player2_can_move:
                print("Both players cannot move. Game over.")
                
                player1_pieces = np.sum(board.board == 1)
                player2_pieces = np.sum(board.board == -1)
                
                board.print_board()

                if player1_pieces > player2_pieces:
                    print(f"Player 1: {player1_pieces}. {type(self.player1).__name__} wins! ({round(player1_time, 2)} seconds left)")
                    print(f"Player 2: {player2_pieces}. {type(self.player2).__name__} loses! ({round(player2_time, 2)} seconds left)")
                    
                elif player2_pieces > player1_pieces:
                    print(f"Player 1: {player1_pieces}. {type(self.player1).__name__} loses! ({round(player1_time, 2)} seconds left)")
                    print(f"Player 2: {player2_pieces}. {type(self.player2).__name__} wins! ({round(player2_time, 2)} seconds left)")
                else:
                    print("The game is a tie!")    
                break
            
    def get_next_state(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        if action == None:
            return None
        b = OthelloBoard(board)
        new_b = b.execute_move(action, player)
        return (new_b.board, -player)