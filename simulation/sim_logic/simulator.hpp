#include <SFML/Graphics.hpp>

#include <stdio.h>
#include <string>
#include <iostream>
#include <fstream>

#include "sim_const.hpp"

class sim_logic
{
public:
    sim_logic() : facing(FRONT_DIR), px(0), py(0), pmap(0){}
    sim_logic(int** _pmap, int _w, int _h, int _x, int _y, char _facing) : facing(_facing), px(_x), py(_y), w(_w), h(_h), pmap(_pmap) {}

    // Map setters
    void load_map(std::string filename);

    void set_map_size(int _w, int _h);
    void set_map(int** _pmap, bool refer = false);
    void set_facing(char _facing);

    // For use of the simulated robot
    void walk_front();
    void walk_back();
    void turn_left();
    void turn_right();

    // Drawing the physical map
    void draw_phys_map(sf::RenderTexture* target);

private:
    // Functions for use of the simulator
    char local_global_dir(char dir);
    char global_local_dir(char dir);

    char rotate_dir(char dir, char rot);

    bool in_map(std::pair<int, int> coords);
    bool has_wall(std::pair <int, int> coords, char dir);

    std::pair<int, int> dir_to_coords(std::pair <int, int> coords, uchar dir);
private:
    char facing;

    int px;
    int py;

    int w;
    int h;

    int** pmap;
};
