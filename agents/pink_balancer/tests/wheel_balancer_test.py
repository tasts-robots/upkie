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

"""Test main balancer functions."""

import os
import unittest

import gin

from agents.pink_balancer.wheel_balancer import WheelBalancer


class TestWholeBodyController(unittest.TestCase):
    def test_init(self):
        agent_dir = os.path.dirname(os.path.dirname(__file__))
        gin.parse_config_file(f"{agent_dir}/config/common.gin")
        gin.parse_config_file(f"{agent_dir}/config/bullet.gin")
        balancer = WheelBalancer(wheel_radius=1.0)
        self.assertEquals(balancer.wheel_radius, 1.0)


if __name__ == "__main__":
    unittest.main()
