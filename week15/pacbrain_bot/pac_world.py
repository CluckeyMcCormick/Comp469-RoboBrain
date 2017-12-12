import draw_pac
import bot_comm as bot

import random
import copy

action_list = [0, 1, 2, 3]

action_dict = {
	0: (0, 1), 
	3: (1, 0),
	2: (0, -1),
	1: (-1, 0) 
}

template = [
	['╔', '═', '═', '═', '═', '═', '╗'],
	['║', '.', '.', '.', '.', '.', '║'],
	['║', '.', '.', '.', '#', '.', '║'],
	['║', '.', '.', '.', '.', '.', '║'],
	['║', '.', '#', '.', '.', '.', '║'],
	['║', '.', '.', '.', '.', '.', '║'],
	['╚', '═', '═', '═', '═', '═', '╝'],
]

template = [
	['╔', '═', '═', '═', '╗'],
	['║', '.', '.', '.', '║'],
	['║', '.', '.', '.', '║'],
	['║', '.', '.', '.', '║'],
	['║', '.', '.', '.', '║'],
	['╚', '═', '═', '═', '╝'],
]

template = [
	['╔', '═', '═', '═', '╗'],
	['║', '.', '.', '.', '║'],
	['║', '.', '.', '.', '║'],
	['║', '.', '#', '.', '║'],
	['║', '.', '.', '.', '║'],
	['╚', '═', '═', '═', '╝'],
]

ghost_dict = {
	1 : 3,
	3 : 1
}

passSet = {'.', ' '}

char_funcs = {
	'║' : draw_pac.draw_vert,
	'═' : draw_pac.draw_horiz,
	'╔' : draw_pac.draw_UL,
	'╗' : draw_pac.draw_UR,
	'╚' : draw_pac.draw_LL,
	'╝' : draw_pac.draw_LR,
	'.' : draw_pac.draw_dot,
	' ' : draw_pac.draw_void,
	'#' : draw_pac.draw_box,
	'D' : draw_pac.draw_vert_cap_down,
	'U' : draw_pac.draw_vert_cap_up,
	'L' : draw_pac.draw_horiz_cap_left,
	'R' : draw_pac.draw_horiz_cap_right,
}

PAC_INITIAL = ( 4, 3 )
# 0 is right, 1 is up
# 2 is left, 3 is down
PAC_START_DIR = 1

GHOST_GREEN_INITIAL = ( 4, 1 )
GHOST_GREEN_DIR = 1

GHOST_RED_INITIAL = ( 6, 3 )
GHOST_RED_DIR = 1

bot.initialize_comms(True)

class Pacworld:

	ROWS = len(template)
	COLS = len(template[0])

	def __init__(self):
		self.reset()

	def reset(self, useRandom=False):
		self.world = copy.deepcopy(template)
		self.pacmult = [ [0] * self.COLS for _ in range(self.ROWS)]

		self.pac_pos   = PAC_INITIAL #(6, 1)
		self.red_pos   = GHOST_RED_INITIAL #(random.randint(1, self.ROWS - 2), self.COLS - 2) #(6, 5)
		self.green_pos = GHOST_GREEN_INITIAL #(random.randint(1, self.ROWS - 2), 1) #(1, 1)

		self.red_dir   = GHOST_RED_DIR
		self.green_dir = GHOST_GREEN_DIR

		# 0 is right, 1 is up
		# 2 is left, 3 is down
		self.pac_dir = PAC_START_DIR

		self.dots = set()

		for y in range(self.ROWS):
			for x in range(self.COLS):
				if self.world[y][x] == '.':
					self.dots.add( (y, x) )

		self.complete = False

	def pac_actions(self):
		available = []

		y, x = self.pac_pos
		for a in action_list:
			addY, addX = action_dict[a]

			if self.valid_place(y + addY, x + addX):
				available.append(a)
		return available

	"""
	Generates a tuplet of what the next state will
	look like, given that pacman does pac_action
	The tuplet is like so:
	pac_pos, red_pos, red_dir, dot_eaten
	"""
	def predict_state(self, pac_action=None):

		new_pac_pos = self.pac_pos

		new_red_pos = self.red_pos
		new_red_dir = None

		new_green_pos = self.green_pos
		new_green_dir = None

		dot_eaten = False

		#PAC-MAN takes action
		if pac_action is not None:
			addY, addX = action_dict[pac_action]
			y, x = self.pac_pos

			if self.valid_place(y + addY, x + addX):
				new_pac_pos = (y + addY, x + addX)

				if self.world[y + addY][x + addX] == '.':
					dot_eaten = True
		
		if new_red_pos != new_pac_pos:
			#GHOST takes action
			action_taken = False
			new_red_dir = self.red_dir
			"""
			while not action_taken:
				addY, addX = action_dict[new_red_dir]
				y, x = new_red_pos

				if not self.valid_place(y + addY, x + addX):
					new_red_dir = ghost_dict[new_red_dir]
				else:
					new_red_pos = (y + addY, x + addX)
					action_taken = True
			"""
		else:
			dot_eaten = False

		if new_green_pos != new_pac_pos:
			action_taken = False
			new_green_dir = self.green_dir
			while not action_taken:

				addY, addX = action_dict[new_green_dir]
				y, x = new_green_pos

				if not self.valid_place(y + addY, x + addX):
					new_green_dir = ghost_dict[new_green_dir]
				else:
					new_green_pos = (y + addY, x + addX)
					action_taken = True
		else:
			dot_eaten = False

		return (new_pac_pos, (new_red_pos, new_red_dir), (new_green_pos, new_green_dir), dot_eaten)

	def do_step(self, scr, pac_action=None):

		reward = -1 

		if self.complete:
			#already complete
			return (True, reward)

		#Look at what we need to change
		result = self.predict_state(pac_action)
		#grab the results
		res_pac, res_red, res_green, res_dot = result

		#If our pacman changed, re-render and update
		if res_pac != self.pac_pos:
			newY, newX = res_pac
			oldY, oldX = self.pac_pos

			self.pac_pos = res_pac

			old_dir = self.pac_dir

			if (self.pac_dir % 2) != (pac_action % 2): 
				self.pac_dir = pac_action

			self.draw_tile( scr, newY, newX )
			self.draw_tile( scr, oldY, oldX )

			bot.do_action(old_dir, pac_action)

		self.pacmult[ self.pac_pos[0] ][ self.pac_pos[1] ] += 1

		#If we ate a dot, remove it
		if res_dot:
			y, x = self.pac_pos
			self.world[y][x] = ' '
			self.dots.discard( self.pac_pos )
			reward = 1							

		if res_red[0] != self.red_pos:
			newY, newX = res_red[0]
			oldY, oldX = self.red_pos
			
			self.red_pos = res_red[0]
			self.red_dir = res_red[1]

			self.draw_tile( scr, newY, newX )
			self.draw_tile( scr, oldY, oldX )

		if res_green[0] != self.green_pos:
			newY, newX = res_green[0]
			oldY, oldX = self.green_pos
			
			self.green_pos = res_green[0]
			self.green_dir = res_green[1]

			self.draw_tile( scr, newY, newX )
			self.draw_tile( scr, oldY, oldX )

		#If pacman and ghost are in the same place,
		#pacman loses! return -1
		if self.pac_pos == self.red_pos or self.pac_pos == self.green_pos:
			self.complete = True
			return (True, -15)

		#If no more dots, return 1!
		if not self.dots:
			self.complete = True
			return (True, 10)

		#Return 0 - we ain't done here yet!
		return (False, reward)


	def valid_place(self, y, x):
		if not (0 <= y < self.ROWS and 0 <= x < self.COLS):
			return False

		return self.world[y][x] in passSet

	def draw_world(self, scr):
		for y in range(self.ROWS):
			for x in range(self.COLS):
				self.draw_tile(scr, y, x)

	def draw_tile(self, scr, y, x):
		if (y, x) == self.red_pos:
			draw_pac.draw_red(scr, y, x, self.red_dir)
		elif (y, x) == self.green_pos:
			draw_pac.draw_green(scr, y, x, self.green_dir)
		elif (y, x) == self.pac_pos:
			draw_pac.draw_pacman(scr, y, x, self.pac_dir)
		else:
			func = char_funcs[ self.world[y][x] ]
			func(scr, y, x)