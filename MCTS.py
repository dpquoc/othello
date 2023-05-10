import logging
import math
import copy

import numpy as np

from utils import *
from OthelloBoard import OthelloBoard
from NNet import NNetWrapper
EPS = 1e-8

log = logging.getLogger(__name__)






class MCTS():

    def __init__(self, othello_board, nnet, args):
        self.othello_board = othello_board
        self.nnet = nnet
        self.args = args
        self.Qsa = {}
        self.Nsa = {}
        self.Ns = {}
        self.Ps = {}

        self.Es = {}  
        self.Vs = {}  

    def getActionProb(self, canonicalBoard, temp=1):
        for i in range(self.args.numMCTSSims):
            self.search(canonicalBoard)

        self.othello_board = OthelloBoard(canonicalBoard)
        
        s = self.othello_board.stringRepresentation()
        counts = [self.Nsa[(s, a)] if (s, a) in self.Nsa else 0 for a in range(65)]

        if temp == 0:
            bestAs = np.array(np.argwhere(counts == np.max(counts))).flatten()
            bestA = np.random.choice(bestAs)
            probs = [0] * len(counts)
            probs[bestA] = 1
            return probs

       
        
        counts = [x ** (1. / temp) for x in counts]
        counts_sum = float(sum(counts))
        
        probs = [x / counts_sum for x in counts]
        return probs

    def search(self, canonicalBoard):
    
        self.othello_board = OthelloBoard(canonicalBoard)
        
        s = self.othello_board.stringRepresentation()

        if s not in self.Es:
            self.Es[s] = self.othello_board.getGameEnded(1)
        if self.Es[s] != 0:
            # terminal node
            return -self.Es[s]
            
        if s not in self.Ps:
            # leaf node
            self.Ps[s], v = self.nnet.predict(canonicalBoard)
            valids = self.othello_board.getValidMoves(1)
            self.Ps[s] = self.Ps[s] * valids  # masking invalid moves
            sum_Ps_s = np.sum(self.Ps[s])
            if sum_Ps_s > 0:
                self.Ps[s] /= sum_Ps_s  # renormalize
            else:
                log.error("All valid moves were masked, doing a workaround.")
                self.Ps[s] = self.Ps[s] + valids
                self.Ps[s] /= np.sum(self.Ps[s])

            self.Vs[s] = valids
            self.Ns[s] = 0
            return -v

        valids = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1

        # pick the action with the highest upper confidence bound
        for a in range(65):
            if valids[a]:
                if (s, a) in self.Qsa:
                    u = self.Qsa[(s, a)] + self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s]) / (
                            1 + self.Nsa[(s, a)])
                else:
                    u = self.args.cpuct * self.Ps[s][a] * math.sqrt(self.Ns[s] + EPS)  # Q = 0 ?

                if u > cur_best:
                    cur_best = u
                    best_act = a

        a = best_act
        
    
        next_s, next_player = self.othello_board.getNextState(a, 1)
        next_s = next_s * next_player

        v = self.search(next_s)

        if (s, a) in self.Qsa:
            self.Qsa[(s, a)] = (self.Nsa[(s, a)] * self.Qsa[(s, a)] + v) / (self.Nsa[(s, a)] + 1)
            self.Nsa[(s, a)] += 1

        else:
            self.Qsa[(s, a)] = v
            self.Nsa[(s, a)] = 1

        self.Ns[s] += 1
        return -v


args = dotdict({
    'numIters': 1000,
    'numEps': 100,              # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,        #
    'updateThreshold': 0.6,     # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'maxlenOfQueue': 200000,    # Number of game examples to train the neural networks.
    'numMCTSSims': 25,          # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,         # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,

    'checkpoint': './temp/',
    'load_model':True,
    'load_folder_file': ('pretrained_models/othello/pytorch/','model.pth'),
    'numItersForTrainExamplesHistory': 20,

})


# # Board size
# BOARD_SIZE = 8

# # Initial state of the board
# board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

# # Add starting pieces
# board[3][3] = -1
# board[4][4] = -1
# board[3][4] = 1
# board[4][3] = 1

# a = NNetWrapper() 
# a.load_checkpoint('model.pth')

# print(board)
# index = np.argmax(MCTS(OthelloBoard(), a, args).getActionProb(board, 1))
# print((int(index/8), index%8))