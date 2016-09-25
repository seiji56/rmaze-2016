#ifndef _UTIL_HPP_
#define _UTIL_HPP_

typedef unsigned char byte;
typedef int method;

namespace logic
{
    struct coords
    {
        coords() : x(0), y(0), f(0) {} 
        coords(int _x, int _y, int _f) : x(_x), y(_y), f(_f) {} 
        int x, y, f;
    };

    struct action
    {
        action() : type(0), cnt(0) {} 
        action(int _type, int _cnt) : type(_type), cnt(_cnt) {} 
        int type;

        int cnt;
    };
}

#endif