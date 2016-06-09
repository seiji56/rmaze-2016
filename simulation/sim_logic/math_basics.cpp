#include "math_basics.hpp"

int kernel::math::round(double n)
{
    return (n >= 0) ? (int)(n + 0.5) : (int)(n - 0.5);
}
