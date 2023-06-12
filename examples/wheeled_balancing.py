#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria

"""Smallest example: balancing using a proportional wheel controller."""

import gym
import numpy as np

import upkie.envs

upkie.envs.register()

if __name__ == "__main__":
    with gym.make("UpkieWheelsEnv-v3", frequency=200.0) as env:
        observation = env.reset()  # connects to the spine
        action = np.zeros(env.action_space.shape)
        for step in range(1_000_000):
            observation, reward, done, _ = env.step(action)
            if done:
                observation = env.reset()
            pitch = observation[0]
            action[0] = 10.0 * pitch
