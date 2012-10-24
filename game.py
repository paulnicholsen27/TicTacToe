import os
import pygame
import random
pygame.font.init()
font = pygame.font.Font(None, 80)
os.system("clear")
if random.randint(1,2) == 1:
	player_turn = True
	print "Player First"
else:
	player_turn = False
	print "Computer First"
width = 500
height = 500

		
screen = pygame.display.set_mode((width, height))
grid = [[None, None, None], [None, None, None], [None, None, None]]
x_shape = pygame.image.load('cross.bmp').convert()
x_shape = pygame.transform.scale(x_shape, (100,100))
x_shape.set_colorkey((255,255,255))
o_shape = pygame.image.load('nought.bmp').convert()
o_shape = pygame.transform.scale(o_shape, (100,100))
o_shape.set_colorkey((255,255,255))

running = True
game_over = False

def board_position(mouseX,mouseY):
	if mouseY < 190:
		row = 0
	elif mouseY < 310:
		row = 1
	else:
		row = 2
	if mouseX < 190:
		column = 0
	elif mouseX < 310:
		column = 1
	else:
		column = 2
	return row, column

def move_placement(row, column):
	if grid[row][column] != None:
		pass
	else: 
		if player_turn == True:
			grid[row][column] = "X"
			player_turn == False
			
def computer_move():
	moved = False
	while moved == False:
		row = random.randint(0,2)
		column = random.randint(0,2)
		if grid[row][column] == None:
			pygame.time.delay(500)
			grid[row][column] = 'O'
			moved = True
	
def check_for_win():
	tie = True
	game_over = False

	for i in range(0,3):
		if grid[i][0] == grid[i][1] == grid[i][2] == 'X' or grid[0][i]==grid[1][i]==grid[2][i] == 'X': 
			end_message = "X is the winner!"
			game_over = True
		elif grid[i][0] == grid[i][1] == grid[i][2] == 'O' or grid[0][i]==grid[1][i]==grid[2][i] == 'O':  
			end_message = "O is the winner!"
			game_over = True
	if game_over == False:
		if grid[0][0] == grid[1][1] == grid[2][2] == 'X' or grid[2][0]==grid[1][1]==grid[0][2] == 'X':
			end_message = "X is the winner!"
			game_over = True
		elif grid[0][0] == grid[1][1] == grid[2][2] == 'O' or grid[2][0]==grid[1][1]==grid[0][2] == 'O':
			end_message = "O is the winner!"
			game_over = True
		elif tie == True:
			for row in grid:
				for column in row:
					if column == None:
						tie = False
						game_over = False
						end_message = ""
			if tie == True:
				end_message = "It's a tie!"
				game_over = True
		else:
			end_message = ""
			game_over = False
	return end_message, game_over

def draw_board():
	for row in range(3):
		for column in range(3):
			placement = pygame.Rect(80 + column * 120, 80 + row * 120, 50, 50)
			if grid[row][column] == 'X':
				screen.blit(x_shape, placement)
			elif grid[row][column] == 'O': 
				screen.blit(o_shape, placement)		
	pygame.display.flip()

while running:
	screen.fill((50,50,50))
	pygame.draw.line(screen,(255,255,255),(70,190),(430,190),4)
	pygame.draw.line(screen,(255,255,255),(70,310),(430,310),4)
	pygame.draw.line(screen,(255,255,255),(190,70),(190,430),4)
	pygame.draw.line(screen,(255,255,255),(310,70),(310,430),4)
	draw_board()
	end_message, game_over = check_for_win()	
	if game_over == True:
		print "Game over"
		end_game = font.render(end_message, True, (0, 200, 0), (0,0,0))
		end_game.set_colorkey((0,0,0))
		endRect = end_game.get_rect(centerx = width/2, centery = height / 2)
		screen.blit(end_game, endRect)
		pygame.display.flip()
		pygame.time.delay(2000)
		running = False
	if running == True and player_turn == False:
		computer_move()
		draw_board()
		end_message, game_over = check_for_win()
		player_turn = True
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseX,mouseY = pygame.mouse.get_pos()
			row, column = board_position(mouseX, mouseY)
			move_placement(row, column)
			player_turn = False
	pygame.display.flip()
