from OthelloPlayer import AlphaBetaPlayer
from OthelloBoard import OthelloBoard

def select_move(cur_state, player_to_move, remain_time):
    return AlphaBetaPlayer().play(OthelloBoard(cur_state), player_to_move, remain_time)