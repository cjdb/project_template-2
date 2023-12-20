# Copyright (c) Christopher Di Bella.
# SPDX-License-Identifier: Apache-2.0 with LLVM Exception
#
cmake_minimum_required(VERSION 3.28 FATAL_ERROR)

project("${project_name}" CXX)

set(CMAKE_CXX_STANDARD ${cxx_standard})
set(CMAKE_CXX_EXTENSIONS No)
set(CMAKE_STANDARD_REQUIRED Yes)
set(CMAKE_EXPORT_COMPILE_COMMANDS Yes)

list(APPEND CMAKE_MODULE_PATH "$${CMAKE_CURRENT_SOURCE_DIR}/config/cmake")

include(handle_options)
include(add_packages)
include(add_targets)
