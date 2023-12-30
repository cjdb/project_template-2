# Copyright (c) Christopher Di Bella.
# SPDX-License-Identifier: Apache-2.0 with LLVM Exception
#
cmake_minimum_required(VERSION 3.28 FATAL_ERROR)

project("${project_name}" CXX)

set(CMAKE_CXX_STANDARD ${cxx_standard})
set(CMAKE_CXX_EXTENSIONS ${extensions})
set(CMAKE_CXX_STANDARD_REQUIRED Yes)
set(CMAKE_EXPORT_COMPILE_COMMANDS Yes)

list(APPEND CMAKE_MODULE_PATH "$${CMAKE_CURRENT_SOURCE_DIR}/config/cmake")

set(build_modes Debug RelWithDebInfo MinSizeRel Release)
if(CMAKE_BUILD_TYPE)
  list(FIND build_modes "$${CMAKE_BUILD_TYPE}" valid_build_type)
  if(valid_build_type EQUAL -1)
    message(FATAL_ERROR "$${CMAKE_BUILD_TYPE} is not a valid value")
  endif()
else()
  message(FATAL_ERROR "CMAKE_BUILD_TYPE must be set")
endif()

include(handle_options)
include(add_packages)
include(add_targets)

add_subdirectory(source)
