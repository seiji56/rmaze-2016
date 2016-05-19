#include "herkulex.hpp"

int main()
{
    herkulex_chain chain("/dev/ttyAMA0", 115200);
    chain.addmot(3, 0, 0);
    printf("Added motor\n");
    chain.setcolor(cyan, 0xfe);
}
