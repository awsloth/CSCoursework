# Import libraries
import pygame
import sys

from pygame.locals import *

from graph import Graph
from algorithms import Dijkstras, Kruskals, Prims
from guiElements import Button, Label
from settings import Settings

# Main function of the interface program
def gui(screen):
    screen.fill((255, 255, 255))

# Only run if this program is the main one being run
if __name__ == "__main__":

    # Create a window to display elements on
    screen = pygame.display.set_mode((600, 500), RESIZABLE)
    
    global_settings = Settings(600, 500)

    # Clock to handle fps
    clock = pygame.time.Clock()

    # Graph Data Structure
    graph = Graph()

    buttons = [
        Button(10, 480, 40, 20, "Dijkstras"),
        Button(60, 480, 40, 20, "Prims"),
        Button(110, 480, 40, 20, "Kruskals"),
        Button(160, 480, 40, 20, "Next"),
        Button(210, 480, 40, 20, "Prev")
        ]

    entries = []
    

    # Clicking variable
    clicked_node = None
    mouse_function = None

    help_text = Label(5, 5, "", 20)

    l_wait = 0
    CLICK_WAIT = 12
    wait = 1
    WAIT_AMOUNT = 6
    cur_algorithm = None
    start_algorithm = None
    start_node = None

    # Loop forever
    while 1:
        # Set fps to 60
        clock.tick(60)
        pressed_keys = []

        wait -= 1
        left_down = False
        right_down = False

        if (l_wait - 1):
            l_wait -= 1

        if l_wait == 1:
            left_down = True
            l_wait = 0


        if pygame.key.get_pressed()[K_BACKSPACE] and wait <= 0:
            pressed_keys.append("back")
            wait = WAIT_AMOUNT

        if pygame.key.get_pressed()[K_RETURN]:
            pressed_keys.append("enter")

        # Get each window event
        for event in pygame.event.get():

            # If the window event is a quit type exit the GUI
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key not in [K_BACKSPACE, K_RETURN]:
                    pressed_keys.append(event.unicode)

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    l_wait = CLICK_WAIT
                elif event.button == 3:
                    right_down = True

            if event.type == MOUSEBUTTONUP:
                mouse_function = None

            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)

        # Run the main function
        gui(screen)

        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()
        mouse_state = [*pygame.mouse.get_pressed()]
        mouse_state[0] = left_down

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

        help_text.draw(screen)

        if type(cur_algorithm) == Dijkstras:
                for box in cur_algorithm.boxes.values():
                    box.draw(screen)

        graph.draw(screen)

        if mouse_function is None:
            action = graph.run_mouse(mouse_pos, mouse_state)
            if action == 1:
                mouse_function = "graph"

        graph.run_keys(pressed_keys)

        if left_down and not action and mouse_function is None:
            if any([button.on_hover(mouse_pos) for button in buttons]):
                # Do button function
                for button in buttons:
                    if button.on_click(mouse_pos, mouse_state):
                        mouse_function = "button"
                        if button.label in ["Dijkstras", "Prims"]:
                            start_algorithm = button.label
                            help_text.text = "Click node to select start node"
                        elif button.label == "Kruskals":
                            cur_algorithm = Kruskals(graph)
                        elif button.label == "Next":
                            if cur_algorithm is not None:
                                if cur_algorithm.next_step() == "Finished":
                                    cur_algorithm.clear_up()
                                    cur_algorithm = None
                        elif button.label == "Prev":
                            if cur_algorithm is not None:
                                cur_algorithm.prev_step()
            elif any([entry.on_hover(mouse_pos, mouse_state) for entry in entries]):
                # Do something with entries?
                mouse_function = "entry"
            elif any([node.on_hover(mouse_pos) for node in graph.nodes]):
                # Edit node settings
                for node in graph.nodes:
                    if node.on_hover(mouse_pos):
                        if start_algorithm is not None:
                            if start_algorithm == "Dijkstras":
                                if start_node is None:
                                    start_node = node
                                    node.highlight()
                                    help_text.text = "Click node to select end node"
                                elif node != start_node:
                                    cur_algorithm = Dijkstras(graph, start_node, node)
                                    start_node = None
                                    start_algorithm = None
                                    help_text.text = ""
                            else:
                                node.highlight()
                                cur_algorithm = Prims(node, graph)
                                start_algorithm = None
                                help_text.text = ""
                        else:
                            graph.open_menu(node)
                            mouse_function = "node"
            elif any([edge.on_hover(mouse_pos) for edge in graph.edges]):
                # Edit edge settings
                for edge in graph.edges:
                    if edge.on_hover(mouse_pos):
                        graph.open_menu(edge)
                        mouse_function = "edge"
            else:
                # Create node
                graph.add_node(mouse_pos)
        elif not action and pygame.mouse.get_pressed()[0]:
            for node in graph.nodes:
                if node.on_hover(mouse_pos):
                    node.x, node.y = mouse_pos
                    mouse_function = "drag"
                    break

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
