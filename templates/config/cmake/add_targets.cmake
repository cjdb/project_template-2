# Copyright (c) Christopher Di Bella.
# SPDX-License-Identifier: Apache-2.0 with LLVM Exception
#
macro(ADD_TARGET_EXTRACT_ARGS optional_values single_values multi_values)
  list(APPEND optional_values "")
  list(APPEND single_values TARGET)
  list(APPEND multi_values COMPILE_OPTIONS INCLUDE DEFINE LINK_OPTIONS LINK_TARGETS SOURCES)

  cmake_parse_arguments(add_target_args "$${optional_values}" "$${single_values}" "$${multi_values}" $${ARGN})

  if(NOT add_target_args_TARGET)
    message(FATAL_ERROR "TARGET is not set; cannot build a $${CMAKE_CURRENT_FUNCTION} without naming the TARGET")
  endif()

  if(NOT add_target_args_SOURCES)
    message(FATAL_ERROR "SOURCES must be set for $${add_target_args_TARGET}")
  endif()
endmacro()

function(add_scoped_options target scope compile_options macros includes link_options link_targets)
  set(enable_thin_lto "$$<AND:$$<CONFIG:Release>,$$<CXX_COMPILER_ID:Clang>,$$<BOOL:${project_name}_ENABLE_LTO>")
  set(enable_lto "$$<AND:$$<CONFIG:Release>,$$<CXX_COMPILER_ID:GNU>,$$<BOOL:${project_name}_ENABLE_LTO>")
  set(enable_cfi "$$<AND:enable_thin_lto,enable_cfi>")

  target_compile_options(
    $${target} $${scope}
    "$${compile_options}"
    $$<$$<BOOL:$${${project_name}_ENABLE_SANITIZERS}>:-fsanitize=address,undefined>
    $$<$$<BOOL:enable_lto>:-flto>
    $$<$$<BOOL:enable_thin_lto>:-flto=thin>
    $$<$$<BOOL:enable_cfi>:-fsanitize=cfi>
  )
  target_compile_definitions($${target} $${scope} "$${macros}")
  target_include_directories($${target} $${scope} "$${includes}")

  target_link_options(
    $${target} $${scope}
    $$<$$<BOOL:$${${project_name}_ENABLE_SANITIZERS}>:-fsanitize=address,undefined>
    $$<$$<BOOL:enable_lto>:-flto>
    $$<$$<BOOL:enable_thin_lto>:-flto=thin>
    $$<$$<BOOL:enable_cfi>:-fsanitize=cfi>
    "$${link_options}"
  )
  target_link_libraries($${target} $${scope} "$${link_targets}")
endfunction()

function(cxx_binary)
  ADD_TARGETS_EXTRACT_ARGS("" "" "" $${ARGN})

  add_executable($${add_target_args_TARGET} "$${add_target_args_SOURCES}")
  add_scoped_options(
    $${add_target_args_TARGET} PRIVATE
    "$${add_target_args_COMPILE_OPTIONS}"
    "$${add_target_args_DEFINE}"
    "$${add_target_args_INCLUDE}"
    "$${add_target_args_LINK_OPTIONS}"
    "$${add_target_args_LINK_TARGETS}"
  )
endfunction()

function(check_library_type library_type)
  set(valid_types STATIC SHARED MODULE OBJECT)
  list(FIND valid_types "$${library_type}" library_type_result)
  if(library_type_result EQUAL -1)
    message(ERROR "unknown library type `$${library_type}`")
  endif()
endfunction()

function(cxx_library)
  set(single_args LIBRARY_TYPE)
  set(multi_args INCLUDE_AND_EXPORT DEFINE_AND_EXPORT LINK_AND_EXPORT)
  ADD_TARGETS_EXTRACT_ARGS("" "$${single_args}" "$${multi_args}" $${ARGN})
  check_library_type("$${add_target_args_LIBRARY_TYPE}")

  add_library(
    $${add_target_args_TARGET}
    $${add_target_args_LIBRARY_TYPE}
    "$${add_target_args_SOURCE}"
  )
  add_scoped_options(
    $${add_target_args_TARGET} PRIVATE
    "$${add_target_args_COMPILE_OPTIONS}"
    "$${add_target_args_DEFINE}"
    "$${add_target_args_INCLUDE}"
    "$${add_target_args_LINK_OPTIONS}"
    "$${add_target_args_LINK_TARGETS}"
  )
  add_scoped_options(
    $${add_target_args_TARGET} PUBLIC
    ""
    "$${add_target_args_DEFINE_AND_EXPORT}"
    "$${add_target_args_INCLUDE_AND_EXPORT}"
    ""
    "$${add_target_args_LINK_TARGETS_AND_EXPORT}"
  )
endfunction()

function(cxx_module)
  message(FATAL_ERROR "cxx_module is not implemented yet")
endfunction()

function(cxx_test)
  cxx_binary($${ARGN})
  ADD_TARGETS_EXTRACT_ARGS("" "" "" $${ARGN})
  add_test(test.$${add_target_args_TARGET} $${add_target_args_TARGET})
endfunction()

function(std_module target)
  if(NOT ${project_name}_ENABLE_MODULES)
    return
  endif()

  target_compile_options(target $$<$$<COMPILE_LANGUAGE:CXX>:"-fprebuilt-module-path=$${CMAKE_BINARY_DIR}/_deps/std-build/CMakeFiles/std.dir/">)
  target_compile_options(target $$<$$<COMPILE_LANGUAGE:CXX>:"-fprebuilt-module-path=$${CMAKE_BINARY_DIR}/_deps/std-build/CMakeFiles/std.compat.dir/">)
  target_compile_options(target $$<$$<COMPILE_LANGUAGE:CXX>:"-nostdinc++">)
  target_compile_options(target $$<$$<COMPILE_LANGUAGE:CXX>:"-isystem">)
  target_compile_options(target $$<$$<COMPILE_LANGUAGE:CXX>:"$${LIBCXX_BUILD}/include/c++/v1">)

  target_link_options(target $$<$$<COMPILE_LANGUAGE:CXX>:"-nostdlib++")
  target_link_options(target $$<$$<COMPILE_LANGUAGE:CXX>:"-L$${LIBCXX_BUILD}/lib")
  target_link_options(target $$<$$<COMPILE_LANGUAGE:CXX>:"-Wl,-rpath,$${LIBCXX_BUILD}/lib")

  target_link_libraries($${target} PRIVATE std c++)
  target_link_libraries($${target} PRIVATE std.compat c++)
endfunction()
