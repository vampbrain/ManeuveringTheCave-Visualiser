# Install required packages first
# pip install streamlit matplotlib numpy pillow

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from PIL import Image
import random

# Function to find all paths
@st.cache_data
def find_paths(i, j, path, grid, end, limit_paths=100):
    paths = []
    def backtrack(i, j, path):
        if len(paths) >= limit_paths:
            return  # Stop finding more paths if limit is reached
        if i > end[0] or j > end[1]:
            return
        path.append((i, j))
        if (i, j) == end:
            paths.append(list(path))  # Store a copy of the path
        else:
            backtrack(i, j + 1, path)  # Move right
            backtrack(i + 1, j, path)  # Move down
        path.pop()  # Backtrack
    backtrack(i, j, path)
    return paths

# Streamlit app for user input and visualization
st.title("Optimized Grid Path Visualizer")

# User input for grid size and start/end points
m = st.slider("Grid Rows (m)", 2, 10, 5)
n = st.slider("Grid Columns (n)", 2, 10, 5)

start_row = st.slider("Start Point Row", 0, m - 1, 0)
start_col = st.slider("Start Point Column", 0, n - 1, 0)
end_row = st.slider("End Point Row", 0, m - 1, m - 1)
end_col = st.slider("End Point Column", 0, n - 1, n - 1)

start = (start_row, start_col)
end = (end_row, end_col)

# Grid setup and pathfinding
grid = np.zeros((m, n))
paths = find_paths(start[0], start[1], [], grid, end, limit_paths=50)  # Limit to 50 paths for performance

# Create the figure and axis for plotting
fig, ax = plt.subplots()
ax.matshow(grid, cmap="Greys")

# Mark start and end points
ax.plot(start[1], start[0], "go", markersize=10)  # Start point in green
ax.plot(end[1], end[0], "ro", markersize=10)      # End point in red

# Initialize an empty line object for animation
path_line, = ax.plot([], [], "bo", markersize=8)

# Function to update the animation at each frame
def update(frame):
    # Get the current path up to the current frame step
    path = paths[frame % len(paths)]
    x_data = [p[1] for p in path]
    y_data = [p[0] for p in path]
    
    path_line.set_data(x_data, y_data)
    return path_line,

# Create the animation
ani = FuncAnimation(fig, update, frames=len(paths), interval=300, blit=True, repeat=True)

# Save the animation as a GIF
gif_path = "/tmp/path_animation.gif"
ani.save(gif_path, writer="pillow", fps=2)

# Display the GIF in Streamlit
st.image(gif_path)

st.write("Total number of paths visualized:", len(paths))
