import time

import arcade

from src.reinforcement.agent import Agent
from src.reinforcement.environment import TetrisEnvironment
from src.game.tetrominos.tetrominos_factory import TetrominosFactory
from src.game.window import TetrisWindow

LINE_COUNT = 20
COLUMN_COUNT = 10

PIECES = TetrominosFactory.create_tetrominos()

if __name__ == '__main__':
    wants_graphic_interface = True
    wants_to_display_board = False

    env = TetrisEnvironment(LINE_COUNT, COLUMN_COUNT, PIECES)
    agent = Agent(env)

    if wants_graphic_interface:
        window = TetrisWindow(agent, wants_to_display_board)
        window.setup()
        arcade.run()
    else:
        iteration_wanted = 50
        iteration = 0
        agent.reset()

        for i in range(iteration_wanted):
            while not agent.is_over:
                agent.step()
                agent.print_board_if_needed(wants_to_display_board)
                time.sleep(0.2)
            agent.reset()
            iteration += 1
            print(f"#{iteration:04d} Score : {agent.score:.2f} T°C : {agent.exploration:.2f}")
