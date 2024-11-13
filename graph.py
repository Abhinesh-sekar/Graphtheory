import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

st.title("Weighted Graph Visualization")

num_vertices = st.number_input("Enter the number of vertices:", min_value=2, max_value=10, value=4)

matrix = np.zeros((num_vertices, num_vertices), dtype=int)

# Style settings for aesthetics
st.write("""
    <style>
    .matrix-cell {
        padding: 8px;
        background-color: #f0f0f0;
        border-radius: 5px;
        text-align: center;
        margin: 4px;
        font-weight: bold;
    }
    .matrix-cell-gray {
        background-color: #d3d3d3;
        color: #808080;
    }
    </style>
    """, unsafe_allow_html=True)

st.write("Enter the weights for the adjacency matrix (0 means no edge):")
for i in range(num_vertices):
    cols = st.columns(num_vertices)
    for j in range(num_vertices):
        if i == j:
            cols[j].markdown(
                f"<div class='matrix-cell matrix-cell-gray'>0</div>", 
                unsafe_allow_html=True
            )
            matrix[i, j] = 0
        else:
            matrix[i, j] = cols[j].number_input(
                f"Weight ({i}, {j})", 
                min_value=0, 
                value=int(matrix[i, j]), 
                label_visibility="collapsed"
            )

graph = nx.Graph()
if st.button("Generate Graph"):
    for i in range(num_vertices):
        for j in range(i + 1, num_vertices):
            if matrix[i, j] != 0:
                graph.add_edge(i, j, weight=matrix[i, j])

    fig, ax = plt.subplots(figsize=(8, 8))
    pos = nx.spring_layout(graph)  

    nx.draw(graph, pos, ax=ax, node_color='lightblue', edge_color='gray', with_labels=True)

    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    st.pyplot(fig)
    
if st.button("Genereate Graph")
    
