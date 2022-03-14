# Import base libraries
import pygame
from typing import Union

# Import custom scripts
import guiElements
from colour import Colour

# Initialise the python font library
pygame.font.init()

def wordFilter(word):
    ...

class Node:
    """Class to handle nodes"""
    def __init__(self, x: Union[int, float], y: Union[int, float], name: str) -> None:
        """Initialisation function of node class"""
        # Check that arguments are of correct type
        if any([type(v) not in [int, float] for v in [x, y]]):
            raise BaseException("Entered wrong type")
        if type(name) != str:
            raise BaseException("Entered wrong type for name")

        # Create instance variables
        self.x = x
        self.y = y
        self.name = name
        self.show_name = False
        self.colour = Colour(0, 1, 1)

        # Create instance constants
        self.RADIUS = 10
        self.TEXT_COLOUR = Colour(0, 0, 0)
        self.TEXT_BG = Colour(0, 0, 1)
        self.FONT = pygame.font.SysFont("Helvetica", 10)

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
        if self.show_name:

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
    def __init__(self, start_node: Node, end_node: Node, weight: int) -> None:
        """Initialisation function of edge class"""
        if type(weight) != int:
            raise BaseException("Entered wrong type for weight")
        # Create instance variables
        self.A = start_node
        self.B = end_node
        self.weight = weight
        self.colour = Colour(0, 0, 0)
        self.show_weight = False

        # Constants
        self.WIDTH = 10
        self.TEXT_COLOUR = Colour(0, 0, 0)
        self.TEXT_BG = Colour(0, 0, 1)
        self.FONT = pygame.font.SysFont("Helvetica", 15)

    def highlight(self) -> None:
        """Function to highlight the edge"""
        # Increase brightness by 50%
        self.colour.v = self.colour.v + 0.5

    def unhighlight(self) -> None:
        """Function to unhighlight the edge"""
        # Decrease brightness by 50%
        self.colour.v = self.colour.v - 0.5

    def on_hover(self, mouse_pos) -> bool:
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
        if self.show_weight:
            # IF showing weight render the weight as a surface
            self.render = self.FONT.render(str(self.weight), True, self.TEXT_COLOUR.rgb, self.TEXT_BG.rgb)

            # Blit the text to the screen
            screen.blit(self.render, (
                (self.A.x+self.B.x-self.render.get_width())/2,
                (self.A.y+self.B.y-self.render.get_height())/2))


# Graph class
class Graph:
    """Class to handle graphs"""
    def __init__(self) -> None:
        """Initialisation function of graph class"""
        # Create instance variables
        self.adjacency_lists: dict[Node, dict[Node, Edge]] = {}
        self.current_setting: Union[Node, Edge, None] = None

        # Create instance constants
        self.S_HEIGHT = 100
        self.S_WIDTH = 150
        self.S_X = 450
        self.PADDING = 10
        self.NAME_LABEL = guiElements.Label(self.S_X+self.PADDING*2+20, self.PADDING, "Node", 20)
        self.ENTRY_LABEL = guiElements.Label(self.S_X+self.PADDING, 20+2*self.PADDING, "Name: ", 10)
        self.ENTRY = guiElements.EntryBox(self.S_X+self.PADDING+50, 20+2*self.PADDING, 70, 20)
        self.CLOSE_BUTTON = guiElements.Button(self.S_X+self.PADDING, self.PADDING, 20, 20, "X")
        self.DELETE_BUTTON = guiElements.Button(self.S_X+self.PADDING, self.PADDING*3+40, 50, 20, "Delete")

    def add_node(self, mouse_pos: tuple[int, int]) -> None:
        """Adds node to the graph"""
        # Create a new node
        new_node = Node(*mouse_pos, f"NewNode{len(self.adjacency_lists)}")

        # Update the adjacency list with the new node
        self.adjacency_lists.update({new_node: {}})

    def add_edge(self, start_node: Node, end_node: Node) -> None:
        """Adds an edge to the graph"""
        # Create a new edge
        edge = Edge(start_node, end_node, 0)

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

    def draw(self, screen: pygame.Surface) -> None:
        """Display graph to screen"""
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
        mouse_state: tuple[int, int, int]
        ) -> int:
        # Check is settings open
        if self.current_setting:
            # Check if any elements are clicked
            if self.ENTRY.on_click(mouse_pos, mouse_state):
                return 1

            if self.CLOSE_BUTTON.on_click(mouse_pos, mouse_state):
                self.current_setting = None
                return 1

            if self.DELETE_BUTTON.on_click(mouse_pos, mouse_state):
                # Delete the node/edge by running the function
                if type(self.current_setting) == Edge:
                    self.delete_edge(self.current_setting)
                    self.current_setting = None
                else:
                    self.delete_node(self.current_setting)
                    self.current_setting = None

                return 1
            
            # Check if mouse over
            x, y = mouse_pos

            if x > self.S_X and y < self.S_HEIGHT:
                return 2

    def run_keys(self, pressed_keys: list[str]) -> None:
        """Function to run keyboard events for graph"""
        # Check if settings open
        if self.current_setting:
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
        g = Graph()

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
