cmake_minimum_required(VERSION 3.14)
project(CalculatorProject)

# 添加gtest测试框架
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
)
FetchContent_MakeAvailable(googletest)

# 添加可执行文件和源文件
add_executable(run_tests main.cpp calculator.cpp)

# 链接gtest
target_link_libraries(run_tests GTest::gtest_main)

# 包含头文件目录
target_include_directories(run_tests PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

# 添加测试
include(GoogleTest)
gtest_discover_tests(run_tests)