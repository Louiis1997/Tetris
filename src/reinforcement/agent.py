import os
import pickle
from random import *

from src.game.tetrominos.piece import Piece
import numpy as np
from sklearn.neural_network import MLPRegressor

LEFT = 'L'
RIGHT = 'R'
ROTATE = 'U'
NONE = 'N'
ACTIONS = [LEFT, RIGHT, ROTATE, NONE]


def clear_console():
    """Clear console"""
    os.system('cls' if os.name == 'nt' else 'clear')


class Agent:
    def __init__(self, environment, alpha=1, gamma=1, exploration=0, cooling_rate=0.99):
        self.__environment = environment
        self.reset(False)
        self.__alpha = alpha
        self.__gamma = gamma
        self.__exploration = exploration
        self.__cooling_rate = cooling_rate

        self.__history = []
        self.__state = None
        self.__score = 0

        # Initialisation du réseau de neurones
        # Ici : 1 couche cachée de 2000 neurones
        self.__mlp = MLPRegressor(hidden_layer_sizes=2000,
                                  activation='tanh',
                                  solver='sgd',
                                  learning_rate_init=alpha,
                                  max_iter=1,
                                  warm_start=True)
        self.__mlp.fit([[0]], [[0] * len(ACTIONS)])

        self.is_over = False

    def state_to_vector(self, state):
        x = round(state / pow(10, len(str(abs(state)))), 2)
        return [x]

    def best_action(self):
        if uniform(0, 1) < self.__exploration:
            self.__exploration *= self.__cooling_rate
            index = randrange(len(ACTIONS))
        else:
            qvector = self.__mlp.predict([self.state_to_vector(self.__state)])[0]
            index = np.argmax(qvector)

        return index, ACTIONS[index]

    def reset(self, append_score=True):
        if append_score:
            self.__history.append(self.__score)
        self.__state = None
        self.__score = 0
        self.is_over = False
        self.__environment.reset(self.__environment.height, self.__environment.width)

    def heat(self):
        self.__exploration = 1

    @property
    def environment(self):
        return self.__environment

    @property
    def score(self):
        return self.__score

    @property
    def exploration(self):
        return self.__exploration

    @property
    def history(self):
        return self.__history

    def load(self, filename):
        with open(filename, 'rb') as file:
            try:
                self.__mlp, self.__history = pickle.load(file)
            except EOFError:
                print("/!\\ The file is empty")
            except Exception as e:
                print(f"/!\\ Error while loading the file : {e}")

            file.close()

    def save(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump((self.__mlp, self.__history), file)
            file.close()

    def safe_move_down(self, current_piece: Piece) -> bool:
        """Move down if possible"""
        if self.__environment.entering_in_collision(current_piece, True, False, False) is False:
            self.__environment.move_down(current_piece)
            return True
        return False

    def print_board_if_needed(self, should_display_board):
        if should_display_board:
            self.__environment.print_board()

    def update_current_states(self):
        # The current state is the hash of :
        #   - The current piece (piece and rotation)
        #   - The radar of the piece (witch are 2 and are 3height x 4width)
        #   - The y position of the current piece on the board
        current_piece_blocks = [(block.x - self.__environment.get_current_piece().current_matrix_position_in_board[0],
                                 block.y - self.__environment.get_current_piece().current_matrix_position_in_board[1])
                                for block in self.__environment.get_current_piece().blocks]
        radar = [value for value in self.__environment.states_1.values()]

        ys = [block.y for block in self.__environment.get_current_piece().blocks]

        self.__state = hash((tuple(current_piece_blocks), tuple(radar), tuple(ys)))

    def set_current_piece(self, current_piece):
        self.__environment.set_current_piece(current_piece)

    def get_current_piece(self):
        return self.__environment.get_current_piece()

    def step(self):
        """Do a step"""
        # TODO -> Implement reinforcement learning
        # TODO      -> Implement Q-learning
        # OR
        # TODO      -> Implement Neural Network
        # TODO      -> BEST OPTION -> BOTH
        action = None
        rewards = 0

        for movement in range(10):
            self.update_current_states()
            i_action, action = self.best_action()
            current_piece, reward = self.__environment.do(action)
            reward *= 1E-3

            maxQ = max(self.__mlp.predict([self.state_to_vector(self.__state)])[0])
            expected = reward + self.__gamma * maxQ

            qvector = self.__mlp.predict([self.state_to_vector(self.__state)])[0]
            # qvector : Q(s, a1), Q(s, a2)...
            # i_action : index de l'action effectivement réalisée
            qvector[i_action] = expected
            self.__mlp.fit([self.state_to_vector(self.__state)], [qvector])

            self.__score += reward

            self.set_current_piece(current_piece)
            if self.__environment.entering_in_collision(current_piece, True, False, False) is True:
                break

        if self.safe_move_down(self.get_current_piece()) is False:
            self.__environment.clear_lines()

            self.__environment.next_piece()
            self.__environment.place_piece_at_base_position(self.get_current_piece())

            if self.__environment.entering_in_collision(self.get_current_piece(), down=False, left=False, right=False,
                                                        without_current_piece=False) is True:
                self.is_over = True
                return
            self.__environment.place_piece_in_board(self.get_current_piece())
