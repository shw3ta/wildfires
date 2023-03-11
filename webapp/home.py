import streamlit as st
from PIL import Image
import os

#homepage

st.title("Forest fire simulation")
st.write("Cellular automata simulation of forest fires based on [Malamud et. al, 1998](https://github.com/shw3ta/wildfires/blob/main/references/MalamudTurcotteMorein_ForestFires_Science_1998.pdf) made for the purpose of Introduction to Python course at University of Tübingen in an academic year 2022/23 by Shweta Prasad and Weronika Sójka.")
st.markdown("---")
st.write("""
         ## Introduction
         
         Forest fire model is an example of dynamical system displaying self-organized criticality. The model forest consists of randomly planted trees on a square grid at successive time stamps, randomly dropping a match on a grid at given frequency. There are three possible states: empty (0), planted (1) and burning (2). A maximum of one tree can occupy each grid site. If a match is dropped on empty site, nothing happens. If it is dropped on a planted site, tree starts to burn and a fire consumes all adjacent nondiagonal trees.
         """)
