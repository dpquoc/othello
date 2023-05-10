# Othello AI

This document provides an overview of an Othello AI implementation that utilizes both the Alpha-Beta Pruning and AlphaZero algorithms.

## Alpha-Beta Pruning

Alpha-Beta Pruning is a search algorithm used in game-playing AI to improve the performance of the minimax algorithm. It reduces the number of nodes that need to be evaluated by pruning branches of the game tree that are determined to be irrelevant. The algorithm maintains two values, alpha and beta, to keep track of the best possible scores for the maximizing and minimizing players, respectively. By pruning branches that cannot possibly affect the final decision, Alpha-Beta Pruning significantly reduces the search space.

## AlphaZero

AlphaZero is a machine learning algorithm that combines deep neural networks and Monte Carlo tree search (MCTS) to learn to play games. It doesn't rely on any prior human knowledge of the game and learns solely through self-play. AlphaZero uses a neural network to evaluate positions and perform simulations via MCTS to determine the best move. Through a process of reinforcement learning, it updates its neural network by playing numerous games against itself, gradually improving its play over time.

In the context of Othello, the AlphaZero algorithm can learn to make strategic moves and develop advanced gameplay strategies through self-play and reinforcement learning.

## Implementation

The Othello AI implementation incorporates both Alpha-Beta Pruning and AlphaZero algorithms. It uses Alpha-Beta Pruning during the search to efficiently explore the game tree and identify the best moves. Additionally, it leverages the AlphaZero algorithm to learn and improve its gameplay through self-play and reinforcement learning. The implementation includes:

- Game state representation
- Evaluation function based on neural networks
- Monte Carlo tree search for exploration
- Reinforcement learning to update neural networks
- Self-play to generate training data

By combining these algorithms, the Othello AI can make informed and strategic decisions, optimizing its gameplay and gradually improving its performance.

## Getting Started

To start the Othello game, follow these steps:

1. Install the necessary dependencies:

```
pip install -r requirements.txt
```

2. Run the game with the desired player type:

```
python main.py --player1 <player_type> --player2 <player_type>
```

Replace <player_type> with one of the following options:

* alphabeta: Play against the Alpha-Beta Pruning AI.
* alphazero: Play against the AlphaZero AI.
* greedy: Play against the Greedy AI.
* random: Play against the Random AI.
* human: Play against another human player.

Enjoy the Othello game against the chosen player type!

## Contributing
If you would like to contribute to this project, please feel free to submit a pull request or open an issue on GitHub. We welcome contributions from the community!