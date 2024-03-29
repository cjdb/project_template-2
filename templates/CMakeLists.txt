# Copyright (c) Christopher Di Bella.
# SPDX-License-Identifier: Apache-2.0 with LLVM Exception
#
cmake_minimum_required(VERSION 3.28 FATAL_ERROR)

project("${project_name}" C CXX)

set(CMAKE_CXX_STANDARD ${cxx_standard})
set(CMAKE_CXX_EXTENSIONS ${extensions})
set(CMAKE_CXX_STANDARD_REQUIRED Yes)
set(CMAKE_EXPORT_COMPILE_COMMANDS Yes)

if(CMAKE_CXX_EXTENSIONS)
  message(STATUS "Building with C++$${CMAKE_CXX_STANDARD} (extensions enabled)")
else()
  message(STATUS "Building with C++$${CMAKE_CXX_STANDARD} (extensions disabled)")
endif()

list(APPEND CMAKE_MODULE_PATH "$${CMAKE_CURRENT_SOURCE_DIR}/config/cmake")

enable_testing()
include(CTest)
include(handle_options)
include(add_packages)
include(add_targets)

add_subdirectory(source)
