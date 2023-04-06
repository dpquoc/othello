from othello.OthelloBoard import OthelloBoard

class OthelloState():
    
    def __init__(self, matrix, current_player):
        self.current_player = current_player
        self.board = OthelloBoard(matrix)
    
    
    