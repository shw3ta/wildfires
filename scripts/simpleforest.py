import numpy as np
from datetime import datetime

# file to store outputs, in sequential order for now
file = open("log_prelim.txt", "a+")


# basic square forest
# each cell has 3 possible states: 0, 1, 2 corresponding to empty, tree, fire


##################
# Test functions #
##################

#grid_collector = np.array()


def init_forest(dim):	
	"""Create a forest as a grid of dim x dim size. 
    
    Input:
    dim (int): dimension of the forest grid.
    
    Output:
    dim x dim forest grid with randomly planted trees."""
    
	forest = np.zeros((dim, dim))
	n_trees = np.random.randint(dim * dim)

	loc_trees = set()
	for i in range(n_trees):
		coords = np.random.randint(dim, size=2)
		loc_trees.add(tuple(coords))
		
	
	for tree in loc_trees:
		forest[tree[0], tree[1]] = 1

	print("\n Here is the initial forest config:\n", forest)
	return forest


def get_valid_neighbours(cell, forest, dim):
	print("\nEntered get_valid_neighbours()")
	
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
		print("\n -- adjacent cells indices are: ", neighbours)


		for i, (r, c) in enumerate(neighbours):
			if r < 0 or c < 0 or r == dim or c == dim:
				neighbours[i] = None
			elif forest[r, c] != 1 :
				neighbours[i] = None

		print("\n -- after None-ifying non tree cells and invalid edge cases: ", neighbours)

		valid_neighbours = []
		for n in neighbours:
			if n != None:
				valid_neighbours.append(n)

		print("\n Final valid list: ", valid_neighbours)
		return valid_neighbours


def pick_fire_location(dim):
	return np.random.randint(dim, size=2)



def spread_to(valid_neighbours, forest, dim, burnt):

	print("\n---------------------------\nThe next degree neighbours are at: ", valid_neighbours)
	
	# now we burn all of them:
	for (row, col) in valid_neighbours:
		# decimate: first set to 2
		forest[row, col] = 2
		burnt.append((row, col))
	print("\n incendio \n", forest)

	# spread to second degree neighbours
	for cell in valid_neighbours:
		next_neighbours = get_valid_neighbours(cell, forest, dim)
		if len(next_neighbours) != 0: # i.e has somewhere to spread to
			spread_to(next_neighbours, forest, dim, burnt)

	print("\n----------DONE RECURSING---------")

def simulate_one_fire(dim):
	'''
	at the moment, this inits the forest, but ideally, it should inherit a forest instance where multiple fires can occur following the frequency parameter

	collects/returns area information as a diagnostic, should put it into a file with simulation number and details of the simulation
	'''
	forest = init_forest(dim)
	file.write(f"\nEntry time: {datetime.now()}\nInitial config: {forest}")
	
	fire_at = pick_fire_location(dim)
	file.write(f"\nFire started at: {fire_at}")
	burnt = []

	# 0 means empty cell, 1 means cell has a tree
	forest[fire_at[0], fire_at[1]] = 2 
	print(f"\n fire started at {fire_at}: \n", forest)
	burnt.append(fire_at)	

	# start and spread
	neighbours = get_valid_neighbours(fire_at, forest, dim)
	spread_to(neighbours, forest, dim, burnt)

	# go to all burnt sites and set them to 0 at the end of one spread.
	for (r, c) in burnt:
		forest[r, c] = 0

	print("\n After the damage:\n ", forest)
	area_burnt = len(burnt) # in cells; assuming one cell == one square unit of area
	# print(f"\nArea burnt in this fire: {area_burnt} sq. units.\n")

	return area_burnt
#----------------------------------------------------------------------------

dim = int(input("\nEnter the dimension of the forest you want to simulate: "))
damage = simulate_one_fire(dim)

file.write(f"\nArea burnt: {damage} sq. units")