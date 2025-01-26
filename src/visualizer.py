import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

def visualize_dependency_graph(dependencies, output_file=None):
    """
    Visualize the dependency graph using networkx and matplotlib or pyvis.
    Args:
        dependencies (dict): A dictionary of dependencies, where keys are package names
                             and values are lists of dependencies.
        output_file (str, optional): Path to save the visualization as an HTML file (for pyvis).
    Returns:
        None
    """
    # Create a directed graph
    graph = nx.DiGraph()

    # Add nodes and edges
    for package, deps in dependencies.items():
        graph.add_node(package)
        for dep in deps:
            graph.add_node(dep)
            graph.add_edge(package, dep)

    if output_file:
        # Use pyvis for interactive visualization
        net = Network(notebook=False, directed=True)
        net.from_nx(graph)
        net.show(output_file)
        print(f"Graph saved to {output_file}")
    else:
        # Use matplotlib for static visualization
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(graph, seed=42)
        nx.draw(graph, pos, with_labels=True, node_color='skyblue', edge_color='gray', font_weight='bold', node_size=2000)
        plt.title("Dependency Graph", fontsize=16)
        plt.show()
