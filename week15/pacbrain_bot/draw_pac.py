
import curses

CP_PACMAN = 0
CP_R_GHOST = 0
CP_R_EYES = 0
CP_G_GHOST = 0
CP_G_EYES = 0
CP_WALL = 0

def init_color():
	global CP_PACMAN
	global CP_R_GHOST
	global CP_R_EYES
	global CP_G_GHOST
	global CP_G_EYES
	global CP_WALL

	curses.start_color()

	curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)

	curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)

	curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(5, curses.COLOR_RED, curses.COLOR_WHITE)

	curses.init_pair(6, curses.COLOR_BLUE, curses.COLOR_BLACK)

	CP_PACMAN = curses.color_pair(1)

	CP_R_GHOST = curses.color_pair(2)
	CP_R_EYES = curses.color_pair(3)

	CP_G_GHOST = curses.color_pair(4)
	CP_G_EYES = curses.color_pair(5)

	CP_WALL = curses.color_pair(6)	

box_size = 3

def draw_pacman(scr, y, x, pac_dir):
	calcY = y * box_size
	calcX = x * box_size

	for adjY in range(3):
		for adjX in range(3):
			scr.addstr(calcY + adjY, calcX + adjX,"█", CP_PACMAN)

	if pac_dir == 1:
		scr.addstr(calcY, calcX + 1, " ")
		scr.addstr(calcY + 1, calcX + 1, " ")
	elif pac_dir == 2:
		scr.addstr(calcY + 1, calcX, " ")
		scr.addstr(calcY + 1, calcX + 1, " ")
	elif pac_dir == 3:
		scr.addstr(calcY + 1, calcX + 1, " ")
		scr.addstr(calcY + 2, calcX + 1, " ")
	else:
		scr.addstr(calcY + 1, calcX + 1, " ")
		scr.addstr(calcY + 1, calcX + 2, " ")

def draw_red(scr, y, x, ghost_dir):
	calcY = y * box_size
	calcX = x * box_size

	if ghost_dir == 1:
		scr.addstr(calcY, calcX, "▀", CP_R_EYES)
		scr.addstr(calcY, calcX + 2, "▀", CP_R_EYES)
	else:
		scr.addstr(calcY, calcX, "▄", CP_R_EYES)
		scr.addstr(calcY, calcX + 2, "▄", CP_R_EYES)
	scr.addstr(calcY, calcX + 1, "█", CP_R_GHOST)

	scr.addstr(calcY + 1, calcX,     "█", CP_R_GHOST)
	scr.addstr(calcY + 1, calcX + 1, "█", CP_R_GHOST)
	scr.addstr(calcY + 1, calcX + 2, "█", CP_R_GHOST)

	scr.addstr(calcY + 2, calcX,     "▀", CP_R_GHOST)
	scr.addstr(calcY + 2, calcX + 1, "▀", CP_R_GHOST)
	scr.addstr(calcY + 2, calcX + 2, "▀", CP_R_GHOST)

def draw_green(scr, y, x, ghost_dir):
	calcY = y * box_size
	calcX = x * box_size

	if ghost_dir == 1:
		scr.addstr(calcY, calcX, "▀", CP_G_EYES)
		scr.addstr(calcY, calcX + 2, "▀", CP_G_EYES)
	else:
		scr.addstr(calcY, calcX, "▄", CP_G_EYES)
		scr.addstr(calcY, calcX + 2, "▄", CP_G_EYES)
	scr.addstr(calcY, calcX + 1, "█", CP_G_GHOST)

	scr.addstr(calcY + 1, calcX,     "█", CP_G_GHOST)
	scr.addstr(calcY + 1, calcX + 1, "█", CP_G_GHOST)
	scr.addstr(calcY + 1, calcX + 2, "█", CP_G_GHOST)

	scr.addstr(calcY + 2, calcX,     "▀", CP_G_GHOST)
	scr.addstr(calcY + 2, calcX + 1, "▀", CP_G_GHOST)
	scr.addstr(calcY + 2, calcX + 2, "▀", CP_G_GHOST)

def draw_void(scr, y, x):
	calcY = y * box_size
	calcX = x * box_size

	for adjY in range(3):
		for adjX in range(3):
			scr.addstr(calcY + adjY, calcX + adjX," ")

def draw_dot(scr, y, x):
	calcY = y * box_size
	calcX = x * box_size

	for adjY in range(3):
		for adjX in range(3):
			scr.addstr(calcY + adjY, calcX + adjX," ")
	scr.addstr(calcY + 1, calcX + 1,"█")

def draw_box(scr, y, x):
	calcY = y * box_size
	calcX = x * box_size

	for adjY in range(3):
		for adjX in range(3):
			scr.addstr(calcY + adjY, calcX + adjX,"█", CP_WALL)
	scr.addstr(calcY + 1, calcX + 1, "▒", CP_WALL)

def draw_vert(scr, y, x):
	calcY = y * box_size
	calcX = x * box_size

	scr.addstr(calcY,     calcX, "█", CP_WALL)
	scr.addstr(calcY + 1, calcX, "█", CP_WALL)
	scr.addstr(calcY + 2, calcX, "█", CP_WALL)

	scr.addstr(calcY,     calcX + 1, "▒", CP_WALL)
	scr.addstr(calcY + 1, calcX + 1, "▒", CP_WALL)
	scr.addstr(calcY + 2, calcX + 1, "▒", CP_WALL)

	scr.addstr(calcY,     calcX + 2, "█", CP_WALL)
	scr.addstr(calcY + 1, calcX + 2, "█", CP_WALL)
	scr.addstr(calcY + 2, calcX + 2, "█", CP_WALL)

def draw_horiz(scr, y, x):
	calcY = y * box_size
	calcX = x * box_size

	scr.addstr(calcY, calcX,     "█", CP_WALL)
	scr.addstr(calcY, calcX + 1, "█", CP_WALL)
	scr.addstr(calcY, calcX + 2, "█", CP_WALL)

	scr.addstr(calcY + 1, calcX,     "▒", CP_WALL)
	scr.addstr(calcY + 1, calcX + 1, "▒", CP_WALL)
	scr.addstr(calcY + 1, calcX + 2, "▒", CP_WALL)

	scr.addstr(calcY + 2, calcX,     "█", CP_WALL)
	scr.addstr(calcY + 2, calcX + 1, "█", CP_WALL)
	scr.addstr(calcY + 2, calcX + 2, "█", CP_WALL)

def draw_UL(scr, y, x):
	calcY = y * box_size
	calcX = x * box_size

	scr.addstr(calcY, calcX,     "█", CP_WALL)
	scr.addstr(calcY, calcX + 1, "█", CP_WALL)
	scr.addstr(calcY, calcX + 2, "█", CP_WALL)

	scr.addstr(calcY + 1, calcX,     "█", CP_WALL)
	scr.addstr(calcY + 1, calcX + 1, "▒", CP_WALL)
	scr.addstr(calcY + 1, calcX + 2, "▒", CP_WALL)

	scr.addstr(calcY + 2, calcX,     "█", CP_WALL)
	scr.addstr(calcY + 2, calcX + 1, "▒", CP_WALL)
	scr.addstr(calcY + 2, calcX + 2, "█", CP_WALL)

def draw_UR(scr, y, x):
	calcY = y * box_size
	calcX = x * box_size

	scr.addstr(calcY, calcX,     "█", CP_WALL)
	scr.addstr(calcY, calcX + 1, "█", CP_WALL)
	scr.addstr(calcY, calcX + 2, "█", CP_WALL)

	scr.addstr(calcY + 1, calcX,     "▒", CP_WALL)
	scr.addstr(calcY + 1, calcX + 1, "▒", CP_WALL)
	scr.addstr(calcY + 1, calcX + 2, "█", CP_WALL)

	scr.addstr(calcY + 2, calcX,     "█", CP_WALL)
	scr.addstr(calcY + 2, calcX + 1, "▒", CP_WALL)
	scr.addstr(calcY + 2, calcX + 2, "█", CP_WALL)

def draw_LL(scr, y, x):
	calcY = y * box_size
	calcX = x * box_size

	scr.addstr(calcY, calcX,     "█", CP_WALL)
	scr.addstr(calcY, calcX + 1, "▒", CP_WALL)
	scr.addstr(calcY, calcX + 2, "█", CP_WALL)

	scr.addstr(calcY + 1, calcX,     "█", CP_WALL)
	scr.addstr(calcY + 1, calcX + 1, "▒", CP_WALL)
	scr.addstr(calcY + 1, calcX + 2, "▒", CP_WALL)

	scr.addstr(calcY + 2, calcX,     "█", CP_WALL)
	scr.addstr(calcY + 2, calcX + 1, "█", CP_WALL)
	scr.addstr(calcY + 2, calcX + 2, "█", CP_WALL)

def draw_LR(scr, y, x):
	calcY = y * box_size
	calcX = x * box_size

	scr.addstr(calcY, calcX,     "█", CP_WALL)
	scr.addstr(calcY, calcX + 1, "▒", CP_WALL)
	scr.addstr(calcY, calcX + 2, "█", CP_WALL)

	scr.addstr(calcY + 1, calcX,     "▒", CP_WALL)
	scr.addstr(calcY + 1, calcX + 1, "▒", CP_WALL)
	scr.addstr(calcY + 1, calcX + 2, "█", CP_WALL)

	scr.addstr(calcY + 2, calcX,     "█", CP_WALL)
	scr.addstr(calcY + 2, calcX + 1, "█", CP_WALL)
	scr.addstr(calcY + 2, calcX + 2, "█", CP_WALL)

def draw_vert_cap_down(scr, y, x):
	calcY = y * box_size
	calcX = x * box_size

	draw_vert(scr, y, x)

	scr.addstr(calcY + 2, calcX + 1, "█", CP_WALL)

def draw_vert_cap_up(scr, y, x):
	calcY = y * box_size
	calcX = x * box_size

	draw_vert(scr, y, x)

	scr.addstr(calcY, calcX + 1, "█", CP_WALL)

def draw_horiz_cap_left(scr, y, x):
	calcY = y * box_size
	calcX = x * box_size

	draw_horiz(scr, y, x)

	scr.addstr(calcY + 1, calcX, "█", CP_WALL)

def draw_horiz_cap_right(scr, y, x):
	calcY = y * box_size
	calcX = x * box_size

	draw_horiz(scr, y, x)

	scr.addstr(calcY + 1, calcX + 2, "█", CP_WALL)