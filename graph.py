import pygame

pygame.font.init()

class Node:
    def __init__(self, x: int, y: int, name: str):
        # Entered variables
        self.x = x
        self.y = y
        self.name = name

        # Constants
        self.colour = [255, 0, 0]
        self.radius = 10
        self.text_colour = [0, 0, 0]
        self.text_bg = [255, 255, 255]
        self.font = pygame.font.SysFont("Helvetica", 10)

        # Variables
        self.show_name = False

    def neighbours(self):
        # List all neighbour nodes
        ...

    def dist_to_node(self, node):
        # Dist to node, if not connected then None
        ...

    def on_hover(self, mouse_pos):
        # Get mouse x and y
        x, y = mouse_pos

        # If mouse in surrounding circle, then return True and show name
        if (x-self.x)**2 + (y-self.y)**2 <= self.radius**2:
            self.show_name = True
            return True

        # If mouse not on node hide name (Add feature to have names always on?)
        self.show_name = False

    def draw(self, screen: pygame.Surface):
        # Draw circle for node
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)

        # If showing the name
        if self.show_name:

            # Render name as text
            self.render = self.font.render(self.name, True, self.text_colour, self.text_bg)

            # Display text to screen
            screen.blit(
                self.render, (self.x-self.render.get_width()/2,
                self.y-self.radius-self.render.get_height())
                )

class Edge:
    def __init__(self, start_node: Node, end_node: Node, weight: int):
        # Entered variables
        self.A = start_node
        self.B = end_node
        self.weight = weight

        # Constants
        self.colour = [0, 0, 0]
        self.width = 10
        self.text_colour = [0, 0, 0]
        self.text_bg = [255, 255, 255]
        self.font = pygame.font.SysFont("Helvetica", 15)

        # Variables
        self.show_weight = False


    def on_hover(self, mouse_pos):
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
            if abs(y - A.y) <= self.width / 2 and A.x <= x <= B.x:
                self.show_weight = True
                return True

        elif A.x == B.x:
            # Handle edge case where the nodes are vertically above each other
            if abs(x - A.x) <= self.width / 2 and A.y <= y <= B.y:
                self.show_weight = True
                return True

        else:
            # Work out the gradient and intercept of the line
            self.m = (A.y-B.y)/(A.x-B.x)
            self.c = A.y-self.m*A.x

            # If mouse is in the bounding box return True
            if (
                (abs(y - self.m*x - self.c) <= (self.width / 2) * (1 + self.m ** 2)**0.5) and
                (y >= -x/self.m + A.y + A.x/self.m) and
                (y <= -x/self.m + B.y + B.x/self.m)
                ):
                self.show_weight = True
                return True

        self.show_weight = False
    
    def draw(self, screen):
        # Draw a line to represent the edge
        pygame.draw.line(screen, self.colour, (self.A.x, self.A.y), (self.B.x, self.B.y), self.width)

        if self.show_weight:
            self.render = self.font.render(str(self.weight), True, self.text_colour, self.text_bg)

            screen.blit(self.render, (
                (self.A.x+self.B.x-self.render.get_width())/2,
                (self.A.y+self.B.y-self.render.get_height())/2))


class Graph:
    def __init__(self):
        self.graph = {}

    def add_node(self, mouse_pos):
        new_node = Node(*mouse_pos, f"NewNode{len(self.graph)}")
        self.graph.update({new_node: {}})

    def add_edge(self, start_node, end_node):
        edge = Edge(start_node, end_node, 0)
        self.graph[start_node].update({end_node: edge})
        self.graph[end_node].update({start_node: edge})

    def display_graph(self):
        print(*self.graph)

    @property
    def nodes(self) -> list[Node]:
        return self.graph.keys()

    @property
    def edges(self) -> list[Edge]:
        edges = []
        for val in self.graph.values():
            if val != {}:
                for (_, e) in val.items():
                    edges.append(e)

        return [*set(edges)]    
