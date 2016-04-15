#include <stdio.h>

class sim_logic
{
public:
    sim_logic() : x(0), y(0), facing('U'), pmap(0){}
    sim_logic(int** _pmap, int _x, int _y, char _facing) : x(_x), y(_y), facing(_facing), pmap(_pmap) {}

    void set_map(int** _pmap);
    void set_facing();

    void walk_front();
    void walk_back();
    void turn_left():
    void turn_right();
private:
    char facing;
    int x, y;
    int** pmap;
};
