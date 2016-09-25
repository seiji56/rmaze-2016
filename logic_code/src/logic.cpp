#include "ai.hpp"

logic::ai robot(new logic::map (10), false);

int main(int argc, char *argv[])
{
    kernelTL::init();

    while (1)
    {
        robot.loop ();
    }

    kernelTL::clean();
    return 0;
}
