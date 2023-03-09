import numpy as np
from datetime import datetime

# file to store outputs, in sequential order for now
file = open("log_prelim.txt", "a+")


# basic square forest
# each cell has 3 possible states: 0, 1, 2 corresponding to empty, tree, fire

# this class is not done, I keep adding properties after testing them out individually
class square_forest:
	# ideally evolves till full destruction, but we can set a hard limit on time

	def __init__(self):
		self.dim = int(input("\nEnter dimension of your square forest: "))
		self.cells = np.zeros((self.dim, self.dim))
		print(f"\npre-init of forest grid \n{self.cells}\n")
		self.burnt = [] # not really a property, just easier to not pass this hehe

	
	# def set_dim(self):
	# 	self.dim = int(input("\nEnter dimension of your square forest: "))
	
	
	def init_cells(self):
		# random init with some number of trees; upper limit = dim * dim
		n_max = np.random.randint(self.dim * self.dim) 

		loc_trees = set()
		for i in range(n_max):
			coords = tuple(np.random.randint(self.dim, size=2))
			loc_trees.add(coords)
			
		
		for tree in loc_trees:
			# note here that the actual no. of trees in the init config is <= n_trees since the guessed locations need not be unique
			self.cells[tree[0], tree[1]] = 1

		print(f"\nafter random tree planting: \n{self.cells}")
	
	def get_valid_neighbours(self, cell):
		row, col = cell[0], cell[1]
		if row < 0 : 
			raise Exception("negative row index encountered")

		elif col < 0 : 
			raise Exception("negative column index encountered")

		elif row >= self.dim : 
			raise Exception("row index out of dimension bounds")

		elif col >= self.dim : 
			raise Exception("column index out of dimension bounds")

		else:

			neighbours = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
			# print("\n -- adjacent cells indices are: ", neighbours)


			for i, (r, c) in enumerate(neighbours):
				if r < 0 or c < 0 or r == self.dim or c == self.dim:
					neighbours[i] = None
				elif self.cells[r, c] != 1 :
					neighbours[i] = None

			# print("\n -- after None-ifying non tree cells and invalid edge cases: ", neighbours)

			valid_neighbours = []
			for n in neighbours:
				if n != None:
					valid_neighbours.append(n)

			print("\n Final valid list: ", valid_neighbours)
			return valid_neighbours

	
	def get_fire_loc(self):
		return np.random.randint(self.dim, size=2)

	
	def spread_to(self, valid_neighbours):
		# print("\n---------------------------\nThe next degree neighbours are at: ", valid_neighbours)
	
		# now we burn all of them:
		for (row, col) in valid_neighbours:
			# decimate: first set to 2
			self.cells[row, col] = 2
			self.burnt.append((row, col))
		# print("\n incendio \n", self.cells)
		print(f"\nIntermediate spreading: \n{self.cells}")
		# spread to second degree neighbours
		for cell in valid_neighbours:
			next_neighbours = self.get_valid_neighbours(cell)
			if len(next_neighbours) != 0: # i.e has somewhere to spread to
				self.spread_to(next_neighbours)

		# print("\n----------DONE RECURSING---------")

	
	def simulate_fire_at(self, fire_loc):

		self.cells[fire_loc[0], fire_loc[1]] = 2
		print(f"\n fire started at {fire_loc}:\n{self.cells}")
		self.burnt.append(fire_loc)

		# spread
		neighbours = self.get_valid_neighbours(fire_loc)
		self.spread_to(neighbours)
		#--------------------------------------------
		# spread_to() will set the states to 2
		print(f"\nFinal decimation: \n{self.cells}\n")
		# now we change it to 0 so that the simulation can proceed as required
		for (r, c) in self.burnt:
			self.cells[r, c] = 0

		area_burnt = len(self.burnt)
		self.burnt = [] # reset for next simulation
		print(f"\nAfter reset: \n{self.cells}\n")
		return area_burnt
#-------------------------------------------------------------------------------

forest = square_forest() #initialize a square forest

forest.init_cells()

start_loc = forest.get_fire_loc()
area_burnt = forest.simulate_fire_at(start_loc)
print(f"area burnt : {area_burnt}")