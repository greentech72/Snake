import tkinter as tk
import random as rand

# Consts
DEBUG = False

# For Main Menu
MAIN_MENU_WIDTH = 400
MAIN_MENU_HEIGHT = 500
BUTTON_WIDTH = 10
CHECK_BUTTON_VALUE = None

# For game
GAME_WIDTH = 800
GAME_HEIGHT = 800
SIZE = 50
SPEED = 500
DIE_BY_BORDER = False

# Objects
root = None
canv = None

# Lists
MAIN_MENU = []
GAME_WINDOW_CONFIG = {"width" : GAME_WIDTH, "height" : GAME_HEIGHT, "size" : SIZE, "in_game" : False, "speed" : SPEED, "score" : 0}
GAME_OBJECTS = {"snake" : None, "apple" : None}

# Classes
class apple:
	def __init__(self, canv, GAME_WINDOW_CONFIG):
		# Preparing consts
		SIZE = GAME_WINDOW_CONFIG['size']
		self.SIZE = SIZE
		self.canv = canv
		# Randomsize apple position
		x, y = rand.randint(0, GAME_WINDOW_CONFIG['width'] / SIZE) - 1, rand.randint(0, GAME_WINDOW_CONFIG['height'] / SIZE - 1)
		# Create apple
		self.obj = canv.create_oval(SIZE * x, SIZE * y, SIZE * (x + 1), SIZE * (y + 1), fill = '#e31251')

	# recreate out apple
	def re(self):
		# Randomize apple position
		x, y = rand.randint(0, GAME_WINDOW_CONFIG['width'] / SIZE - 1), rand.randint(0, GAME_WINDOW_CONFIG['height'] / SIZE - 1)
		# recreate apple
		self.canv.delete(self.obj)
		self.obj = canv.create_oval(SIZE * x, SIZE * y, SIZE * (x + 1), SIZE * (y + 1), fill = '#e31251')

class snake:
	def __init__(self, canv, color, WINDOW_WIDTH, WINDOW_HEIGHT, SIZE, APPLE, DIE_BY_BORDER):
		# Preparing consts
		self.DIE_BY_BORDER = DIE_BY_BORDER
		self.GAME_WIDTH = WINDOW_WIDTH
		self.GAME_HEIGHT = WINDOW_HEIGHT
		self.SIZE = SIZE
		self.color = color
		self.canv = canv 
		self.vector = ['r','r','r']
		self.SCORE = 0
		self.APPLE = APPLE
		self.SCORE_TEXT = self.canv.create_text(self.GAME_WIDTH / 2, 10, font = 'Arial 20', fill = 'red', text = str(self.SCORE))
		# Create snake
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

	def check_apple_eat(self, APPLE):
		if(self.canv.coords(self.segments[0]) == self.canv.coords(APPLE.obj)):
			self.add_seg()
			APPLE.re()
			return True
		return False

	def check_border(self):
		if(self.DIE_BY_BORDER):
			x1, y1, x2, y2 = self.canv.coords(self.segments[0])
			if(x1 < 0 or y1 < 0 or x2 > self.GAME_WIDTH or y2 > self.GAME_HEIGHT):
				return True
		else:
			for seg in self.segments:
				x1, y1, x2, y2 = self.canv.coords(seg)
				if(x1 < 0):
					x1 = self.GAME_WIDTH
					x2 = x1 + self.SIZE
				elif(x2 > self.GAME_WIDTH):
					x2 = 0
					x1 = 0 - self.SIZE
				if(y1 < 0):
					y1 = self.GAME_HEIGHT
					y2 = y1 + self.SIZE
				elif(y2 > self.GAME_HEIGHT):
					y2 = 0
					y1 = 0 - self.SIZE
				canv.coords(seg, x1, y1, x2, y2)
		return False

	def add_seg(self):
		self.SCORE += 10
		self.canv.delete(self.SCORE_TEXT)
		self.SCORE_TEXT = self.canv.create_text(self.GAME_WIDTH / 2, 10, font = 'Arial 20', fill = 'red', text = str(self.SCORE))
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
		APPLE = self.APPLE
		if(vector != ""):
			self.vector[0] = vector
		i = 0
		if(self.check_self_eat()):
			GAME_ = False
			print("DEFEAT")
			Defeat(0, canv, self.GAME_WIDTH, self.GAME_HEIGHT, self.SCORE)
			return
		if(self.check_apple_eat(APPLE) and SPEED != None):
			SPEED -= 10
		if(self.check_border()):
			Defeat(1, canv, self.GAME_WIDTH, self.GAME_HEIGHT, self.SCORE)
			print("DEFEAT")
			return 
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
# Grid function for DEBUG
def grid(canv, GAME_WINDOW_CONFIG):
	for i in range(0, GAME_WINDOW_CONFIG['width'], GAME_WINDOW_CONFIG['size']):
		canv.create_line(i, 0, i, GAME_WINDOW_CONFIG['width'], width = 2, fill = 'red')
	for i in range(0, GAME_WINDOW_CONFIG['height'], GAME_WINDOW_CONFIG['size']):
		canv.create_line(0, i, GAME_WINDOW_CONFIG['height'], i, width = 2, fill = 'red')

def save(name, score):
	file = open("data.dat", 'a+')
	file.write(str(name) + " : " + str(score) + "\n")
	file.close()

def score_save(root, SCORE):
	global BUTTON_WIDTH
	top = tk.Toplevel(root, bg = '#e7ff6e')	
	geometry, x, y = str(root.geometry()).split("+")
	top.geometry( "300x300+" + str(x) + "+" + str(y) )
	top.title("Score saver")
	# Edit
	e = tk.Entry(top, font = 'Georgia 20')
	tk.Label(top,bg = '#e7ff6e', text = "Enter your nickname", font = 'Georgia 20').place(x = 0, y = 0)
	b_exit = tk.Button(top, bg = '#d16eff', width = BUTTON_WIDTH, font = 'Georgia 20', text = "Exit", command = top.quit)
	b_comit = tk.Button(top, bg = '#d16eff', width = BUTTON_WIDTH, font = 'Georgia 20', text = "Submit", command = lambda: save(e.get(), SCORE))

	b_comit.place(x = 50, y = 90)
	b_exit.place(x = 50, y = 180)
	e.place(x = 0, y = 40)
	top.bind("q", lambda a: top.quit())
	top.mainloop()

def Defeat(reason, canv, WIDTH, HEIGHT, SCORE):
	global root
	# 0 - self
	# 1 - border
	canv.create_text(WIDTH / 2, HEIGHT/ 2, text = "Defeat by " +("self eat" if reason == 0 else "border"),fill = 'red', font = 'Arial 20')
	canv.create_text(WIDTH / 2, HEIGHT/ 2 + 30, text = "'q' for exit" ,fill = 'red', font = 'Arial 12')	
	canv.create_text(WIDTH / 2, HEIGHT/ 2 + 60, text = "'r' to restart your game" ,fill = 'red', font = 'Arial 12')	
	canv.create_text(WIDTH / 2, HEIGHT/ 2 + 90, text = "'h' to save your scorer" ,fill = 'red', font = 'Arial 12')	
	root.bind("h", lambda a: score_save(root, SCORE))

def start(root, canv, GAME_WINDOW_CONFIG, objects_list, GAME_OBJECTS, DIE_BY_BORDER):
	global DEBUG
	canv.delete("all")
	GAME_WINDOW_CONFIG['in_game'] = True
	# Prepare GAME WINDOW
	for object in objects_list:
		object.destroy()
	geometry, x, y = str(root.geometry()).split("+")
	root.geometry(str(GAME_WINDOW_CONFIG['width']) + "x" + str(GAME_WINDOW_CONFIG['height']) + "+" + str(x) + "+" + str(y))
	canv.configure(width = GAME_WINDOW_CONFIG['width'], height = GAME_WINDOW_CONFIG['height'])
	canv.pack()
	# Prepare GAME configurations
	GAME_OBJECTS['apple'] = apple(canv, GAME_WINDOW_CONFIG) 					# Create apple
	GAME_OBJECTS['snake'] = snake(canv, ['blue', 'green'], GAME_WINDOW_CONFIG['width'], GAME_WINDOW_CONFIG['height'],GAME_WINDOW_CONFIG['size'], 
	GAME_OBJECTS['apple'], DIE_BY_BORDER) 	# Create snake
	GAME_OBJECTS['snake'].bind(root)						# Standart binds
	if(DEBUG):
		grid(canv, GAME_WINDOW_CONFIG)
		root.bind("l", lambda a: GAME_OBJECTS['snake'].add_seg())
	# MAIN LOOP FUNCTION
	root.after(SPEED, lambda: GAME_OBJECTS['snake'].move(root = root, SPEED = GAME_WINDOW_CONFIG['speed']))

# START OF THE PROGRAM
#---------------------

# Main window configuration
root = tk.Tk()
root.title("Snake - main menu")
root.geometry(str(MAIN_MENU_WIDTH)+"x"+str(MAIN_MENU_HEIGHT)+"+150+150")
root.iconbitmap("img.ico")

# Canvas object
canv = tk.Canvas(root, width = MAIN_MENU_WIDTH, height = MAIN_MENU_HEIGHT, bg = "#e7ff6e")

# Main Menu buttons and their config
b_frame = tk.Frame(root, width = 200, height = 300, bg = "#e7ff6e") #e7ff6e 

b_start = tk.Button(b_frame, bg = '#d16eff', width = BUTTON_WIDTH,font = 'Georgia 20', text = "Start", 
	command = lambda: start(root, canv, GAME_WINDOW_CONFIG, MAIN_MENU, GAME_OBJECTS, DIE_BY_BORDER))
b_score = tk.Button(b_frame, bg = '#d16eff', width = BUTTON_WIDTH,font = 'Georgia 20', text = "Score", command = None)
b_exit = tk.Button(b_frame, bg = '#d16eff', width = BUTTON_WIDTH,font = 'Georgia 20', text = "Exit", command = root.quit)

b_exit.place(x = 0, y = 190)
b_score.place(x = 0, y = 110)
b_start.place(x = 0, y = 0)
b_frame.place(x = MAIN_MENU_WIDTH / 2 - 90, y = 110)

MAIN_MENU.append(b_start)
MAIN_MENU.append(b_score)
MAIN_MENU.append(b_exit)
MAIN_MENU.append(b_frame)

def BORDER(val):
	global DIE_BY_BORDER
	if(val):
		DIE_BY_BORDER = True
	else:
		DIE_BY_BORDER = False

# CHECK BUTTON
CHECK_BUTTON_VALUE = tk.IntVar()
cb_check = tk.Checkbutton(b_frame,width = 14, bg = '#d16eff', font = "Georgia 13", 
	text = "Defeat by border", variable = CHECK_BUTTON_VALUE, command = lambda: BORDER(CHECK_BUTTON_VALUE.get()))

cb_check.place(x = 0, y = 52)

root.bind("q", lambda a: root.quit())
root.bind("r", lambda a: start(root, canv, GAME_WINDOW_CONFIG, MAIN_MENU, GAME_OBJECTS, DIE_BY_BORDER))

# MAIN LOOP AND canv pack
canv.pack() # use pack() because we need root at (0, 0)
root.mainloop()













