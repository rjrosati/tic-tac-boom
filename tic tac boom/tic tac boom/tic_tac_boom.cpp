#include "map.h"
#include "lodepng.h" // to read image, native screenshots are pngs in android


colors* color = new colors();
int main(int argc, char** argv) {
	string fname_img = argc > 1 ? argv[1] : "test.png";
	tile root_mboard[9][9] = { {B} };
	tile root_cboards[9] = { B };

	tile next_player =  B ;
	board next_board = BOARD_UL;

	// naive image checking
	// basically, O's have a hole, X's don't
	// check that pixel:
	// if white we have an X
	// else check a pixel where an O would be
	// if white we have an O
	// else we have a blank

#ifdef _MSC_VER // if using microsoft compiler
	color->disable(); // Microsoft, in its infinite wisdom, didn't give cmd.exe ANSI support
#endif

	std::vector<unsigned char> image; //the raw pixels
	unsigned int max_X, max_Y;

	//decode
	unsigned int error = lodepng::decode(image, max_X, max_Y, fname_img);

	//if there's an error, display it
	if (error) std::cout << "decoder error " << error << ": " << lodepng_error_text(error) << std::endl;

	//the pixels are now in the vector "image", 4 bytes per pixel, ordered RGBARGBA...

	// magic numbers pulled from a 1080x1920 image, hopefully scale with size.
	unsigned int spacing       = (unsigned int)(max_X * (107.0 / 1080.0)); // from one tile to next, assume same in X and Y
	unsigned int board_start_Y = (unsigned int)(max_Y * (625.0 / 1920.0)); // coords of center of upper-left tile
	unsigned int board_start_X = spacing;
	unsigned int board_spacing = (unsigned int)(max_X * (326.0 / 1080.0)); // distance between individual boards
	unsigned int O_correction  = (unsigned int)(max_X * (23.0  / 1080.0));
    unsigned int tile_corrxion = (unsigned int)(max_X * ()); 
	unsigned int next_player_X = (unsigned int)(max_X * (543.0 / 1080.0)); // coords of large center X or O
	unsigned int next_player_Y = (unsigned int)(max_Y * (352.0 / 1080.0));
    unsigned int next_player_c = (unsigned int)(max_X * (635.0 / 1080.0)); // X for red or blue spot near giant X or O
	unsigned int next_player_blank_X = (unsigned int)(max_X * (671.0 / 1080.0)); // X for outer ring of this X or O

	std::cout << "First pixel R: " << (int)image[(board_start_Y*max_X + board_start_X) * 4 + 0]
					   	<<  " G: " << (int)image[(board_start_Y*max_X + board_start_X) * 4 + 1]
						<<  " B: " << (int)image[(board_start_Y*max_X + board_start_X) * 4 + 2]
						<<  " A: " << (int)image[(board_start_Y*max_X + board_start_X) * 4 + 3]
						<< std::endl;

	unsigned char next_player_R, next_player_G, next_player_B;
	unsigned char next_player_blank_R, next_player_blank_G, next_player_blank_B;
	next_player_R = image[(next_player_Y*max_X + next_player_X) * 4];
	next_player_G = image[(next_player_Y*max_X + next_player_X) * 4 + 1];
	next_player_B = image[(next_player_Y*max_X + next_player_X) * 4 + 2];
	if (next_player_R == 255 && next_player_G == 255 && next_player_B == 255) {
		next_player = X;
	}
	else {
		next_player = O;
	}
	next_player_R = image[(next_player_Y*max_X + next_player_c) * 4 + 0];
	next_player_G = image[(next_player_Y*max_X + next_player_c) * 4 + 1];
	next_player_B = image[(next_player_Y*max_X + next_player_c) * 4 + 2];

	next_player_blank_R = image[(next_player_Y*max_X + next_player_blank_X) * 4 + 0];
	next_player_blank_G = image[(next_player_Y*max_X + next_player_blank_X) * 4 + 1];
	next_player_blank_B = image[(next_player_Y*max_X + next_player_blank_X) * 4 + 2];

	unsigned char r, g, b;
	unsigned int x, y;
	for (int i = 0; i < 9; i++) {
		for (int j = 0; j < 9; j++) {

			x = board_start_X + (j%3)*spacing + (i%3)*board_spacing;
			y = board_start_Y + (j/3)*spacing + (i/3)*board_spacing;

			r = image[(y*max_X + x) * 4 + 0];
			g = image[(y*max_X + x) * 4 + 1];
			b = image[(y*max_X + x) * 4 + 2];

			if (r == 255 && g == 255 && b == 255) { // all white, this is an X
				root_mboard[i][j] = X;
                // determine square state
                // check top right corner, see if this X is opposite colored
                if (root_cboards[i] == B) {
                    
                }
			}
			else {
				// check where an O should be
				x += O_correction;

				r = image[(y*max_X + x) * 4 + 0];
				g = image[(y*max_X + x) * 4 + 1];
				b = image[(y*max_X + x) * 4 + 2];
				if (r == 255 && g == 255 && b == 255) {
					root_mboard[i][j] = O;
				}
				else {
                 // already initialized to B, check if this board has been won
                 if (r==next_player_blank_R && g == next_player_blank_G && b == next_player_blank_B) {
                     // this board is owned by next player
                     root_cboards[i] = next_player;

                 }
                 else if (r==167 && g ==167 && b==167) {
                    // this board is owned by no one
                    root_cboards[i] = B;
                 }
                 else {
                    // this board is owned by opp
                    root_cboards[i] = next_player == O ? X : O;
                 }

                }
			}
		} // end j loop
	} // end i loop



    Map * root = new Map(root_mboard,next_board,next_player,root_cboards,NULL,0);

    root->pretty_print_me();

    // now have read in image info, check if it's right
    char ans;
    std::cout << "Is this correct? (y/n): ";
    std::cin >> ans;
    if (ans == 'n' || ans == 'N') {
        // maybe offer ability to make corrections, etc.
        return -1;
    }

    delete root;

    return 0;
}
