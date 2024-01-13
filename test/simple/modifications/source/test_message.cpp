#include "message.hpp"
#include <catch2/catch_test_macros.hpp>

TEST_CASE("test_message")
{
	CHECK(__cplusplus == 202002L);
	CHECK(message() == "Hello, world!");
}
