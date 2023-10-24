#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2023 Inria
# SPDX-License-Identifier: Apache-2.0

from dataclasses import dataclass
from typing import Optional, Tuple, Dict

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
    init_rand: Dict[str, float]
    max_episode_duration: float
    max_ground_accel: float
    max_ground_velocity: float
    seed: Optional[int]
    spine_config: Dict
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
    learning_rate_steps: int
    max_grad_norm: float
    n_epochs: int
    n_steps: int
    net_arch_pi: Tuple[int, int]
    net_arch_vf: Tuple[int, int]
    normalize_advantage: bool
    sde_sample_freq: int
    target_kl: Optional[float]
    use_sde: bool
    vf_coef: float
