import os
import sys
import time

import numpy as np

from utils import *

import torch

from OthelloNNet import OthelloNNet as onnet


sys.path.append('../../')
from utils import *

import torch

from OthelloNNet import OthelloNNet as onnet

class dotdict(dict):
    def __getattr__(self, name):
        return self[name]

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': torch.cuda.is_available(),
    'num_channels': 512,
})


class NNetWrapper():
    def __init__(self):
        self.nnet = onnet(args)
        self.board_x, self.board_y = (8,8)
        self.action_size = 8*8 + 1

        if args.cuda:
            self.nnet.cuda()

    def predict(self, board):
        """
        board: np array with board
        """
        # timing
        start = time.time()
        
        # preparing input
        board = torch.FloatTensor(board.astype(np.float64))
        if args.cuda: board = board.contiguous().cuda()
        board = board.view(1, self.board_x, self.board_y)
        self.nnet.eval()
        with torch.no_grad():
            pi, v = self.nnet(board)

        # print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return torch.exp(pi).data.cpu().numpy()[0], v.data.cpu().numpy()[0]
    
    def loss_pi(self, targets, outputs):
        return -torch.sum(targets * outputs) / targets.size()[0]

    def loss_v(self, targets, outputs):
        return torch.sum((targets - outputs.view(-1)) ** 2) / targets.size()[0]
    
    def load_checkpoint(self, filename='checkpoint.pth.tar'):
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        if not os.path.exists(filename):
            raise ("No model in path {}".format(filename))
        map_location = None if args.cuda else 'cpu'
        checkpoint = torch.load(filename, map_location=map_location)
        self.nnet.load_state_dict(checkpoint['state_dict'])


# # Board size
# BOARD_SIZE = 8

# # Initial state of the board
# board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)

# # Add starting pieces
# board[3][3] = -1
# board[4][4] = -1
# board[3][4] = 1
# board[4][3] = 1


# print(board)
# a = NNetWrapper() 
# a.load_checkpoint('model.pth')
# print(a.predict(board))