# Upkie wheeled biped robot

[![CI](https://github.com/tasts-robots/upkie/actions/workflows/bazel.yml/badge.svg)](https://github.com/tasts-robots/upkie/actions/workflows/bazel.yml)
[![Build instructions](https://img.shields.io/badge/build-instructions-brightgreen?logo=read-the-docs&style=flat)](https://github.com/tasts-robots/upkie/wiki)
[![Documentation](https://img.shields.io/badge/docs-online-brightgreen?style=flat)](https://tasts-robots.org/doc/upkie/)
[![Coverage](https://coveralls.io/repos/github/tasts-robots/upkie/badge.svg?branch=main)](https://coveralls.io/github/tasts-robots/upkie?branch=main)
[![PyPI version](https://img.shields.io/pypi/v/upkie)](https://pypi.org/project/upkie/)
[![Chat](https://img.shields.io/badge/matrix-chat-%234eb899)](https://app.element.io/#/room/#tasts-robots:matrix.org)

Build instructions and software for **Upkie** wheeled bipeds. Develop on Linux 🐧 or macOS 🍏, deploy to the robot's Raspberry Pi 🍓. Questions are welcome in the [Discussions](https://github.com/tasts-robots/upkie/discussions) forum or on the [Chat](https://app.element.io/#/room/#tasts-robots:matrix.org).

## Quick sim

If you have Python and a C++ compiler (setup one-liners: [Fedora](https://github.com/tasts-robots/upkie/discussions/100), [Ubuntu](https://github.com/tasts-robots/upkie/discussions/101)), you can run an Upkie simulation right from the command line. It won't install anything on your machine, as everything will run locally from the repository:

<img src="https://user-images.githubusercontent.com/1189580/170496331-e1293dd3-b50c-40ee-9c2e-f75f3096ebd8.png" height="100" align="right" />

```console
git clone https://github.com/tasts-robots/upkie.git
cd upkie
./start_wheel_balancer.sh
```

Click on the robot in the simulator window to apply external forces 😉

## Running a spine

Upkie's code is organized into *spines*, which communicate with the simulation or mjbots actuators, and *agents*, the programs that implement robot behaviors. We use [Bazel](https://bazel.build/) to build spines, both for simulation on your development computer or for running on the robot's Raspberry Pi. Bazel builds everything locally, does not install anything on your system, and makes sure that all versions of all dependencies are correct. Check out [this introduction](https://github.com/tasts-robots/vulp#readme) for more details.

### Simulation spine

In the example above we ran an agent called "wheel balancer". We could also start the simulation spine independently, and let it run waiting for agents to connect:

```console
./start_simulation.sh
```

This script is just an alias for a Bazel ``run`` command:

```console
./tools/bazelisk run -c opt //spines:bullet -- --show
```

The ``-c opt`` flag selects the optimized compilation mode. It is actually the default in this project, we just show it here for example.

### Robot spine

To run a spine on the robot, we first build it locally and upload it to the onboard Raspberry Pi:

```console
make build
make upload UPKIE_NAME=your_upkie
```

Next, log into the Pi and run a pi3hat spine:

```console
$ ssh foo@robot
foo@robot:~$ cd upkie
foo@robot:upkie$ make run_pi3hat_spine
```

Once the spine is running, you can run any agent in a separate shell on the robot, for example the wheel balancer:

```console
foo@robot:upkie$ make run_wheel_balancer
```

## Running a Python agent

We develop Python agents using the ``upkie`` interface distributed on PyPI. This interface is already [fast enough](https://github.com/tasts-robots/vulp#performance) for real-time control. To install it:

```console
pip install upkie
```

The repository ships a number of [agents](#agents) that have been tested on several Upkie's. You will find them in the [`agents/`](https://github.com/tasts-robots/upkie/tree/main/agents) directory. To run an agent, call its main Python script:

```console
python agents/<agent_name>/main.py <args>
```

For instance, to run the PPO balancer on the ``foobar`` policy:

```console
python agents/ppo_balancer/main.py foobar
```

## Example of a custom agent

You can develop your own agent using the [environments](#environments) distributed in ``upkie.envs``. For example, [run a spine](#running-a-spine) and try executing the following code in a Python interpreter:

```python
import gymnasium as gym
import upkie.envs

upkie.envs.register()

with gym.make("UpkieWheelsEnv-v4", frequency=200.0) as env:
    observation = env.reset()
    action = 0.0 * env.action_space.sample()
    for step in range(1_000_000):
        observation, reward, done, _ = env.step(action)
        if done:
            observation = env.reset()
        pitch = observation[0]
        action[0] = 10.0 * pitch
```

With a simulation spine, this code will reset the robot's state and execute the policy continuously. In a pi3hat spine, this code will control the robot directly. You can check out the [`examples/`](https://github.com/tasts-robots/upkie/tree/main/examples) directory for more examples.

## Code overview

### Agents

<dl>
  <dt>MPC balancer</dt>
  <dd>An agent that balances the robot in place, using wheels only, by closed-loop model predictive control. It performs better than the <em>Wheel balancer</em> with significantly less hacks ;-)</dd>

  <dt>Pink balancer</dt>
  <dd>A more capable agent that combines wheeled balancing with inverse kinematics computed by <a href="https://github.com/tasts-robots/pink">Pink</a>. This is the controller that runs in the <a href="https://www.youtube.com/shorts/8b36XcCgh7s">first</a> <a href="https://www.youtube.com/watch?v=NO_TkHGS0wQ">two</a> videos of Upkie.</dd>

  <dt>PPO balancer</dt>
  <dd>An agent trained by reinforcement learning to balance with straight legs. Training uses the <code><a href="https://tasts-robots.org/doc/upkie/classupkie_1_1envs_1_1upkie__wheels__env_1_1UpkieWheelsEnv.html#details">UpkieWheelsEnv</a></code> gym environment and the PPO implementation from <a href="https://github.com/DLR-RM/stable-baselines3/">Stable Baselines3</a>.</dd>

  <dt>Wheel balancer</dt>
  <dd>A baseline agent designed to check out Upkie's physical capabilities. The robot balances with its wheels only, following PD feedback from the head pitch and wheel odometry to wheel velocities, plus a feedforward <a href="https://github.com/tasts-robots/upkie/blob/662d76180e03a855e8810d60eeb5b229c95b68fb/agents/wheel_balancer/wheel_balancer.py#L378-L400">non-minimum phase trick</a> for smoother transitions from standing to rolling.</dd>
</dl>

### Environments

<dl>
  <dt><code><a href="https://tasts-robots.org/doc/upkie/classupkie_1_1envs_1_1upkie__servos__env_1_1UpkieServosEnv.html#details">UpkieServosEnv</a></code></dt>
  <dd>Upkie with full observation and joint position-velocity-torque actions.</dd>
  <dt><code><a href="https://tasts-robots.org/doc/upkie/classupkie_1_1envs_1_1upkie__wheels__env_1_1UpkieWheelsEnv.html#details">UpkieWheelsEnv</a></code></dt>
  <dd>Upkie with full observation but only wheel velocity actions.</dd>
</dl>

Environments are single-threaded rather than vectorized. In return, they run as-is on the real robot.

### Observers

<img src="https://tasts-robots.org/doc/upkie/observers.png" align="right">

<dl>
  <dt><a href="https://tasts-robots.org/doc/upkie/classupkie_1_1observers_1_1FloorContact.html#details">Floor contact</a></dt>
  <dd>Detect contact between the wheels and the floor. The pink and wheel balancers use contact as a reset flag for their integrators, to avoid over-spinning the wheels while the robot is in the air.</dd>

  <dt><a href="https://tasts-robots.org/doc/upkie/classupkie_1_1observers_1_1WheelContact.html#details">Wheel contact</a></dt>
  <dd>Detect contact between a given wheel and the floor.</dd>

  <dt><a href="https://tasts-robots.org/doc/upkie/classupkie_1_1observers_1_1WheelOdometry.html#details">Wheel odometry</a></dt>
  <dd>Measure the relative motion of the floating base with respect to the floor. Wheel odometry is part of their secondary task (after keeping the head straight), which is to stay around the same spot on the floor.</dd>
</dl>

### Spines

<dl>
  <dt>Bullet</dt>
  <dd>Spawn Upkie in a <a href="http://bulletphysics.org/">Bullet</a> simulation. Resetting this spine moves the robot back to its initial configuration in this world.</dd>
  <dt>pi3hat</dt>
  <dd>Spine is made to be called from a Raspberry Pi with an onboard mjbots <a href="https://mjbots.com/products/mjbots-pi3hat-r4-4b">pi3hat</a>. Servos are stopped when the spine is stopped, and switch to <a href="https://github.com/mjbots/moteus/blob/main/docs/reference.md#theory-of-operation">position mode</a> (which is a position-velocity-torque controller) when the spine idles. Check out the <a href="https://tasts-robots.org/doc/vulp/classvulp_1_1spine_1_1StateMachine.html#details">spine state machine</a> for details.</dd>
</dl>
