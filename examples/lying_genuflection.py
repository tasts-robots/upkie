#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria

"""Genuflect while lying on a horizontal floor."""

import gym
import numpy as np

import upkie.envs

nb_genuflections = 10
genuflection_steps = 200
amplitude = 1.0  # in radians

config = {
    "bullet": {
        "orientation_init_base_in_world": [0.707, 0.0, -0.707, 0.0],
        "position_init_base_in_world": [0.0, 0.0, 0.1],
    }
}

if __name__ == "__main__":
    upkie.envs.register()
    with gym.make("UpkieServosEnv-v2", config=config, frequency=200.0) as env:
        observation = env.reset()
        action = np.zeros(env.action_space.shape)
        for step in range(nb_genuflections * genuflection_steps):
            observation, _, _, _ = env.step(action)
            x = float(step % genuflection_steps) / genuflection_steps
            y = 4.0 * x * (1.0 - x)  # in [0, 1]
            A = amplitude  # in radians
            action[[0, 1, 3, 4]] = A * y * np.array([1.0, -2.0, -1.0, 2.0])
