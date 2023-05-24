# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

### Added

- Example: wheeled balancing with CPU isolation
- Example: wheeled balancing with action-observation logging
- Makefile to build, upload and run Raspberry Pi targets
- Script to start a simulation directly from the repository
- Specify Bazel version in ``.bazelversion``

### Changed

- Remove ``utils.logging`` submodule, deprecated by mpacklog
- Rename "blue balancer" agent to "test balancer"
- Simplify test balancer code
- Update Bazelisk to v1.16.0
- UpkieWheelsEnv: version 2

### Fixed

- Conversion warnings in servos and wheels environments
- Examples: make sure environments are closed before exiting
- PPO balancer: fix testing script
- PPO balancer: save policy with new environment
- PPO balancer: simplify training
- Pink balancer: default frequency is 200 Hz

## [0.4.0] - 2023/04/06

### Added

- Environment: ``UpkieServosEnv-v1``
- PPO balancer: distribute sample policy
- Pink balancer: ``--visualize`` argument
- Spine: Air Bullet, same as Bullet but floating in the air
- Utils: Pinocchio utility functions

### Changed

- Load description from local package rather than cloning a repository
- Rename ``UpkieWheelsReward`` to ``StandingReward``

### Fixed

- UpkieWheelsEnv: observation limits for ground position and velocity
- Pink balancer: reduce LM damping to fix stalling when crouching
- PPO balancer: get environment id (thanks @Varun-GP)

## [0.3.1] - 2023/03/15

### Added

- UpkieWheelsEnv: return action and observation dicts in ``info``

## [0.3.0] - 2023/03/13

### Added

- Add ``upkie_locomotion.envs.register`` function
- PPO balancer: setting for total number of training timesteps
- UpkieWheelsEnv: simple example

### Changed

- UpkieWheelsEnv: remove dependency on gin

## [0.2.0] - 2023/03/03

### Added

- Agent: PPO balancer
- Environment: ``UpkieWheelsEnv-v1``
- Observers: Base pitch

### Changed

- Promote ``utils.imu`` to a proper Python observer
- Switch from ``aiorate`` to ``loop_rate_limiters``

### Fixed

- Document both C++ and Python code with Doxygen
- Python requirements and dependencies in Bazel

## [0.1.0] - 2022/09/12

Starting this changelog.
