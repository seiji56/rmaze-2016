#include "sim_const.hpp"

class sim_logic
{
public:
    sim_logic() : lamp(false), facing(FRONT_DIR), px(0), py(0), pmap(0) {}
    sim_logic(std::string filename) : lamp(false), facing(FRONT_DIR), px(0), py(0) {load_map(filename);}
    sim_logic(int** _pmap, int _w, int _h, int _x, int _y, char _facing) : lamp(false), facing(_facing), px(_x), py(_y), w(_w), h(_h), pmap(_pmap) {}

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

    void blink();

    bool is_black();
    bool is_silver();
    int cm_to_dir(char side);

    // Time handling
    unsigned int millis_since_start();
    void zero_clock();

    // Drawing the physical map
    void draw_phys_map(sf::RenderTexture* target);

public:
    // Functions for use of the simulator and simulations
    char local_global_dir(char dir);
    char global_local_dir(char dir);

    char rotate_dir(char dir, char rot);

    bool in_map(std::pair<int, int> coords);
    bool has_wall(std::pair <int, int> coords, char dir);

    std::pair<int, int> dir_to_coords(std::pair <int, int> coords, uchar dir);

private:
    sf::Clock clock;
private:
    bool lamp;

    char facing;

    int px;
    int py;

    int w;
    int h;

    int** pmap;
};
