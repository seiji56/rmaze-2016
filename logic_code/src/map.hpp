#ifndef _MAP_HPP_
#define _MAP_HPP_

#include "logic_util.hpp"
#include "defines.hpp"

namespace logic
{
    class map
    {
    public:
        map (int s);

        ~map();

        int at (int x, int y, int f);
        int at (coords c);
        void set (int x, int y, int f, int v);
        void set (coords c, int v);
        void mark (int x, int y, int f, int m, bool v);
        void mark (coords c, int m, bool v);
        void setWall (int x, int y, int f, byte d, bool v);
        void setWall (coords c, byte d, bool v);

        bool wall (int x, int y, int f, byte d);
        bool wall (coords c, byte d);
        void search (std::vector<coords>& results, int m, int v);

        int getsz ();

    private:
        int sz;
        int ***M;
    };
}

#endif