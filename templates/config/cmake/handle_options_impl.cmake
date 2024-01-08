# Copyright (c) Christopher Di Bella.
# SPDX-License-Identifier: Apache-2.0 with LLVM Exception
#
# Defines the default options for all project templates. Do not modify this file, as add_targets.cmake
# heavily depends on it.

set(build_modes Debug RelWithDebInfo MinSizeRel Release)
message(STATUS "Build type: $${CMAKE_BUILD_TYPE}")
if(CMAKE_BUILD_TYPE)
  list(FIND build_modes "$${CMAKE_BUILD_TYPE}" valid_build_type)
  if(valid_build_type EQUAL -1)
    message(FATAL_ERROR "$${CMAKE_BUILD_TYPE} is not a valid value")
  endif()
else()
  message(FATAL_ERROR "CMAKE_BUILD_TYPE must be set")
endif()

option(
  ${project_name}_USE_CLANG_TIDY
  "Toggles enabling Clang Tidy. Defaults to Yes."
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
if(${project_name}_USE_CLANG_TIDY)
  message(STATUS "Clang Tidy enabled")
else()
  message(STATUS "Clang Tidy disabled")
endif()

option(
  ${project_name}_USE_CXX20_MODULES
  "Toggles use of C++20 modules. Defaults to No."
  No
)
if(${project_name}_USE_CXX20_MODULES)
  message(STATUS "C++20 modules enabled")
else()
  message(STATUS "C++20 modules disabled")
endif()

option(
  ${project_name}_USE_LTO
  "Toggles enabing LTO (GCC) and ThinLTO (Clang) for 'CMAKE_BUILD_TYPE=Release'. Defaults to Yes."
  Yes
)
if(${project_name}_USE_LTO)
  message(STATUS "LTO enabled")
else()
  message(STATUS "LTO disabled")
endif()

option(
  ${project_name}_USE_CFI
  "Toggles enabling ControlFlowIntegrity when ThinLTO is enabled for Clang. Defaults to 'Yes'."
  Yes
)
if(${project_name}_USE_CFI)
  message(STATUS "ControlFlowIntegrity enabled")
else()
  message(STATUS "ControlFlowIntegrity disabled")
endif()

function(validate_option value option valid_values)
  list(FIND "$${valid_values}" "$${value}" found)

  if(found EQUAL -1)
    message(FATAL_ERROR "invalid value '$${value}' for $${option} (valid values are [$${$${valid_values}}])")
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
validate_option("$${${project_name}_USE_SANITIZER}" ${project_name}_USE_SANITIZER valid_options)

set(
  # Variable
  ${project_name}_USE_SANITIZER_WITH_BUILD_TYPE
  # Default value
  Debug RelWithDebInfo
  CACHE STRING
  "A semicolon-separated list of build modes that sanitisers are enabled for. Valid options are \
'Debug', 'RelWithDebInfo', 'MinSizeRel', and 'Release'. 'None' cannot be combined with \
other values. Defaults to 'Debug;RelWithDebInfo'.")

foreach(build_mode IN LISTS ${project_name}_USE_SANITIZER_WITH_BUILD_TYPE)
  validate_option("$${build_mode}" ${project_name}_USE_SANITIZER_WITH_BUILD_TYPE build_modes)
endforeach()

if(${project_name}_USE_SANITIZER)
  message(STATUS "Sanitizers enabled: $${${project_name}_USE_SANITIZER}")
  message(STATUS "Sanitizers will be built in $${${project_name}_USE_SANITIZER_WITH_BUILD_TYPE} modes")
else()
    message(STATUS "Sanitizers disabled")
endif()


set(
  # Variable
  ${project_name}_PROFILE_COVERAGE
  # Default value
  No
  CACHE STRING
  "Defines what code coverage analysis is used. Valid options are 'No', and 'SanitizerCoverage'. Defaults to 'No'."
)

set(valid_options "No" "SanitizerCoverage")
validate_option("$${${project_name}_PROFILE_COVERAGE}" ${project_name}_PROFILE_COVERAGE valid_options)

if(${project_name}_PROFILE_COVERAGE)
  message(STATUS "Code coverage set to $${${project_name}_PROFILE_COVERAGE}")
else()
  message(STATUS "Code coverage disabled")
endif()
