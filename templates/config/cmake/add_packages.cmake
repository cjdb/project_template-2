if(${project_name}_ENABLE_MODULES)
  find_package(StdModules REQUIRED)
endif()

if(${project_name}_ENABLE_CLANG_TIDY)
  find_package(Clang REQUIRED)
  find_package(ClangTidy REQUIRED)
endif()
