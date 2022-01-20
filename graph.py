import pygame

class Graph:
    def __init__(self):
        ...

    def add_node(self, x, y, adjacency_list=None):
        # Create new Node and add edges if adjacency list provided
        ...

    def remove_node(self, node):
        # Remove node node and connecting edges
        ...


class Node:
    def __init__(self, x: int, y: int, name: str):
        self.x = x
        self.y = y
        self.name = name

        self.colour = [255, 0, 0]
        self.radius = 10

    def neighbours(self):
        # List all neighbour nodes
        ...

    def dist_to_node(self, node):
        # Dist to node, if not connected then None
        ...

    def on_hover(self, mouse_pos):
        x, y = mouse_pos
        if (x-self.x)**2 + (y-self.y)**2 <= self.radius**2:
            return True

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)

class Edge:
    def __init__(self, start_node: Node, end_node: Node, weight: int):
        self.A = start_node
        self.B = end_node

        self.weight = weight
        self.colour = [0, 0, 0]
        self.width = 10

    def on_hover(self, mouse_pos):
        x, y = mouse_pos

        if self.A.y < self.B.y:
            A = self.A
            B = self.B
        elif self.A.y > self.B.y:
            A = self.B
            B = self.A
        else:
            if self.A.x < self.B.x:
                A = self.A
                B = self.B
            else:
                A = self.B
                B = self.A

            if abs(y - A.y) <= self.width / 2 and A.x <= x <= B.x:
                return True
            else:
                return False


        if A.x == B.x:
            if abs(x - A.x) <= self.width / 2 and A.y <= y <= B.y:
                return True
            else:
                return False
    
        self.m = (A.y-B.y)/(A.x-B.x)
        self.c = A.y-self.m*A.x

        if (
            (abs(y - self.m*x - self.c) <= (self.width / 2) * (1 + self.m ** 2)**0.5) and
            (y >= -x/self.m + A.y + A.x/self.m) and
            (y <= -x/self.m + B.y + B.x/self.m)
        ):
            return True

        return False

    def draw(self, screen):
        pygame.draw.line(screen, self.colour, (self.A.x, self.A.y), (self.B.x, self.B.y), self.width)
