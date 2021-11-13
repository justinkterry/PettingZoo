import os

from .base_atari_env import BaseAtariEnv, base_env_wrapper_fn, parallel_wrapper_fn

"""
Mixed sum game involving scoring points in an unforgiving world. Careful positioning, timing,
and control is essential, as well as awareness of your opponent.

In Joust, you score points by hitting the opponent and NPCs when
you are above them. If you are below them, you lose a life.
In a game, there are a variety of waves with different enemies
and different point scoring systems. However, expect that you can earn
around 3000 points per wave.

[Official joust manual](https://atariage.com/manual_html_page.php?SoftwareLabelID=253)

#### Environment parameters

Environment parameters are common to all Atari environments and are described in the [base Atari documentation](../atari) .
"""

def raw_env(**kwargs):
    return BaseAtariEnv(game="joust", num_players=2, mode_num=None, env_name=os.path.basename(__file__)[:-3], **kwargs)


env = base_env_wrapper_fn(raw_env)
parallel_env = parallel_wrapper_fn(env)
