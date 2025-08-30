#include "gtest/gtest.h"
#include "calculator.h"

// 创建一个测试固件
class CalculatorTest : public ::testing::Test {
protected:
    Calculator calc;
};

// 测试加法功能
TEST_F(CalculatorTest, TestAdd) {
    EXPECT_EQ(calc.add(2, 3), 5);
    EXPECT_EQ(calc.add(-1, 1), 0);
}