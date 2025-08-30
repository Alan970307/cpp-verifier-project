#include "calculator.h"

int Calculator::add(int a, int b) {
    return a + b;
}

// 这里有一个故意的Bug！减法实现成了加法。
int Calculator::subtract(int a, int b) {
    return a + b; 
}