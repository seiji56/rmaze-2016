#include "ai.hpp"

logic::ai::ai (map *m, bool zero_t) : M(m), d(0), donetop(false), pos(coords())
{
    printf("Creating AI object...\n");
    int tmpsize = M->getsz()*2 - 1;
    printf("AI: Alocating temporary map for PF\n");
    PFm = new short *[M->getsz()*2 - 1];
    for (int i = 0; i < M->getsz()*2 - 1; i++) PFm[i] = new short[M->getsz()*2 - 1];
    printf("AI: Allocated PF map\n");
    if (zero_t)
    {
        kernelTL::out::others::zeroTimer();
        printf("AI: Zeroed timer\n");
    }
    printf("AI: Robot position is 0, 0, 0\n");
}

logic::ai::ai (map *m, bool zero_t, coords init_pos) : M(m), d(0), donetop(false), pos(init_pos)
{
    printf("Creating AI object...\n");
    int tmpsize = M->getsz()*2 - 1;
    printf("AI: Alocating temporary map for PF\n");
    PFm = new short *[M->getsz()*2 - 1];
    for (int i = 0; i < M->getsz()*2 - 1; i++) PFm[i] = new short[M->getsz()*2 - 1];
    printf("AI: Allocated PF map\n");
    if (zero_t)
    {
        kernelTL::out::others::zeroTimer();
        printf("AI: Zeroed timer\n");
    }
    printf("AI: Robot position is %d, %d, %d\n", init_pos.x, init_pos.y, init_pos.f);
}

logic::ai::~ai ()
{
    printf("AI: Destroying AI object...\n");
    delete PFm;
    for (int i = 0; i < M->getsz()*2 - 1; i++) delete PFm[i];
}

// This is executed every tile... base function for logic
void logic::ai::loop ()
{
    action act;

    scan_tile ();

    switch (method ())
    {
    case PATHFINDING:
        {
            std::vector<coords> path;
            find_path (path);
            std::vector<action> acts;
            translate_path (acts, path);
            act = acts[0];
        }
         break;
    case IMMEDIATE:
        {
            act = immediate ();
        }
        break;
    case PULLBACK:
        {
            act = action(BACK, 1);
        }
        break;
    default:
        throw "Unknown method";
        return;
    }

    apply (act, kernelTL::out::locomotion::execute (act));
}

// Still needs to implement checkpoint and locate functions...

// Chooses method to use in current situation
method logic::ai::best_method ()
{
    // Check if on black
    if (!kernelTL::in::sensors::color()) return PULLBACK;

    // Check if there are any neighboring non-visited tiles
    std::vector<coords> available;
    accessible (available, pos);

    int disponible = 0;
    for (int i = 0; i < available.size(); i++)
    {
        if (!(M->at(available[i]) & VISITED)) disponible++;
    }

    if (disponible > 0) return IMMEDIATE;

    // If the situation can not be handled by pullback or immediate methods
    return PATHFINDING;
}

// Apply successful iterations of actions on the ai memory
bool logic::ai::apply (action act, int success)
{
    act.cnt = success;
    int sz = M->getsz();
    switch (act.type)
    {
    case BACK:
        act.cnt = -act.cnt;
    case FRONT:
        switch (d%4)
        {
        case 0:
            act.cnt = -act.cnt;
        case 2:
            if (pos.y + act.cnt > sz - 1 || pos.y + act.cnt < 1 - sz) return false;
            pos.y += act.cnt;
            break;
        case 3:
            act.cnt = -act.cnt;
        case 1:
            if (pos.x + act.cnt > sz - 1 || pos.x + act.cnt < 1 - sz) return false;
            pos.x += act.cnt;
            break;
        default:
            break;
        }
        break;
    case LEFT:
        act.cnt = -act.cnt;
    case RIGHT:
        d = (d + act.cnt + 4)%4; 
        break;
    default:
        throw "Unknown action";
        return false;
    }

    return true;
}

// Get accessible tiles from tile at (x, y, f)
void logic::ai::accessible (std::vector<coords>& result, int x, int y, int f)
{
    int sz = M->getsz();
    if (x > 1 - sz && !M->wall (x, y, f, 3)) result.push_back (coords (x - 1, y, f));
    if (x < sz - 1 && !M->wall (x, y, f, 1)) result.push_back (coords (x + 1, y, f));
    if (y > 1 - sz && !M->wall (x, y, f, 0)) result.push_back (coords (x, y - 1, f));
    if (y < sz - 1 && !M->wall (x, y, f, 2)) result.push_back (coords (x, y + 1, f));
}

void logic::ai::accessible (std::vector<coords>& result, coords c)
{
    accessible (result, c.x, c.y, c.f);
}

// Find best path to take
void logic::ai::find_path (std::vector<coords>& path)
{
    printf("AI: Searching for path from %d, %d, %d\n", pos.x, pos.y, pos.f);
    int sz = M->getsz () - 1;
    int f = pos.f;

    for (int i = 0; i < M->getsz()*2 - 1; i++)
    {
        for (int j = 0; j < M->getsz()*2 - 1; j++) PFm[i][j] = -1;
    }

    std::queue<std::pair<coords, int> > BFSQ;
    PFm[pos.x + sz][pos.y + sz] = 0;
    BFSQ.push (std::pair<coords, int> (pos, 1));

    bool found = false;
    bool foundramp = false;
    coords unvisited, ramp;

    while (!BFSQ.empty () && !found)
    {
        for (; !BFSQ.empty () && !found; BFSQ.pop())
        {
            coords next = BFSQ.front().first;
            int dist = BFSQ.front().second;
            // printf("next = %d, %d, %d\n", next.x, next.y, next.f);

            PFm[next.x + sz][next.y + sz] = dist;

            // Verify and add neighbor nodes
            std::vector<coords> neighbors;
            accessible (neighbors, next);
            for (int i = 0; i < neighbors.size(); i++)
            {
                coords tmp = neighbors[i];
                // printf("NB%d = %d, %d, %d\n", i, tmp.x, tmp.y, tmp.f);
                // printf("NB%d was %svisited\n", i, M->at (tmp) & VISITED?"":"never ");
                // printf("NB%d has cost of %d\n", i, PFm[tmp.x + sz][tmp.y + sz]);

                if (M->at (tmp) & VISITED // It must have been visited
                    && PFm[tmp.x + sz][tmp.y + sz] == -1 // And have dist of -1
                    && !(M->at (tmp) & RAMP)) // And not be a ramp
                {
                    // printf("NB%d qualified\n", i);
                    BFSQ.push (std::pair<coords, int> (tmp, dist + 1));
                } else if (!(M->at (tmp) & VISITED)) // If it was never visited
                {
                    // printf("NB%d is target\n", i);
                    found = true;
                    unvisited = tmp;
                    PFm[tmp.x + sz][tmp.y + sz] = dist + 1;
                    break;
                }

                if (M->at (tmp) & RAMP) // If it is a ramp
                {
                    foundramp = true;
                    ramp = tmp;
                    PFm[tmp.x + sz][tmp.y + sz] = dist + 1;
                }
            }
        }
    }

    // Traceback
    printf(found?"Path found! starting traceback...\n":"Path not found...\n");

    if (found) path.push_back (unvisited);
    else if (foundramp && !donetop) path.push_back (ramp);
    else path.push_back(coords(0, 0, f));

    while (PFm[path.back ().x + sz][path.back ().y + sz] != 1)
    {
        std::vector<coords> possible;
        accessible(possible, path.back ());
        for (int i = 0; i < possible.size(); i++)
        {
            coords tmp = possible[i];
            printf("Acessible: %d, %d, %d\n", tmp.x, tmp.y, tmp.f);
            printf("Now & accessible: %d, %d\n", PFm[path.back ().x + sz][path.back ().y + sz], PFm[tmp.x + sz][tmp.y + sz]);
            if (PFm[path.back ().x + sz][path.back ().y + sz] == PFm[tmp.x + sz][tmp.y + sz] + 1)
            {
                path.push_back (tmp);
                break;
            }
        }
    }
}

// Translate from coordinates list to actions vector
void logic::ai::translate_path (std::vector<action>& translated, std::vector<coords>& path)
{
    printf("AI: Translating path from %d, %d, %d front to %d\n", pos.x, pos.y, pos.f, d);
    coords tmppos = path.back();
    byte tmpd = d;

    while (!path.empty ())
    {
        path.pop_back();
        if (path.back().y == tmppos.y - 1)
        {
            if (tmpd != 0)
            {

                if (tmpd == 3) 
                {
                    translated.push_back(action(RIGHT, 1));
                } else {
                    translated.push_back(action(LEFT, tmpd));
                }
                tmpd = 0;
            }
            tmppos = path.back();
        } else
        if (path.back().x == tmppos.x + 1) 
        {
            if (tmpd != 1)
            {

                if (tmpd == 0)
                {
                    translated.push_back(action(RIGHT, 1));
                } else {
                    translated.push_back(action(LEFT, tmpd - 1));
                }
                tmpd = 1;
            }
            tmppos = path.back();
        } else
        if (path.back().y == tmppos.y + 1) 
        {
            if (tmpd != 2)
            {

                if (tmpd == 3)
                {
                    translated.push_back(action(LEFT, 1));
                } else {
                    translated.push_back(action(RIGHT, 2 - tmpd));
                }
                tmpd = 2;
            }
            tmppos = path.back();
        } else
        if (path.back().x == tmppos.x - 1) 
        {
            if (tmpd != 3)
            {

                if (tmpd == 0) 
                {
                    translated.push_back(action(LEFT, 1));
                } else {
                    translated.push_back(action(RIGHT, 3 - tmpd));
                }
                tmpd = 3;
            }
            tmppos = path.back();
        }
        translated.push_back(action(FRONT, 1));
    }
    path.pop_back();
}

// Immediate response
logic::action logic::ai::immediate ()
{
    std::vector<coords> available;
    accessible (available, pos);
    for (int i = 0; i < 4; i++)
    {
        switch ((preferable_directions[i] + d)%4)
        {
        case 0:
            for (int j = 0; j < available.size(); j++)
            {
                if (pos.x == available[j].x && pos.y - 1 == available[j].y)
                    return action (FRONT, 1);
            }
            break;
        case 1:
            for (int j = 0; j < available.size(); j++)
            {
                if (pos.x + 1 == available[j].x && pos.y == available[j].y)
                    return action (RIGHT, 1);
            }
            break;
        case 2:
            for (int j = 0; j < available.size(); j++)
            {
                if (pos.x == available[j].x && pos.y + 1 == available[j].y)
                    return action (BACK, 1);
            }
            break;
        case 3:
            for (int j = 0; j < available.size(); j++)
            {
                if (pos.x - 1 == available[j].x && pos.y == available[j].y)
                    return action (LEFT, 1);
            }
            break;
        }
    }
    return action (FRONT, 0);
}

// Scan tile properties (walls, color, etc...)
void logic::ai::scan_tile ()
{
    // Verify Walls and distance (subject to change)
    for (int i = 0; i < 4; i++) M->setWall (pos, i, !kernelTL::in::sensors::distance ((i - d + 4)%4));
    M->mark (pos, VISITED, true);

    // Verify Color of the tile
    byte color = kernelTL::in::sensors::color();
    switch (color)
    {
    case 0:
        M->mark (pos, COLOR, false);
        break;
    case 1:
        M->mark (pos, COLOR, true);
        break;
    case 2:
        M->mark (pos, COLOR, true);
        M->mark (pos, CHECK, true);
        break;
    }
}
