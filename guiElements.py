from __future__ import annotations

# Base libraries
import pygame
from typing import Union

# Custom scripts
from colour import Colour
from typing import Union, TYPE_CHECKING

# Block off for type checking so cyclic import does not occur
if TYPE_CHECKING:
    # Import custom scripts
    from settings import Settings

# Initialise pygame font library for use later
pygame.font.init()

# List of allowed characters to type
allowed_chars = "!\"$%^&*()_+-=qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM,.<>[]{};';@#~/?1234567890"

# Button class
class Button:
    """Class to handle the creation of buttons"""

    def __init__(
        self, x_pos: Union[int, float],
        y_pos: Union[int, float], width: Union[int, float],
        height: Union[int, float], text: Union[str, int, float],
        settings: Settings, tooltip: Union[str, None] = None
        ) -> None:
        # Checks arguments are of the expected types
        if any(type(x) not in [int, float] for x in [x_pos, y_pos, width, height]):
            raise BaseException("Error, invalid type entered to dimensions")
        if type(text) not in [str, int, float]:
            raise BaseException("Error, invalid label type")

        # Create instance variables
        self.x = x_pos
        self.y = y_pos
        self.width = width
        self.height = height
        self.label = text
        self.tooltip = tooltip
        self.settings = settings
        self.colour = Colour(0, 0, 1)
        self.border_colour = Colour(0, 0, 0)
        self.hovered = False

        # Instance constants
        self.FONT = pygame.font.SysFont(self.settings.font, 10)
        self.TEXT = self.FONT.render(str(self.label), True, (0, 0, 0))
        if self.tooltip is not None:
            self.TOOLTIP_TEXT = self.FONT.render(self.tooltip, True, (0, 0, 0), (255, 255, 255))

    def draw(self, screen: pygame.Surface) -> None:
        """Function to draw the button"""

        # Draw a white rectangle for the button background
        pygame.draw.rect(screen, self.colour.rgb, ((self.x + 2, self.y + 2, self.width - 4, self.height - 4)))
        
        # Display the text in the centre of the button
        screen.blit(self.TEXT, (self.x + (self.width - self.TEXT.get_width()) / 2, self.y + (self.height - self.TEXT.get_height()) / 2))

        # Draw a hollow black rectangle with border 5
        pygame.draw.rect(screen, self.border_colour.rgb, (self.x, self.y, self.width, self.height), 5)

        if self.hovered:
            if self.tooltip is not None:
                screen.blit(self.TOOLTIP_TEXT, (self.x, self.y - self.TOOLTIP_TEXT.get_height() - 2))


    def on_hover(self, mouse_pos: tuple[int, int]) -> bool:
        """Function to detect hover"""
        # Unwrap mouse position from list to two variables
        mouse_x, mouse_y = mouse_pos

        # If mouse pos in box return True, else False
        if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
            if not self.hovered:
                self.highlight()
                self.hovered = True
            return True
        else:
            if self.hovered:
                self.unhighlight()
                self.hovered = False
            return False

    def on_click(self, mouse_pos: tuple[int, int], mouse_state: tuple[bool, bool, bool]) -> bool:
        """Function to check click"""
        # Get left mouse button state
        click = mouse_state[0]

        # If hovering and clicked with left mouse button return True, else False
        if self.on_hover(mouse_pos) and click:
            return True
        else:
            return False

    def highlight(self) -> None:
        self.colour.v = self.colour.v - 0.2

    def unhighlight(self) -> None:
        self.colour.v = self.colour.v + 0.2

# Entry box class, inherits from button
class Entry(Button):
    """Class to handle the creation of entry boxes"""
    def __init__(
        self, x_pos: Union[int, float], y_pos: Union[int, float],
        width: Union[int, float], height: Union[int, float],
        settings: Settings, font_size: int = 10
        ) -> None:
        # Run parent initialisation function
        super().__init__(x_pos, y_pos, width, height, "", settings)

        # Create instance variables
        self.typing = False
        self.settings = settings

        self.FONT = pygame.font.SysFont(self.settings.font, font_size)

    def draw(self, screen: pygame.Surface) -> None:
        """Function to draw entry box"""

        # Rerender text
        self.text = self.FONT.render(self.label, True, (0, 0, 0))

        while self.text.get_width() > self.width - 10:
            self.label = self.label[:-1]
            self.text = self.FONT.render(self.label, True, (0, 0, 0))

        # Draw a white rectangle for the button background
        pygame.draw.rect(screen, self.colour.rgb, ((self.x + 2, self.y + 2, self.width - 4, self.height - 4)))
        
        # Display the text in the centre of the button
        screen.blit(self.text, (self.x + 5, self.y + (self.height - self.text.get_height()) / 2))

        # Draw a hollow black rectangle with border 5
        pygame.draw.rect(screen, self.border_colour.rgb, (self.x, self.y, self.width, self.height), 5)

    def on_click(self, mouse_pos: tuple[int, int], mouse_state: tuple[bool, bool, bool]) -> bool:
        """Function to check whether click and run functions if happening"""

        # Get left mouse button state
        click = mouse_state[0]

        # If hovering and clicked with left mouse button return True, else False
        if self.on_hover(mouse_pos) and click:
            # Set so typing and change bg colour to show
            if not self.typing:
                # Changes the colour only once
                self.highlight()
                self.typing = True
            return True
        elif click:
            # Set so not typing and change bg colour back to show
            if self.typing:
                # Changes the colour only once
                self.unhighlight()
                self.typing = False

    def get_input(self, pressed_keys: list[str]) -> Union[str, None]:
        """Function to get keyboard input"""
        if self.typing:
            # For every pressed key, add the pressed key or remove on backspace
            for key in pressed_keys:
                if key == "back":
                    if self.label != "":
                        self.label = self.label[:-1]
                elif key == "enter":
                    self.unhighlight()
                    self.typing = False
                else:
                    if key in allowed_chars:
                        self.label += key

            return self.label

    def set_label(self, val: str) -> None:
        """Function to set label"""
        self.label = val


# Label class
class Label:
    """Class to handle the creation of labels"""
    def __init__(
        self, x: Union[int, float], y: Union[int, float],
        text: Union[str, int, float], size: int, settings: Settings
        ) -> None:
        """Initialising function for label class"""

        # Create instance variables
        self.x = x
        self.y = y
        self._text = str(text)
        self.size = size
        self.text_colour = Colour(0, 0, 0)
        self.settings = settings

        # Create instance constants
        self.FONT = pygame.font.SysFont(self.settings.font, size)

    def draw(self, screen: pygame.Surface) -> None:
        """Function to draw the label"""
        # Re-render the text in case it has changed
        self.render = self.FONT.render(self._text, True, self.text_colour.rgb)

        # Blit the text to the screen
        screen.blit(self.render, (self.x, self.y))

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, text: Union[str, int, float]) -> None:
        self._text = str(text)
