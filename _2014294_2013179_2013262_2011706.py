from OthelloPlayer import AlphaZeroPlayer

def select_move(cur_state, player_to_move, remain_time):
    return AlphaZeroPlayer().play(cur_state, player_to_move, remain_time)
