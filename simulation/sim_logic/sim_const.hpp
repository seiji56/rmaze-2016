#include <SFML/Graphics.hpp>

#include <stdio.h>
#include <string>
#include <iostream>
#include <fstream>

#include "RoundedRectangleShape.hpp"

// typedefs
typedef unsigned char uchar;

// Direction definitions
#define FRONT_DIR   0
#define RIGHT_DIR   1
#define BACK_DIR    2
#define LEFT_DIR    3

// Simulation error definitions
#define INVALID_MOVE        01

// System Error definitions
#define ALLOC_ERR           01
#define FILE_OPEN_ERR       02

// Map memory mask
#define WALL_UP             0x001
#define WALL_LEFT           0x002
#define IS_BLACK            0x004
#define IS_SILVER           0x008
#define VIC_UP              0x010
#define VIC_RIGHT           0x020
#define VIC_LEFT            0x040
#define VIC_DOWN            0x080
#define VISITED             0x100
#define TO_VISIT            0x200
