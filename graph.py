# Import base libraries
import pygame
import json
import os
from typing import Union

# Import custom scripts
import guiElements
from colour import Colour
from settings import Settings
from algorithms import Prims, Dijkstras

# Initialise the python font library
pygame.font.init()

def wordFilter(word):
    ...

class Node:
    """Class to handle nodes"""
    def __init__(self, x: Union[int, float], y: Union[int, float], name: str, settings: Settings) -> None:
        """Initialisation function of node class"""
        # Check that arguments are of correct type
        if any([type(v) not in [int, float] for v in [x, y]]):
            raise BaseException("Entered wrong type")
        if type(name) not in [str, int, float]:
            raise BaseException("Entered wrong type for name")

        # Create instance variables
        self.x = x
        self.y = y
        self.name = str(name)
        self.show_name = False
        self.colour = Colour(0, 1, 1)
        self.settings = settings

        # Create instance constants
        self.RADIUS = 10
        self.TEXT_COLOUR = Colour(0, 0, 0)
        self.TEXT_BG = Colour(0, 0, 1)
        self.FONT = pygame.font.SysFont(self.settings.font, 10)

    def highlight(self) -> None:
        """Function to highlight the node"""
        # Up the hue of the colour
        self.colour.h = self.colour.h + 120

    def unhighlight(self) -> None:
        """Function to unhighlight the node"""
        # Down the hue of the colour
        self.colour.h = self.colour.h - 120

    def on_hover(self, mouse_pos: tuple[int, int]) -> bool:
        """Function to check whether node is hovered over"""
        # Get mouse x and y
        x, y = mouse_pos

        # If mouse in surrounding circle, then return True and show name
        if (x-self.x)**2 + (y-self.y)**2 <= self.RADIUS**2:
            self.show_name = True
            return True

        # If mouse not on node hide name
        self.show_name = False

        return False

    def draw(self, screen: pygame.Surface) -> None:
        """Function to draw the node"""
        # Draw circle for node
        pygame.draw.circle(screen, self.colour.rgb, (self.x, self.y), self.RADIUS)

        # If showing the name
        if self.show_name or self.settings.show_names:

            # Render name as text
            self.render = self.FONT.render(self.name, True, self.TEXT_COLOUR.rgb, self.TEXT_BG.rgb)

            # Display text to screen
            screen.blit(
                self.render, (self.x-self.render.get_width()/2,
                self.y-self.RADIUS-self.render.get_height())
                )

# Edge class
class Edge:
    """Class to handle creation of edges"""
    def __init__(self, start_node: Node, end_node: Node, weight: int, settings: Settings) -> None:
        """Initialisation function of edge class"""
        if type(weight) != int:
            raise BaseException("Entered wrong type for weight")
        if any(type(n) != Node for n in [start_node, end_node]):
            raise BaseException("Entered wrong type for nodes")
        # Create instance variables
        self.A = start_node
        self.B = end_node
        self.weight = weight
        self.colour = Colour(0, 0, 0)
        self.show_weight = False
        self.settings = settings

        # Constants
        self.WIDTH = 10
        self.TEXT_COLOUR = Colour(0, 0, 0)
        self.TEXT_BG = Colour(0, 0, 1)
        self.FONT = pygame.font.SysFont(self.settings.font, 15)

    def highlight(self) -> None:
        """Function to highlight the edge"""
        # Increase brightness by 50%
        self.colour.v = self.colour.v + 0.5

    def unhighlight(self) -> None:
        """Function to unhighlight the edge"""
        # Decrease brightness by 50%
        self.colour.v = self.colour.v - 0.5

    def on_hover(self, mouse_pos: tuple[int, int]) -> bool:
        """Check whether the edge is hovered over"""
        # Get mouse position
        x, y = mouse_pos

        # Set it such that A is vertically below A
        if self.A.y < self.B.y:
            A = self.A
            B = self.B
        elif self.A.y > self.B.y:
            A = self.B
            B = self.A
        else:
            # If A and B are level, make A the left-most node
            if self.A.x < self.B.x:
                A = self.A
                B = self.B
            else:
                A = self.B
                B = self.A

        if self.A.y == self.B.y:
            # Handle edge case where nodes are horizontally aligned
            if abs(y - A.y) <= self.WIDTH / 2 and A.x <= x <= B.x:
                self.show_weight = True
                return True

        elif A.x == B.x:
            # Handle edge case where the nodes are vertically above each other
            if abs(x - A.x) <= self.WIDTH / 2 and A.y <= y <= B.y:
                self.show_weight = True
                return True

        else:
            # Work out the gradient and intercept of the line
            self.m = (A.y-B.y)/(A.x-B.x)
            self.c = A.y-self.m*A.x

            # If mouse is in the bounding box return True
            if (
                (abs(y - self.m*x - self.c) <= (self.WIDTH / 2) * (1 + self.m ** 2)**0.5) and
                (y >= -x/self.m + A.y + A.x/self.m) and
                (y <= -x/self.m + B.y + B.x/self.m)
                ):
                self.show_weight = True
                return True

        self.show_weight = False
        return False
    
    def draw(self, screen: pygame.Surface) -> None:
        """Displays the edge to the screen"""
        # Draw a line to represent the edge
        pygame.draw.line(screen, self.colour.rgb, (self.A.x, self.A.y), (self.B.x, self.B.y), self.WIDTH)

        # Test if showing weight
        if self.show_weight or self.settings.show_weight:
            # IF showing weight render the weight as a surface
            self.render = self.FONT.render(str(self.weight), True, self.TEXT_COLOUR.rgb, self.TEXT_BG.rgb)

            # Blit the text to the screen
            screen.blit(self.render, (
                (self.A.x+self.B.x-self.render.get_width())/2,
                (self.A.y+self.B.y-self.render.get_height())/2))


# Graph class
class Graph:
    """Class to handle graphs"""
    def __init__(self, settings: Union[Settings, None] = None) -> None:
        """Initialisation function of graph class"""
        # Create instance variables
        self.adjacency_lists: dict[Node, dict[Node, Edge]] = {}
        self.current_setting: Union[Node, Edge, None] = None
        self.clicked_node = None

        # Create instance constants
        self.S_HEIGHT = 100
        self.S_WIDTH = 150
        self.S_X = 450
        self.PADDING = 10
        self.NAME_LABEL = guiElements.Label(self.S_X+self.PADDING*2+20, self.PADDING, "Node", 20, settings)
        self.ENTRY_LABEL = guiElements.Label(self.S_X+self.PADDING, 20+2*self.PADDING, "Name: ", 10, settings)
        self.ENTRY = guiElements.Entry(self.S_X+self.PADDING+50, 20+2*self.PADDING, 70, 20, settings)
        self.CLOSE_BUTTON = guiElements.Button(self.S_X+self.PADDING, self.PADDING, 20, 20, "X", settings, "Close menu")
        self.DELETE_BUTTON = guiElements.Button(self.S_X+self.PADDING, self.PADDING*3+40, 50, 20, "Delete", settings, "Delete Node/Edge")
        self.settings = settings

    def add_node(self, mouse_pos: tuple[int, int]) -> None:
        """Adds node to the graph"""
        # Create a new node
        new_node = Node(*mouse_pos, f"NewNode{len(self.adjacency_lists)}", self.settings)

        # Update the adjacency list with the new node
        self.adjacency_lists.update({new_node: {}})

    def add_edge(self, start_node: Node, end_node: Node) -> None:
        """Adds an edge to the graph"""
        # Create a new edge
        edge = Edge(start_node, end_node, 0, self.settings)

        # Update adjacency list for both start and end node
        self.adjacency_lists[start_node].update({end_node: edge})
        self.adjacency_lists[end_node].update({start_node: edge})

    def delete_edge(self, edge: Edge) -> None:
        """Removes edge from graph"""
        # Loop through the adjacency list
        for (node, a_list) in self.adjacency_lists.items():
            # For each pair, if the edge is not the one being
            # removed add it to the copt
            l_copy = {}
            for (k, v) in a_list.items():
                if v != edge:
                    l_copy.update({k: v})
            
            # Replace the list with the edge removed
            self.adjacency_lists[node] = l_copy
    
    def delete_node(self, node: Node) -> None:
        """Removes node from graph"""
        # Iterate through adjacency list
        copy = {}
        for (k,v) in self.adjacency_lists.items():
            # Check if node referenced is not node to be deleted
            if k != node:
                # Iterate through inner dictionary
                adjacent = {}
                for (a_node, edge) in v.items():
                    # Check that node is not node to be deleted
                    if a_node != node:
                        adjacent.update({a_node: edge})
                    else:
                        # If it is node to be deleted, delete any connected edges
                        self.delete_edge(edge)
            
                copy.update({k:adjacent})
        
        # Update adjacency list
        self.adjacency_lists = copy

        if self.clicked_node == node:
            self.clicked_node = None

    def open_menu(self, item: Union[Node, Edge]) -> None:
        """Opens menu for graph element"""
        # Set current setting to set item
        self.current_setting = item

        # Check type of item
        if type(item) == Node:
            # If item is a node, update label and entry to match
            self.NAME_LABEL.text = "Node"
            self.ENTRY_LABEL.text = "Name: "
            self.ENTRY.set_label(item.name)
        else:
            # If item is an edge, update label entry to match
            self.NAME_LABEL.text = "Edge"
            self.ENTRY_LABEL.text = "Weight: "
            self.ENTRY.set_label(str(item.weight))

        # Set entry to be autoselected
        self.ENTRY.typing = True
        self.ENTRY.highlight()

    def draw(self, mouse_pos: tuple[int, int], screen: pygame.Surface) -> None:
        """Display graph to screen"""
        # Draw all nodes and edges
        for edge in self.edges:
            edge.draw(screen)

        if self.clicked_node is not None:
            pygame.draw.line(
                screen, (0, 0, 0),
                (self.clicked_node.x, self.clicked_node.y),
                (mouse_pos[0], mouse_pos[1]), 10)

        for node in self.nodes:
            node.draw(screen)

        # Check if setting are open
        if self.current_setting:
            # Draw box for settings to be in
            pygame.draw.rect(screen, [0, 0, 0], [self.S_X, 0, self.S_WIDTH, self.S_HEIGHT])
            pygame.draw.rect(screen, [255, 255, 255], [
                self.S_X+self.PADDING//2, 0, self.S_WIDTH-self.PADDING//2, self.S_HEIGHT-self.PADDING//2
                ])

            # Draw each of the elements of the settings
            self.ENTRY.draw(screen)
            self.CLOSE_BUTTON.draw(screen)
            self.DELETE_BUTTON.draw(screen)
            self.NAME_LABEL.draw(screen)
            self.ENTRY_LABEL.draw(screen)

    def run_mouse(
        self, mouse_pos: tuple[int, int],
        mouse_state: tuple[bool, bool, bool],
        left_state: bool
        ) -> int:
        # Check is settings open
        self.over_menu = False
        if self.current_setting:
            # Check if any elements are clicked
            if self.ENTRY.on_click(mouse_pos, mouse_state):
                self.settings.mouse_function = "Entry"

            if self.CLOSE_BUTTON.on_click(mouse_pos, mouse_state):
                self.current_setting = None

                self.settings.mouse_function = "Close"

            if self.DELETE_BUTTON.on_click(mouse_pos, mouse_state):
                # Delete the node/edge by running the function
                if type(self.current_setting) == Edge:
                    self.delete_edge(self.current_setting)
                    self.current_setting = None
                else:
                    self.delete_node(self.current_setting)
                    self.current_setting = None

                self.settings.mouse_function = "Delete"
            
            # Check if mouse over settings box
            x, y = mouse_pos

            if x > self.S_X and y < self.S_HEIGHT:
                self.over_menu = True
        
        # Check if any nodes clicked
        if any([node.on_hover(mouse_pos) for node in self.nodes]):
            dragged = False
            for node in self.nodes:
                if node.on_hover(mouse_pos):
                    if mouse_state[0] and self.settings.mouse_function is None:
                        if self.settings.start_algorithm is not None:
                            if self.settings.start_algorithm == "Dijkstras":
                                if self.settings.start_node is None:
                                    self.settings.start_node = node
                                    self.settings.help_label.text = "Click node to select end node"
                                    node.highlight()
                                elif self.settings.start_node != node:
                                    self.settings.cur_algorithm = Dijkstras(self.copy(), self.settings.start_node, node)
                                    self.settings.start_algorithm = None
                                    self.settings.start_node = None
                                    self.settings.help_label.text = ""
                            elif self.settings.start_algorithm == "Prims":
                                self.settings.cur_algorithm = Prims(node, self.copy())
                                self.settings.start_algorithm = None
                                self.settings.help_label.text = ""
                                node.highlight()
                        else:
                            self.open_menu(node)
                        self.settings.mouse_function = "Node"
                    elif mouse_state[1]:
                        if self.clicked_node is not None and self.clicked_node != node:
                            self.add_edge(self.clicked_node, node)
                            self.clicked_node = None
                        else:
                            self.clicked_node = node
                    elif left_state and not dragged:
                        node.x, node.y = mouse_pos
                        dragged = True
                        self.settings.mouse_function = "drag"

        # Check if any edges clicked
        elif any([edge.on_hover(mouse_pos) for edge in self.edges]):
            for edge in self.edges:
                if edge.on_hover(mouse_pos) and mouse_state[0] and self.settings.mouse_function is None:
                    self.open_menu(edge)
                    self.settings.mouse_function = "Edge"

        if self.settings.mouse_function is None and not self.over_menu and mouse_state[0]:
            self.add_node(mouse_pos)

        if mouse_state[1] and self.clicked_node is not None and not any([node.on_hover(mouse_pos) for node in self.nodes]):
            self.clicked_node = None

    def run_keys(self, pressed_keys: list[str]) -> None:
        """Function to run keyboard events for graph"""
        # Check if settings open
        if self.current_setting:
            if self.ENTRY.typing and "enter" in pressed_keys:
                self.current_setting = None
                return

            # Update entry contents
            val = self.ENTRY.get_input(pressed_keys)

            # Check if typing
            if val is not None:
                # Check type of current settings
                if type(self.current_setting) == Node:
                    # Update node name corresponding
                    self.current_setting.name = val
                else:
                    # Check input is a number
                    if val.isnumeric():
                        # Update edge weight corresponding
                        self.current_setting.weight = int(val)
        

    def copy(self):
        """Returns a copy of the graph"""
        # Create a new graph
        g = Graph(self.settings)

        # Make the adjacency list a copy of this instance's list
        g.adjacency_lists = self.adjacency_lists.copy()

        # Return the graph
        return g

    @property
    def nodes(self) -> list[Node]:
        return [*self.adjacency_lists.keys()]

    @property
    def edges(self) -> list[Edge]:
        # Get every edge
        edges = []
        for val in self.adjacency_lists.values():
            if val != {}:
                for (_, e) in val.items():
                    edges.append(e)

        # Return the edges
        return [*set(edges)]    

    def save_graph(self, file_name: str) -> None:
        """Function to save graphs"""
        if set("\/:*?\"<>|").intersection(set(file_name)) is not None:
            return "Error"
            
        # Get the graph adjacency list
        adjacency_list = self.adjacency_lists

        # Give each node and edge a name
        nodes = dict([(node, f"node{i}") for i, node in enumerate(self.nodes)])
        edges = dict([(edge, f"edge{i}") for i, edge in enumerate(self.edges)])

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

    def load_graph(self, file_name: str) -> None:
        """Function to load a graph"""
        # Open the given file
        if not os.path.exists(f"graphs//{file_name}.json"):
            return "Error"
        
        with open(f"graphs/{file_name}.json") as f:
            content = f.read()

        # Convert from json format to a dictionary
        graph = json.loads(content)['info']

        # Get all the nodes
        nodes = graph['nodes']

        # Create a new node for each node in the file
        new_nodes = {}
        for (name, info) in nodes.items():
            new_nodes.update({name: Node(*info['pos'], info['name'], self.settings)})

        # Get all the edges
        edges = graph['edges']

        # Create a new edge for each edge in the file
        new_edges = {}
        for (name, info) in edges.items():
            new_edges.update({name: Edge(new_nodes[info['start_node']], new_nodes[info['end_node']], info['weight'], self.settings)})

        # Translate the string version of the adjacency list to hold classes
        old_adj_list = graph['adjacency_list']
        translated_list = {}
        for (node, adj_list) in old_adj_list.items():
            inner_list = {}
            for (c_node, edge) in adj_list.items():
                inner_list.update({new_nodes[c_node]:new_edges[edge]})
            translated_list.update({new_nodes[node]:inner_list})

        # Swap out the graph adjacency list
        self.adjacency_lists = translated_list