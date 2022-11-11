import arcade

from src.reinforcement.agent import Agent
from src.reinforcement.environment import TetrisEnvironment
from src.game.tetrominos.tetrominos_factory import TetrominosFactory
from src.game.window import TetrisWindow

LINE_COUNT = 20
COLUMN_COUNT = 10

PIECES = TetrominosFactory.create_tetrominos()

if __name__ == '__main__':
    env = TetrisEnvironment(LINE_COUNT, COLUMN_COUNT, PIECES)
    agent = Agent(env)
    window = TetrisWindow(agent)
    window.setup()

    arcade.run()
