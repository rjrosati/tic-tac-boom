#include <vector>
#include <string>
#include <stdint.h>
#include <iostream>


#define B 0
#define X 1
#define O 2
#define W 3

#ifndef NULL
#define NULL 0
#endif

using namespace std;
//#pragma pack(push, 1)
struct Twobits {
	uint8_t a_:2;
};
//#pragma pack(pop, 1)
typedef unsigned char tile; // might be able to bitfield this later, stick to this for now.

typedef enum {
		BOARD_UL,
		BOARD_UM,
		BOARD_UR,
		BOARD_ML,
		BOARD_MM,
		BOARD_MR,
		BOARD_LL,
		BOARD_LM,
		BOARD_LR
} board;

class Map {
public:
    // describes a tic tactics game in full.
    tile megaboard[9][9]; 
    vector<Map> children;
    tile conquered_boards[9];
    bool conquests_locked;
    board board_to_move;
    tile player;
    Map* parent;
    unsigned short depth;
    tile forced_win_possible;
    tile megaboard_state;

    // functions
    tile opp();
    void createChild();
    void board_state(unsigned char[9], unsigned char);
    uint8_t* which_boards_won();
    bool board_unwinnable(unsigned char[9]);
    void update_megaboard_state();
    void generate_possible_moves();
    void pretty_print_me();
    Map(tile[][9],board&,tile&,tile[],Map*,uint8_t); // useful constructor
    Map(); // default constructor
    ~Map(); // destructor
};
// hopefully this class stays pretty small
// Let's see... (9*9 + 9 + 1 + 1 + 1 + 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4)
// = 143 bytes. An order of magnitude better than Python.
// plus children vector of course


struct colors {
    // Provides ANSI color codes for pretty printing Maps
    bool disabled;       // = False
	string magenta; // = "\033[95m";
	string blue;   //= '\033[94m'
	string green;  //'\033[92m'
	string yellow; // = '\033[93m'
	string red;    // = '\033[91m'
	string END;   // = '\033[0m'
    colors();
    void disable();
    ~colors();
};