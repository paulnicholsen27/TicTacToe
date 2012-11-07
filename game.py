import os
import pygame
import random
from copy import deepcopy
pygame.font.init()
os.system("clear")

width = 500
height = 500


screen = pygame.display.set_mode((width, height))
x_shape = pygame.image.load('cross.bmp').convert()
x_shape = pygame.transform.scale(x_shape, (100,100))
x_shape.set_colorkey((255,255,255))
o_shape = pygame.image.load('nought.bmp').convert()
o_shape = pygame.transform.scale(o_shape, (100,100))
o_shape.set_colorkey((255,255,255))

running = True
game_over = False

class Gameplay:
	def __init__(self):
		self.grid = [[None, None, None], [None, None, None], [None, None, None]]
		if random.randint(1,2) == 1:
			self.player_turn = True
			print "Player First"
		else:
			self.player_turn = False
			print "Computer First"

	def board_position(self, mouseX,mouseY):
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

	def check_for_win(self, grid):
		tie = True
		x_win = False
		o_win = False
		game_over = False
		for i in range(0,3):
			if grid[i][0] == grid[i][1] == grid[i][2] == 'X' or grid[0][i]==grid[1][i]==grid[2][i] == 'X':
				end_message = "X is the winner!"
				game_over = True
				x_win = True
				o_win = False
			elif grid[i][0] == grid[i][1] == grid[i][2] == 'O' or grid[0][i]==grid[1][i]==grid[2][i] == 'O':
				end_message = "O is the winner!"
				game_over = True
				o_win = True
		if game_over == False:
			if grid[0][0] == grid[1][1] == grid[2][2] == 'X' or grid[2][0]==grid[1][1]==grid[0][2] == 'X':
				end_message = "X is the winner!"
				game_over = True
				x_win = True
			elif grid[0][0] == grid[1][1] == grid[2][2] == 'O' or grid[2][0]==grid[1][1]==grid[0][2] == 'O':
				end_message = "O is the winner!"
				game_over = True
				o_win = True
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
		return end_message, game_over, tie, x_win, o_win

	def move_placement(self, row, column):
		if self.grid[row][column] == None and self.player_turn == True:
			self.grid[row][column] = "X"
			self.player_turn = False

	def computer_move(self):
		if self.player_turn == False:
			pygame.time.delay(500)
			if self.grid[1][1] == None:
				self.grid[1][1] = 'O'
				return self.grid
			elif self.grid == [[None, None, None], [None, 'X', None], [None, None, None]]:
					self.grid = [['O', None, None], [None, 'X', None], [None, None, None]]
					return self.grid
			else:
				self.minimax_decision(self.grid)

	def possible_maker(self, board, character = ""):
		#generates all possible next moves
		if character == "":
			if self.player_turn == True:
				character = 'X'
			else:
				character = 'O'
		test_grid = deepcopy(board)
		possible_boards = []
		for i in range(3):
			for j in range(3):
				if test_grid[i][j] == None:
					current_poss = deepcopy(test_grid)
					current_poss[i][j] = character
					possible_boards.append(current_poss)
		return possible_boards

	def minimax_decision(self, state):
		#with max/min_move, finds best possible next move using minimax algorithm
		current_utilities = []
		next_boards = self.possible_maker(state, "O")
		winner_found = False
		for board in next_boards:
			current_utilities.append((board, self.max_move(board)))
			end_message, game_over, tie, x_win, o_win = self.check_for_win(board)
			if o_win:
				winner_found = True #?Why not just "if winner"
				winner = board
		current_utilities.sort(key = lambda tup: tup[1])
		if winner_found:
			self.grid = winner
		else:
			self.grid = current_utilities[0][0]
		self.player_turn = True

	def max_move(self, state):
		utility = -2
		end_message, game_over, tie, x_win, o_win = self.check_for_win(state)
		if x_win or tie or o_win:
			if x_win:
				utility = 1
			elif o_win:
				utility = -1
			elif tie:
				utility = 0
			return utility
		for board in self.possible_maker(state, "X"):
			utility = max(utility, self.min_move(board))
		return utility


	def min_move(self, state):
		utility = 2
		end_message, game_over, tie, x_win, o_win = self.check_for_win(state)
		if x_win or tie or o_win:
			if x_win:
				utility = 1
			elif o_win:
				utility = -1
			elif tie:
				utility = 0
			return utility
		for board in self.possible_maker(state, "O"):
			utility = min(utility, self.max_move(board))
		return utility

class Gamescreen:
	def __init__(self, surface):
		self.surface = surface
		self.font = pygame.font.Font(None, 80)

	def draw_board(self):
		#create board, redraw as x/o are placed
		screen.fill((50,50,50))
		pygame.draw.line(screen,(255,255,255),(70,190),(430,190),4)
		pygame.draw.line(screen,(255,255,255),(70,310),(430,310),4)
		pygame.draw.line(screen,(255,255,255),(190,70),(190,430),4)
		pygame.draw.line(screen,(255,255,255),(310,70),(310,430),4)
		for row in range(3):
			for column in range(3):
				placement = pygame.Rect(80 + column * 120, 80 + row * 120, 50, 50)
				if current_game.grid[row][column] == 'X':
					screen.blit(x_shape, placement)
				elif current_game.grid[row][column] == 'O':
					screen.blit(o_shape, placement)
		pygame.display.flip()


play_area = Gamescreen(screen)
current_game = Gameplay()

#GAMEPLAY
while running:
	play_area.draw_board()
	end_message, game_over, tie, x_win, o_win = current_game.check_for_win(current_game.grid)
	if game_over == True:
		print "Game over"
		end_game = play_area.font.render(end_message, True, (0, 200, 0), (0,0,0))
		end_game.set_colorkey((0,0,0))
		endRect = end_game.get_rect(centerx = width/2, centery = height / 2)
		screen.blit(end_game, endRect)
		pygame.display.flip()
		pygame.time.delay(2000)
		running = False
	if running == True and current_game.player_turn == False:
		current_game.computer_move()
		play_area.draw_board()
		end_message, game_over, tie, x_win, o_win = current_game.check_for_win(current_game.grid)
		current_game.player_turn = True
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			mouseX,mouseY = pygame.mouse.get_pos()
			row, column = current_game.board_position(mouseX, mouseY)
			current_game.move_placement(row, column)
	pygame.display.flip()
