#include "kernelTL.hpp"

kernel::kernel_tl::kernel_tl(kernel_ml* _mid_layer, unsigned int millis) : mid_layer(_mid_layer), start_mill(millis)
{
}

int kernel::kernel_tl::out_walk(int tiles)
{
    for (int i = 0; i < tiles; i++)
    {
        types::dist distance = in_dist(types::FRONT) - types::dist(5);
        int dist_tiles = math::round(distance.tiles());
        if (dist_tiles <= 0) return i;
        simulator->walk_front();
    }

    for (int i = 0; i > tiles; i--)
    {
        types::dist distance = in_dist(types::BACK) - types::dist(5);
        int dist_tiles = math::round(distance.tiles());
        if (dist_tiles <= 0) return i;
        simulator->walk_back();
    }
    return tiles;
}

void kernel::kernel_tl::out_turn(int times)
{
    for (int i = 0; i < times; i++)
        simulator->turn_right();

    for (int i = 0; i > times; i--)
        simulator->turn_left();
}

float kernel::kernel_tl::out_align(int tout)
{
    return 0;
}

void kernel::kernel_tl::out_ramp()
{
}

void kernel::kernel_tl::out_drop (types::side where)
{

}

void kernel::kernel_tl::out_blink ()
{
    simulator->blink();
}

void kernel::kernel_tl::out_IOIOupdate ()
{
}

types::time kernel::kernel_tl::sys_time ()
{
    return types::time(simulator->millis_since_start());
}

types::temp kernel::kernel_tl::in_temp (types::side where)
{
    return types::temp(0);
}

types::dist kernel::kernel_tl::in_dist (types::side where)
{
    return types::dist(simulator->cm_to_dir(where));
}

types::color kernel::kernel_tl::in_color ()
{
    if (simulator->is_black()) return types::BLACK;
    if (simulator->is_silver()) return types::SILVER;
    return types::WHITE;
}
