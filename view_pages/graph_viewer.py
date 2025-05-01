# import networkx as nx
# >>> import matplotlib.pyplot as plt
# >>> G = nx.read_graphml('test.graphml')
# >>> nx.draw(G)
# >>> plt.show()

import streamlit as st
import networkx as nx
from pyvis.network import Network
import os
from datetime import datetime
from GraphRAGWrapper import GraphRAGWrapper


def visualize_graph(G):
	net = Network(height='700px', width='100%', bgcolor='#ffffff', font_color='black')
	net.force_atlas_2based()

	for node in G.nodes():
		net.add_node(node, label=node, title=f"Node: {node}", size=10 + G.degree[node])

	for edge in G.edges():
		net.add_edge(edge[0], edge[1])

	net.set_options("""
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "solver": "forceAtlas2Based"
      }
    }
    """)

	html_path = "temp_network.html"
	net.save_graph(html_path)
	with open(html_path, 'r', encoding='utf-8') as f:
		html_content = f.read()
	os.remove(html_path)
	return html_content


# Page setup
st.title("GraphRAG Knowledge Graph Viewer")
st.markdown("Interactive visualization of the knowledge graph")
st.markdown("-----")

# Initialize GraphRAG client
graphrag_client = GraphRAGWrapper()
G = graphrag_client.get_knowledge_graph()  # Assuming this method exists

# Sidebar metrics
with st.sidebar:
	st.header("Graph Statistics")
	st.metric("Total Nodes", len(G.nodes()))
	st.metric("Total Edges", len(G.edges()))
	st.metric("Graph Density", round(nx.density(G), 4))

	st.markdown("----")
	st.header("Node Search")
	search_node = st.text_input("Search for a node:", "")
	if search_node:
		matching_nodes = [n for n in G.nodes() if search_node.lower() in str(n).lower()]
		if matching_nodes:
			selected_node = st.selectbox("Select node:", matching_nodes)
			if selected_node:
				st.write("Node Properties:")
				st.write(dict(G.nodes[selected_node]))
				st.write("Connected to:")
				for neighbor in G.neighbors(selected_node):
					st.write(f"- {neighbor}")
		else:
			st.warning("No matching nodes found")

# Main visualization
try:
	html_content = visualize_graph(G)
	st.components.v1.html(html_content, height=700)
except Exception as e:
	st.error(f"Error visualizing graph: {str(e)}")

# Controls below visualization
col1, col2 = st.columns(2)
with col1:
	if st.button("Reset View"):
		st.rerun()
with col2:
	if st.button("Export Graph"):
		try:
			export_path = f"export/graph_{datetime.now().strftime('%Y%m%d_%H%M%S')}.graphml"
			os.makedirs('export', exist_ok=True)
			nx.write_graphml(G, export_path)
			with open(export_path, 'rb') as f:
				st.download_button(
					label="Download GraphML",
					data=f,
					file_name=os.path.basename(export_path),
					mime="application/xml"
				)
		except Exception as e:
			st.error(f"Export failed: {str(e)}")