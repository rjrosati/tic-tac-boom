import sys
import pdb

class colors:
	# ANSI escape codes for color printout.
	# Probably won't work in Windows CMD
	disabled = False
	magenta = '\033[95m'
	blue = '\033[94m'
	green = '\033[92m'
	yellow = '\033[93m'
	red = '\033[91m'
	END = '\033[0m'
	def disable(self):
		self.disabled = True
		self.magenta = ''
		self.blue = ''
		self.green = ''
		self.yellow = ''
		self.red = ''
		self.END = ''
		
def mk_color(s, t):
	global color
	# board state overrides intrinsic color
	# X's are red, O's are blue. W's are purple, (and so are you)
	if t == ' ':
		if s == 'O':
			return color.blue + s + color.END
		elif s == 'X':
			return color.red + s + color.END
		else:	
			return s
	elif t == 'W':
		return color.magenta + s + color.END
	elif t == 'X':
		return color.red + s + color.END
	elif t == 'O':
		return color.blue + s + color.END
	else:
		return s
		
		
class Map:
	def __init__(self, tiles, board_to_move, player, conquered=[' ']*9, parent=None, depth=0):
		if len(tiles)!= 9 and len(tiles[0])!= 9:
			#error, wrong size
			sys.exit("Bad array size")
		self.Map = tiles
		self.conquered_boards = conquered[:]
		self.conquests_locked = False
		self.board_to_move = board_to_move
		self.children = []
		self.player = player
		self.parent = parent
		self.depth = depth
		self.forced_win_possible = ' '
		self.state = ' '
	def createChild(self, new_map, board_to_move, player):
		self.children.append(Map(new_map, board_to_move, player, self.conquered_boards[:], self, self.depth+1))
	def which_boards_won(self):
		won_boards = [' ']*9
		for i in range(len(self.Map)):
			state = self.board_state(self.Map[i], self.player)
			won_boards[i] = state
		return won_boards
	def board_state(self, board, player):
		player2 = self.opp()
		if all(x in (player,'W') for x in [board[0],board[1],board[2]])  or \
		   all(x in (player,'W') for x in [board[3],board[4],board[5]])  or \
		   all(x in (player,'W') for x in [board[6],board[7],board[8]])  or \
		   all(x in (player,'W') for x in [board[0],board[3],board[6]])  or \
		   all(x in (player,'W') for x in [board[1],board[4],board[7]])  or \
		   all(x in (player,'W') for x in [board[2],board[5],board[8]])  or \
		   all(x in (player,'W') for x in [board[0],board[4],board[8]])  or \
		   all(x in (player,'W') for x in [board[2],board[4],board[6]]) :
		   return player
		elif all(x in (player2,'W') for x in [board[0],board[1],board[2]])  or \
		   all(x in (player2,'W') for x in [board[3],board[4],board[5]])  or \
		   all(x in (player2,'W') for x in [board[6],board[7],board[8]])  or \
		   all(x in (player2,'W') for x in [board[0],board[3],board[6]])  or \
		   all(x in (player2,'W') for x in [board[1],board[4],board[7]])  or \
		   all(x in (player2,'W') for x in [board[2],board[5],board[8]])  or \
		   all(x in (player2,'W') for x in [board[0],board[4],board[8]])  or \
		   all(x in (player2,'W') for x in [board[2],board[4],board[6]]) :
		   return player2
		elif self.board_unwinnable(board):
			return 'W'
		else: return ' '
	def opp(self):
		return 'X' if self.player == 'O' else 'O'
	def board_unwinnable(self, board):
		# boards are only unwinnable if full and not already won or...
		# one tile is empty and can't generate a win.
		# all combinations of more than one empty tile can be won
		if board.count(' ') > 1: return False
		if ' ' not in board: return True
		# one spot free, check to see if board winnable
		board_cpy = board[:]
		board_cpy[board.index(' ')] = self.player
		if self.board_state(board_cpy, self.player) == 'W':
			board_cpy = board[:]
			board_cpy[board.index(' ')] = self.opp()
			if self.board_state(board_cpy, self.opp()) == 'W':
				return True
		return False
	def Map_state(self):
		if not self.conquests_locked:
			self.lock_in_conquests()
		#print(self.conquered_boards)
		state = self.board_state(self.conquered_boards, self.player)
		return state
	def lock_in_conquests(self):
		won_boards_now = self.which_boards_won()
		for i in range(9):
			if self.conquered_boards[i] == ' ':
				self.conquered_boards[i] = won_boards_now[i]
		self.conquests_locked = True
	def generate_possible_moves(self):
		if self.Map_state() != ' ':
			raise StopIteration
		if self.depth + 1 > MAX_DEPTH:
			raise StopIteration
		board = self.Map[self.board_to_move]
		new_map = self.Map[:]
		if ' ' not in board:
			# sent to full square, look at full map for possibilities
			for i in range(len(self.Map)):
				new_map = self.Map[:]
				for j in range(len(self.Map[i])):
					if self.Map[i][j] != ' ': continue
					new_board = self.Map[i][:]
					new_board[j] = self.player
					new_map[i] = new_board
					yield (new_map[:], j)
		for i in range(len(board)):
			if board[i] != ' ': continue
			new_board = board[:]
			new_board[i] = self.player
			new_map[self.board_to_move] = new_board
			#print("player: " + self.player + " moved in board " + str(self.board_to_move) + " on tile " + str(i))
			yield (new_map[:], i)


def make_babies(this_map):
	# pdb.set_trace()
	global nodes
	# explore all possible moves, make children of this map
	for (move, board_to_move) in this_map.generate_possible_moves():
		this_map.createChild(move, board_to_move, this_map.opp())
	nodes += len(this_map.children)
	#if (nodes%10000==0):
	#	print(nodes, this_map.depth)
	#elif this_map.depth<4:
	#	print(nodes, this_map.depth)
	for child in this_map.children:
		child.lock_in_conquests()
		#pretty_print_Map(child.Map)
		#print("player: " + child.player + " on board " + str(child.board_to_move))
		#print(child.conquered_boards)
		#raw_input()
	for child in this_map.children:
		make_babies(child)

def print_babies(this_map):
	for child in this_map.children:
		print_babies(child)
	else:
		pretty_print_Map(this_map.Map)
		#print(this_map.Map)
		print(this_map.conquered_boards)
		print(this_map.Map_state())

def pretty_print_map(this_map):
	global color
	print(" "+"-"*19)
	for i in range(3):
		#print one row of Map
		for j in range(3):
			t = this_map.conquered_boards[3*i:3*(i+1)]
			print(' | '+''.join([mk_color(x,t[0]) for x in this_map.Map[i*3+0][j*3:(j+1)*3]])+' | '+
						''.join([mk_color(x,t[1]) for x in this_map.Map[i*3+1][j*3:(j+1)*3]])+' | '+
						''.join([mk_color(x,t[2]) for x in this_map.Map[i*3+2][j*3:(j+1)*3]])+' | ')	
		print(" "+"-"*19)
	if color.disabled:
		print(this_map.conquered_boards)
	if this_map.state in ('X','O'):
		print(this_map.Map_state() + ' wins.')
	elif this_map.state == 'W':
		print('Draw.')
	else:
		print("Next move: " +this_map.player + " on board " + str(this_map.board_to_move))


def get_stats(this_map):
	global X_wins, O_wins, draws, oops, root
	if len(this_map.children) != 0:
		for child in this_map.children:
			get_stats(child)
	else: 
		#pdb.set_trace()
		this_map.state = this_map.Map_state()
		if this_map.state == 'X':
			X_wins+=1
		elif this_map.state == 'O':
			O_wins+=1
		elif this_map.state == 'W':
			draws+=1
		else: # still unknown
			oops+=1
			# pretty_print_map(this_map)

def update_wins(this_map):
	for child in this_map.children:
		update_wins(child)
		child.state = child.Map_state()

def tag_forced_wins(this_map):
	# a state is forced win for player if all child states have forced_win_possible==player 
	# a state is forced win for opp if one child state has forced_win_possible==opp
	# a won state has forced_win_possible==player
	# pdb.set_trace()
	if len(this_map.children) != 0:
		for child in this_map.children:
			tag_forced_wins(child)
	else:
		if this_map.Map_state() in ['X','O']:
			tag_up(this_map)
	
def tag_up(this_map):
	global fwins
	#pdb.set_trace()
	if this_map.state in ('X','O'):
		this_map.forced_win_possible = this_map.state
		fwins.append(this_map)
		#assert(this_map.state == this_map.opp())
		assert(len(this_map.children)==0)
		tag_up(this_map.parent)
	else:
		player_fwin = True
		for child in this_map.children:
			# forced win for opp if one child state has forced_win_possible==opp
			if (child.forced_win_possible == this_map.opp()):
				this_map.forced_win_possible = this_map.opp()
				fwins.append(this_map)
			        if this_map.parent is not None:
				     tag_up(this_map.parent)
				return
			# forced win for player if all child states have forced_win_possible==player 
			elif (child.forced_win_possible != this_map.player):
				player_fwin = False
				# can't return here, might still need checks for opp
		if player_fwin:
			this_map.forced_win_possible = this_map.player
			fwins.append(this_map)
			if this_map.parent is not None:
				tag_up(this_map.parent)
				
'''				
root = Map([ ['X','X','O','O','X',' ','O',' ',' '], [' ',' ',' ',' ','X','X','O',' ',' '], ['O',' ','O','X','X','X','O',' ','X'],
			 [' ',' ',' ','X',' ','O','X','O','O'], ['O','X','X',' ','O',' ','O',' ','O'], [' ',' ',' ','X','X',' ',' ','O',' '],
			 ['X',' ','X',' ','X','O','O','X','O'], ['X',' ','O','X',' ','O',' ',' ',' '], [' ','O',' ',' ','O',' ','X','X',' '],
		   ],
		   0, 'O', [' ',' ','X',' ','O',' ',' ',' ',' '])
'''
'''
root = Map([ [' ',' ','X','O',' ','X',' ',' ',' '], ['X',' ',' ','O',' ',' ',' ',' ',' '], ['O','O',' ',' ',' ',' ',' ','X',' '],
			 [' ','X','X','O',' ',' ',' ',' ',' '], ['X',' ',' ',' ',' ',' ',' ',' ','X'], [' ',' ',' ','X',' ','O',' ',' ',' '],
			 [' ',' ',' ','X',' ','X',' ','O','O'], [' ',' ',' ',' ','O',' ',' ',' ',' '], [' ',' ','O',' ','X','O',' ',' ',' '],
		   ],
		   0, 'O', [' ',' ',' ',' ',' ',' ',' ',' ',' '])
'''
				
'''
root = Map([ ['X','O','O','X','O',' ','X','O','O'], ['X',' ',' ',' ',' ',' ',' ','O',' '], ['X',' ',' ',' ',' ','O',' ','X','O'],
			 ['O','X',' ',' ','O',' ',' ','X',' '], ['O','X','X',' ','X','O','X','O',' '], [' ',' ',' ','O','X','X','X',' ',' '],
			 ['O','O',' ','O','X',' ','O','X',' '], ['X','X',' ','X','X','X','O','O','X'], [' ',' ',' ',' ','O',' ','O','O','X'],
		   ],
		   1, 'O', ['O',' ',' ',' ','X',' ','O','X',' '])

'''
'''
root = Map([ ['X','X','O','O','X','X','O','O','O'], [' ','O',' ','O','X','X','O',' ','O'], ['O','X','O','X','X','X','O','X','X'],
			 ['X','X','O','X','O','O','X','O','O'], ['O','X','X','O','O','X','O',' ','O'], [' ',' ','O','X','X',' ','O','O','O'],
			 ['X','X','X','X','X','O','O','X','O'], ['X',' ','O','X','X','O','O',' ',' '], ['O','O',' ','X','O','X','X','X','X'],
		   ],
		   1, 'X', ['O',' ','X','X','O','O','X',' ','X'])
'''
		   
				
'''
root = Map([ ['O','O','X','O',' ','X','O',' ','O'], ['X','X','X','O','O','X','X','X','O'], ['O','O','O','X','X','O',' ','X','X'],
			 [' ',' ',' ','O','X','X','X','X','X'], [' ','O','X',' ','O','X','X','O','X'], ['O','O','O','O','X','X','O','O','O'],
			 ['X','O','O','X','X',' ','O','X','X'], ['X','X','X','O','O','O','O','X','O'], ['X',' ','X','O',' ','X','X','O','O'],
		   ],
		   8, 'O', ['O','X','O','X','O','O','X','X',' '])
'''

'''
root = Map([ ['O','O','X','O',' ',' ',' ',' ',' '], [' ','O','X',' ','O','X','X','O',' '], ['X','X','O','X','X','O','O','X','O'],
			 [' ',' ','X','O',' ',' ','O','X','X'], ['X',' ','O',' ',' ',' ','O','X','X'], ['O',' ',' ','O',' ',' ',' ',' ',' '],
			 [' ','X','O','O','X','X','X','X',' '], [' ',' ','O','O',' ','X','O','O',' '], [' ',' ','O',' ',' ',' ','X','X',' '],
		   ],
		   3, 'X', [' ','O','O',' ',' ',' ','X',' ',' '])
'''
		   
'''
root = Map([ ['O',' ','X',' ','O',' ','O',' ','O'], [' ','O',' ',' ','X',' ','O','O',' '], [' ',' ','X','O','O','O','O',' ','O'],
			 ['X',' ','X','O','X','O','O','O','O'], ['X','X','O','X','X','O','X','X','O'], [' ',' ',' ','X','O','X','X',' ',' '],
			 ['X',' ','O','X','O',' ','X','X','O'], [' ',' ','X','O','O',' ',' ',' ',' '], ['X','X','X','X','O',' ','X','X','X'],
		   ],
		   6, 'X', ['O',' ','O','O','O',' ','X',' ','X'])
'''

root = Map([ [' ','X','X',' ',' ',' ',' ',' ',' '], [' ',' ','O',' ',' ','X','X',' ','O'], ['O',' ','X','O',' ',' ','X','O','X'],
			 [' ',' ',' ',' ','X','X',' ',' ','X'], ['X','O',' ',' ',' ',' ',' ','O','X'], [' ',' ',' ','O','O','O',' ',' ','X'],
			 [' ','O',' ',' ',' ',' ','O','O','O'], [' ',' ','O','X',' ',' ','X','X',' '], [' ','O','O','O',' ','O','X','X','X'],
		   ],
		   3, 'X', [' ',' ',' ',' ',' ','O','O',' ','X'])
		   
'''
root = Map([ ['X','O',' ','X','O','X','X',' ','O'], ['O','O','X','X',' ','X',' ','O',' '], ['O','O','X',' ',' ','O','X',' ',' '],
			 ['X',' ','O',' ',' ','O',' ',' ','O'], [' ','X',' ','O',' ','O',' ',' ',' '], ['O','X',' ','O',' ',' ',' ',' ',' '],
			 [' ','O',' ',' ','X',' ',' ','X',' '], [' ','X',' ',' ',' ',' ',' ',' ',' '], ['X','X',' ','X',' ','X','O','O',' '],
		   ],
		   5, 'X', ['X',' ',' ','O',' ',' ',' ',' ',' '])
'''

nodes = 1
X_wins = 0
O_wins = 0
draws = 0
oops = 0
states = 0
fwins = []
color = colors()


MAX_DEPTH=9
#current_depth=0

#color.disable()
pretty_print_map(root)
sys.stdout.flush()
make_babies(root)
print("Total nodes: {0}".format(nodes))
get_stats(root)
states = X_wins+O_wins+draws+oops
print("X wins:  {0} ({1:.2%})".format(X_wins,float(X_wins)/states))
print("O_wins:  {0} ({1:.2%})".format(O_wins,float(O_wins)/states))
print("Draws:   {0} ({1:.2%})".format(draws,float(draws)/states))
print("Unknown: {0} ({1:.2%})".format(oops,float(oops)/states))
sys.stdout.flush()
tag_forced_wins(root)
min_depth_X = float("inf")
min_depth_O = float("inf")
max_depth = 0
highest_fwin_X = None
highest_fwin_O = None
real_fwins = []
for x in fwins:
	if x.state not in ('X','O'):
		real_fwins.append(x)
if len(real_fwins) > 0:
	for win in real_fwins:
		if win.forced_win_possible == 'X':
			if win.depth < min_depth_X:
				min_depth_X = win.depth
				highest_fwin_X = win
			if win.depth > max_depth:
				max_depth = win.depth
		else:
			if win.depth < min_depth_O:
				min_depth_O = win.depth
				highest_fwin_O = win
			if win.depth > max_depth:
				max_depth = win.depth
			
	print("Found " + str(len(real_fwins)) + " forced wins. Longest " + str(max_depth) + " moves.")
	#print("Shortest " + str() + " moves.")
	if highest_fwin_O is not None:
		print("Chain starts at depth {0} for {1}".format(highest_fwin_O.depth, highest_fwin_O.forced_win_possible))
		pretty_print_map(highest_fwin_O)
	if highest_fwin_X is not None:
		print("Chain starts at depth {0} for {1}".format(highest_fwin_X.depth, highest_fwin_X.forced_win_possible))
		pretty_print_map(highest_fwin_X)

	#pdb.set_trace()
else:
	print("No real forced wins found.")
