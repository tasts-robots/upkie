# Upkie wheeled biped

[![Build](https://img.shields.io/github/actions/workflow/status/tasts-robots/upkie/bazel.yml?branch=main)](https://github.com/tasts-robots/upkie/actions/workflows/bazel.yml)
[![Documentation](https://img.shields.io/badge/docs-online-brightgreen?logo=read-the-docs&style=flat)](https://tasts-robots.org/doc/upkie/)
[![Coverage](https://coveralls.io/repos/github/tasts-robots/upkie/badge.svg?branch=main)](https://coveralls.io/github/tasts-robots/upkie?branch=main)
[![Vulp](https://img.shields.io/badge/%F0%9F%A6%8A%20vulp-1.1.1-orange)](https://github.com/tasts-robots/vulp)
[![Chat](https://img.shields.io/badge/matrix-joint%20chat-%234eb899)](https://app.element.io/#/room/#tasts-robots:matrix.org)

Main repository to build and control **Upkie** wheeled bipeds. Made for Linux 🐧

Questions about using the code, contributing, or balancing robots in general are welcome in the [Discussions](https://github.com/tasts-robots/upkie/discussions) forum or on the [Chat](https://github.com/tasts-robots/upkie/discussions).

## Quick test

Run a simulated Upkie right away from the command line, no installation required:

<img src="https://user-images.githubusercontent.com/1189580/170496331-e1293dd3-b50c-40ee-9c2e-f75f3096ebd8.png" height="100" align="right" />

```console
$ git clone https://github.com/tasts-robots/upkie.git
$ cd upkie
$ ./start_test_balancer.sh
```

Connect a USB controller to move the robot around 🎮

## Example

```python
import gym
import loop_rate_limiters
import upkie.envs

upkie.envs.register()

with gym.make("UpkieWheelsEnv-v2") as env:
    observation = env.reset()
    action = 0.0 * env.action_space.sample()
    rate = loop_rate_limiters.RateLimiter(frequency=200.0)
    for step in range(1_000_000):
        observation, reward, done, _ = env.step(action)
        if done:
            observation = env.reset()
        pitch = observation[0]
        action[0] = 10.0 * pitch
        rate.sleep()
```

## Installation

### PyPI

[![PyPI version](https://img.shields.io/pypi/v/upkie)](https://pypi.org/project/upkie/)
[![PyPI downloads](https://pepy.tech/badge/upkie/month)](https://pepy.tech/project/upkie)

```console
$ pip install upkie
```

## Code overview

This repository uses [Bazel](https://bazel.build/) for building and testing. One benefit of this choice is that there is no dependency to install: Bazel builds everything locally in a local cache. Compilation will only take a while the first time.

Locomotion code is organized into *spines*, which communicate with the simulator or actuators using [Vulp](https://github.com/tasts-robots/vulp), and *agents*, the main programs that implement behaviors in Python. In the example above we ran the test balancer. We could also start the Bullet spine independently, and let it run waiting for agents to connect:

```console
$ ./tools/bazelisk run -c opt //spines:bullet -- --show
```

The ``-c opt`` argument to Bazel makes sure we compile optimized code, while the ``--show`` argument to the spine displays the Bullet visualization.

### Agents

<dl>
  <dt>Test balancer</dt>
  <dd>A baseline agent designed to check out Upkie's physical capabilities. It balances the robot using PD feedback from the head's pitch and wheel odometry to wheel velocities, plus a feedforward <a href="https://github.com/tasts-robots/upkie/blob/662d76180e03a855e8810d60eeb5b229c95b68fb/agents/test_balancer/wheel_balancer.py#L378-L400">non-minimum phase trick</a> for smoother transitions from standing to rolling.</dd>

  <dt>Pink balancer</dt>
  <dd>A more capable agent that combines wheeled balancing with inverse kinematics computed by <a href="https://github.com/tasts-robots/pink">Pink</a>. This is the controller that runs in the <a href="https://www.youtube.com/shorts/8b36XcCgh7s">first</a> <a href="https://www.youtube.com/watch?v=NO_TkHGS0wQ">two</a> videos of Upkie.</dd>

  <dt>PPO balancer</dt>
  <dd>An agent trained by reinforcement learning to balance with straight legs. Training uses the <code><a href="https://tasts-robots.org/doc/upkie/classenvs_1_1upkie__wheels__env_1_1UpkieWheelsEnv.html#details">UpkieWheelsEnv</a></code> gym environment and the PPO implementation from <a href="https://github.com/DLR-RM/stable-baselines3/">Stable Baselines3</a>.</dd>
</dl>

### Environments

<dl>
  <dt><code><a href="https://tasts-robots.org/doc/upkie/classenvs_1_1upkie__servos__env_1_1UpkieServosEnv.html#details">UpkieServosEnv</a></code></dt>
  <dd>Upkie with full observation and joint position-velocity-torque actions.</dd>
  <dt><code><a href="https://tasts-robots.org/doc/upkie/classenvs_1_1upkie__wheels__env_1_1UpkieWheelsEnv.html#details">UpkieWheelsEnv</a></code></dt>
  <dd>Upkie with full observation but only wheel velocity actions.</dd>
</dl>

Environments are single-threaded rather than vectorized. In return, they run as-is on the real robot.

### Observers

<img src="https://tasts-robots.org/doc/upkie/observers.png" align="right">

<dl>
  <dt><a href="https://tasts-robots.org/doc/upkie/classupkie__locomotion_1_1observers_1_1FloorContact.html#details">Floor contact</a></dt>
  <dd>Detect contact between the wheels and the floor. The Pink and test balancers use contact as a reset flag for their integrators, to avoid over-spinning the wheels while the robot is in the air.</dd>

  <dt><a href="https://tasts-robots.org/doc/upkie/classupkie__locomotion_1_1observers_1_1WheelContact.html#details">Wheel contact</a></dt>
  <dd>Detect contact between a given wheel and the floor.</dd>

  <dt><a href="https://tasts-robots.org/doc/upkie/classupkie__locomotion_1_1observers_1_1WheelOdometry.html#details">Wheel odometry</a></dt>
  <dd>Measure the relative motion of the floating base with respect to the floor. Wheel odometry is part of their secondary task (after keeping the head straight), which is to stay around the same spot on the floor.</dd>
</dl>

### Spines

<dl>
  <dt>Bullet</dt>
  <dd>Spawn Upkie in a <a href="http://bulletphysics.org/">Bullet</a> simulation. Resetting this spine moves the robot back to its initial configuration in this world.</dd>
  <dt>pi3hat</dt>
  <dd>Spine is made to be called from a Raspberry Pi with an onboard mjbots <a href="https://mjbots.com/products/mjbots-pi3hat-r4-4b">pi3hat</a>. Servos are stopped when the spine is stopped, and switch to <a href="https://github.com/mjbots/moteus/blob/main/docs/reference.md#theory-of-operation">position mode</a> (which is a position-velocity-torque controller) when the spine idles. Check out the <a href="https://tasts-robots.org/doc/vulp/classvulp_1_1spine_1_1StateMachine.html#details">spine state machine</a> for details.</dd>
</dl>

## See also

- [Project page on Hackaday](https://hackaday.io/project/185729-upkie-wheeled-biped-robot)
