import os

import matplotlib.pyplot as plt
import arcade

from src.reinforcement.agent import Agent, clear_console
from src.reinforcement.environment import TetrisEnvironment
from src.game.tetrominos.tetrominos_factory import TetrominosFactory
from src.game.window import TetrisWindow, SAVE_FILES, get_filename, WANTS_NEW_SAVE_FILE, SAVE_FOLDER

LINE_COUNT = 20
COLUMN_COUNT = 10

PIECES = TetrominosFactory.create_tetrominos()

if __name__ == '__main__':
    iteration_wanted = 5
    wants_graphic_interface = False
    wants_to_display_board = False

    env = TetrisEnvironment(LINE_COUNT, COLUMN_COUNT, PIECES)
    agent = Agent(env, alpha=0.5, gamma=0.9, exploration=0.1, cooling_rate=0.99)

    filename = get_filename(SAVE_FILES, WANTS_NEW_SAVE_FILE)

    if os.listdir(SAVE_FOLDER) != 0 and os.path.exists(filename):
        print('Load file.')
        agent.load(filename)
        plt.plot(agent.history)
        plt.show()

    if wants_graphic_interface:
        window = TetrisWindow(agent, wants_to_display_board)
        window.setup()
        arcade.run()

    else:
        iteration = 0
        agent.reset(False)

        for i in range(iteration_wanted):
            while not agent.is_over:
                agent.step()
                agent.print_board_if_needed(wants_to_display_board)
            iteration += 1
            clear_console()
            agent.save(filename)
            agent.reset()
            print(f"#{iteration:04d} Score : {agent.score:.2f} T°C : {agent.exploration:.2f}")
