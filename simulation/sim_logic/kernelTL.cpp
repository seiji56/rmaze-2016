#include "kernelTL.hpp"

kernel::kernel_tl::kernel_tl(kernel_ml* _mid_layer, unsigned int millis) : mid_layer(_mid_layer), start_mill(millis)
{
}

bool kernel::kernel_tl::out_walk(int tiles, int *expected)
{

}
