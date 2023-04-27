import numpy as np
import copy
from OthelloState import OthelloState

class RandomPlayer():
    def __init__(self):
        pass
        
    def play(self, board, current_player, remain_time):
        actions = board.get_legal_moves(current_player)
        if len(actions) == 0:
            return None
        i = np.random.randint(len(actions))
        return actions[i]
class GreedyPlayer():
    def __init__(self):
        pass
        
    def play(self, board, current_player, remain_time):
        actions = board.get_legal_moves(current_player)
        
        if not actions:
            return None
        
        max_value = float('-inf')
        best_action = None
        
        for action in actions:
            # Evaluate the resulting state of the action
            new_board = copy.deepcopy(board)
            new_board.execute_move(action, current_player)
            value = new_board.evaluate(current_player)
            
            # Update max_value and best_action if necessary
            if value > max_value:
                max_value = value
                best_action = action
                
        return best_action
class AlphaBetaPlayer():
    def __init__(self):
        pass

    def play(self, board, current_player, remain_time):
        init_state = OthelloState(board, current_player, True)
        value, best_child = self.alphabeta(init_state, 4, float('-inf'), float('inf'), True)

        if len(init_state.children) == 0:
            return None
        else:
           return best_child.from_action

    def alphabeta(self, state, depth, alpha, beta, maximizing_player):
        if depth == 0:
            return state.evaluate(), None
        state.get_children()
        if len(state.children) == 0:
            return state.evaluate(), None
        if maximizing_player:
            best_child = None
            value = float('-inf')
            for child in state.children:
                child_value, _ = self.alphabeta(child, depth - 1, alpha, beta, False)
                if child_value > value:
                    value = child_value
                    best_child = child
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_child
        else:
            best_child = None
            value = float('inf')
            for child in state.children:
                child_value, _ = self.alphabeta(child, depth - 1, alpha, beta, True)
                if child_value < value:
                    value = child_value
                    best_child = child
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value, best_child
        
class HumanPlayer():
    def __init__(self):
        pass
        
    def play(self, board, current_player, remain_time):
        pass