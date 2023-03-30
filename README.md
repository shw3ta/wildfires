
# Studying the dynamics of forest fires 

This repository contains a cellular automaton simulation of forest fires based on [Malamud et. al, 1998](https://github.com/shw3ta/wildfires/blob/main/references/MalamudTurcotteMorein_ForestFires_Science_1998.pdf) made as the final project for [Introduction to Python](https://github.com/eulerlab/pyclass23) at the University of Tübingen (2022-23), submitted by Shweta Prasad and Weronika Sójka. 

You can find the original problem description on the [course repo](https://github.com/eulerlab/pyclass23/tree/main/exams). 

## Repository organization
```bash
.
|-- LICENSE
|-- README.md
|-- animations
|   |-- animation_128_0.002.mp4
|   |-- animation_128_0.002_demo_high_res.mp4
|   `-- animation_128_0.002_demo_low_res.mp4
|-- logfiles
|   
|-- references
|   |-- MalamudTurcotteMorein_ForestFires_Science_1998.pdf
|   `-- Models_data_mechanisms_Quantifying_wildfire_regime.pdf
|-- scripts
|   |-- params.txt
|   `-- simulation.py
`-- webapp
    `-- home.py
```
### Instructions to run the program on your CLI:

All scripts can be found in [wildfires/scripts](https://github.com/shw3ta/wildfires/tree/main/scripts). 

To run the simulation script, navigate to this repository on your terminal and do
```bash
cd scripts/
python3 simulation.py
```

Further instructions are provided in the interface. 

## Caveats of this model and implementation
The model in the paper defines the neighbourhood of each cell as its 4 adjacent cells, i.e, the cells at the immediate top, left, bottom and right of the cell of interest. The cells in the diagonal neighbourhood are not included, and as a result, the way the fire spreads (as can be observed in the animation) reflects the underlying recursion as opposed to the expected radial spread of real fires. That being said, the final frame after the fire cannot spread any further reflects the total area burnt by the fire, and is, for the purpose of this project, the useful metric to analyze area-of-spread dynamics.

By default, we represent a forest as a square grid of dimensions $128 \times 128$. If you wish to change any of the parameters of your simulation, you can add/delete lines to/from the ```params.txt``` file in the ```scripts/``` folder as a comma-separated tuple of grid size, 1/fire frequency and number of generations per simulation. For example: ```128,2000,1000000000```. 

We provide two main modes to run this program in. 
1. ***fast mode***:
As required, this is the "number crunching" mode that does not display the state of the forest grid in any manner. It simulates $10^9$ generations on one grid instance and has a total run time of $\sim8$ hours if you choose to run a new simulation. Of course, if you reduce the order of simulations by a factor of $2$, the program runs in the order of minutes and not hours. On the CLI, you are shown how many generations of the total have been completed. \
We have already run multiple simulations on $128 \times 128$ grids with the $3$ fire frequency parameters given in the paper, namely at $1/125$, $1/500$ and $1/2000$. The corresponding output files are available in the repository under ```logfiles/``` with the naming convention ```logfile_{fq}_{gridsize}.csv```.  If you choose this mode to run the program in, we also provide you with the _much_ faster option of producing the analysis of just these older simulations as a proof of concept: we don't want you to be running the entire simulation epoch from scratch. Alternatively, please make changes to ```params.txt``` to run parameters of your choice: every new line is a new set of parameters.\
For very low fire frequencies on big grids, we may encounter maximum recursion depth errors, which in our case implies more than $12000$ recursive calls were made to the ```forest.spread_to()``` function: in case such an exception is encountered, the corresponding area burnt is randomly set to a value between $12000$ and $12800$.

2. ***slow mode***:
In this mode, we collect and use the grid state of the forest to display an animation. By default, the program shows you a grid of dimensions $128 \times 128$, running for $10000$ generations with a fire frequency of $1/500$. Any animation produced with this set of parameters will have 20 fires.\ 

To note: the animation is saved to ```animations/``` as a ```.mp4	``` file and is shown after frame by frame compression to ensure that memory usage does not explode with frames. We currently use a round-about method which requires that you have ```ffmpeg``` installed, but it's guaranteed to be at least three times faster than matplotlib's animation utilities. In case you do want to produce a high resolution output and have a lot of time on your hands, we provide you with a choice on that matter too.

