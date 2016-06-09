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
#define WALL_UP             0x01
#define WALL_LEFT           0x02
#define IS_BLACK            0x04
#define IS_SILVER           0x08
#define VIC_UP              0x10
#define VIC_RIGHT           0x20
#define VIC_LEFT            0x40
#define VIC_DOWN            0x80
