#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria
# SPDX-License-Identifier: Apache-2.0

"""!
Domain randomization of Upkie environments.
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np
from numpy.typing import NDArray
from scipy.spatial.transform import Rotation as ScipyRotation


@dataclass
class InitRandomization:

    """!
    Domain randomization parameters for Upkie's initial state.
    """

    roll: float = 0.0
    pitch: float = 0.0
    x: float = 0.0
    z: float = 0.0
    v_x: float = 0.0
    v_z: float = 0.0
    omega_x: float = 0.0
    omega_y: float = 0.0

    def update(
        self,
        roll: Optional[float] = None,
        pitch: Optional[float] = None,
        x: Optional[float] = None,
        z: Optional[float] = None,
        v_x: Optional[float] = None,
        v_z: Optional[float] = None,
        omega_x: Optional[float] = None,
        omega_y: Optional[float] = None,
    ) -> None:
        if roll is not None:
            self.roll = roll
        if pitch is not None:
            self.pitch = pitch
        if x is not None:
            self.x = x
        if z is not None:
            self.z = z
        if v_x is not None:
            self.v_x = v_x
        if v_z is not None:
            self.v_z = v_z
        if omega_x is not None:
            self.omega_x = omega_x
        if omega_y is not None:
            self.omega_y = omega_y

    def sample_orientation(self, np_random) -> ScipyRotation:
        yaw_pitch_roll_bounds = np.array([0.0, self.pitch, self.roll])
        yaw_pitch_roll = np_random.uniform(
            low=-yaw_pitch_roll_bounds,
            high=+yaw_pitch_roll_bounds,
            size=3,
        )
        return ScipyRotation.from_euler("ZYX", yaw_pitch_roll)

    def sample_position(self, np_random) -> NDArray[float]:
        default_position = np.array([0.0, 0.0, 0.6])
        return default_position + np_random.uniform(
            low=np.array([-self.x, 0.0, 0.0]),
            high=np.array([+self.x, 0.0, self.z]),
            size=3,
        )

    def sample_linear_velocity(self, np_random) -> NDArray[float]:
        return np_random.uniform(
            low=np.array([-self.v_x, 0.0, -self.v_z]),
            high=np.array([+self.v_x, 0.0, +self.v_z]),
            size=3,
        )

    def sample_angular_velocity(self, np_random) -> NDArray[float]:
        return np_random.uniform(
            low=np.array([-self.omega_x, -self.omega_y, 0.0]),
            high=np.array([+self.omega_x, +self.omega_y, 0.0]),
            size=3,
        )
