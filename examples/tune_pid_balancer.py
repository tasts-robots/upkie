#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Inria

"""Tune a pitch-position PI balancing controller from the command line."""

import multiprocessing as mp

import gymnasium as gym
import numpy as np
import valmix
from matplotlive import RecentPast

import upkie.envs

upkie.envs.register()


def make_plot(dt: float, max_pitch: float, max_position: float) -> RecentPast:
    plot = RecentPast(
        timestep=dt,
        duration=2.0,
        ylim=(-max_pitch, max_pitch),
        ylim_right=(-max_position, max_position),
    )
    plot.add_left("pitch", "b-")
    plot.left_axis.set_ylabel("Pitch (rad)", color="b")
    plot.left_axis.tick_params(axis="y", labelcolor="b")
    plot.left_axis.grid(True)
    plot.add_right("position", "g-")
    plot.right_axis.set_ylabel("Ground position (m)", color="g")
    plot.right_axis.tick_params(axis="y", labelcolor="g")
    plot.redraw()
    return plot


def main(pitch_kp, pitch_ki, position_kp, position_ki):
    pitch_integrator = 0.0
    position_integrator = 0.0
    with gym.make("UpkieGroundVelocity-v3", frequency=100.0) as env:
        dt = env.unwrapped.dt
        plot = make_plot(dt, 0.5, 0.5)
        observation, _ = env.reset()  # connects to the spine
        action = 0.0 * env.action_space.sample()  # 1D action: [velocity]
        for step in range(1_000_000):
            pitch = observation[0]
            position = observation[1]
            pitch_integrator += pitch * dt
            position_integrator += position * dt
            commanded_velocity = (
                pitch_kp.value * pitch
                + pitch_ki.value * pitch_integrator
                + position_kp.value * position
                + position_ki.value * position_integrator
            )
            action[0] = commanded_velocity
            observation, reward, terminated, truncated, _ = env.step(action)
            if terminated or truncated:
                observation, _ = env.reset()
                pitch_integrator = 0.0
                position_integrator = 0.0

            # Our signal that the TUI has closed :p
            if pitch_kp.value < -0.5:
                break

            # We update the plot in the control loop to keep the example short,
            # but in practice this should be handled in a lower-priority thread
            plot.send("pitch", pitch)
            plot.send("position", position)
            plot.update()


if __name__ == "__main__":
    # We wrap parameters we want to tune into multiprocessing values
    pitch_kp = mp.Value("f", 10.0)
    pitch_ki = mp.Value("f", 1.0)
    position_kp = mp.Value("f", 10.0)
    position_ki = mp.Value("f", 1.0)

    # Call the main function in a separate process
    main_process = mp.Process(
        target=main,
        args=(pitch_kp, pitch_ki, position_kp, position_ki),
    )
    main_process.start()

    # Display the terminal user interface in this process (blocking call)
    valmix.run(
        {
            "pitch_kp": (pitch_kp, np.arange(0.0, 20.0, 0.5)),
            "pitch_ki": (pitch_ki, np.arange(0.0, 10.0, 0.5)),
            "position_kp": (position_kp, np.arange(0.0, 20.0, 0.5)),
            "position_ki": (position_ki, np.arange(0.0, 10.0, 0.5)),
        }
    )

    # We are now done, let's signal the main function to break its loop
    pitch_kp.value = -1.0  # that's our signal :p
    main_process.join()
