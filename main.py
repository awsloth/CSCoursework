# Import libraries
import pygame
import sys

from pygame.locals import *

from graph import Graph
from settings import Settings
from interface import Interface

# Create a window to display elements on
screen = pygame.display.set_mode((600, 500), RESIZABLE)

settings = Settings(600, 500)
interface = Interface(settings)
graph = Graph(settings)

# Clock to handle fps
clock = pygame.time.Clock()

l_wait = 0
CLICK_WAIT = 12
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
            # Save settings on exit
            with open("config.txt", "r") as f:
                lines = f.readlines()

            with open("config.txt", "w") as f:
                for line in lines:
                    print(line)
                    start, change = line.split(":")
                    if start == "font":
                        change = settings.font+"\n"
                    elif start == "show_names":
                        change = str(settings.show_names)+"\n"
                    elif start == "show_weights":
                        change = settings.show_weight
                    print(f"{start}:{change}", end="", file=f)
            
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN and event.key not in [K_BACKSPACE, K_RETURN]:
                pressed_keys.append(event.unicode)

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                l_wait = CLICK_WAIT
            elif event.button == 3:
                right_down = True
                settings.mouse_function = None

        if event.type == MOUSEBUTTONUP:
            settings.mouse_function = None

        if event.type == VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), RESIZABLE)
    
    # Clear screen
    screen.fill((255, 255, 255))

    # Get the mouse position
    mouse_pos = pygame.mouse.get_pos()
    mouse_state = [left_down, right_down]

    # Draw interface and graph
    interface.draw(screen)
    graph.draw(mouse_pos, screen)

    # Run interface and graph
    interface.run_mouse(mouse_pos, mouse_state, graph)
    graph.run_mouse(mouse_pos, mouse_state, pygame.mouse.get_pressed()[0])

    interface.run_keys(pressed_keys)
    graph.run_keys(pressed_keys)

    # Update the window
    pygame.display.update()
