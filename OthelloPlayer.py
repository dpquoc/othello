import numpy as np
import copy
import threading
import time
from OthelloState import OthelloState
from OthelloBoard import OthelloBoard
from NNet import NNetWrapper
from MCTS import MCTS
from utils import *





class RandomPlayer():
    def __init__(self):
        pass
        
    def play(self, board, current_player, remain_time):
        board = OthelloBoard(board)
        actions = board.get_legal_moves(current_player)
        if len(actions) == 0:
            return None
        i = np.random.randint(len(actions))
        return actions[i]

class GreedyPlayer():
    def __init__(self):
        pass
        
    def play(self, board, current_player, remain_time):
        board = OthelloBoard(board)
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
        min_depth = 2
        max_depth = 5
        start_time = time.time()
        board = OthelloBoard(board)
        init_state = OthelloState(board, current_player, True)

        results = {}
        threads = []
        for depth in range(min_depth, max_depth + 1):
            t = threading.Thread(target=self.run_alphabeta, args=(init_state, depth, results, start_time))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
            
        for depth in range(max_depth, min_depth - 1, -1):
            best_child = results[depth]
            if best_child != "Out of time":
                # print(depth)
                if best_child == None:
                    return None
                return best_child.from_action
            
        
    
    def run_alphabeta(self, state, depth, results, start_time):
        value, best_child = self.alphabeta(copy.deepcopy(state), depth, float('-inf'), float('inf'), True, start_time)
        results[depth] = best_child
        
    def alphabeta(self, state, depth, alpha, beta, maximizing_player, start_time):
        if time.time() - start_time >= 2.8 :
            return -123456 , "Out of time"
        
        if depth == 0:
            return state.evaluate(), None
        state.get_children()
        if len(state.children) == 0:
            return state.evaluate(), None

        if maximizing_player:
            best_child = None
            value = float('-inf')
            for child in state.children:
                child_value, _ = self.alphabeta(child, depth - 1, alpha, beta, False, start_time)
                
                if child_value == -123456 :
                    return -123456 , "Out of time"
                
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
                child_value, _ = self.alphabeta(child, depth - 1, alpha, beta, True, start_time)
                if child_value == -123456 :
                    return -123456 , "Out of time"
                if child_value < value:
                    value = child_value
                    best_child = child
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value, best_child



args = dotdict({
    'MCTS_iterations': 40,
    'cpuct': 1,
})


class AlphaZeroPlayer():
    def __init__(self):
        pass
        
    def play(self, board, current_player, remain_time):
        if isinstance(board, np.ndarray):
            pass
        elif isinstance(board, (list, tuple)):
           board = np.array(board)
           
        
        temp_board = OthelloBoard(board)
        actions = temp_board.get_legal_moves(current_player)
        if not actions:
            return None
        
        
        a = NNetWrapper() 
        a.load_checkpoint('model.pth')

        probs = MCTS(OthelloBoard(), a, args).getActionProb(board*current_player, 0)
        index = np.argmax(probs)
        
        if index == 64:
            return None
        return (int(index/8), index%8)
              
class HumanPlayer():
    def __init__(self):
        pass
        
    def play(self, board, current_player, remain_time):
        board = OthelloBoard(board)
        actions = board.get_legal_moves(current_player)
        board.print_board()
        if not actions:
            print("No valid moves available. Press any key to continue.")
            input()
            return None
        print("Available moves:")
        for i, move in enumerate(actions):
            print(f"{i}: {move}")
        while True:
            try:
                choice = int(input("Enter the index of your move: "))
                if choice < 0 or choice >= len(actions):
                    raise ValueError
                return actions[choice]
            except ValueError:
                print("Invalid input. Please enter a valid index.")
                print("Available moves:")
                for i, move in enumerate(actions):
                    print(f"{i}: {move}")