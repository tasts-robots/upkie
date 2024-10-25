# Gym environments {#environments}

Upkie has reinforcement learning environments following the [Gymnasium API](https://gymnasium.farama.org/).

- [UpkieBaseEnv](\ref upkie.envs.upkie_base_env.UpkieBaseEnv): base class for all Upkie environments.
    - [UpkieGroundVelocity](\ref upkie_ground_velocity_description): behave like a wheeled inverted pendulum.
    - [UpkieServos](\ref upkie_servos_description): action and observation correspond to the full servo API.
        - [UpkieServoPositions](\ref upkie_servo_positions_description): joint position control only.
        - [UpkieServoTorques](\ref upkie_servo_torques_description): joint torque control only.

Upkie environments are single-threaded and run as-is in both simulation and on real robots. While each environment has its own observation and action spaces, all of them also report full [spine observations](\ref observations) in their `info` dictionaries.
