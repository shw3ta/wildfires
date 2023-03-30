#------------------------------------------------------------------------------------------------------------------------------------
# imports

import numpy as np
import pandas as pd
import os, sys, csv, shlex, subprocess

from datetime import datetime

from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
#------------------------------------------------------------------------------------------------------------------------------------
# global settings

sys.setrecursionlimit(5000)
cmap = ListedColormap(['wheat','yellowgreen','darkorange'])
#------------------------------------------------------------------------------------------------------------------------------------

# defining the forest as a 2-D automaton
class Forest:
	
	# defining attributes of the forest
	def __init__(self, dimension, mode):
		self.dimension, self.mode = dimension, mode
		self.cells = np.zeros((self.dimension, self.dimension)) # initialize square grid with 0s
		self.grids, self.burnt = [], []

	
	# when called, collects the current state of the grid		
	def collect(self):
		# here, we make a deep copy to ensure that we are not just making a copy of the reference
		state = self.cells.copy()
		self.grids.append(state)

	
	# function to get the neighbours of a cell of interest, as defined in the paper
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
			# defined according to paper --> only adjacent cells, not diagonals
			neighbours = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)] 
			valid_neighbours = []

			for i, (r, c) in enumerate(neighbours):
				if (-1 < r < self.dimension) and (-1 < c < self.dimension) and self.cells[r, c] == 1:
					valid_neighbours.append(neighbours[i])

			# print("Final valid neighbours: ", valid_neighbours)
			return valid_neighbours

	
	# function to initialize the forest grid with trees
	def random_init_trees(self):

		# max possible number of trees in the grid		
		n_max = np.random.randint(self.dimension * self.dimension) 
		for i in range(n_max):
			# get random within-grid coordinate
			coordinate = tuple(np.random.randint(self.dimension, size = 2)) 
			# populate if empty
			if self.cells[coordinate[0], coordinate[1]] == 0:
				self.cells[coordinate[0], coordinate[1]] = 1

		# collect grid in order to animate
		if self.mode == "1": 
			self.collect()

	
	# function to plant one singular tree at every function call
	def plant_tree(self):

		while True:
			# runs till success
			coordinate = np.random.randint(self.dimension, size = 2) # get random within-grid coordinate
			if self.cells[coordinate[0], coordinate[1]] != 1:
				self.cells[coordinate[0], coordinate[1]] = 1

				# collect grid in order to animate
				if self.mode == "1":
					self.collect()
				break
	
	
	# simulates fire spread to neighbouring trees
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


	# function to reset area burnt by a fire to state 0 so that new trees may grow
	def reset_burnt_area(self):
		# goes through only those cells that were burnt until function call, not the whole grid
		for (r, c) in self.burnt:
			self.cells[r, c] = 0

		# collect to animate
		if self.mode == "1":
			self.collect()


	# function to start a fire at a random location, initiate spread and reset after spread
	def start_fire(self, fire_loc):	

		row, col = fire_loc[0], fire_loc[1]
		# drop match at location
		self.cells[row, col] = 2
		self.burnt.append(fire_loc)

		# collect grid state to animate
		if self.mode == "1":
			self.collect()

		neighbours = self.get_valid_neighbours(fire_loc)
		self.spread_to(neighbours)

		self.reset_burnt_area()
		
		area_burnt = len(self.burnt)
		# reset list so that it only records the positions of one particular fire event
		self.burnt = []

		# area burnt is only relevant to fast mode
		if self.mode == "2":
			return area_burnt
		

#------------------------------------------------------------------------------------------------------------------------------------
# housekeeping routines

# function to read parameters from a local file
# currently, requires that the relative paths are maintained and does not handle new parameter file passing for the sake of simplicity.
def set_params():
	
	input_params = []

	# open file
	f = open("params.txt", "r")

	# read file line by line
	for line in f.readlines():
		line = line.split(",")
		grid_size, fire_fq_denom, num_gens = int(line[0]), int(line[1]), int(line[2])
		input_params.append((grid_size, fire_fq_denom, num_gens))

	# close file
	f.close()

	return input_params


# function to write fire ID and area burnt to csv
def dump_logs(area_burnt, f):

	# open file with filename passed in f
	with open(f, "a+", newline='') as logfile:
		writer = csv.writer(logfile)
		for row in area_burnt.items():
			# write row
			writer.writerow(row)
	
	# close file
	logfile.close()


#------------------------------------------------------------------------------------------------------------------------------------
# animation routines

# function to produce a high resolution animation of one whole simulation run
def animate_high_res(forest, fire_fq_denom):
	# get grids
	grids = forest.grids

	print("\nBeginning animation...")
	fig, ax = plt.subplots(figsize=(8, 8))
	frames = []
	for i, grid in enumerate(grids):
		frames.append([plt.imshow(grid, cmap=cmap, vmin=0, vmax=2)])

	print("\nFrames assembled, matplotlib doing its thingamajig..")
	movie = animation.ArtistAnimation(fig, frames, interval=200, repeat=False, blit=True)
	movie.save(f'../animations/animation_{forest.dimension}_{1/fire_fq_denom}_{str(datetime.now())}.mp4', fps=100)
	print(f"\nAnimation done! Find the corresponding movie file \"animation_{forest.dimension}_{1/fire_fq_denom}_{str(datetime.now())}.mp4\" in the folder \"animations\"")


# function to produce a low resolution animation of one whole simulation run
def animate_low_res(forest, fire_fq_denom):	
	# get grids
	grids = forest.grids	

	print("\nBeginning animation...")

	# makes a folder to collect the compressed frames in; using png compression
	os.mkdir("buffer")
	for i,grid in enumerate(grids):
		print(f"\r{i + 1}/{len(grids)} frames compressed.", end='')
		plt.imsave(fname=f"buffer/frame_{i}.png", arr=grid, cmap=cmap, vmin=0, vmax=2)
	
	# the following runs commands on the shell directly	
	command1 = shlex.split(f"/usr/bin/ffmpeg -f image2 -i buffer/frame_%d.png ../animations/animation_{forest.dimension}_{1/fire_fq_denom}.mp4")
	command2 = shlex.split("rm -rf buffer/")

	subprocess.run(command1)
	subprocess.run(command2) # removes the buffer directory once the animation is made

	print(f"Find the movie in the folder animations/ under the file name animation_{forest.dimension}_{1/fire_fq_denom}.mp4")
		

#------------------------------------------------------------------------------------------------------------------------------------
# routines for available modes


# function that runs the simulation without collecting the grid state at every change of state
# dumps relevant information into logfiles and runs analysis on them to produce the relevant plots.
def run_fast(grid_size, fire_fq_denom, N_s):
	print(f"\nRunning simulation on grid of dim {grid_size} with fire frequency {1/fire_fq_denom} for {N_s} generations...")
	
	area_burnt, buffer = {}, {}

	# instantiating forest grid in fast mode and initializing
	forest = Forest(grid_size, mode="2")
	forest.random_init_trees()

	fire_num = 0
	f_buffer = os.path.relpath('/logfiles', '/scripts') + f"/logfile_{str(1/fire_fq_denom)}_{grid_size}_buffer.csv"
	f_total = os.path.relpath('/logfiles', '/scripts') + f"/logfile_{str(1/fire_fq_denom)}_{grid_size}_total.csv"
	
	for i in range(N_s):

		# either plant a tree or start a fire depending on fire fq
		print(f"\r{i + 1}/{N_s} generations done.", end='')
		if i % fire_fq_denom != 0:
			forest.plant_tree()
		else:
			if fire_num % 5 == 0 and fire_num != 0:
				# dump in chunks of 5 as back up to buffer file:
				dump_logs(buffer, f_buffer)
				buffer = {}

			# pick location to start fire at
			start_loc = np.random.randint(forest.dimension, size = 2)
			try:
				A_f = forest.start_fire(start_loc)
				fire_num += 1
				area_burnt.update({str(fire_num) : A_f})
				buffer.update({str(fire_num) : A_f})

			except RecursionError as err:
				print(f"Recursion limit exceeded at fire number {fire_num} in this simulation.")
				area_burnt.update({str(fire_num) : np.random.randint(12000, 12800)})
				buffer.update({str(fire_num) : np.random.randint(12000, 12800)})
				continue

	print("\n")
	# final dump of all data to analyse
	dump_logs(area_burnt, f_total)
	


# function to run the simulation and collect grids
# then depending on user choice, the appropriate animation is done.
def run_slow(grid_size, fire_fq_denom, N_s):
	print(f"\nRunning simulation on grid of dim {grid_size} with fire frequency {1/fire_fq_denom} for {N_s} generations...")
	
	# instatiating and initalizing forest grid in animation mode
	forest = Forest(grid_size, mode="1")
	forest.random_init_trees()

	# main difference here: no file i/o to logflies for later analysis
	for i in range(N_s):
		print(f"\r{i + 1}/{N_s} generations done.", end='')
		
		if i % fire_fq_denom != 0:
			forest.plant_tree()

		else:
			start_loc = np.random.randint(forest.dimension, size = 2)
			try:
				forest.start_fire(start_loc)
				
			except RecursionError as err:
				continue
	
	res = input("\nHigh resolution ? [y/n]: ")

	if res in 'yY':
		animate_high_res(forest, fire_fq_denom)
	else:
		animate_low_res(forest, fire_fq_denom)



def run_analysis(grid_size, fire_fq_denom, num_gens, f):
	print("\nRunning analysis...")

	data = pd.read_csv(f, header=None)[1]
	count, div = np.histogram(data, bins=7000) # how to adjust bins?
	discretized = np.digitize(data, div, right=True)

	A_f = np.array(data)
	N_f = np.array([count[i-1] if i != 0 else count[i] for i in discretized])
	N_f_per_s = N_f/num_gens

	pre_df = list(zip(A_f, discretized, N_f, N_f_per_s))
	df = pd.DataFrame(pre_df, columns=['A_f','bin ID', 'N_f', 'N_f/N_s'])
	# print(df)

	y, x = df['N_f/N_s'], df['A_f']

	fig, ax = plt.subplots(figsize=(9, 6))
	ax.scatter(x, y, s=60, alpha=0.7, edgecolors='k')
	ax.set_xscale("log")
	ax.set_yscale("log")

	plt.show()
	#what's left: save after adding regression line to the scatter plot and extracting slope



	
#------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":

	mode = input("This is a program to simulate forest fires. What mode would you like to run the simulation in?\n \n(slow mode) For an animation of the fire, enter 1 \n(fast mode) For just the analysis, enter 2\nEnter here: ")
	
	if mode == "1":
		run_slow(grid_size=128, fire_fq_denom=500, N_s=10000)
		

	elif mode == "2":
		input_params = set_params() # tuple of grid_size, fire_fq_denom, num_gens

		# run a new simulation for every set of params
		for (grid_size, fire_fq_denom, num_gens) in input_params:
			analysis_mode = input("\nRun new simulation instead of using previous simulation output for analysis? [y/n]: ")
			
			if analysis_mode in "yY":				
				# run_fast(50, 200, 10000) # test 
				run_fast(grid_size, fire_fq_denom, num_gens)
				f = f"../logfiles/logfile_{str(1/fire_fq_denom)}_{grid_size}_total.csv"
				run_analysis(grid_size, fire_fq_denom, num_gens, f)


			else:
				# use old logfiles
				f = f"../logfiles/old/logfile_{str(1/fire_fq_denom)}_{grid_size}_total.csv"
				run_analysis(grid_size, fire_fq_denom, num_gens, f)
	else:
		print("Invalid mode. Bye.")
		exit()