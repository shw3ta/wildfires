import streamlit as st
from PIL import Image
import os

#homepage

st.title("Forest fire simulation")
st.write("Cellular automata simulation of forest fires based on [Malamud et. al, 1998](https://github.com/shw3ta/wildfires/blob/main/references/MalamudTurcotteMorein_ForestFires_Science_1998.pdf) made for the purpose of Introduction to Python course at University of Tübingen in an academic year 2022/23 by Shweta Prasad and Weronika Sójka.")
st.markdown("---")
st.write("""
         ## Introduction
         
         Forest fire model is an example of dynamical system displaying self-organized criticality. 
         The model forest consists of randomly planted trees on a square grid at successive time stamps, 
         randomly dropping a match on a grid at given frequency. 
         There are three possible states: empty (0), planted (1) and burning (2). 
         A maximum of one tree can occupy each grid site. 
         If a match is dropped on empty site, nothing happens. 
         If it is dropped on a planted site, tree starts to burn and a fire consumes all adjacent nondiagonal trees.

         """)


st.markdown("---")
st.write(""" 

        ## Slow mode simulation

        Below you can specify all required parameters and run a simulation yourself. 
        The simulation will run on a grid with randomly planted trees. 
        You have to specify a dimension of the grid, how often the fire will sparkle and how many simulations will be run.)

        """)

grid_size = st.number_input("Enter the dimension of a grid you want to define:", min_value=2, max_value=70)

if type(grid_size) != int: 
    st.write("Invalid entry, enter an integer number.")

fire_freq_denom = st.number_input("Enter a number after how many time steps you want to spark a fire:", min_value=100, max_value=500)

if type(fire_freq_denom) != int:
    st.write("Invalid entry, enter an integer number.")

num_sims = st.number_input("Enter a number of simulations you want to run:", min_value=100, max_value=10000)

if type(num_sims) != int:
    st.write("Invalid entry, enter an integer number.")

# open .txt and overwrite
path = os.getcwd() + "\\scripts"
#os.chdir(path)

#lst = [grid_size, fire_freq_denom, num_sims]
#str_lst = ','.join(str(x) for x in lst)

#with open('slow_mode.txt','r+') as f:
#    f.write(str_lst)

# run the app


st.markdown("---")
st.write(""" 
        ## Fast mode simulation 

        In an original paper of [Malamud et. al, 1998](https://github.com/shw3ta/wildfires/blob/main/references/MalamudTurcotteMorein_ForestFires_Science_1998.pdf), 
        the authors stated that the frequency of occurrence of fires versus fire size follows a power law. 
        We have reproduced these results on our fire models. 
        Below you can see animations and noncumulative frequency-area distributions of model forest for a grid size of 128x128 at three sparking frequencies. 
        
        """)

