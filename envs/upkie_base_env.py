#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria
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

import abc
from os import path
from typing import Dict, Optional, Tuple, Union

import gym
import numpy as np
import yaml
from vulp.spine import SpineInterface

from upkie_locomotion.observers.base_pitch import compute_base_pitch_from_imu


class UpkieBaseEnv(abc.ABC, gym.Env):

    """!
    Base class for Upkie environments.

    This class implements "dict_" variants of the standard act, observe and
    reset functions from the Gym API. Child classes are responsible for
    implementing their own act, observe and reset functions.

    The base environment has the following attributes:

    - ``_config``: Configuration dictionary, also sent to the spine.
    - ``_spine``: Internal spine interface.

    @note This environment is made to run on a single CPU thread rather than on
    GPU/TPU. The downside for reinforcement learning is that computations are
    not massively parallel. The upside is that it simplifies deployment to the
    real robot, as it relies on the same spine interface that runs on Upkie.
    """

    _config: dict
    _spine: SpineInterface

    def __init__(
        self,
        config: dict,
        fall_pitch: float,
        shm_name: str,
    ) -> None:
        """!
        Initialize environment.

        @param config Configuration dictionary, also sent to the spine.
        @param shm_name Name of shared-memory file.
        """
        if config is None:
            envs_dir = path.dirname(__file__)
            with open(f"{envs_dir}/spine.yaml", "r") as fh:
                config = yaml.safe_load(fh)
        self._config = config
        self._fall_pitch = fall_pitch
        self._spine = SpineInterface(shm_name)

    def close(self) -> None:
        """!
        Stop the spine properly.
        """
        self._spine.stop()

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        return_info: bool = False,
        options: Optional[dict] = None,
    ) -> Union[np.ndarray, Tuple[np.ndarray, Dict]]:
        """!
        Resets the spine and get an initial observation.

        @param seed Will be used once we upgrade to gym >= 0.21.0.
        @param return_info If true, return an extra info dictionary.
        @param options Currently unused.
        @returns
            - ``observation``: the initial vectorized observation.
            - ``info``: an optional dictionary containing extra information.
                It is only returned if ``return_info`` is set to true.
        """
        # super().reset(seed=seed)  # we are pinned at gym==0.21.0
        self._spine.stop()
        self._spine.start(self._config)
        self._spine.get_observation()  # might be a pre-reset observation
        observation_dict = self._spine.get_observation()
        self.parse_first_observation(observation_dict)
        observation = self.vectorize_observation(observation_dict)
        if not return_info:
            return observation
        else:  # return_info
            return observation, {}

    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, dict]:
        """!
        Run one timestep of the environment's dynamics. When end of episode is
        reached, you are responsible for calling `reset()` to reset the
        environment's state.

        @param action Action from the agent.
        @returns
            - ``observation``: Agent's observation of the environment.
            - ``reward``: Amount of reward returned after previous action.
            - ``done``: Whether the agent reaches the terminal state, which can
              be a good or a bad thing. If true, the user needs to call
              :func:`reset()`.
            - ``info``: Contains auxiliary diagnostic information (helpful for
              debugging, logging, and sometimes learning).
        """
        action_dict = self.compute_action_dict(action)
        self._spine.set_action(action_dict)
        observation_dict = self._spine.get_observation()
        imu = observation_dict["imu"]
        pitch = compute_base_pitch_from_imu(imu["orientation"])
        observation = self.vectorize_observation(observation_dict)
        reward = self.reward.get(observation)
        done = self.detect_fall(pitch)
        info = {
            "action": action_dict,
            "observation": observation_dict,
        }
        return observation, reward, done, info

    def detect_fall(self, pitch: float) -> bool:
        """!
        Detect a fall based on the body-to-world pitch angle.

        @param pitch Current pitch angle in [rad].
        @returns True if and only if a fall is detected.
        """
        return abs(pitch) > self._fall_pitch

    @abc.abstractmethod
    def parse_first_observation(self, observation_dict: dict) -> None:
        """!
        Parse first observation after the spine interface is initialize.

        @param observation_dict First observation.
        """

    @abc.abstractmethod
    def vectorize_observation(self, observation_dict: dict) -> np.ndarray:
        """!
        Extract observation vector from a full observation dictionary.

        @param observation_dict Full observation dictionary from the spine.
        @returns Observation vector.
        """

    @abc.abstractmethod
    def dictionarize_action(self, action: np.ndarray) -> dict:
        """!
        Convert action vector into a spine action dictionary.

        @param action Action vector.
        @returns Action dictionary.
        """
