import logging
import math
import time
import numpy as np
from utils import *
from OthelloBoard import OthelloBoard
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

    def getActionProb(self, standardized_board, temp=1):
        start_time = time.time()
        for i in range(self.args.MCTS_iterations):
            if time.time() - start_time > 2.5:
                break
            
            self.search(standardized_board)
            

        self.othello_board = OthelloBoard(standardized_board)
        
        s = self.othello_board.string_represent()
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

    def search(self, standardized_board):
    
        self.othello_board = OthelloBoard(standardized_board)
        
        s = self.othello_board.string_represent()

        if s not in self.Es:
            self.Es[s] = self.othello_board.is_game_end(1)
        if self.Es[s] != 0:
            # terminal node
            return -self.Es[s]
            
        if s not in self.Ps:
            # leaf node
            self.Ps[s], v = self.nnet.predict(standardized_board)
            valids = self.othello_board.get_valid_moves(1)
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
        
    
        next_s, next_player = self.othello_board.get_next_state(a, 1)
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

