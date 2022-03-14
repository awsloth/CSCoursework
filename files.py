# Import base libraries
import json

# Import custom scripts
from graph import Graph, Node, Edge

def save_graph(graph: Graph, file_name: str) -> None:
    """Function to save graphs"""
    # Get the graph adjacency list
    adjacency_list = graph.adjacency_lists

    # Give each node and edge a name
    nodes = dict([(node, f"node{i}") for i, node in enumerate(graph.nodes)])
    edges = dict([(edge, f"edge{i}") for i, edge in enumerate(graph.edges)])

    # Translate the adjacency list using the above assigned names
    stored_list = {}
    for (key, adj_list) in adjacency_list.items():
        new_adj_list = {}
        for (key2, edge) in adj_list.items():
            new_adj_list.update({nodes[key2]: edges[edge]})
        stored_list.update({nodes[key]: new_adj_list})

    # Encode the nodes, storing their name and positions
    stored_nodes = {}
    for (node, name) in nodes.items():
        stored_nodes.update({name:{"name": node.name, "pos": [node.x, node.y]}})

    # Encode the edges, storing their weight and start and end names
    stored_edges = {}
    for (edge, name) in edges.items():
        stored_edges.update({name:{"weight": edge.weight, "start_node": nodes[edge.A], "end_node": nodes[edge.B]}})

    # Create a dictionary storing all the information
    file_content = {"info": {"adjacency_list": stored_list, "nodes": stored_nodes, "edges": stored_edges}}
    
    # Format the dictionary as a json format
    to_write = json.dumps(file_content)

    # Write the dictionary to a file
    with open(f"graphs/{file_name}.json", "w") as f:
        f.write(to_write)

def load_graph(file_name: str) -> Graph:
    """Function to load a graph"""
    # Open the given file
    with open(f"graphs/{file_name}.json") as f:
        content = f.read()

    # Convert from json format to a dictionary
    graph = json.loads(content)['info']

    # Get all the nodes
    nodes = graph['nodes']

    # Create a new node for each node in the file
    new_nodes = {}
    for (name, info) in nodes.items():
        new_nodes.update({name: Node(*info['pos'], info['name'])})

    # Get all the edges
    edges = graph['edges']

    # Create a new edge for each edge in the file
    new_edges = {}
    for (name, info) in edges.items():
        new_edges.update({name: Edge(new_nodes[info['start_node']], new_nodes[info['end_node']], info['weight'])})

    # Translate the string version of the adjacency list to hold classes
    old_adj_list = graph['adjacency_list']
    translated_list = {}
    for (node, adj_list) in old_adj_list.items():
        inner_list = {}
        for (c_node, edge) in adj_list.items():
            inner_list.update({new_nodes[c_node]:new_edges[edge]})
        translated_list.update({new_nodes[node]:inner_list})

    # Create a new graph
    g = Graph()

    # Swap out the graph adjacency list
    g.adjacency_lists = translated_list

    # Return the graph
    return g


if __name__ == "__main__":
    g = Graph()

    g.add_node([10, 10])
    g.add_node([10, 90])
    g.add_node([90, 10])
    g.add_node([90, 90])

    g.add_edge(g.nodes[0], g.nodes[1])
    g.add_edge(g.nodes[0], g.nodes[2])
    g.add_edge(g.nodes[0], g.nodes[3])
    g.add_edge(g.nodes[1], g.nodes[2])
    g.add_edge(g.nodes[1], g.nodes[3])
    g.add_edge(g.nodes[2], g.nodes[3])

    for (i, edge) in enumerate(g.edges):
        edge.weight = i+1

    save_graph(g, "new_graph")

    print([[n.name, n.x, n.y] for n in g.nodes])
    print([g.weight for g in g.edges])

    g = load_graph("new_graph")

    print([[n.name, n.x, n.y] for n in g.nodes])
    print([g.weight for g in g.edges])
