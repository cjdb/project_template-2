# Copyright (c) Morris Hafner.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
include(FindPackageHandleStandardArgs)

set(clang_tidy_path "$${${project_name}_CLANG_TIDY_PATH}")
if(NOT clang_tidy_path)
  get_filename_component(clang_tidy_path "$${CMAKE_CXX_COMPILER}" DIRECTORY)
  set(clang_tidy_path "$${clang_tidy_path}/clang-tidy")
endif()

if(EXISTS "$${clang_tidy_path}")
  set(ClangTidy_FOUND Yes)
  set(CMAKE_CXX_CLANG_TIDY "$${clang_tidy_path}" -p="$${CMAKE_BINARY_DIR}")
  message(STATUS "path '$${clang_tidy_path}' found")
else()
  set(ClangTidy_FOUND No)
  message(STATUS "path '$${clang_tidy_path}' not found")
endif()

find_package_handle_standard_args(ClangTidy REQUIRED_VARS ClangTidy_FOUND)
