# Copyright (c) Christopher Di Bella.
# SPDX-License-Identifier: Apache-2.0 with LLVM Exception
#
set(CMAKE_SYSTEM_NAME ${system_name})
set(CMAKE_SYSTEM_PROCESSOR ${target})

set(CMAKE_C_COMPILER "${prefix}/bin/${cc}")
set(CMAKE_C_COMPILER_TARGET ${triple})

set(CMAKE_CXX_COMPILER "${prefix}/bin/${cxx}")
set(CMAKE_CXX_COMPILER_TARGET ${triple})

set(CMAKE_AR "${prefix}/bin/${ar}")
set(CMAKE_RC "${prefix}/bin/${rc}")
set(CMAKE_RANLIB "${prefix}/bin/${ranlib}")

string(
  JOIN " " CMAKE_CXX_FLAGS_INIT
    -fdiagnostics-color=always
    -fstack-protector-strong
    -fvisibility=hidden
    -Werror
    -pedantic
    -Wall
    -Wattributes
    -Wcast-align
    -Wconversion
    -Wdouble-promotion
    -Wextra
    -Wformat=2
    -Wnon-virtual-dtor
    -Wnull-dereference
    -Wodr
    -Wold-style-cast
    -Woverloaded-virtual
    -Wshadow
    -Wsign-conversion
    -Wsign-promo
    -Wunused
    -Wno-ignored-attributes
    -Wno-cxx-attribute-extension
    -Wno-gnu-include-next
    -Wno-private-header
    -Wno-unused-command-line-argument
    ${stdlib}
    ${hardening}
    ${exceptions}
    ${rtti}
)

string(
  JOIN " " CMAKE_EXE_LINKER_FLAGS_INIT
    ${linker} ${exceptions} ${rtti} ${compiler_rt} ${libunwind}
)
