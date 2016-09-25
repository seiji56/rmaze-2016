#ifndef _AI_HPP_
#define _AI_HPP_

#include "logic_util.hpp"
#include "kernelTL.hpp"
#include "map.hpp"
#include "defines.hpp"

namespace logic
{
    class ai
    {
    public:
        ai (map *m, bool zero_t);
        ai (map *m, bool zero_t, coords init_po);
        ~ai();
        bool loop ();

        void checkpoint ();
        void locate ();

    private:
        map *M;
        short **PFm; 
        coords pos;
        byte d;
        bool donetop;
        byte preferable_directions[4];
    public:
        method best_method ();

        bool apply (action act, int success);
        void accessible (std::vector<coords>& result, int x, int y, int f);
        void accessible (std::vector<coords>& result, coords c);

        void find_path (std::vector<coords>& path);
        void translate_path (std::vector<action>& translated, std::vector<coords>& path);

        action immediate ();

        void scan_tile ();
    };
}

#endif
