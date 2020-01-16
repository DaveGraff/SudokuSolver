import SudokuBoard
import numpy as np
import pyautogui as inter


#Get Board size
botright_sq = inter.locateOnScreen('images/botright.png', grayscale=True, confidence=.9)
topleft_sq = inter.locateOnScreen('images/topleft.png', grayscale=True, confidence=.9)

topleft = inter.center(topleft_sq)
botright = inter.center(botright_sq)


#Get most accurate reading of the size of a box
x_width = botright.x - topleft.x
y_width = botright.y - topleft.y

box_width = int((x_width + y_width) / 18)


#Create the board
board = np.zeros((9,9), dtype=tuple)
board[0][0] = (topleft.x + (box_width/2), topleft.y + (box_width/2))

#FIll in
for y, row in enumerate(board):
	for x, cell in enumerate(row):
		x_val, y_val = None, None

		if x != 0:
			x_val = board[x-1][y][0] + box_width
		else:
			x_val = board[0][0][0]

		if y != 0:
			y_val = board[x][y-1][1] + box_width
		else:
			y_val = board[0][0][1]

		board[x][y] = (x_val, y_val)


browser_board = SudokuBoard.Board(board)


#Read values from board
import os
#Find all given nums
for file in os.listdir('images/numbers'):
	filename = 'images/numbers/' + file
	for pos in inter.locateAllOnScreen(filename, confidence=.95):
		browser_board.add_read_val(pos, int(file[0]), box_width)

# browser_board.solve()
browser_board.get_board()
print("________________________")
browser_board.solve()
browser_board.get_board()
