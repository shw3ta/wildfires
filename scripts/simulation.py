import numpy as np
import os
import sys
import json 
from datetime import datetime
import gc

from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap

sys.setrecursionlimit(4000)

class Forest:
	
	# defining attributes of the forest
	def __init__(self, dimension, mode):
		self.dimension, self.mode = dimension, mode
		self.cells = np.zeros((self.dimension, self.dimension)) # initialize square grid with 0s
		self.grids, self.burnt = [], []

	# when called, collects the current state of the grid		
	def collect(self):
		state = self.cells.copy()
		self.grids.append(state)

		del state 
		gc.collect()

	def get_valid_neighbours(self, cell):

		row, col = cell[0], cell[1]

		# STEP 1. remove edge cases 
		if row < 0 : 
			raise Exception("negative row index encountered")

		elif col < 0 : 
			raise Exception("negative column index encountered")

		elif row >= self.dimension : 
			raise Exception("row index out of dimension bounds")

		elif col >= self.dimension : 
			raise Exception("column index out of dimension bounds")

		# STEP 2.
		else: 
			neighbours = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)] # defined according to paper --> only adjacent cells, not diagonals
			valid_neighbours = []

			for i, (r, c) in enumerate(neighbours):
				if (-1 < r < self.dimension) and (-1 < c < self.dimension) and self.cells[r, c] == 1:
					valid_neighbours.append(neighbours[i])

			# print("Final valid neighbours: ", valid_neighbours)
			return valid_neighbours


	def random_init_trees(self):
		n_max = np.random.randint(self.dimension * self.dimension) # max possible number of trees in the grid
		
		# @wero: i removed the second loop; now we directly change state.
		for i in range(n_max):
			coordinate = tuple(np.random.randint(self.dimension, size = 2)) # get random within-grid coordinate
			if self.cells[coordinate[0], coordinate[1]] == 0:
				self.cells[coordinate[0], coordinate[1]] = 1

		if self.mode == "1": 
			self.collect()

	def plant_tree(self):
		while True:
			coordinate = np.random.randint(self.dimension, size = 2) # get random within-grid coordinate
			if self.cells[coordinate[0], coordinate[1]] != 1:
				self.cells[coordinate[0], coordinate[1]] = 1

				if self.mode == "1":
					self.collect()
				break
	

	def spread_to(self, valid_neighbours):
		for (row, col) in valid_neighbours:
			self.cells[row, col] = 2
			self.burnt.append((row, col))
			if self.mode == "1":
				self.collect()

		# now spread to 2nd degree neighbours
		for cell in valid_neighbours:
			next_neighbours = self.get_valid_neighbours(cell)
			if len(next_neighbours) != 0:
				# spread only if there is something to spread to
				self.spread_to(next_neighbours)


	def reset_burnt_area(self):
		# goes through only those cells that were burnt until function call, not the whole grid
		for (r, c) in self.burnt:
			self.cells[r, c] = 0

		if self.mode == "1":
			self.collect()


	def start_fire(self, fire_loc):
		
		row, col = fire_loc[0], fire_loc[1]
		# drop match at location
		self.cells[row, col] = 2
		self.burnt.append(fire_loc)
		if self.mode == "1":
			self.collect()

		neighbours = self.get_valid_neighbours(fire_loc)
		self.spread_to(neighbours)

		self.reset_burnt_area()
		
		area_burnt = len(self.burnt)
		self.burnt = []

		return area_burnt
		

#---------------------------------
def set_params():
	# reads params from file
	input_params = []
	f = open("params.txt", "r")
	for line in f.readlines():
		line = line.split(",")
		grid_size, fire_fq_denom = int(line[0]), int(line[1])
		input_params.append((grid_size, fire_fq_denom))

	f.close()

	return input_params


def dump_logs(dimension, area_burnt, fire_fq_denom):
	f = os.path.relpath('/logfiles', '/scripts') + f"/logfile_{str(1/fire_fq_denom)}.json"
	logfile = open(f, "a+")

	to_write = 	{"time": str(datetime.now()), "gridsize": dimension, "N_fires_recorded": len(area_burnt), "A_f_per_fire": area_burnt}
	jsonified = json.dumps(to_write, indent=4)
	logfile.write(jsonified)

	logfile.close()


def animate(grids_collected, grid_size, fire_fq_denom):
	color_lst = ['wheat','yellowgreen','darkorange']
	cmap = ListedColormap(color_lst)

	print("\nRunning animation...")
	grids = grids_collected
	fig, ax = plt.subplots(figsize=(8, 8))
	frames = []
	for grid in grids:
		frames.append([plt.imshow(grid, cmap=cmap, vmin=0, vmax=2)])

	movie = animation.ArtistAnimation(fig, frames, interval=1000, repeat=False, blit=True)
	movie.save(f'../animations/animation_{grid_size}_{1/fire_fq_denom}_{str(datetime.now())}.mp4', fps=100)
	print(f"\nAnimation done! Find the corresponding movie file \"animation_{grid_size}_{1/fire_fq_denom}_{str(datetime.now())}.mp4\" in the folder \"animations\"")


def run_simulation(grid_size, fire_fq_denom, N_s, mode):
	print(f"\nRunning simulation on grid of dim {grid_size} with fire frequency {1/fire_fq_denom} for {N_s} generations...")
	
	area_burnt, buffer = {}, {}

	forest = Forest(grid_size, mode)
	forest.random_init_trees()

	fire_num = 0
	for i in range(N_s):
		if i % fire_fq_denom != 0:
			forest.plant_tree()
		else:
			if fire_num % 5 == 0 and fire_num != 0:
				# dump in chunks:
				dump_logs(forest.dimension, buffer, fire_fq_denom)
				buffer = {}

			start_loc = np.random.randint(forest.dimension, size = 2)
			try:
				A_f = forest.start_fire(start_loc)
				fire_num += 1
				area_burnt.update({fire_num : A_f})
				buffer.update({fire_num : A_f})

			except RecursionError as err:
				print(f"Recursion limit exceeded at fire number {fire_num} in this simulation.")
				area_burnt.update({fire_num : None})
				buffer.update({fire_num : None})
				continue
	
	dump_logs(forest.dimension, area_burnt, fire_fq_denom)
	
	return forest



def run_analysis(grid_size, fire_fq_denom):
	print("\nRunning analysis...")
	pass
#---------------------------------

def main():
	mode = input("This is a program to simulate forest fires. What mode would you like to run the simulation in?\n \n(slow mode) For an animation of the fire, enter 1, \n(fast mode) For just the analysis, enter 2.\n")
	
	input_params = set_params() # tuple of grid_size, fire_fq_denom

	for (grid_size, fire_fq_denom) in input_params:

		# run simulation in slow mode
		if mode == "1":
			num_gens = 10000
			print(f"\nInitiating simulation with grid_size {grid_size} and fire frequency {1/fire_fq_denom}...")
			forest = run_simulation(grid_size, fire_fq_denom, num_gens, mode)
		
			animate(forest.grids, grid_size, fire_fq_denom)

		elif mode == "2":
			num_gens = 100000000
			forest = run_simulation(grid_size, fire_fq_denom, num_gens, mode)
			print("done.")

			# run_analysis(grid_size, fire_fq_denom)

		else:
			print("Invalid mode. Bye.")
			exit()

main()