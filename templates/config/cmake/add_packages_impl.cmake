if(${project_name}_USE_CXX20_MODULES)
  find_package(StdModules REQUIRED)
endif()

if(${project_name}_USE_CLANG_TIDY)
  find_package(Clang REQUIRED)
  find_package(ClangTidy REQUIRED)
endif()
