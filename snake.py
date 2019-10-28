import tkinter as tk
import random as rand

# Consts
DEBUG = True

# For Main Menu
MAIN_MENU_WIDTH = 400
MAIN_MENU_HEIGHT = 500
BUTTON_WIDTH = 10

# For game
GAME_WIDTH = 800
GAME_HEIGHT = 800
SIZE = 50
SPEED = 300
GAME_ = False
SCORE = 0
SCORE_TEXT = None

# Objects
root = None
canv = None

# Game OBJECTS
SNAKE = None
APPLE = None

# Lists
MAIN_MENU = []
GAME_WINDOW_CONFIG = {"width" : GAME_WIDTH, "height" : GAME_HEIGHT}

# Classes
class apple:
	def __init__(self, canv):
		global SIZE, GAME_WIDTH, GAME_HEIGHT
		self.SIZE = SIZE
		self.canv = canv
		x, y = rand.randint(0, GAME_WIDTH / SIZE) - 1, rand.randint(0, GAME_HEIGHT / SIZE - 1)
		self.obj = canv.create_oval(SIZE * x, SIZE * y, SIZE * (x + 1), SIZE * (y + 1), fill = 'red')

	def re(self):
		x, y = rand.randint(0, GAME_WIDTH / SIZE - 1), rand.randint(0, GAME_HEIGHT / SIZE - 1)
		self.canv.delete(self.obj)
		self.obj = canv.create_oval(SIZE * x, SIZE * y, SIZE * (x + 1), SIZE * (y + 1), fill = 'red')


class snake:
	def __init__(self, canv, color):
		global SIZE
		self.SIZE = SIZE
		self.color = color
		self.canv = canv 
		self.vector = ['r','r','r']
		self.segments = [canv.create_rectangle(SIZE * 4, SIZE, SIZE * 5, SIZE * 2, fill = color[0], outline = color[0]),
		canv.create_rectangle(SIZE * 3, SIZE, SIZE * 4, SIZE * 2, fill = color[1], outline = color[1]),
		canv.create_rectangle(SIZE * 2, SIZE, SIZE * 3, SIZE * 2, fill = color[1], outline = color[1])] # list for all segments

	def check_self_eat(self):
		el = self.segments[0]
		for el_ in self.segments:
			if(el == el_):
				continue
			if(self.canv.coords(el) == self.canv.coords(el_)):
				return True
		return False

	def check_apple_eat(self):
		global APPLE
		if(self.canv.coords(self.segments[0]) == self.canv.coords(APPLE.obj)):
			self.add_seg()
			APPLE.re()

	def add_seg(self):
		global SCORE, SCORE_TEXT, GAME_WIDTH
		SCORE += 10
		self.canv.delete(SCORE_TEXT)
		SCORE_TEXT = self.canv.create_text(GAME_WIDTH / 2, 10, font = 'Arial 20', fill = 'red', text = str(SCORE))
		coords = self.canv.coords(self.segments[len(self.segments)-1])
		if(self.vector[len(self.vector)-1] == 'r'):
			coords[0] -= self.SIZE
			coords[2] -= self.SIZE
		elif(self.vector[len(self.vector)-1] == 'l'):
			coords[0] += self.SIZE
			coords[2] += self.SIZE
		if(self.vector[len(self.vector)-1] == 'u'):
			coords[1] += self.SIZE
			coords[3] += self.SIZE
		if(self.vector[len(self.vector)-1] == 'd'):
			coords[1] -= self.SIZE
			coords[3] -= self.SIZE
		self.segments.append(self.canv.create_rectangle(coords[0], coords[1], coords[2], coords[3], fill = self.color[1], outline = self.color[1]))
		self.vector.append(self.vector[len(self.vector)-1])

	def move(self, vector = "", root = None, SPEED = None): # vector : l, r, u, d
		if(vector != ""):
			self.vector[0] = vector
		i = 0
		if(self.check_self_eat()):
			GAME_ = False
			# DEFEAT BY SELF EAT
			return
		self.check_apple_eat()
		for seg in self.segments:
			if(self.vector[i] == 'r'):
				self.canv.move(seg, self.SIZE, 0)
			elif(self.vector[i] == 'l'):
				self.canv.move(seg, -self.SIZE, 0)
			elif(self.vector[i] == 'd'):
				self.canv.move(seg, 0, self.SIZE)
			elif(self.vector[i] == 'u'):
				self.canv.move(seg, 0, -self.SIZE)
			i += 1
		for i in range(0, len(self.vector) - 1):
			k = len(self.vector)- 1 - i
			self.vector[k] = self.vector[k - 1]
		if(root != None):
			root.after(SPEED, lambda: self.move(root = root, SPEED = SPEED))


	def bind(self, root):
		root.bind('a', lambda a: self.move('l'))
		root.bind('d', lambda a: self.move('r'))
		root.bind('s', lambda a: self.move('d'))
		root.bind('w', lambda a: self.move('u'))

# Functions
def grid(canv, GAME_WINDOW_CONFIG):
	global SIZE
	for i in range(0, GAME_WINDOW_CONFIG['width'], SIZE):
		canv.create_line(i, 0, i, GAME_WINDOW_CONFIG['width'], width = 2, fill = 'red')
	for i in range(0, GAME_WINDOW_CONFIG['height'], SIZE):
		canv.create_line(0, i, GAME_WINDOW_CONFIG['height'], i, width = 2, fill = 'red')

def start(root, canv, GAME_WINDOW_CONFIG, objects_list):
	global SNAKE, GAME_, DEBUG, SPEED, APPLE
	GAME_ = True
	# Prepare GAME WINDOW
	for object in objects_list:
		object.destroy()
	geometry, x, y = str(root.geometry()).split("+")
	root.geometry(str(GAME_WINDOW_CONFIG['width']) + "x" + str(GAME_WINDOW_CONFIG['height']) + "+" + str(x) + "+" + str(y))
	canv.configure(width = GAME_WINDOW_CONFIG['width'], height = GAME_WINDOW_CONFIG['height'])
	canv.pack()
	# Prepare GAME configurations
	APPLE = apple(canv)
	SNAKE = snake(canv, ['blue', 'green'])
	SNAKE.bind(root)
	if(DEBUG):
		grid(canv, GAME_WINDOW_CONFIG)
		root.bind("l", lambda a: SNAKE.add_seg())
	root.after(SPEED, lambda: SNAKE.move(root = root, SPEED = SPEED))

# Main window
root = tk.Tk()
root.title("Snake - main menu")
root.geometry(str(MAIN_MENU_WIDTH)+"x"+str(MAIN_MENU_HEIGHT)+"+150+150")
root.iconbitmap("img.ico")
# Canvas object
canv = tk.Canvas(root, width = MAIN_MENU_WIDTH, height = MAIN_MENU_HEIGHT, bg = "#e7ff6e")

# Main Menu buttons
b_frame = tk.Frame(root, width = 169, height = 234, bg = "#e7ff6e") 

b_start = tk.Button(b_frame, bg = '#d16eff', width = BUTTON_WIDTH,font = 'Georgia 20', text = "Start", 
	command = lambda: start(root, canv, GAME_WINDOW_CONFIG, MAIN_MENU))
b_score = tk.Button(b_frame, bg = '#d16eff', width = BUTTON_WIDTH,font = 'Georgia 20', text = "Score", command = None)
b_exit = tk.Button(b_frame, bg = '#d16eff', width = BUTTON_WIDTH,font = 'Georgia 20', text = "Exit", command = root.quit)

b_exit.place(x = 0, y = 180)
b_score.place(x = 0, y = 90)
b_start.place(x = 0, y = 0)
b_frame.place(x = MAIN_MENU_WIDTH / 2 - 90, y = 120)

MAIN_MENU.append(b_start)
MAIN_MENU.append(b_score)
MAIN_MENU.append(b_exit)
MAIN_MENU.append(b_frame)

if(DEBUG):
	root.bind("q", lambda a: root.quit())

canv.pack() # use pack() because we need root at (0, 0)
root.mainloop()