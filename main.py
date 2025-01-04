import pygame
from pygame.locals import *
import random
import time

# ration - 2,571428571428571
width = 7
height = 5
walls_count = 14

HEIGHT = 680
WIDTH = 756

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.init()

WHITE = (255,255,255)
YELLOW = (255,255,0)
BLACK = (0,0,0)
GRAY = (196,196,196)
PLAYER_COLOR = (46,113,45)

screen.fill(GRAY)

board = []
verifed = []
save_board = []

def generate_board():
	try:
		pygame.display.set_caption("Robot Game")
		board.clear()
		save_board.clear()
		for i in range(width*height):
			board.append("[ ]")
		generate_walls()
		verifed.clear()
		if checking(board.index("[NP]")) == True:
			save_board.extend(board)
			print_board()
		else:
			generate_board()
	except RecursionError:
		print("RecursionError!")
		time.sleep(1)
		return False

def generate_walls():
	walls = random.sample(range(width*height), walls_count+1)
	for wall in walls:
		if wall == walls[walls_count]:
			board[wall] = "[NP]"
		else:
			board[wall] = "[W]"

def print_board():
	screen.fill(GRAY)
	for i in range(height):
		for d in range(width):
			if board[i*width+d] == "[W]":
				pygame.draw.rect(screen, BLACK, ((WIDTH/width)*d, (HEIGHT/height)*i, WIDTH/width, HEIGHT/height))
			elif board[i*width+d] == "[ ]":
				pygame.draw.rect(screen, BLACK, ((WIDTH/width)*d, (HEIGHT/height)*i, WIDTH/width, HEIGHT/height), 3)
			elif board[i*width+d] == "[S]":
				pygame.draw.rect(screen, YELLOW, ((WIDTH/width)*d, (HEIGHT/height)*i, WIDTH/width, HEIGHT/height), 5)
			elif board[i*width+d] == "[P]":
				pygame.draw.rect(screen, BLACK, ((WIDTH/width)*d, (HEIGHT/height)*i, WIDTH/width, HEIGHT/height), 3)
				pygame.draw.ellipse(screen, PLAYER_COLOR, ((WIDTH/width)*d + 10, (HEIGHT/height)*i + (HEIGHT/height - WIDTH/width)/2 + 10, WIDTH/width - 20, WIDTH/width - 20))
			elif board[i*width+d] == "[PS]":
				pygame.draw.rect(screen, YELLOW, ((WIDTH/width)*d, (HEIGHT/height)*i, WIDTH/width, HEIGHT/height), 5)
				pygame.draw.ellipse(screen, PLAYER_COLOR, ((WIDTH/width)*d + 10, (HEIGHT/height)*i + (HEIGHT/height - WIDTH/width)/2 + 10, WIDTH/width - 20, WIDTH/width - 20))
			elif board[i*width+d] == "[N]":
				pygame.draw.rect(screen, YELLOW, ((WIDTH/width)*d, (HEIGHT/height)*i, WIDTH/width, HEIGHT/height), 6)
				pygame.draw.rect(screen, PLAYER_COLOR, ((WIDTH/width)*d + 1, (HEIGHT/height)*i + 1, WIDTH/width - 2, HEIGHT/height - 2), 4)
			elif board[i*width+d] == "[NP]":
				pygame.draw.rect(screen, YELLOW, ((WIDTH/width)*d, (HEIGHT/height)*i, WIDTH/width, HEIGHT/height), 6)
				pygame.draw.rect(screen, PLAYER_COLOR, ((WIDTH/width)*d + 1, (HEIGHT/height)*i + 1, WIDTH/width - 2, HEIGHT/height - 2), 4)
				pygame.draw.ellipse(screen, PLAYER_COLOR, ((WIDTH/width)*d + 10, (HEIGHT/height)*i + (HEIGHT/height - WIDTH/width)/2 + 10, WIDTH/width - 20, WIDTH/width - 20))

def checking(segment):
	verifed.append(segment)
	checked = []
	if segment == 0:
		checked = [segment+1, segment+width]
	elif segment == width*height - 1:
		checked = [segment-1, segment-width]
	elif segment == width*height - width:
		checked = [segment+1, segment-width]
	elif segment == width - 1:
		checked = [segment-1, segment+width]
	elif segment - width < 0:
		checked = [segment+1, segment-1, segment+width]
	elif segment + width >= width*height:
		checked = [segment+1, segment-1, segment-width]
	elif segment % width == 0:
		checked = [segment+1, segment-width, segment+width]
	elif (segment+1) % width == 0:
		checked = [segment-1, segment-width, segment+width]
	else:
		checked = [segment+1, segment-1, segment+width, segment-width]
	for i in checked:
		if verifed.count(i) == 0 and board[i] == "[ ]": 
			checking(i)
		else:
			pass
	if len(verifed) == width*height - walls_count:
		return True
	else:
		return False

def move(direction):
	player = 0
	try:	
		if board[board.index("[P]")] == "[P]":
			player = board.index("[P]")
	except ValueError:	
		try:	
			if board[board.index("[NP]")] == "[NP]":
				player = board.index("[NP]")
		except ValueError:	
			if board[board.index("[PS]")] == "[PS]":
				player = board.index("[PS]")
	if direction=="left":
		if board[player - 1] == "[W]" or player - 1 < 0 or player % width == 0:
			pass
		else:
			moving(player, player - 1)
	elif direction=="right":
		if player + 1 >= width*height or (player+1) % width == 0 or board[player + 1] == "[W]":
			pass
		else:
			moving(player, player + 1)
	elif direction=="up":
		if board[player - width] == "[W]" or player - width < 0:
			pass
		else:
			moving(player, player - width)
	elif direction=="down":
		if player + width >= width*height or board[player + width] == "[W]":
			pass
		else:
			moving(player, player + width)

def moving(last_pos, new_pose):
	if board[last_pos] == "[P]":
		board[last_pos] = "[ ]"
	elif board[last_pos] == "[NP]":
		board[last_pos] = "[N]"
	else:
		board[last_pos] = "[S]"
	
	if board[new_pose] == "[ ]":
		board[new_pose] = "[PS]"
	elif board[new_pose] == "[N]":
		board[new_pose] = "[NP]"
	else:
		board[new_pose] = "[P]"
	print_board()

generate_board()

running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				generate_board()
			elif event.key == pygame.K_w or event.key == 1073741906:
				move("up")
			elif event.key == pygame.K_a or event.key == 1073741904:
				move("left")
			elif event.key == pygame.K_s or event.key == 1073741905:
				move("down")
			elif event.key == pygame.K_d or event.key == 1073741903:
				move("right")
			elif event.key == 32:
				board.clear()
				board.extend(save_board)
				print_board()
			elif event.key == pygame.K_m:
				writing = True
				num = ""
				while writing:
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN:
							if event.key == 13:
								writing = False
								break
							elif event.key > 47 and event.key < 58:
								num = str(event.key-48)
				if int(num) == 1:
					width = 7
					height = 5
				elif int(num) == 2:
					width = 9
					height = 8
				elif int(num) == 3:
					width = 12
					height = 10
				walls_count = round(int(width*height)/2.571428571428571)
				generate_board()

	pygame.display.update()
	if board.count("[NP]") == 1 and board.count("[ ]") == 0:
		pygame.display.set_caption("You Win!")
		time.sleep(5)
		generate_board()

pygame.quit()