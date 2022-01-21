# Import libraries
import pygame
import sys

import guiElements
from graph import Graph

# Main function of the interface program
def gui(screen):
    screen.fill((255, 255, 255))

# Only run if this program is the main one being run
if __name__ == "__main__":

    # Create a window to display elements on
    screen = pygame.display.set_mode((500, 500))

    # Clock to handle fps
    clock = pygame.time.Clock()

    # Buttons for interface
    buttons = [guiElements.Button(10, 20, 30, 40, "Button")]

    # Graph Data Structure
    graph = Graph()

    # Clicking variables
    created_node = False
    selected_node = False
    clicked_node = None

    # Loop forever
    while 1:
        # Set fps to 60
        clock.tick(60)

        # Get each window event
        for event in pygame.event.get():

            # If the window event is a quit type exit the GUI
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Run the main function
        gui(screen)

        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw and detect hovers for each button
        for button in buttons:
            button.draw(screen)
            button.on_hover(mouse_pos)

        # Draw and detect hovers for each edge
        for edge in graph.edges:
            edge.draw(screen)
            edge.on_hover(mouse_pos)

        # Draw and detect hovers for each node
        for node in graph.nodes:
            node.draw(screen)
            node.on_hover(mouse_pos)

        if pygame.mouse.get_pressed()[0] and not created_node:
            if any([button.on_click(mouse_pos, pygame.mouse.get_pressed()) for button in buttons]):
                # Do button function
                ...
            elif any([node.on_hover(mouse_pos) for node in graph.nodes]):
                # Edit node settings
                ...
            elif any([edge.on_hover(mouse_pos) for edge in graph.edges]):
                # Edit edge settings
                ...
            else:
                # Create node
                graph.add_node(mouse_pos)
                created_node = True

        elif not pygame.mouse.get_pressed()[0] and created_node:
            created_node = False

        if pygame.mouse.get_pressed()[2] and not selected_node:
            # For edges only
            for node in graph.nodes:
                if node.on_hover(mouse_pos):
                    if clicked_node is not None:
                        if clicked_node is not node:
                            graph.add_edge(clicked_node, node)
                        clicked_node = None
                        selected_node = True
                    else:
                        clicked_node = node
                        selected_node = True
            
        elif not pygame.mouse.get_pressed()[2] and selected_node:
            selected_node = False  

        # Update the window
        pygame.display.update()