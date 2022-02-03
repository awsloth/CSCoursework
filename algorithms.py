from graph import Graph, Node

class Prims:
    def __init__(self, start_node: Node, graph: Graph):
        self.graph = graph
        self.visited_nodes = [start_node]
        self.chosen_edges = []
    
    def next_step(self):
        if len(self.visited_nodes) == len(self.graph.nodes):
            return "Finished"

        choice = None
        for node in self.visited_nodes:
            for (dest, edge) in self.graph.adjacency_lists[node].items():
                if dest not in self.visited_nodes and (choice is None or edge.weight < choice[1].weight):
                    choice = [dest, edge]

        self.visited_nodes.append(choice[0])
        self.chosen_edges.append(choice[1])

    def prev_step(self):
        if len(self.visited_nodes) != 0:
            self.visited_nodes = self.visited_nodes[:-1]
            self.chosen_edges = self.chosen_edges[:-1]

class Kruskals:
    def __init__(self, graph: Graph):
        self.graph = graph
        self.visited_nodes = []
        self.chosen_edges = []

    def next_step(self):
        to_pick = [edge for edge in sorted(self.graph.edges, key=lambda a: a.weight) if edge not in self.chosen_edges]

        cycle = True
        g = self.graph.copy()
        for edge in g.edges:
            if edge not in self.chosen_edges:
                g.delete_edge(edge)

        d = DepthFirst(to_pick[0].A, g)
        while d.next_step() != "Finished":
            d.next_step()

        if to_pick[0].B not in d.visited_nodes:
            cycle = False

        while cycle:
            g = self.graph.copy()
            for edge in g.edges:
                if edge not in self.chosen_edges:
                    g.delete_edge(edge)

            d = DepthFirst(to_pick[0].A, g)
            while d.next_step() != "Finished":
                d.next_step()

            if to_pick[0].B not in d.visited_nodes:
                cycle = False
            
            to_pick = to_pick[1:]

            if to_pick == []:
                return "Finished"

        if to_pick[0].A not in self.visited_nodes:
            self.visited_nodes.append(to_pick[0].A)
        if to_pick[0].B not in self.visited_nodes:
            self.visited_nodes.append(to_pick[0].B)

        self.chosen_edges.append(to_pick[0])
        
class DepthFirst:
    def __init__(self, start_node: Node, graph: Graph):
        self.graph = graph
        self.visited_nodes = [start_node]
        self.cur_node = start_node
        self.visit_stack = [start_node]

    def next_step(self):
        to_choose = [node for node in self.graph.adjacency_lists[self.cur_node]]

        if all([node in self.visited_nodes for node in to_choose]):
            self.visit_stack = self.visit_stack[:-1]
            if self.visit_stack == []:
                return "Finished"
                
            self.cur_node = self.visit_stack[-1]
        else:
            while to_choose[0] in self.visited_nodes:
                to_choose = to_choose[1:]

            self.cur_node = to_choose[0]

            self.visited_nodes.append(self.cur_node)
            self.visit_stack.append(self.cur_node)

    def prev_step(self):
        ...


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

    a = g.adjacency_lists

    k = Kruskals(g)
    while k.next_step() != "Finished":
        print(f"Update {[n.name for n in k.visited_nodes]}")
        print(f"Update {[e.weight for e in k.chosen_edges]}")
