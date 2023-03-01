"""Uses Pygame to launch an interactive game of connect four against a random agent (controlled via mouse).

Usage: python connect_four_interactive.py

Author: Elliot Tower (https://github.com/elliottower)
"""

import argparse
import sys
import time

import numpy as np
import pygame

from pettingzoo.classic import connect_four_v3


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--seed", type=int, default=None, help="Set random seed for board and policy"
    )
    parser.add_argument(
        "--no-cpu",
        action="store_true",
        help="Flag to disable CPU players and play as both teams",
    )
    parser.add_argument(
        "--player",
        type=int,
        default=0,
        choices=[0, 1],
        help="Choose which player to play as: 0 to play as red and go first, 1 to play as black and go second",
    )

    return parser


def get_args() -> argparse.Namespace:
    parser = get_parser()
    return parser.parse_known_args()[0]


if __name__ == "__main__":
    args = get_args()

    env = connect_four_v3.env(render_mode="human")
    if args.seed is not None:
        env.reset(seed=args.seed)
        np.random.seed(args.seed)
    else:
        env.reset()

    env.render()  # need to render the environment before pygame can take user input

    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()
        if termination or truncation:
            print(
                f"{'Terminated.' if termination else 'Truncated.'} Reward ({agent}): {reward}"
            )
            env.step(None)
        else:
            if agent == env.agents[args.player] or args.no_cpu:
                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        pygame.display.quit()
                        sys.exit()
                    mousex, mousey = pygame.mouse.get_pos()
                    if 50 <= mousex < 220:
                        action = 0
                    elif 220 <= mousex < 390:
                        action = 1
                    elif 390 <= mousex < 560:
                        action = 2
                    elif 560 <= mousex < 730:
                        action = 3
                    elif 730 <= mousex < 900:
                        action = 4
                    elif 900 <= mousex < 1070:
                        action = 5
                    elif 1070 <= mousex < 1240:
                        action = 6
                    env.unwrapped.preview[agent] = action
                    env.render()
                    pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        env.unwrapped.preview[agent] = -1
                        break
            else:
                action = env.action_space(agent).sample(mask=observation["action_mask"])
                time.sleep(0.25)
            env.step(action)
