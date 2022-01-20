# Import libraries
import pygame
import sys

import guiElements
import graph

# Main function of the interface program
def gui(screen):
    screen.fill((255, 255, 255))

# Only run if this program is the main one being run
if __name__ == "__main__":

    # Create a window to display elements on
    screen = pygame.display.set_mode((500, 500))

    clock = pygame.time.Clock()

    button = guiElements.Button(10, 20, 30, 40, "Button")

    nodes = [graph.Node(100, 400, "Alice"), graph.Node(200, 300, "Bob")]

    edges = [graph.Edge(nodes[0], nodes[1], 1)]

    created_node = False

    selected_node = False
    clicked_node = None

    # Loop forever
    while 1:
        clock.tick(60)

        # Get each window event
        for event in pygame.event.get():

            # If the window event is a quit type exit the GUI
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Run the main function
        gui(screen)

        button.draw(screen)

        for edge in edges:
            edge.draw(screen)

        for node in nodes:
            node.draw(screen)

        if pygame.mouse.get_pressed()[0] and not created_node:
            if button.on_click(pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
                # Do button function
                ...
            elif any([node.on_hover(pygame.mouse.get_pos()) for node in nodes]):
                # Edit node settings
                ...
            elif any([edge.on_hover(pygame.mouse.get_pos()) for edge in edges]):
                print("Edge clicked")
                ...
            else:
                # Create node
                nodes.append(graph.Node(*pygame.mouse.get_pos(), f"NewNode{len(nodes)}"))
                created_node = True

        elif not pygame.mouse.get_pressed()[0] and created_node:
            created_node = False

        if pygame.mouse.get_pressed()[2] and not selected_node:
            for node in nodes:
                if node.on_hover(pygame.mouse.get_pos()):
                    if clicked_node is not None:
                        edges.append(graph.Edge(clicked_node, node, len(edges)+1))
                        clicked_node = None
                        selected_node = True
                    else:
                        clicked_node = node
                        selected_node = True
                        print(f"Selected {node.name}")
            
        elif not pygame.mouse.get_pressed()[2] and selected_node:
            selected_node = False  

        # Update the window
        pygame.display.update()