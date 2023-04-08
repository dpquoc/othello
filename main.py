import argparse
from OthelloGame import OthelloGame
from OthelloPlayer import RandomPlayer, GreedyPlayer, AlphaBetaPlayer, HumanPlayer

def main():
    parser = argparse.ArgumentParser(description='Play Othello')
    parser.add_argument('--player1', type=str, default='random', choices=['random', 'greedy', 'alphabeta', 'human'],
                        help='player 1 type')
    parser.add_argument('--player2', type=str, default='random', choices=['random', 'greedy', 'alphabeta', 'human'],
                        help='player 2 type')
    parser.add_argument('--time', type=int, default=60,
                        help='time limit for each player in seconds')
    args = parser.parse_args()
    
    if args.player1 == 'random':
        player1 = RandomPlayer()
    elif args.player1 == 'greedy':
        player1 = GreedyPlayer()
    elif args.player1 == 'alphabeta':
        player1 = AlphaBetaPlayer()
    else:
        player1 = HumanPlayer()
    
    if args.player2 == 'random':
        player2 = RandomPlayer()
    elif args.player2 == 'greedy':
        player2 = GreedyPlayer()
    elif args.player2 == 'alphabeta':
        player2= AlphaBetaPlayer()
    else:
        player2 = HumanPlayer()
        
    game = OthelloGame(player1, player2, args.time)
    game.start_game()

if __name__ == '__main__':
    main()
