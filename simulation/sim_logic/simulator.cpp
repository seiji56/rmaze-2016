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
    printf("Will load map of size %dx%d\n", w, h);
    pmap = new int*[w];

    for (int i = 0; i < w; i++) pmap[i] = new int[h];

    printf("Allocated memory at %p for map.\n", pmap);
    if (!pmap)
    {
        w = _w;
        h = _h;
        pmap = _pmap;
        throw ALLOC_ERR;
    }
    printf ("Map is: \n");

    for (int y = 0; y < h; y++)
    {
        for (int x = 0; x < w; x++)
        {
            mapfile >> std::hex >> pmap[x][y];
            printf("%d ", pmap[x][y]);
        }
        printf("\n");
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
    char face = local_global_dir(0);
    std::pair<int, int> coords = dir_to_coords(std::pair<int, int> (px, py), face);
    if (!in_map(coords) || has_wall(std::pair<int, int> (px, py), face)) throw INVALID_MOVE;

    px = coords.first;
    py = coords.second;
}

// Simulate walking to back
void sim_logic::walk_back()
{
    char face = local_global_dir(2);
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

// Simulate blinking
void sim_logic::blink()
{
    lamp = false;
    for (int i = 0; i < 6; i++)
    {
        sf::sleep(sf::seconds(1));
        lamp = !lamp;
    }
}

// If is black
bool sim_logic::is_black()
{
    return pmap[px][py] & IS_BLACK;
}

// If is silver
bool sim_logic::is_silver()
{
    return pmap[px][py] & IS_SILVER;
}

// Returns centimeters to wall
int sim_logic::cm_to_dir(char side)
{
    int i = 0;
    char to = local_global_dir(side);
    switch(to)
    {
    case 0:
        {
            while (!has_wall(std::pair<int, int>(px, py - i++), to));
        }
        break;
    case 1:
        {
            while (!has_wall(std::pair<int, int>(px + i++, py), to));
        }
        break;
    case 2:
        {
            while (!has_wall(std::pair<int, int>(px, py + i++), to));
        }
        break;
    case 3:
        {
            while (!has_wall(std::pair<int, int>(px - i++, py), to));
        }
        break;
    default:
        i = -1;
        break;
    }
    return (i-2)*30 + 5;
}

// Milliseconds since start of simulation
unsigned int sim_logic::millis_since_start()
{
    return clock.getElapsedTime().asMilliseconds();
}

// Zero time elapsed
void sim_logic::zero_clock()
{
    clock.restart();
}

// Draw the physical map
void sim_logic::draw_phys_map(sf::RenderTexture* target)
{
    target->clear(sf::Color::White);

    sf::Vector2u target_size_u = target->getSize();
    sf::Vector2f target_size = sf::Vector2f(target_size_u.x, target_size_u.y);

    // Fitting map in drawing surface...
    float map_ew = w*40 + 14;
    float map_eh = h*40 + 14;

    sf::Vector2f ratios = sf::Vector2f(target_size.x/map_ew, target_size.y/map_eh);

    float draw_ratio = ratios.x < ratios.y?ratios.x:ratios.y;

    float real_ratio = draw_ratio;
    float wall_len = 50*draw_ratio;
    float cell_size = 40*draw_ratio;

    float offsetx = (target_size.x - (draw_ratio*map_ew))/2;
    float offsety = (target_size.y - (draw_ratio*map_eh))/2;

    if(draw_ratio > 1)
    {
        draw_ratio = 1;
        real_ratio = ratios.x < ratios.y?(target_size.x - 14*draw_ratio)/(w*40):(target_size.y - 14*draw_ratio)/(h*40);
        wall_len = 40*real_ratio + 10;
        cell_size = wall_len - 10;
    }


    // Drawing walls...

    sf::RoundedRectangleShape wallshape;
    wallshape.setCornersRadius(5*draw_ratio);
    wallshape.setOrigin(5*draw_ratio, 5*draw_ratio);
    wallshape.setCornerPointCount(1000);
    wallshape.setFillColor(sf::Color(128, 217, 255, .75*255));

    float size_percentage = .66;

    sf::RoundedRectangleShape filled_round;
    filled_round.setCornersRadius(5*draw_ratio);
    filled_round.setCornerPointCount(80);
    filled_round.setSize(sf::Vector2f(cell_size*size_percentage, cell_size*size_percentage));
    filled_round.setOrigin(cell_size*(size_percentage/2), cell_size*(size_percentage/2));
    sf::RectangleShape filled_rect;
    filled_rect.setSize(sf::Vector2f(cell_size*(size_percentage/2), cell_size*(size_percentage/2)));
    filled_rect.setOrigin(cell_size*(size_percentage/2), cell_size*(size_percentage/2));

    sf::RoundedRectangleShape robot_base;
    robot_base.setCornersRadius(5*draw_ratio);
    robot_base.setCornerPointCount(80);
    robot_base.setFillColor(sf::Color(149, 117, 205, .9*255));
    robot_base.setSize(sf::Vector2f(cell_size/2, cell_size/2));
    robot_base.setOrigin(cell_size/4, cell_size/4);
    sf::CircleShape robot_heading(cell_size/6, 3);
    robot_heading.setFillColor(sf::Color(187, 222, 251, .9*255));
    robot_heading.setOrigin(cell_size/6, cell_size/6);
    sf::CircleShape robot_lamp(cell_size/20);
    robot_lamp.setFillColor(sf::Color::Red);
    robot_lamp.setOrigin(cell_size/6, cell_size/6);

    sf::RectangleShape victim;
    victim.setSize(sf::Vector2f(cell_size/4, 5*draw_ratio));
    victim.setFillColor(sf::Color(100, 100, 100));
    victim.setOrigin(cell_size/8, cell_size/2);

    sf::CircleShape circle;
    circle.setPointCount(50);
    circle.setRadius(7*draw_ratio);
    circle.setOrigin(7*draw_ratio, 7*draw_ratio);
    circle.setFillColor(sf::Color(21, 0, 255, .50*255));

    for (int x = 0; x <= w; x++)
    {
        for (int y = 0; y <= h; y++)
        {
            sf::Vector2f corner(7*draw_ratio + 40*real_ratio*x + offsetx, 7*draw_ratio + 40*real_ratio*y + offsety);
            sf::Vector2f center(corner.x + cell_size/2, corner.y + cell_size/2);

            if (!(x == w && y == h))
            {
                wallshape.setPosition(corner);
                if (y == h || (x != w && pmap[x][y] & WALL_UP))
                {
                    wallshape.setSize(sf::Vector2f(wall_len , 10*draw_ratio));
                    target->draw(wallshape);
                }
                if (x == w || (y != h && pmap[x][y] & WALL_LEFT))
                {
                    wallshape.setSize(sf::Vector2f(10*draw_ratio , wall_len));
                    target->draw(wallshape);
                }
                if (x < w && y < h)
                {
                    filled_rect.setPosition(center);
                    filled_round.setPosition(center);
                    victim.setPosition(center);
                    if (pmap[x][y] & IS_BLACK)
                    {
                        filled_rect.setFillColor(sf::Color::Black);
                        filled_round.setFillColor(sf::Color::Black);
                        target->draw(filled_rect);
                        target->draw(filled_round);
                    }else if (pmap[x][y] & IS_SILVER){
                        filled_rect.setFillColor(sf::Color(160, 160, 160));
                        filled_round.setFillColor(sf::Color(160, 160, 160));
                        target->draw(filled_rect);
                        target->draw(filled_round);
                    }

                    if (pmap[x][y] & VIC_UP)
                    {
                        victim.setRotation(0);
                        target->draw(victim);
                    }
                    if (pmap[x][y] & VIC_RIGHT)
                    {
                        victim.setRotation(90);
                        target->draw(victim);
                    }
                    if (pmap[x][y] & VIC_DOWN)
                    {
                        victim.setRotation(180);
                        target->draw(victim);
                    }
                    if (pmap[x][y] & VIC_LEFT)
                    {
                        victim.setRotation(270);
                        target->draw(victim);
                    }
                }
            }
            circle.setPosition(corner);
            target->draw(circle);

        }
    }

    sf::Vector2f robot_coords(7*draw_ratio + 40*real_ratio*px + offsetx + cell_size/2, 7*draw_ratio + 40*real_ratio*py + offsety + cell_size/2);
    robot_base.setPosition(robot_coords);
    robot_heading.setPosition(robot_coords);
    robot_lamp.setPosition(robot_coords);
    robot_heading.setRotation(facing*90);
    robot_lamp.setRotation(facing*90);
    target->draw(robot_base);
    target->draw(robot_heading);
    if (lamp) target->draw(robot_lamp);

    sf::RectangleShape border;
    border.setFillColor(sf::Color::Transparent);
    border.setSize(target_size);
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
    else return has_wall(dir_to_coords(std::pair<int, int> (x, y), dir), rotate_dir(dir, 2));
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
