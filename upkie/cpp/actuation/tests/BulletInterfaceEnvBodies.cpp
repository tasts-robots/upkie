// SPDX-License-Identifier: Apache-2.0
// Copyright 2024 Inria

#include <limits>
#include <map>
#include <memory>
#include <string>
#include <vector>

#include "gtest/gtest.h"
#include "tools/cpp/runfiles/runfiles.h"
#include "upkie/cpp/actuation/BulletInterface.h"

namespace upkie::cpp::actuation {

using bazel::tools::cpp::runfiles::Runfiles;

class BulletInterfaceEnvBodies : public ::testing::Test {
 protected:
  //! Set up a new test fixture
  void SetUp() override {
    ServoLayout layout;
    layout.add_servo(1, 1, "right_hip");
    layout.add_servo(2, 1, "right_knee");
    layout.add_servo(3, 1, "right_wheel");
    layout.add_servo(4, 2, "left_hip");
    layout.add_servo(5, 2, "left_knee");
    layout.add_servo(6, 2, "left_wheel");

    std::string error;
    std::unique_ptr<Runfiles> runfiles(Runfiles::CreateForTest(&error));
    ASSERT_NE(runfiles, nullptr);

    BulletInterface::Parameters params;
    params.dt = dt_;
    params.floor = false;   // wheels roll freely during testing
    params.gravity = true;  // default, just a reminder
    params.env_urdf_paths = {runfiles->Rlocation(
        "upkie/upkie/cpp/actuation/bullet/plane/plane.urdf")};
    params.robot_urdf_path =
        runfiles->Rlocation("upkie_description/urdf/upkie.urdf");
    interface_ = std::make_unique<BulletInterface>(layout, params);

    for (const auto& pair : layout.servo_joint_map()) {
      commands_.push_back({});
      commands_.back().id = pair.first;
    }
    replies_.resize(commands_.size());
  }

 protected:
  //! Time step in seconds
  double dt_ = 1.0 / 1000.0;

  //! Bullet actuation interface
  std::unique_ptr<BulletInterface> interface_;

  //! Servo commands placeholder
  std::vector<moteus::ServoCommand> commands_;

  //! Servo replies placeholder
  std::vector<moteus::ServoReply> replies_;
};

TEST_F(BulletInterfaceEnvBodies, MonitorEnvBodies) {
  Dictionary config;
  interface_->reset(config);

  Dictionary observation;
  interface_->cycle([](const moteus::Output& output) {});
  interface_->observe(observation);

  ASSERT_TRUE(observation.has("sim"));
  ASSERT_TRUE(observation("sim").has("plane"));
  ASSERT_TRUE(observation("sim")("plane").has("position"));
  ASSERT_TRUE(observation("sim")("plane").has("orientation"));

  // Plane was loaded at the origin
  ASSERT_EQ(observation("sim")("plane").get<Eigen::Vector3d>("position").x(),
            0.);
  ASSERT_EQ(observation("sim")("plane").get<Eigen::Vector3d>("position").y(),
            0.);
  ASSERT_EQ(observation("sim")("plane").get<Eigen::Vector3d>("position").z(),
            0.);

  // Plane orientation is the identity
  ASSERT_EQ(
      observation("sim")("plane").get<Eigen::Quaterniond>("orientation").w(),
      1.);
  ASSERT_EQ(
      observation("sim")("plane").get<Eigen::Quaterniond>("orientation").x(),
      0.);
  ASSERT_EQ(
      observation("sim")("plane").get<Eigen::Quaterniond>("orientation").y(),
      0.);
  ASSERT_EQ(
      observation("sim")("plane").get<Eigen::Quaterniond>("orientation").z(),
      0.);
}

}  // namespace upkie::cpp::actuation
