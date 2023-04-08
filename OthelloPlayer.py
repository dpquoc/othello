import numpy as np

class RandomPlayer():
    def __init__(self):
        pass
        
    def play(self, board, current_player, remain_time):
        actions = board.get_legal_moves(current_player)
        if len(actions) == 0:
            return None
        i = np.random.randint(len(actions))
        print(actions[i])
        return actions[i]

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