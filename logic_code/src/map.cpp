#include "map.hpp" 

logic::map::map (int s) : sz(s)
{
    printf("Creating MAP object...\n");
    s = 2*sz - 1;

    printf("MAP: Allocating Memory for map...\n");
    // Allocate memory for map
    M = new int**[s];

    for (int i = 0; i < s; i++) M[i] = new int*[s];

    for (int i = 0; i < s; i++)
    {
        for (int j = 0; j < s; j++) M[i][j] = new int[2];
    }
}

logic::map::~map ()
{
    for (int i = 0; i < sz; i++)
    {
        for (int j = 0; j < sz; j++) delete M[i][j];
    }

    for (int i = 0; i < sz; i++) delete M[i];

    delete M;
}

// Get element at given coordinates
int logic::map::at (int x, int y, int f)
{
    return M[x - 1 + sz][y - 1 + sz][f];
}

int logic::map::at (coords c)
{
    return at (c.x, c.y, c.f);
}

// Set element at given coordinates
void logic::map::set (int x, int y, int f, int v)
{
    printf("MAP: Address (%d, %d, %d) set to %d...\n", x, y, f, v);
    M[x - 1 + sz][y - 1 + sz][f] = v;
}

void logic::map::set (coords c, int v)
{
    set (c.x, c.y, c.f, v);
}

// Set certain bits (defined by bitmask) to true or false
void logic::map::mark (int x, int y, int f, int m, bool v)
{
    if (v) M[x - 1 + sz][y - 1 + sz][f] |= m;
    else M[x - 1 + sz][y - 1 + sz][f] &= ~m;
}

void logic::map::mark (coords c, int m, bool v)
{
    mark (c.x, c.y, c.f, m, v);
}

// Mark wall existent or not
void logic::map::setWall (int x, int y, int f, byte d, bool v)
{
    switch (d)
    {
    case 0:
        if (!(y - 1 + sz)) return;
        if (v) M[x - 1 + sz][y - 1 + sz][f] |= WALL_H;
        else M[x - 1 + sz][y - 1 + sz][f] &= ~WALL_H;
    case 1:
        if (!(x + 1 - sz)) return;
        if (v) M[x + sz][y - 1 + sz][f] |= WALL_V;
        else M[x + sz][y - 1 + sz][f] &= ~WALL_V;
    case 2:
        if (!(y + 1 - sz)) return;
        if (v) M[x - 1 + sz][y + sz][f] |= WALL_H;
        else M[x - 1 + sz][y + sz][f] &= ~WALL_H;
    case 3:
        if (!(y - 1 + sz)) return;
        if (v) M[x - 1 + sz][y - 1 + sz][f] |= WALL_V;
        else M[x - 1 + sz][y - 1 + sz][f] &= ~WALL_V;
    default:
        return;
    }
}

void logic::map::setWall (coords c, byte d, bool v)
{
    setWall (c.x, c.y, c.f, d, v);
}

// Check if wall exists to direction d
bool logic::map::wall (int x, int y, int f, byte d)
{
    switch (d)
    {
    case 0:
        if (!(y - 1 + sz)) return true;
        return M[x - 1 + sz][y - 1 + sz][f] & WALL_H;
    case 1:
        if (!(x + 1 - sz)) return true;
        return M[x + sz][y - 1 + sz][f] & WALL_V;
    case 2:
        if (!(y + 1 - sz)) return true;
        return M[x - 1 + sz][y + sz][f] & WALL_H;
    case 3:
        if (!(y - 1 + sz)) return true;
        return M[x - 1 + sz][y - 1 + sz][f] & WALL_V;
    default:
        return false;
    }
}

bool logic::map::wall (coords c, byte d)
{
    return wall (c.x, c.y, c.f, d);
}

// Search for value with relevant bits defined by the bitmask
void logic::map::search (std::vector<coords>& results, int m, int v)
{

    for (int x = 1 - sz; x < sz; x++)
    {
        for (int y = 1 - sz; y < sz; y++)
        {
            for (int f = 0; f < 2; f++)
            {
                if (at(x, y, f) & m == v & m) results.push_back(coords(x, y, f));
            }
        }
    }
}

// Get map size
int logic::map::getsz()
{
    return sz;
}

