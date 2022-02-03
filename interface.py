# Import libraries
import pygame
import sys

from pygame.locals import *

import guiElements
from graph import Graph
from algorithms import Prims

# Main function of the interface program
def gui(screen):
    screen.fill((255, 255, 255))

# Only run if this program is the main one being run
if __name__ == "__main__":

    # Create a window to display elements on
    screen = pygame.display.set_mode((600, 500))

    # Clock to handle fps
    clock = pygame.time.Clock()

    # Buttons for interface
    buttons = [guiElements.Button(10, 20, 30, 40, "Button")]

    entries = [guiElements.EntryBox(10, 100, 40, 30)]

    labels = [guiElements.Label(50, 60, "Hello!", 30)]

    # Graph Data Structure
    graph = Graph()

    # Clicking variable
    clicked_node = None

    wait = 1
    WAIT_AMOUNT = 6

    # Loop forever
    while 1:
        # Set fps to 60
        clock.tick(60)
        pressed_keys = []

        wait -= 1
        left_down = False
        right_down = False

        if pygame.key.get_pressed()[K_BACKSPACE] and wait <= 0:
            pressed_keys.append("back")
            wait = WAIT_AMOUNT

        # Get each window event
        for event in pygame.event.get():

            # If the window event is a quit type exit the GUI
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key != K_BACKSPACE:
                    pressed_keys.append(event.unicode)

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    left_down = True
                elif event.button == 3:
                    right_down = True

        # Run the main function
        gui(screen)

        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()
        mouse_state = pygame.mouse.get_pressed()

        # Draw and detect hovers for each button
        for button in buttons:
            button.draw(screen)
            button.on_hover(mouse_pos)

        for entry in entries:
            entry.draw(screen)
            entry.on_hover(mouse_pos)
            entry.get_input(pressed_keys)
            entry.on_click(mouse_pos, mouse_state)
        
        for label in labels:
            label.draw(screen)

        # Draw and detect hovers for each edge
        for edge in graph.edges:
            edge.draw(screen)
            edge.on_hover(mouse_pos)

        # Draw and detect hovers for each node
        for node in graph.nodes:
            node.draw(screen)
            node.on_hover(mouse_pos)

        graph.draw(screen)
        action = graph.run(mouse_pos, mouse_state, pressed_keys)

        if left_down and not action:
            if any([button.on_click(mouse_pos, mouse_state) for button in buttons]):
                # Do button function
                ...
            elif any([entry.on_click(mouse_pos, mouse_state) for entry in entries]):
                # Do something with entries?
                ...
            elif any([node.on_hover(mouse_pos) for node in graph.nodes]):
                # Edit node settings
                for node in graph.nodes:
                    if node.on_hover(mouse_pos):
                        graph.open_menu(node)
            elif any([edge.on_hover(mouse_pos) for edge in graph.edges]):
                # Edit edge settings
                for edge in graph.edges:
                    if edge.on_hover(mouse_pos):
                        graph.open_menu(edge)
            else:
                # Create node
                graph.add_node(mouse_pos)

        if right_down:
            # For edges only
            if clicked_node not in graph.nodes:
                clicked_node = None

            for node in graph.nodes:
                if node.on_hover(mouse_pos):
                    if clicked_node is not None:
                        if clicked_node is not node:
                            graph.add_edge(clicked_node, node)
                        clicked_node = None
                    else:
                        clicked_node = node

        # Update the window
        pygame.display.update()