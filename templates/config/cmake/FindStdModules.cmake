# Copyright (c) LLVM Project.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
include(FetchContent)
include(FindPackageHandleStandardArgs)

if(NOT CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
  message(FATAL_ERROR "${project_name}_USE_CXX20_MODULES is only compatible with Clang and libc++")
endif()

cmake_policy(VERSION 3.28)

FetchContent_Declare(
  std
  URL "file://$${LIBCXX_BUILD}/modules/c++/v1"
  DOWNLOAD_EXACT_TIMESTAMP TRUE
  SYSTEM
)

FetchContent_MakeAvailable(std)

set(StdModules_FOUND Yes)
find_package_handle_standard_args(StdModules REQUIRED_VARS StdModules_FOUND)
