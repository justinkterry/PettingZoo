from pettingzoo.utils.conversions import parallel_wrapper_fn

from ._mpe_utils.simple_env import SimpleEnv, make_env
from .scenarios.simple_world_comm import Scenario

"""
This environment is similar to simple_tag, except there is food (small blue balls) that the good agents are rewarded for being near, there are 'forests' that hide agents inside from being seen, and there is a ‘leader adversary' that can see the agents at all times and can communicate with the other adversaries to help coordinate the chase. By default, there are 2 good agents, 3 adversaries, 1 obstacles, 2 foods, and 2 forests.

In particular, the good agents reward, is -5 for every collision with an adversary, -2 x bound by the `bound` function described in simple_tag, +2 for every collision with a food, and -0.05 x minimum distance to any food. The adversarial agents are rewarded +5 for collisions and -0.1 x minimum distance to a good agent. s

Good agent observations: `[self_vel, self_pos, landmark_rel_positions, other_agent_rel_positions, other_agent_velocities, self_in_forest]`

Normal adversary observations:`[self_vel, self_pos, landmark_rel_positions, other_agent_rel_positions, other_agent_velocities, self_in_forest, leader_comm]`

Adversary leader observations: `[self_vel, self_pos, landmark_rel_positions, other_agent_rel_positions, other_agent_velocities, leader_comm]`

*Note that when the forests prevent an agent from being seen, the observation of that agents relative position is set to (0,0).*

Good agent action space: `[no_action, move_left, move_right, move_down, move_up]`

Normal adversary action space: `[no_action, move_left, move_right, move_down, move_up]`

Adversary leader discrete action space: `[say_0, say_1, say_2, say_3] X [no_action, move_left, move_right, move_down, move_up]`

Where X is the Cartesian product (giving a total action space of 50).

Adversary leader continuous action space: `[no_action, move_left, move_right, move_down, move_up, say_0, say_1, say_2, say_3]`

### Arguments

:param num_good:  number of good agents
:param num_adversaries:  number of adversaries
:param num_obstacles:  number of obstacles
:param num_food:  number of food locations that good agents are rewarded at
:param max_cycles:  number of frames (a step for each agent) until game terminates
:param num_forests: number of forests that can hide agents inside from being seen
:param continuous_actions: Whether agent action spaces are discrete(default) or continuous
"""

class raw_env(SimpleEnv):
    def __init__(self, num_good=2, num_adversaries=4, num_obstacles=1, num_food=2, max_cycles=25, num_forests=2, continuous_actions=False):
        scenario = Scenario()
        world = scenario.make_world(num_good, num_adversaries, num_obstacles, num_food, num_forests)
        super().__init__(scenario, world, max_cycles, continuous_actions)
        self.metadata['name'] = "simple_world_comm_v2"


env = make_env(raw_env)
parallel_env = parallel_wrapper_fn(env)
