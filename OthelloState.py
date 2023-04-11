from OthelloBoard import OthelloBoard
import copy

class OthelloState():
    
    def __init__(self, board, current_player, is_max_player, parent = None, from_action = None):
        self.current_player = current_player
        self.board = board
        self.is_max_player = is_max_player
        self.parent = parent
        self.from_action = from_action
        self.children = []
        
    def get_children(self):
        moves = self.board.get_legal_moves(self.current_player)
        for move in moves:
            new_board = copy.deepcopy(self.board)
            new_board.execute_move(move, self.current_player)
            child_state = OthelloState(new_board,-self.current_player, not self.is_max_player, self, move)
            
            # Append the child state to the list of children
            self.children.append(child_state)
        return self.children
    
    def evaluate(self):
        if self.is_max_player:
            return self.board.evaluate(self.current_player)
        else:
            return self.board.evaluate(-self.current_player)
        
    
    