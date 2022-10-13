from src.agent import TetrisAgent
from src.environment import TetrisEnvironment, BOARD_HEIGHT, BOARD_WIDTH

if __name__ == '__main__':
    env = TetrisEnvironment(BOARD_HEIGHT, BOARD_WIDTH)

    render_every = 50
    episodes = 1
    max_steps = None
    render_delay = None

    agent = TetrisAgent(env, env.get_state_size())  # TODO: more variables

    scores = []

    for episode in range(episodes):
        current_state = env.reset(BOARD_HEIGHT, BOARD_WIDTH)
        done = False
        steps = 0

        if render_every and episode % render_every == 0:
            render = True
        else:
            render = False

        # Game
        while not done and (not max_steps or steps < max_steps):
            next_states = env.get_next_states()
            best_state = agent.best_state(next_states.values())  # TODO

            best_action = None
            for action, state in next_states.items():
                if state == best_state:
                    best_action = action
                    break

            reward, done = env.do(best_action[0], best_action[1], render=render,
                                  render_delay=render_delay)

            # agent.add_to_memory(current_state, next_states[best_action], reward, done) # TODO
            current_state = next_states[best_action]
            steps += 1

        scores.append(env.score)
