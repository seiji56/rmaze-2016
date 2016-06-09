#include "simulator.hpp"


// Load map form file 'filename'
void sim_logic::load_map(std::string filename)
{
    int _w = w;
    int _h = h;
    int **_pmap = pmap;

    std::ifstream mapfile;
    try
    {
        mapfile.open(filename.c_str());
    }
    catch (std::ifstream::failure e)
    {
        throw FILE_OPEN_ERR;
    }

    mapfile >> w >> h;
    pmap = new int*[w];

    for (int i = 0; i < w; i++) pmap[i] = new int[h];

    if (!pmap)
    {
        w = _w;
        h = _h;
        pmap = _pmap;
        throw ALLOC_ERR;
    }

    for (int y = 0; y < h; y++)
    {
        for (int x = 0; x < w; w++) mapfile >> pmap[x][y];
    }
}

// Set map size
void sim_logic::set_map_size(int _w, int _h)
{
    w = _w;
    h = _h;
}

// Set map of size w, h from other map
void sim_logic::set_map(int **_pmap, bool refer)
{
    if (refer) pmap = _pmap;
    else
    {
        for (int y = 0; y < h; y++)
        {
            for (int x = 0; x < w; w++) pmap[x][y] = _pmap[x][y];
        }
    }
}

// Set facing direction
void sim_logic::set_facing(char _facing)
{
    facing = _facing;
}

// Simulate walking to front
void sim_logic::walk_front()
{
    char face = local_global_dir(facing);
    std::pair<int, int> coords = dir_to_coords(std::pair<int, int> (px, py), face);
    if (!in_map(coords) || has_wall(std::pair<int, int> (px, py), face)) throw INVALID_MOVE;

    px = coords.first;
    py = coords.second;
}

// Simulate walking to back
void sim_logic::walk_back()
{
    char face = local_global_dir(rotate_dir(facing, 2));
    std::pair<int, int> coords = dir_to_coords(std::pair<int, int> (px, py), face);
    if (!in_map(coords) || has_wall(std::pair<int, int> (px, py), face)) throw INVALID_MOVE;

    px = coords.first;
    py = coords.second;
}

// Simulate turning left
void sim_logic::turn_left()
{
    facing = rotate_dir(facing, -1);
}

// Simulate turning right
void sim_logic::turn_right()
{
    facing = rotate_dir(facing, 1);
}

// Draw the physical map
void sim_logic::draw_phys_map(sf::RenderTexture* target)
{
    target->clear(sf::Color(px++, 0, 0));

    sf::Vector2u target_size = target->getSize();

    sf::RectangleShape border;
    border.setFillColor(sf::Color::Transparent);
    border.setSize(sf::Vector2f(target_size.x, target_size.y));
    border.setOutlineColor(sf::Color(127, 127, 127));
    border.setPosition(0, 0);

    target->draw(border);
    target->display();
}

// Convert from local to global directions
char sim_logic::local_global_dir(char dir)
{
    return rotate_dir(facing, dir);
}

// Convert from global to local directions
char sim_logic::global_local_dir(char dir)
{
    return rotate_dir(-facing, dir);
}

// Rotate direction by rot
char sim_logic::rotate_dir(char dir, char rot)
{
    return (((dir + rot)%4) + 4)%4;
}

// Check if coordinates are inside the map
bool sim_logic::in_map(std::pair<int, int> coords)
{
    int x = coords.first;
    int y = coords.second;
    return (x >= 0 && x < w) && (y >= 0 && y < h);
}

// Check if there's a wall to a side of a certain tile
bool sim_logic::has_wall(std::pair<int, int> coords, char dir)
{
    int x = coords.first;
    int y = coords.second;

    if (!in_map(coords)) return true;

    if (dir == 0 || dir == 3) return pmap[x][y] & (dir?0x02:0x01);
    else return has_wall(dir_to_coords(std::pair<int, int> (px, py), dir), rotate_dir(dir, 2));
}

// Convert from coords and a direction to coordinates of faced tile
std::pair<int, int> sim_logic::dir_to_coords(std::pair<int, int> coords, uchar dir)
{
    std::pair<int, int> surr_tiles[4] = {std::pair<int, int>(coords.first, coords.second - 1),
                                        std::pair<int, int>(coords.first + 1, coords.second),
                                        std::pair<int, int>(coords.first, coords.second + 1),
                                        std::pair<int, int>(coords.first - 1, coords.second)};
    return surr_tiles[dir];
}
