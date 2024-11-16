import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

st.title("Hamiltonian Circuit Visualization")

num_vertices = st.number_input("Enter the number of vertices:", min_value=2, max_value=10, value=4)
matrix = np.zeros((num_vertices, num_vertices), dtype=int)

st.write("Enter the weights for the adjacency matrix (0 means no edge):")
for i in range(num_vertices):
    cols = st.columns(num_vertices)
    for j in range(num_vertices):
        if i == j:
            cols[j].markdown(f"<div style='text-align: center;'>0</div>", unsafe_allow_html=True)
            matrix[i, j] = 0
        elif i < j:
            matrix[i, j] = cols[j].number_input(f"Weight ({i}, {j})", min_value=0, value=0, label_visibility="collapsed")
            matrix[j, i] = matrix[i, j] 
        else:
            cols[j].markdown(f"<div style='text-align: center;'>{matrix[i, j]}</div>", unsafe_allow_html=True)


def is_valid(vertex, pos, path, graph):
    if graph[path[pos - 1]][vertex] == 0:
        return False
    if vertex in path:
        return False
    return True

def hamiltonian_util(graph, path, pos, n, all_paths):
    if pos == n:
        if graph[path[pos - 1]][path[0]] != 0:
            path.append(path[0])
            all_paths.append(path[:])
            path.pop()
        return

    for vertex in range(n):
        if is_valid(vertex, pos, path, graph):
            path.append(vertex)
            hamiltonian_util(graph, path, pos + 1, n, all_paths)
            path.pop()

def find_hamiltonian_circuits(graph, start_vertex):
    n = len(graph)
    path = [start_vertex]
    all_paths = []
    hamiltonian_util(graph, path, 1, n, all_paths)
    return all_paths


start_vertex = st.number_input("Enter the starting vertex:", min_value=0, max_value=num_vertices - 1, value=0)
if st.button("Find Hamiltonian Circuits"):
    circuits = find_hamiltonian_circuits(matrix.tolist(), start_vertex)
    st.write(f"Hamiltonian Circuits starting from vertex {start_vertex}:")

    paths_and_costs = []
    
    for circuit in circuits:
        total_cost = sum(matrix[circuit[i], circuit[i + 1]] for i in range(len(circuit) - 1))
        paths_and_costs.append({"Path": " -> ".join(map(str, circuit)), "Total Cost": total_cost})
    
    st.table(paths_and_costs)

    graph = nx.from_numpy_array(matrix)
    pos = nx.spring_layout(graph)

    fig, ax = plt.subplots(figsize=(8, 8))

    def update(num):
        ax.clear()
        nx.draw(graph, pos, ax=ax, node_color='lightblue', edge_color='gray', with_labels=True)
        
        if circuits:
            path = circuits[num % len(circuits)]
            edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
            
            nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color='orange', ax=ax)
            nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='blue', width=2, ax=ax)

            edge_labels = {(u, v): matrix[u, v] for u, v in edges}
            nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax)
            
            ax.set_title(f"Path {num + 1}: {' -> '.join(map(str, path))}")

    ani = FuncAnimation(fig, update, frames=len(circuits), interval=2000, repeat=True)
    ani.save(".hamiltonian_circuits.gif", writer='imagemagick')
    
    st.image(".hamiltonian_circuits.gif", caption="Hamiltonian Circuits Animation", use_container_width=True)
