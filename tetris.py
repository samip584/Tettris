import pygame
import pygame.gfxdraw
import sys
import random
import time
import json

block_size = 20
height_of_arena = 20 * block_size
width_of_arena = 10 * block_size
height_of_next_display = 4 * block_size
width_of_next_display = 8 * block_size
size_of_arena = (width_of_arena, height_of_arena)
size_of_screan = (width_of_arena + width_of_next_display + 3 * block_size, height_of_arena + 2 * block_size)

score = 0
lines = 0
grid = []
locked_positions = {}

with open("shapes", "r") as read_file:
    shapes = json.load(read_file)

pygame.init()
largeText = pygame.font.SysFont('norasi', 45)
smallText = pygame.font.SysFont('ubuntucondensed',30)
screen = pygame.display.init()
pygame.display.set_caption("Tetris")


class Piece():
	def __init__(self, x, y, shape):
		self.x = x
		self.y = y
		self.format = shape["format"]
		self.color = shape["color"]
		self.rotation = 0 



def main_screan():
	global placed
	global screen
	global grid
	global locked_positions

	clock = pygame.time.Clock()
	fall_time = 0
	change_piece = False	
	current_piece = Piece(5, 0, get_shape())
	next_piece = Piece(5, 0, get_shape())

	screen = pygame.display.set_mode(size_of_screan)
	screen.fill((135,206,250))
	pygame.draw.rect(screen, (70,130,180), (12 * block_size, 14 * block_size, 8 * block_size, 4 * block_size ))
	TextSurf, TextRect = text_objects("TETRIS", largeText, (255,69,5))
	TextRect.center = (16 * block_size, 16 * block_size)
	screen.blit(TextSurf, TextRect)
	pygame.draw.rect(screen, (70,130,180), (block_size - 2, block_size - 2, width_of_arena + 4, height_of_arena + 4 ), 4)
	display_next_piece(next_piece)
	display_score()
	while True:
		fall_speed = 0.27
		# move shape down
		grid = create_grid(locked_positions)
		fall_time += clock.get_rawtime()
		clock.tick()

		# PIECE FALLING CODE
		if fall_time/1000 >= fall_speed:
			fall_time = 0
			current_piece.y += 1
			if not (valid_move(current_piece)) and current_piece.y > 0:
				current_piece.y -= 1
				change_piece = True


		for event in pygame.event.get():
			if event.type ==pygame.QUIT:
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					#move left
					current_piece.x -= 1
					if not valid_move(current_piece): #to chaeck if position after moving is valid
						current_piece.x += 1
				elif event.key == pygame.K_RIGHT:
					#move right
				    current_piece.x += 1
				    if not valid_move(current_piece):
				    	current_piece.x -= 1
				elif event.key == pygame.K_UP:
				    # rotate shape
				    current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.format)
				    if not valid_move(current_piece):
				    	current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.format)
				if event.key == pygame.K_DOWN:
					#move down
					current_piece.y += 1
					if not valid_move(current_piece):
						current_piece.y -= 1
		
	    
		
	    #make color of grid change as peace moves
		shape_pos = convert_shape_format(current_piece)
		for pos in shape_pos:
			x, y = pos
			if y > -1:
				grid[y][x] = current_piece.color
				

		if change_piece:
			for pos in shape_pos:
				locked_positions[(pos[0], pos[1])] = current_piece.color
			clear_row()
			current_piece = next_piece
			next_piece = Piece(5, 0, get_shape())
			display_next_piece(next_piece)
			change_piece = False
			

		display_arena()

		if check_defeat(locked_positions):
			sys.exit()



def create_grid(locked_positions={}):
    grid = [[(135,206,250) for x in range(10)] for y in range(20)]
    for i in range(20):
        for j in range(10):
            if (j,i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

def get_shape():
	return random.choice(shapes)


def convert_shape_format(piece):
	positions = []
	new_format = piece.format[piece.rotation]
	for i, line in enumerate(new_format):
		row = list(line)
		for j, column in enumerate(row):
		    if column == '0':
		        positions.append((piece.x + j, piece.y + i))	#adding the position of the block of piece in the position list

	for i, pos in enumerate(positions):
		positions[i] = (pos[0] - 2, pos[1] - 4)		#offsetting the blocks

	return positions

def valid_move(shape):
	accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (135,206,250)] for i in range(20)]
	accepted_pos = [j for sub in accepted_pos for j in sub]			#flattening the 2D array
	formatted = convert_shape_format(shape)
	for pos in formatted:
		if pos not in accepted_pos:
			if pos[1] > -1:
				return False

	return True

def check_defeat(positions):
	for pos in positions:
		x, y = pos
		if y < 1:
			return True

	return False
	
def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def clear_row():
	global score
	global grid
	global locked_positions
	global lines
	inc = 0
	for i, row in enumerate(grid):
		if (135,206,250) not in row:

			inc += 1
			# add positions to remove from locked
			ind = i
			for j in range(10):
				try:
					del locked_positions[(j, i)]
				except:
					continue
	if inc > 0:
		lines += inc
		if(inc == 1):
			score += 60
		elif(inc == 2):
			score += 100
		elif(inc == 3):
			score += 300
		elif(inc == 4):
			score += 1200
		display_score()
		for key in sorted(list(locked_positions), key=lambda x: x[1])[::-1]:
			x, y = key
			if y < ind:
				newKey = (x, y + inc)
				locked_positions[newKey] = locked_positions.pop(key)

def display_arena():

	for i, row in enumerate(grid):
		for j, color in enumerate(row):
			pygame.draw.rect(screen, color, (j * block_size + block_size, i * block_size + block_size, block_size, block_size))
			if color != (135,206,250):
				pygame.draw.rect(screen, (0,0,0), (j * block_size + block_size, i * block_size + block_size, block_size, block_size), 1)
	pygame.display.update()


def display_next_piece(next_piece):
	global screen

	pygame.draw.rect(screen, (135,206,250), (12 * block_size, block_size, 8 * block_size, 6 * block_size ))
	pygame.draw.rect(screen, (70,130,180), (12 * block_size, block_size - 2, 8 * block_size, 6 * block_size ), 4)

	new_format = next_piece.format[next_piece.rotation]
	for i, line in enumerate(new_format):
		row = list(line)
		for j, column in enumerate(row):
		    if column == '0':
		    	pygame.draw.rect(screen, next_piece.color, ((13 + j)*block_size, (2+i)*block_size, block_size, block_size))
		    	pygame.draw.rect(screen, (0,0,0), ((13 + j)*block_size, (2 + i)*block_size, block_size, block_size), 1)
	pygame.display.update()


def display_score():
	pygame.draw.rect(screen, (135,206,250), (12 * block_size, 8 * block_size , 8 * block_size, 2 * block_size ))
	pygame.draw.rect(screen, (70,130,180), (12 * block_size, 8 * block_size - 2, 8 * block_size, 2 * block_size ), 4)
	pygame.draw.rect(screen, (135,206,250), (12 * block_size, 10 * block_size , 8 * block_size, 2 * block_size ))
	pygame.draw.rect(screen, (70,130,180), (12 * block_size, 10 * block_size - 2, 8 * block_size, 2 * block_size ), 4)

	TextSurf, TextRect = text_objects("score", smallText, (70,130,180))
	TextRect.center = (14 * block_size, 9 * block_size - 4)
	screen.blit(TextSurf, TextRect)
	
	TextSurf, TextRect = text_objects(str(score), smallText, (10,10,10))
	TextRect.center = (19 * block_size, 9 * block_size - 4)
	screen.blit(TextSurf, TextRect)
	

	TextSurf, TextRect = text_objects("lines", smallText, (70,130,180))
	TextRect.center = (14 * block_size - 5, 11 * block_size - 2)
	screen.blit(TextSurf, TextRect)

	TextSurf, TextRect = text_objects(str(lines), smallText, (10,10,10))
	TextRect.center = (19 * block_size, 11 	* block_size - 2)
	screen.blit(TextSurf, TextRect)
	

if __name__ == "__main__":
	main_screan()


