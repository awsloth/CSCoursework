import pygame
from pygame.math import enable_swizzling

pygame.font.init()

class Button:
    def __init__(self, x_pos, y_pos, width, height, text):
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.text = text

        self.font = pygame.font.SysFont("Helvetica", 10)
        self.text = self.font.render(self.text, True, (0, 0, 0))

    def draw(self, screen: pygame.Surface):

        # Draw a white rectangle for the button background
        pygame.draw.rect(screen, (255, 255, 255), ((self.x + 2, self.y + 2, self.width - 4, self.height - 4)))
        
        # Display the text in the centre of the button
        screen.blit(self.text, (self.x + (self.width - self.text.get_width()) / 2, self.y + (self.height - self.text.get_height()) / 2))

        # Draw a hollow black rectangle with border 5
        pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height), 5)

    def on_hover(self, mouse_pos):
        # Unwrap mouse position from list to two variables
        mouse_x, mouse_y = mouse_pos

        # If mouse pos in box return True, else False
        if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
            return True
        else:
            return False

    def on_click(self, mouse_pos, mouse_state):
        # Get left mouse button state
        click = mouse_state[0]

        # If hovering and clicked with left mouse button return True, else False
        if self.on_hover(mouse_pos) and click:
            return True
        else:
            return False
