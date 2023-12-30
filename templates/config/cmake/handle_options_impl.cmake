# Copyright (c) Christopher Di Bella.
# SPDX-License-Identifier: Apache-2.0 with LLVM Exception
#
# Defines the default options for all project templates. Do not modify this file, as add_targets.cmake
# heavily depends on it.

option(
  ${project_name}_ENABLE_CLANG_TIDY
  "Toggles enabling clang-tidy. Defaults to Yes."
  Yes
)
option(
  ${project_name}_ENABLE_MODULES
  "Toggles use of C++20 modules. Defaults to No."
  No
)
option(
  ${project_name}_ENABLE_LTO
  "Toggles enabing LTO (GCC) and ThinLTO (Clang). Defaults to Yes."
  Yes
)
option(
  ${project_name}_ENABLE_CFI
  "Toggles enabling ControlFlowIntegrity when ThinLTO is enabled for Clang. Defaults to 'Yes'."
  Yes
)

set(
  # Variable
  ${project_name}_CLANG_TIDY_PATH
  # Default value
  ""
  CACHE STRING
  "Path to the Clang Tidy binary. Defaults to the same directory as CMAKE_CXX_COMPILER."
)

function(validate_option value valid_values)
  list(FIND "$${valid_values}" "$${$${value}}" found)
  if(found EQUAL -1)
    message(FATAL_ERROR "invalid value '$${$${value}}' for option $${value}")
  endif()
endfunction()

set(
  # Variable
  ${project_name}_USE_SANITIZER
  # Default value
  "address,undefined"
  CACHE STRING
  "Defines the sanitisers used to build ${project_name} binaries. Possible values are 'No', 'address', \
'memory', 'memory-track-origins', 'undefined', 'data-flow', 'thread', and 'address,undefined'. \
Defaults to 'address,undefined'."
)

set(
  valid_options
  "No" "address" "memory" "memory-track-origins" "undefined" "data-flow" "thread" "address,undefined"
)
validate_option(${project_name}_USE_SANITIZER valid_options)

set(
  # Variable
  ${project_name}_USE_SANITIZER_WITH_BUILD_TYPE
  # Default value
  Debug RelWithDebInfo
  CACHE STRING
  "A semicolon-separated list of build modes that sanitisers are enabled for. Valid options are \
'None', 'Debug', 'RelWithDebInfo', 'MinSizeRel', and 'Release'. 'None' cannot be combined with \
other values. Defaults to 'Debug;RelWithDebInfo'.")

foreach(build_mode IN LISTS ${project_name}_USE_SANITIZER_WITH_BUILD_TYPE)
  if("$${build_mode}" EQUAL "None")
    list(LENGTH ${project_name}_USE_SANITIZER_WITH_BUILD_TYPE size)
    if(NOT size EQUAL 1)
      message(FATAL_ERROR "${project_name}_USE_SANITIZER_WITH_BUILD_TYPE value 'None' cannot be combined with other values")
    endif()
    continue()
  endif()

  validate_option(build_mode build_modes)
endforeach()


set(
  # Variable
  ${project_name}_PROFILE_COVERAGE
  # Default value
  No
  CACHE STRING
  "Defines what code coverage analysis is used. Valid options are 'No', and 'SanitizerCoverage'. Defaults to 'No'."
)

set(valid_options "No" "SanitizerCoverage")
validate_option(${project_name}_PROFILE_COVERAGE valid_options)
