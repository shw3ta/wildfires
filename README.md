# Forest fires model 

This repository contains a cellular automaton simulation of forest fires based on [Malamud et. al, 1998](https://github.com/shw3ta/wildfires/blob/main/references/MalamudTurcotteMorein_ForestFires_Science_1998.pdf) made as the final project for the course [Introduction to Python](https://github.com/eulerlab/pyclass23) at the University of Tübingen in the academic year 2022-23 by Shweta Prasad and Weronika Sójka. 

You can find the original problem description on the [course repo](https://github.com/eulerlab/pyclass23/tree/main/exams). To test out the functionality of the submitted code, run simulation.py from the scripts/ folder. The programme will prompt you to choose one of two modes as required in the problem description:

- *slow mode*: This produces an animation of the epoch just simulated. This is a proof of concept mode, so it runs 10^5 generations per epoch on a grid of size 128x128 (as in the paper). Running all 10^9 generations in this mode is not tractable for a (relatively) quick demonstration. To customize the input parameters that the programme runs, just add a new line to the params.txt file in the scripts/ folder with grid-size and denominator of the frequency of fires you want to simulatie per epoch, as comma-separated values. Eg: "128,2000" for a square grid of dimension 128x128, with a fire frequency of 1/2000. For details about the fire frequency, refer to the original paper or the webapp. 

When no fire has been started, a tree is added at a random empty position. When a fire is started, we follow it through to every cell that it spreads to according to the rules underlying this automaton. We find that as a caveat of the fire only spreading to adjacent neighbours and not diagonal neighbours, the spread follows depth-first-search projections, which after all the recursive function calls have returned, reflect the final state of the spread, which is the most relevant state as far as this paper is concerned -- this is the only state that reflects the total area afflicted by the fire. Once the spread is done, we "reset" the respective cells, and new trees are allowed to grow until another fire starts. To note, no new trees are added when a fire is spreading. 

You can find movies of some previous simulations in the animations/ subfolder. Note that while the simulation runs in under 1s for 10^5 generations per epoch, the animation is time consuming and can take up to half an hour to assemble. This is a caveat of the packages we are using to produce the animations. You may also find that if you do not locally have ffmpeg installed, the animations will not be saved.

- *fast mode*: Runs analysis on the logfiles generated during simulations.



All scripts can be found in [wildfires/scripts](https://github.com/shw3ta/wildfires/tree/main/scripts). 