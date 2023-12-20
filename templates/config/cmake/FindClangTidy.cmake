# Copyright (c) Morris Hafner.
# SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
#
include(FindPackageHandleStandardArgs)

set(clang_tidy_path "$${${project_name}_CLANG_TIDY_PATH}")

if(EXISTS "$${clang_tidy_path}")
  set(ClangTidy_FOUND Yes)
  set(CMAKE_CXX_CLANG_TIDY "$${clang_tidy_path}" -p="$${CMAKE_BINARY_DIR}")
else()
  set(ClangTidy_FOUND No)
  message(STATUS "path '$${clang_tidy_path}' not found")
endif()

find_package_handle_standard_args(ClangTidy REQUIRED_VARS ClangTidy_FOUND)
