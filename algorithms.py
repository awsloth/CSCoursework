from __future__ import annotations

# Import base libraries
import pygame
from typing import Union, TYPE_CHECKING

# Block off for type checking so cyclic import does not occur
if TYPE_CHECKING:
    # Import custom scripts
    from graph import Graph, Node, Edge

# Initialise pygame font library
pygame.font.init()

# Prims class
class Prims:
    """Class to run prims minimum spanning tree algorithm"""
    def __init__(self, start_node: Node, graph: Graph) -> None:
        """Initialisation function of the prims class"""

        # Create instance variables
        self.graph = graph
        self.visited_nodes: list[Node] = [start_node]
        self.chosen_edges: list[Edge] = []
    
    def next_step(self) -> Union[str, None]:
        """Runs the next step of the algorithm"""
        # If all nodes visited, return finished so the algorithm stops
        if len(self.visited_nodes) == len(self.graph.nodes):
            return "Finished"

        # Choose the next node to visit
        choice = None

        #  Iterate through each visited node
        for node in self.visited_nodes:
            # Iterate through each node and edge connection
            for (dest, edge) in self.graph.adjacency_lists[node].items():
                # If the connected node is not already visited and the weight is lower than
                # the current choice, swap out the connected node to choose
                if dest not in self.visited_nodes and (choice is None or edge.weight < choice[1].weight):
                    choice = [dest, edge]

        # Add node and connecting edge to corresponding visited lists
        self.visited_nodes.append(choice[0])
        self.chosen_edges.append(choice[1])

        # Highlight node and edge just used to show user what has happenned
        choice[0].highlight()
        choice[1].highlight()

    def prev_step(self) -> None:
        """Function to step back through the algorithm"""
        if self.visited_nodes != [] and self.chosen_edges != []:
            # Unhighlight just visited node and edge
            self.visited_nodes[-1].unhighlight()
            self.chosen_edges[-1].unhighlight()

            # Remove node and edge from corresponding visited lists
            self.visited_nodes = self.visited_nodes[:-1]
            self.chosen_edges = self.chosen_edges[:-1]

    def clear_up(self) -> None:
        """Function to clear up highlights after finishing"""
        # For each node visited unhighlight the node
        for node in self.visited_nodes:
            node.unhighlight()

        # For each edge visited unhighlight the edge
        for edge in self.chosen_edges:
            edge.unhighlight()

# Kruskals class
class Kruskals:
    """Handles running of Kruskal's algorithm for minimum spanning tree"""
    def __init__(self, graph: Graph) -> None:
        """Initialising function for Kruskals class"""
        # Create instance variables
        self.graph = graph
        self.visited_nodes: list[Node] = []
        self.chosen_edges: list[Edge] = []

    def next_step(self) -> Union[str, None]:
        """Runs next step of the algorithm"""
        # Get list of edges to pick from in weight order
        # already chosen edges are removed
        to_pick = [edge for edge in sorted(self.graph.edges, key=lambda a: a.weight) if edge not in self.chosen_edges]

        if to_pick == []:
            return "Finished"
        
        # variable to check for a cycle
        cycle = True

        # Copy the current graph
        g = self.graph.copy()

        # Remove all edges not chosen
        for edge in g.edges:
            if edge not in self.chosen_edges:
                g.delete_edge(edge)

        # Run depth first until complete on subgraph
        d = DepthFirst(to_pick[0].A, g)
        while d.next_step() != "Finished":
            d.next_step()

        # If node B not connected to node A then no cycle will be created
        if to_pick[0].B not in d.visited_nodes:
            cycle = False

        # Repeat cycle check until edge found
        # or until no valid edge is available
        while cycle:
            # Remove invalid edge
            to_pick = to_pick[1:]

            # If no valid edges, return finished to stop the algorithm
            if to_pick == []:
                return "Finished"

            # Running depth first on sub graph
            g = self.graph.copy()
            for edge in g.edges:
                if edge not in self.chosen_edges:
                    g.delete_edge(edge)

            d = DepthFirst(to_pick[0].A, g)
            while d.next_step() != "Finished":
                d.next_step()

            if to_pick[0].B not in d.visited_nodes:
                cycle = False

        # Check nodes not already visited
        if to_pick[0].A not in self.visited_nodes:
            # If not visited, add to visited list and highlight
            self.visited_nodes.append(to_pick[0].A)
            to_pick[0].A.highlight()
        if to_pick[0].B not in self.visited_nodes:
            # If not visited, add to visited list and highlight
            self.visited_nodes.append(to_pick[0].B)
            to_pick[0].B.highlight()

        # Add node to chosen edges and highlight
        self.chosen_edges.append(to_pick[0])
        to_pick[0].highlight()
    
    def prev_step(self) -> None:
        """Step back through the algorithm"""
        # Check that there are visited edges
        if self.chosen_edges != []:
            # Unhighlight last picked edge and remove from list
            self.chosen_edges[-1].unhighlight()
            self.chosen_edges = self.chosen_edges[:-1]

            # Get all nodes connected to current edges
            nodes = []
            for edge in self.chosen_edges:
                nodes.append(edge.A)
                nodes.append(edge.B)

            # Turn nodes into set, such that no nodes are repeated
            nodes = [*set(nodes)]

            # Unhighlight all nodes connected to removed edge
            # if not in above nodes
            for node in nodes:
                if node not in self.visited_nodes:
                    node.unhighlight()
                    
            # Update visited nodes
            self.visited_nodes = nodes

    def clear_up(self) -> None:
        """Clear up graph after algorithm is finished"""
        # Unhighlight visited nodes
        for node in self.visited_nodes:
            node.unhighlight()

        # Unhighlight chosen edges
        for edge in self.chosen_edges:
            edge.unhighlight()

# Depth first class    
class DepthFirst:
    """Class to handle the running of the depth first search algorithm"""
    def __init__(self, start_node: Node, graph: Graph) -> None:
        """Initialisation function of depth first class"""
        # Create instance variables
        self.graph = graph
        self.visited_nodes: list[Node] = [start_node]
        self.cur_node = start_node
        self.visit_stack: list[Node] = [start_node]

    def next_step(self) -> Union[str, None]:
        """Steps through the algorithm"""
        # Gets list of nodes adjacent to current node
        to_choose = [node for node in self.graph.adjacency_lists[self.cur_node]]

        # Check if all nodes already visited
        if all([node in self.visited_nodes for node in to_choose]):
            # Step back to parent node
            self.visit_stack = self.visit_stack[:-1]

            # If visit stack is empty the algorithm is finished
            if self.visit_stack == []:
                return "Finished"
                
            # Set the current node to the parent node
            self.cur_node = self.visit_stack[-1]
        else:
            # Select the first unvisited node
            while to_choose[0] in self.visited_nodes:
                # Reduce the list if the first node is already visited
                to_choose = to_choose[1:]

            # Change the current node to the choice
            self.cur_node = to_choose[0]

            # Add the node to the visited nodes and stack
            self.visited_nodes.append(self.cur_node)
            self.visit_stack.append(self.cur_node)

    def prev_step(self):
        """Steps back through the algorithm"""
        ...
        
# Box class
class Box:
    """Handles boxes, which are used in dijkstra's algorithm"""
    def __init__(self, node: Node) -> None:
        """Initialisation function for the box class"""
        # Create instance variable
        self.left: Union[str, int] = " "
        self.right: Union[str, int] = " "
        self.notes: list[int] = []
        self.node = node
        
        # Create instance constants
        self.FONT = pygame.font.SysFont("Helvetica", 10)
        self.PADDING = 4

    def draw(self, screen: pygame.Surface) -> None:
        """Function to draw the box to the screen"""
        # Get x and y of paired node
        x, y = self.node.x, self.node.y

        # Render each piece of text
        top_left = self.FONT.render(str(self.left), True, (0, 0, 0), (255, 255, 255))
        top_right = self.FONT.render(str(self.right), True, (0, 0, 0), (255, 255, 255))
        notes = self.FONT.render(", ".join([str(w) for w in self.notes]), True, (0, 0, 0), (255, 255, 255))

        # Work out box width and height
        box_width = max(notes.get_width(), top_left.get_width()+top_right.get_width()) + self.PADDING*3
        box_height = top_left.get_height() + notes.get_height() + self.PADDING*3

        # Work out the position of the top left of the box
        top_x = x - box_width//2
        top_y = y - self.node.RADIUS - 2 - box_height

        # Draw the containing box for the text
        pygame.draw.rect(screen, (255, 255, 255), (
            top_x+self.PADDING//2, top_y+self.PADDING//2,
            box_width-self.PADDING, box_height-self.PADDING))
        pygame.draw.rect(screen, (0, 0, 0), (top_x, top_y, box_width, box_height), self.PADDING)

        # Display the text
        screen.blit(top_left, (top_x+self.PADDING, top_y + self.PADDING))
        screen.blit(top_right, (top_x+top_left.get_width()+self.PADDING*2, top_y + self.PADDING))
        screen.blit(notes, (top_x+self.PADDING, top_y+top_left.get_height()+self.PADDING*2))

        # Draw the inner lines in the box
        pygame.draw.line(screen, (0, 0, 0), (x-self.PADDING//2, top_y), (x-self.PADDING//2, top_y+box_height//2), self.PADDING)
        pygame.draw.line(screen, (0, 0, 0), (top_x, top_y+box_height//2), (top_x+box_width, top_y+box_height//2), self.PADDING)
        
# Dijkstras class
class Dijkstras:
    """Handles Dijkstras shortest path algorithm"""
    def __init__(self, graph: Graph, start_node: Node, end_node: Node) -> None:
        """Initialisation function for dijkstras"""
        # Create instance variables
        self.start = start_node
        self.end = end_node
        self.graph = graph
        self.cur_node = self.start

        # Create a box for each node
        self.boxes: dict[Node, Box] = dict([[node, Box(node)] for node in self.graph.nodes])

        # Set up the start box
        self.boxes[self.start].left = 1
        self.boxes[self.start].right = 0

    def next_step(self) -> Union[str, None]:
        """Steps through the algorithm"""
        if self.cur_node == self.end:
            return "Finished"
        # Get all adjacent nodes
        new_nodes = [node for node in self.graph.adjacency_lists[self.cur_node]]

        # Highlight each new edge being considered
        for node in [n for n in new_nodes if self.boxes[n].left == " "]:
            self.graph.adjacency_lists[self.cur_node][node].highlight()

        # Iterate through each new node
        for node in new_nodes:
            # Calculate the weight to the node
            new_weight = self.graph.adjacency_lists[self.cur_node][node].weight+self.boxes[self.cur_node].right
            if self.boxes[node].notes != []:
                # If there are already notes check
                # that the new weight is less than the last note 
                if new_weight < self.boxes[node].notes[-1]:
                    # If it is lower add as a note
                    self.boxes[node].notes.append(new_weight)
            else:
                # If the box has no notes add the weight regardless
                self.boxes[node].notes.append(new_weight)

        # Get a list of unvisited nodes
        unvisited = [node for node in self.boxes if self.boxes[node].right == " " and self.boxes[node].notes != []]

        # If no nodes are unvisited return Finished to stop running
        if unvisited == []:
            return "Finished"

        # Sort the nodes by weight from the beginning and pick the first
        lowest = sorted(unvisited, key=lambda x: self.boxes[x].notes[-1])[0]

        # Update the new node's box with the new weight
        self.boxes[lowest].left = self.boxes[self.cur_node].left + 1
        self.boxes[lowest].right = self.boxes[lowest].notes[-1]

        # Update the current node
        self.cur_node = lowest

        # Highlight the node
        lowest.highlight()

    def prev_step(self) -> None:
        """Steps back through the algorithm"""
        if self.cur_node != self.start:
            self.cur_node.unhighlight()
            prev = self.boxes[self.cur_node].left - 1
            self.boxes[self.cur_node].left = " "
            self.boxes[self.cur_node].right = " "

            for (node, box) in self.boxes.items():
                if box.left == prev:
                    self.cur_node = node
                    break

            # Get all adjacent nodes
            new_nodes = [node for node in self.graph.adjacency_lists[self.cur_node]]

            # Highlight each new edge being considered
            for node in [n for n in new_nodes if self.boxes[n].left == " "]:
                self.graph.adjacency_lists[self.cur_node][node].unhighlight()

            # Iterate through each new node
            for node in new_nodes:
                self.boxes[node].notes = self.boxes[node].notes[:-1]

    def clear_up(self):
        """Cleans up after the algorithm is finished"""
        # Collect all visited nodes
        nodes = []
        for (node, box) in self.boxes.items():
            if box.left != " ":
                nodes.append(node)

        # Unhighlight all nodes
        for node in nodes:
            node.unhighlight()

        # Collect all visited edges
        edges = []
        for start_node in nodes:
            edges += [*self.graph.adjacency_lists[start_node].values()]

        edges = [*set(edges)]

        # Unhighlight all edges
        for edge in edges:
            edge.unhighlight()