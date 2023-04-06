import numpy as np


class RandomPlayer():
    def __init__(self):
        pass
        
    def play(self, board, current_player, remain_time):
        a = np.random.randint(self.game.getActionSize())
        valids = self.game.getValidMoves(board, 1)
        while valids[a]!=1:
            a = np.random.randint(self.game.getActionSize())
        return a

class GreedyPlayer():
    def __init__(self):
        pass
        
    def play(self, board, current_player, remain_time):
        pass

class AlphaBetaPlayer():
    def __init__(self):
        pass
        
    def play(self, board, current_player, remain_time):
        pass

class HumanPlayer():
    def __init__(self):
        pass
        
    def play(self, board, current_player, remain_time):
        pass