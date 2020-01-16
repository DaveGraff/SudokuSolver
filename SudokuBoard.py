import numpy as np
from time import sleep
import pyautogui as inter 

class Cell:
	"""A single cell in a Sudoku game"""
	def __init__(self, value, given, x, y, pos=None):
		self.value = value #Integer 1-9
		self.given = given #Whether or not this was a given
		self.x = x
		self.y = y
		self.pos = pos 			#Position onscreen

class Board:
	"""A board comprised of 9x9 cells"""

	def __init__(self, values):
		self.board = [[None for _ in range(9)] for _ in range(9)]
		# self.box_width = None	#Size of the box onscreen
		for i, row in enumerate(values):
			for j, cell in enumerate(row):
				#Allow for positions
				if isinstance(cell, tuple):
					self.board[i][j] = Cell(0, False, i, j, cell)
				else:
					self.board[i][j] = Cell(cell, cell != 0, i, j)

	"""Print board in readable format"""
	def get_board(self):
		for row in self.board:
			for cell in row:
				print(cell.value, end=" ")
			print()

	"""Add a value from a board being read"""
	def add_read_val(self, pos, val, box_width):
		board = self.board

		x = 0
		while x < 8:
			if pos[0] < board[x][0].pos[0] + (box_width/2):
				break
			x += 1

		y = 0
		while y < 8:
			if pos[1] < board[0][y].pos[1] + (box_width/2):
				break
			y += 1

		self.board[x][y].value = val
		self.board[x][y].given = True

	"""Places a cell"""
	
	def set_cell(self, cell, val):
		if not cell.pos:
			return

		inter.click(cell.pos)

		if val == 0:
			inter.press('backspace')
			cell.value = 0
			return

		inter.write(str(val))
		cell.value = val		


	"""Determine the validity of a single cell"""
	def is_valid(self, cell):
		x,y = cell.x, cell.y
		#Check Axes
		x_val = [self.board[x][i].value for i in range(9) if self.board[x][i].value != 0]
		y_val = [self.board[i][y].value for i in range(9) if self.board[i][y].value != 0]

		if len(x_val) != len(set(x_val)) or len(y_val) != len(set(y_val)):
			return False

		#Check square, currently only supports 9x9
		x_start = 3 * int(x/3)
		y_start = 3 * int(y/3)
		values = [i+1 for i in range(9)]

		for i in range(3):
			for j in range(3):
				val = self.board[x_start + i][y_start + j].value

				if val == 0:
					continue
				elif val in values:
					values.remove(val)
				else:
					return False

		return True


	"""Solve using the backtrace method"""
	def solve(self):
		solve_list = []

		for row in self.board:
			for cell in row:
				if not cell.given:
					solve_list.append(([i+1 for i in range(9)], cell))

		index = 0
		while index < len(solve_list):
			if index < 0:
				return False

			cell = solve_list[index][1]
			vals = solve_list[index][0]

			#All possibilities exhausted
			if len(vals) == 0:
				self.set_cell(cell, 0)
				solve_list[index] = ([i+1 for i in range(9)], cell)
				index -= 1
				continue

			#Find a valid move in the current context
			while len(vals) > 0:
				cell.value = vals[len(vals)-1]
				vals.remove(cell.value)
				if self.is_valid(cell):
					self.set_cell(cell, cell.value)
					solve_list[index] = (vals, cell)
					break
				else:
					cell.value = 0

			#No valid move found, backtrace
			if cell.value == 0:
				self.set_cell(cell, 0)
				solve_list[index] = ([i+1 for i in range(9)], cell)
				index -= 1
			#Valid move found
			else:
				index += 1
