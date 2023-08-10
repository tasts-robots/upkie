#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

import gymnasium as gym

from .reward import Reward
from .upkie_base_env import UpkieBaseEnv

__all__ = [
    "Reward",
    "UpkieBaseEnv",
    "register",
]

__envs__ = {}

try:
    from .upkie_servos_env import UpkieServosEnv

    __all__.append("UpkieServosEnv")
    __envs__["UpkieServosEnv"] = UpkieServosEnv
except ImportError as import_error:
    __envs__["UpkieServosEnv"] = import_error

try:
    from .upkie_wheels_env import UpkieWheelsEnv

    __all__.append("UpkieWheelsEnv")
    __envs__["UpkieWheelsEnv"] = UpkieWheelsEnv
except ImportError as import_error:
    __envs__["UpkieWheelsEnv"] = import_error


def register(max_episode_steps: int = 1_000_000_000) -> None:
    """!
    Register Upkie environments with Gymnasium.

    @param max_episode_steps Maximum number of steps per episode.
    """
    for env_name, Env in __envs__.items():
        if isinstance(Env, ModuleNotFoundError):
            import_error = str(Env)
            logging.warning(
                f"Cannot register {env_name} "
                f"due to missing dependency: {import_error}"
            )
            logging.info(
                "To install optional dependencies: "
                "``pip install upkie[the_full_monty]``"
            )
        else:  # valid gym.Env subclass
            gym.envs.registration.register(
                id=f"{env_name}-v{Env.version}",
                entry_point=f"upkie.envs:{env_name}",
                max_episode_steps=max_episode_steps,
            )
