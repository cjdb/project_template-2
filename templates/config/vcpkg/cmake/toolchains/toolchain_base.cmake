# Copyright (c) Christopher Di Bella.
# SPDX-License-Identifier: Apache-2.0 with LLVM Exception
#
set(VCPKG_TARGET_ARCHITECTURE x64)
set(VCPKG_CRT_LINKAGE dynamic)
set(VCPKG_LIBRARY_LINKAGE static)

set(VCPKG_CMAKE_SYSTEM_NAME ${system_name})

set(VCPKG_INSTALL_OPTIONS "--clean-after-build")
set(VCPKG_CHAINLOAD_TOOLCHAIN_FILE "$${CMAKE_CURRENT_LIST_FILE}")
set(VCPKG_TARGET_TRIPLET ${triplet_name})

set(CMAKE_C_COMPILER "${prefix}/bin/${cc}")
set(CMAKE_C_COMPILER_TARGET ${triple})

set(CMAKE_CXX_COMPILER "${prefix}/bin/${cxx}")
set(CMAKE_CXX_COMPLIER_TARGET ${triple})

set(CMAKE_AR "${prefix}/bin/${ar}")
set(CMAKE_RC_COMPILER "${prefix}/bin/${rc}")
set(CMAKE_RANLIB "${prefix}/bin/${ranlib}")

string(
  JOIN " " CMAKE_CXX_FLAGS_INIT
  -fdiagnostics-color=always
  -fstack-protector-strong
  -fvisibility=hidden
  ${stdlib}
  ${hardening}
  ${exceptions}
  ${rtti}
)

string(
  JOIN " " CMAKE_EXE_LINKER_FLAGS_INIT
    ${linker} ${compiler_rt} ${libunwind} ${exceptions} ${rtti}
)
