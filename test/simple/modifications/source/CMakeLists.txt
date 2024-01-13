cxx_library(
  TARGET message
  SOURCES message.cpp
  LIBRARY_TYPE OBJECT
)

cxx_binary(
  TARGET hello
  SOURCES hello.cpp
  LINK_TARGETS message
)

cxx_test(
  TARGET test_message
  SOURCES test_message.cpp
  LINK_TARGETS message Catch2::Catch2 Catch2::Catch2WithMain
)
