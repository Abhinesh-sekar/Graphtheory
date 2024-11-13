import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

matrix = np.array([
    [0, 1, 1, 0,1],
    [1, 0, 1, 1,0],
    [1, 1, 0, 1,0],
    [0, 1, 1, 0,1],
    [1, 1, 0, 0,0]
])

graph = nx.from_numpy_array(matrix
all_paths = list(nx.all_simple_paths(graph, source=0, target=4))
fig, ax = plt.subplots(figsize=(6, 6))
pos = nx.spring_layout(graph)

nx.draw(graph, pos, ax=ax, node_color='lightblue', edge_color='gray', with_labels=True)

def update(num):
    ax.clear()
    nx.draw(graph, pos, ax=ax, node_color='lightblue', edge_color='gray', with_labels=True)  
    path = all_paths[num % len(all_paths)]
    edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color='orange', ax=ax)
    nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='blue', width=2, ax=ax)
    ax.set_title(f"Path {num + 1}: {' -> '.join(map(str, path))}")

ani = FuncAnimation(fig, update, frames=len(all_paths), interval=1000, repeat=True)
plt.show()
