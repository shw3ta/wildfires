import numpy as np
import math

# basic square forest
# each cell has 3 possible states: 0, 1, 2 corresponding to empty, tree, fire

# this class is not done, I keep adding properties after testing them out individually
class square_forest:
	# ideally evolves till full destruction, but we set a hard limit on time

	def __init__(self):
		self.dim = 0 
		self.cells = np.zeros((self.dim, self.dim))

	def set_dim(self):
		self.dim = int(input("\nEnter dimension of your square forest: "))
	
	def init_cells(self):
		# random init with some number of trees; upper limit = dim * dim
		n_trees = np.random.randint(self.dim * self.dim)

		loc_trees = []
		for i in range(n_trees):
			coords = tuple(np.random.randint(self.dim, size=2))
			# print(f"tree {i+1} of {n_trees} spawned")
			if coords not in loc_trees:
				loc_trees.append(coords)
			# else:
			# 	print("again ")
			# print(f"at {coords}")
		
		for tree in loc_trees:
			self.cells[tree[0], tree[1]] = 1


##############################################################################

##################
# Test functions #
##################



def init_forest(dim):	
	forest = np.zeros((dim, dim))
	n_trees = np.random.randint(dim * dim)

	loc_trees = []
	for i in range(n_trees):
		coords = np.random.randint(dim, size=2)
		loc_trees.append(coords)
		
	
	for tree in loc_trees:
		forest[tree[0], tree[1]] = 1

	print("\n Here is the final forest config:\n", forest)
	return forest


def get_valid_neighbours(cell, dim):
	

	row, col = cell[0], cell[1]
	if row < 0 : 
		raise Exception("negative row index encountered")

	elif col < 0 : 
		raise Exception("negative column index encountered")

	elif row >= dim : 
		raise Exception("row index out of dimension bounds")

	elif col >= dim : 
		raise Exception("column index out of dimension bounds")

	else:
		neighbours = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
	
		# validation
		for i, neighbour in enumerate(neighbours):
			if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] == dim or neighbour[1] == dim: 
				# top, bottom, left, right edges
				neighbours[i] = None

		return neighbours


def pick_fire_location(dim):
	return np.random.randint(dim, size=2)

def spread(valid_neighbours, forest, dim):

	for nb in valid_neighbours:
		if nb != None and forest[nb[0], nb[1]] == 1 :
			forest[nb[0], nb[1]] = 2 
			print("\n", forest)
			# then call spread on this cell
			spread(get_valid_neighbours(nb, dim), forest, dim)
			forest[nb[0], nb[1]] = 0 # 2 -> 0 i.e fire then dead
			print("\n", forest)


def simulate_one_fire(dim):
	forest = init_forest(dim)
	fire_at = pick_fire_location(dim)

	# 0 means empty cell, 1 means cell had a tree
	forest[fire_at[0], fire_at[1]] = 2 
	print("\n", forest)

	# start and spread
	spread(get_valid_neighbours(fire_at, dim), forest, dim)



simulate_one_fire(14)
###################################################################################