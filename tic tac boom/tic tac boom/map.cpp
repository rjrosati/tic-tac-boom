#include "map.h"

extern colors* color;

Map::Map(tile megaboard[][9], board& board_to_move, tile& player,
         tile conquered_boards[], Map* parent = NULL, uint8_t depth = 0)
        : board_to_move(board_to_move), player(player), parent(parent), depth(depth) {
        for (int i=0; i<9; i++) {
            for (int j=0;j<9;j++){
                   this->megaboard[i][j] = megaboard[i][j];
            }
        }

        for (int i=0;i<9;i++) {
            this->conquered_boards[i] = conquered_boards[i];
        }


        this->update_megaboard_state();

}

void Map::update_megaboard_state() {
    return;
}

tile Map::opp() {
    return this->player == O ? X : O;
}

void Map::createChild() {
    //this->children.push_back(new Map(this->
}

string tile2txt(tile tile1, tile board_tile) {
    switch (board_tile) {
    case B:
        switch (tile1) {
        case B:
            return " ";
            break;
        case X:
            return color->red + "X" + color->END;
            break;
        case O:
            return color->blue + "O" + color->END;
            break;
        case W:
            return color->magenta + "W" + color->END;
            break;
        }
    case W:
        switch (tile1) {
        case B:
            return " ";
            break;
        case X:
            return color->magenta + "X" + color->END;
            break;
        case O:
            return color->magenta + "O" + color->END;
            break;
        case W:
            return color->magenta + "W" + color->END;
            break;
        }
        break;
    case X:
        switch (tile1) {
        case B:
            return " ";
            break;
        case X:
            return color->red + "X" + color->END;
            break;
        case O:
            return color->red + "O" + color->END;
            break;
        case W:
            return color->red + "W" + color->END;
            break;
        }
        break;
    case O:
        switch (tile1) {
        case B:
            return " ";
            break;
        case X:
            return color->blue + "X" + color->END;
            break;
        case O:
            return color->blue + "O" + color->END;
            break;
        case W:
            return color->blue + "W" + color->END;
            break;
        }
        break;
    }
    return "?";
}

void Map::pretty_print_me() {
    cout<<string(19,'-')<<endl;
    for (int i=0; i<3; i++) {
        for (int j=0; j<3; j++) {
            cout << "| "  << tile2txt(megaboard[i*3+0][3*j+0], conquered_boards[i*3])
                          << tile2txt(megaboard[i*3+0][3*j+1], conquered_boards[i*3])
                          << tile2txt(megaboard[i*3+0][3*j+2], conquered_boards[i*3]);
            cout << " | " << tile2txt(megaboard[i*3+1][3*j+0], conquered_boards[i*3+1])
                          << tile2txt(megaboard[i*3+1][3*j+1], conquered_boards[i*3+1])
                          << tile2txt(megaboard[i*3+1][3*j+2], conquered_boards[i*3+1]);
            cout << " | " << tile2txt(megaboard[i*3+2][3*j+0], conquered_boards[i*3+2])
                          << tile2txt(megaboard[i*3+2][3*j+1], conquered_boards[i*3+2])
                          << tile2txt(megaboard[i*3+2][3*j+2], conquered_boards[i*3+2]);
            cout << " |" <<endl;
        }
     cout<<string(19,'-')<<endl;
    }
}

Map::~Map() {
    // clean up memory
    return;
}

colors::colors() {
    disabled = false;
    magenta = "\033[95m";
    blue = "\033[94m";
    green = "\033[92m";
    yellow = "\033[93m";
    red = "\033[91m";
    END = "\033[0m";
}

void colors::disable() {
    disabled = true;
    magenta = "";
    blue = "";
    green = "";
    yellow = "";
    red = "";
    END = "";
}
