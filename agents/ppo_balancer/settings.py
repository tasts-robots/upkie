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

from dataclasses import dataclass
from typing import Optional, Tuple

import gin


@gin.configurable
@dataclass
class EnvSettings:
    """!
    Environment settings.
    """

    agent_frequency: int
    discounted_horizon_duration: float
    env_id: str
    init_pitch_rand: float
    max_episode_duration: float
    max_ground_accel: float
    max_ground_velocity: float
    seed: Optional[int]
    spine_frequency: int
    total_timesteps: int
    velocity_filter: Optional[float]
    velocity_filter_rand: Optional[Tuple[float, float]]


@gin.configurable
@dataclass
class PPOSettings:
    """PPO algorithm settings."""

    batch_size: int
    clip_range: float
    clip_range_vf: Optional[float]
    ent_coef: float
    gae_lambda: float
    learning_rate: float
    max_grad_norm: float
    n_epochs: int
    n_steps: int
    normalize_advantage: bool
    sde_sample_freq: int
    target_kl: Optional[float]
    use_sde: bool
    vf_coef: float
