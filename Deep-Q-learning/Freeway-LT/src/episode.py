import time
from typing import List
import src.agents as agents
class Episode(object):

    def __init__(self):
        self.S = []
        self.A = []
        self.R = []
        self.scores = []

        self.length = 0

    def add_step(self, state, action, reward, score):
        self.S.append(state)
        self.A.append(action)
        self.R.append(reward)
        self.scores.append(score)

        self.length += 1

    def get_final_score(self):
        return max(self.scores)

    def get_total_reward(self):
        return sum(self.R)

    def print_final_score(self):
        final_score = self.get_final_score()
        print(f"Final Score at t = {self.length}: {int(final_score)}")

def generate_episode(env,
                     reduce_state,
                     reward_policy,
                     agent: agents.Agent,
                     RAM_mask: List[int],
                     render: bool=False) -> Episode:
    epi = Episode()
    game_over = False
    state = env.reset()
    state = reduce_state(state[0])[RAM_mask].data.tobytes()  # Select useful bytes
    action = agent.act(state)

    score = 0

    while not game_over:
        if render:
            time.sleep(0.005)
            env.render()

        ob, reward, game_over, _ = env.step(action)

        ob = reduce_state(ob)
        reward = reward_policy(reward, ob, action)
        if reward == reward_policy.REWARD_IF_CROSS:
            score += 1

        epi.add_step(state, action, reward, score)
        state = ob[RAM_mask].data.tobytes()
        action = agent.act(state)  # Next action

    return epi