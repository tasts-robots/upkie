// SPDX-License-Identifier: Apache-2.0
// Copyright 2022 Stéphane Caron

#pragma once

#include <cstdint>

//! Main control loop between agents and actuators.
namespace upkie::cpp::spine {

//! Request flag used for shared-memory inter-process communication.
enum class Request : uint32_t {
  //! Flag set when there is no active request.
  kNone = 0,

  //! Flag set to indicate an action has been supplied.
  kAction = 1,

  //! Flag set to start the spine.
  kStart = 2,

  //! Flag set to stop the spine.
  kStop = 3,

  //! Flag set when the last request was invalid.
  kError = 4
};

}  // namespace upkie::cpp::spine
