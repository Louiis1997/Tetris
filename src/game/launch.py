import os

import arcade

from src.reinforcement.agent import Agent, clear_console
from src.reinforcement.environment import TetrisEnvironment
from src.game.tetrominos.tetrominos_factory import TetrominosFactory
from src.game.window import TetrisWindow, FILE_AGENT

LINE_COUNT = 20
COLUMN_COUNT = 10

PIECES = TetrominosFactory.create_tetrominos()

if __name__ == '__main__':
    iteration_wanted = 1800
    wants_graphic_interface = False
    wants_to_display_board = False

    env = TetrisEnvironment(LINE_COUNT, COLUMN_COUNT, PIECES)
    agent = Agent(env)

    if os.path.exists(FILE_AGENT):
        agent.load(FILE_AGENT)

    if wants_graphic_interface:
        window = TetrisWindow(agent, wants_to_display_board)
        window.setup()
        arcade.run()

    else:
        iteration = 0
        agent.reset()

        for i in range(iteration_wanted):
            while not agent.is_over:
                agent.step()
                agent.save(FILE_AGENT)
                agent.print_board_if_needed(wants_to_display_board)
            agent.reset()
            iteration += 1
            clear_console()
            print(f"#{iteration:04d} Score : {agent.score:.2f} T°C : {agent.exploration:.2f}")
