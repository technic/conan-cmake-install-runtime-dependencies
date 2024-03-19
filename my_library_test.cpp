#include <gtest/gtest.h>
#include <my_library.h>

TEST(MyLibraryTest, BasicAssertions) {
  const int two = 2;
  const int result = add_two(two);
  test_zlib();
  EXPECT_TRUE(result == 4);
}

