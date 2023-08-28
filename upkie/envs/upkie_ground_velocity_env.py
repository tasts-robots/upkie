#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
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

import math
from typing import Optional

import numpy as np
from gymnasium import spaces

from .reward import Reward
from .survival_reward import SurvivalReward
from .upkie_pendulum_env import UpkiePendulumEnv


class UpkieGroundVelocityEnv(UpkiePendulumEnv):

    """!
    Environment where Upkie balances by ground velocity control.

    The environment id is ``UpkieGroundVelocityEnv-v1``.

    ### Action space

    Vectorized actions have the following structure:

    <table>
        <tr>
            <td><strong>Index</strong></td>
            <td><strong>Description</strong></td>
            </tr>
        <tr>
            <td>``0``</td>
            <td>Ground velocity in [m] / [s].</td>
        </tr>
    </table>

    ### Observation space

    Vectorized observations have the following structure:

    <table>
        <tr>
            <td><strong>Index</strong></td>
            <td><strong>Description</strong></td>
        </tr>
        <tr>
            <td>0</td>
            <td>Pitch angle of the base with respect to the world vertical, in
            radians. This angle is positive when the robot leans forward.</td>
        </tr>
        <tr>
            <td>1</td>
            <td>Position of the average wheel contact point, in meters.</td>
        </tr>
        <tr>
            <td>2</td>
            <td>Body angular velocity of the base frame along its lateral axis,
            in radians per seconds.</td>
        </tr>
        <tr>
            <td>3</td>
            <td>Velocity of the average wheel contact point, in meters per
            seconds.</td>
        </tr>
    </table>

    ### Attributes

    The environment class defines the following attributes:

    - ``fall_pitch``: Fall pitch angle, in radians.
    - ``max_ground_velocity``: Maximum commanded ground velocity in m/s.
    - ``version``: Environment version number.
    - ``wheel_radius``: Wheel radius in [m].

    """

    fall_pitch: float
    max_ground_velocity: float
    version: int = 1
    wheel_radius: float

    LEG_JOINTS = [
        f"{side}_{joint}"
        for side in ("left", "right")
        for joint in ("hip", "knee")
    ]

    def __init__(
        self,
        reward: Optional[Reward] = None,
        fall_pitch: float = 1.0,
        frequency: float = 200.0,
        max_ground_velocity: float = 1.0,
        shm_name: str = "/vulp",
        spine_config: Optional[dict] = None,
        wheel_radius: float = 0.06,
    ):
        """!
        Initialize environment.

        @param reward Reward function.
        @param fall_pitch Fall pitch angle, in radians.
        @param frequency Regulated frequency of the control loop, in Hz.
        @param max_ground_velocity Maximum commanded ground velocity in m/s.
        @param shm_name Name of shared-memory file.
        @param spine_config Additional spine configuration overriding the
            defaults from ``//config:spine.yaml``. The combined configuration
            dictionary is sent to the spine at every :func:`reset`.
        @param wheel_radius Wheel radius in [m].
        """
        super().__init__(
            reward=reward if reward is not None else SurvivalReward(),
            fall_pitch=fall_pitch,
            frequency=frequency,
            shm_name=shm_name,
            spine_config=spine_config,
        )

        # gymnasium.Env: action_space
        self.action_space = spaces.Box(
            -np.float32(max_ground_velocity),
            +np.float32(max_ground_velocity),
            shape=(1,),
            dtype=np.float32,
        )

        self.wheel_radius = wheel_radius

    def dictionarize_action(self, action: np.ndarray) -> dict:
        """!
        Convert action vector into a spine action dictionary.

        @param action Action vector.
        @returns Action dictionary.
        """
        commanded_velocity: float = action[0]
        action_dict = {
            "servo": {
                joint: {
                    "position": self.init_position[joint],
                    "velocity": 0.0,
                }
                for joint in self.LEG_JOINTS
            }
        }
        action_dict["servo"]["left_wheel"] = {
            "position": math.nan,
            "velocity": +commanded_velocity / self.wheel_radius,
        }
        action_dict["servo"]["right_wheel"] = {
            "position": math.nan,
            "velocity": -commanded_velocity / self.wheel_radius,
        }
        return action_dict
