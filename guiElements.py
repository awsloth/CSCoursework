import pygame

pygame.font.init()

allowed_chars = "!\"$%^&*()_+-=qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.<>[]{};';@#~/?1234567890"

class Button:
    def __init__(self, x_pos, y_pos, width, height, text):
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.label = text


        self.colour = [255, 255, 255]
        self.border_colour = [0, 0, 0]
        self.font = pygame.font.SysFont("Helvetica", 10)
        self.text = self.font.render(self.label, True, (0, 0, 0))

    def draw(self, screen: pygame.Surface):

        # Draw a white rectangle for the button background
        pygame.draw.rect(screen, self.colour, ((self.x + 2, self.y + 2, self.width - 4, self.height - 4)))
        
        # Display the text in the centre of the button
        screen.blit(self.text, (self.x + (self.width - self.text.get_width()) / 2, self.y + (self.height - self.text.get_height()) / 2))

        # Draw a hollow black rectangle with border 5
        pygame.draw.rect(screen, self.border_colour, (self.x, self.y, self.width, self.height), 5)

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

class EntryBox(Button):
    def __init__(self, x_pos, y_pos, width, height):
        super().__init__(x_pos, y_pos, width, height, "")
        self.typing = False

    def draw(self, screen: pygame.Surface):
        # Rerender text
        self.text = self.font.render(self.label, True, (0, 0, 0))

        # Draw a white rectangle for the button background
        pygame.draw.rect(screen, self.colour, ((self.x + 2, self.y + 2, self.width - 4, self.height - 4)))
        
        # Display the text in the centre of the button
        screen.blit(self.text, (self.x + 3, self.y + (self.height - self.text.get_height()) / 2))

        # Draw a hollow black rectangle with border 5
        pygame.draw.rect(screen, self.border_colour, (self.x, self.y, self.width, self.height), 5)

    def on_click(self, mouse_pos, mouse_state):
        # Get left mouse button state
        click = mouse_state[0]

        # If hovering and clicked with left mouse button return True, else False
        if self.on_hover(mouse_pos) and click:
            # Set so typing and change bg colour to show
            if not self.typing:
                # Changes the colour only once
                self.colour = [val*0.8 for val in self.colour]
            self.typing = True
            return True
        elif click:
            # Set so not typing and change bg colour back to show
            if self.typing:
                # Changes the colour only once
                self.colour = [val/0.8 for val in self.colour]
            self.typing = False

    def get_input(self, pressed_keys):
        if self.typing:
            # For every pressed key, add the pressed key or remove on backspace
            for key in pressed_keys:
                if key == "back":
                    if self.label != "":
                        self.label = self.label[:-1]
                else:
                    if key in allowed_chars:
                        self.label += key

            return self.label

    def set_label(self, val):
        self.label = val

class Label:
    def __init__(self, x, y, text, size):
        self.x = x
        self.y = y
        self._text = text
        self.size = size

        self.text_colour = [0, 0, 0]
        self.font = pygame.font.SysFont("Helvetica", size)

    def draw(self, screen: pygame.Surface):
        self.render = self.font.render(self._text, True, self.text_colour)

        screen.blit(self.render, (self.x, self.y))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text