#ifndef _AI_DEF_
#define _AI_DEF_

#include <vector>
#include <stdio.h>
#include <queue>

// Bit definitions

#define WALL_H  0x01
#define WALL_V  0x02
#define VISITED 0x04
#define RAMP    0x18
#define COLOR   0x20
#define CHECK   0x40

// Color definitions

#define BLACK   0x00
#define WHITE   0x01
#define GRAY    0x02

// Action definitions

#define FRONT   0
#define BACK    2
#define RIGHT   1
#define LEFT    3

// Method definitions

#define IMMEDIATE   0
#define PATHFINDING 1
#define PULLBACK    2

#endif