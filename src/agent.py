import random
from typing import Dict, Any

import numpy as np


class TetrisAgent:
    __state: dict[Any, Any]
    __temperature: float
    state_size: int

    def __init__(self, env, state_size, alpha=0.1, gamma=0.01):
        self.__env = env
        self.__qtable = {}

        self.__alpha = alpha
        self.__gamma = gamma

        self.state_size = state_size

        self.__temperature = 0.0

        self.reset()

    def reset(self):
        self.__state = {}

    def predict_value(self, state):
        """Predict the value of a state."""
        print("Predicting value for state : ", state)
        return 1 / state[0][2]  # TODO

    def best_state(self, states):
        """Get the best state from a list of states."""
        max_value = None
        best_state = None

        print("States : ", states)

        if random.random() < self.__temperature:
            # Explore
            return random.choice(list(states.values()))

        else:
            for state in states:
                value = self.predict_value(np.reshape(state, [1, self.state_size]))
                print("Max value : ", max_value)
                print("Value : ", value)
                if not max_value or value > max_value:
                    max_value = value
                    best_state = state

        return best_state
