import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define an example adjacency matrix
matrix = np.array([
    [0, 1, 1, 0,1],
    [1, 0, 1, 1,0],
    [1, 1, 0, 1,0],
    [0, 1, 1, 0,1],
    [1, 1, 0, 0,0]
])

# Generate the graph from the adjacency matrix
graph = nx.from_numpy_array(matrix)

# Find all paths between nodes, e.g., from node 0 to node 3
all_paths = list(nx.all_simple_paths(graph, source=0, target=4))

# Set up the figure and axis for the plot
fig, ax = plt.subplots(figsize=(6, 6))
pos = nx.spring_layout(graph)  # Position nodes for visualization

# Draw the graph structure with all edges in a light color
nx.draw(graph, pos, ax=ax, node_color='lightblue', edge_color='gray', with_labels=True)

# Function to animate each path
def update(num):
    ax.clear()
    nx.draw(graph, pos, ax=ax, node_color='lightblue', edge_color='gray', with_labels=True)
    
    # Highlight the path being animated
    path = all_paths[num % len(all_paths)]
    edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    
    # Draw the nodes and edges of the current path in a distinct color
    nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color='orange', ax=ax)
    nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='blue', width=2, ax=ax)

    # Label the current path
    ax.set_title(f"Path {num + 1}: {' -> '.join(map(str, path))}")

# Create the animation
ani = FuncAnimation(fig, update, frames=len(all_paths), interval=1000, repeat=True)

# Display the animation
plt.show()
