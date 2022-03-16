# Import base libraries
import pygame

# Import custom scripts
from guiElements import Label, Button, Entry
from graph import Graph
from settings import Settings
from algorithms import Kruskals, Dijkstras

class Interface:
    """Class to handle the interface of the program"""
    def __init__(self, settings: Settings) -> None:
        """Initialisation function of the interface class"""
        self.buttons: list[Button] = [
            Button(10, 470, 40, 20, "Dijkstras", settings, "Shortest path algorithm"),
            Button(60, 470, 40, 20, "Prims", settings, "Minimum spanning tree algorithm"),
            Button(110, 470, 40, 20, "Kruskals", settings, "Minimum spanning tree algorithm"),
            Button(160, 470, 40, 20, "Next", settings, "Runs next step in algorithm"),
            Button(210, 470, 40, 20, "Prev", settings, "Steps back through the algorithm"),
            Button(540, 440, 50, 20, "Save Graph", settings, "Saves graph to file"),
            Button(540, 470, 50, 20, "Load Graph", settings, "Loads graph from file"),
            Button(260, 470, 40, 20, "Settings", settings, "Access and change settings")
        ]

        self.entries: list[Entry] = [
            Entry(370, 440, 160, 50, settings, 30)
        ]

        self.settings_content = [
            # Button() for always show node names
            # Button() for always show edge weights
            # Button() for change font? -> would have to update everywhere
            # unless font is rendered each loop rather than at the start
        ]

        self.settings = settings
        self.settings_open = False

        self.help_label: Label = self.settings.help_label

    def draw(self, screen: pygame.Surface) -> None:
        """Displays the interface to the screen"""
        for button in self.buttons:
            button.draw(screen)

        for entry in self.entries:
            entry.draw(screen)

        self.help_label.draw(screen)

        if type(self.settings.cur_algorithm) == Dijkstras:
            for box in self.settings.cur_algorithm.boxes.values():
                    box.draw(screen)


    def run_mouse(
        self, mouse_pos: tuple[int, int],
        mouse_state: tuple[bool, bool, bool],
        graph: Graph
        ) -> bool:
        """Runs mouse functions of the interface"""
        # Run all button functions
        for button in self.buttons:
            button.on_hover(mouse_pos)
            if self.settings.mouse_function is None and button.on_click(mouse_pos, mouse_state):
                self.settings.mouse_function = "button"
                if button.label in ["Dijkstras", "Prims"]:
                    self.settings.start_algorithm = button.label
                    self.settings.help_label.text = "Click node to select start node"
                elif button.label == "Kruskals":
                    self.settings.cur_algorithm = Kruskals(graph)
                elif button.label == "Next":
                    if self.settings.cur_algorithm is not None:
                        if self.settings.cur_algorithm.next_step() == "Finished":
                            self.settings.cur_algorithm.clear_up()
                            self.settings.cur_algorithm = None
                elif button.label == "Prev":
                    if self.settings.cur_algorithm is not None:
                        self.settings.cur_algorithm.prev_step()
                elif button.label == "Save Graph":
                    graph.save_graph(self.entries[0].label)
                    self.entries[0].label = ""
                    self.entries[0].typing = False
                    self.entries[0].unhighlight()
                elif button.label == "Load Graph":
                    graph.load_graph(self.entries[0].label)
                    self.entries[0].label = ""
                    self.entries[0].typing = False
                    self.entries[0].unhighlight()
                elif button.label == "Settings":
                    self.settings_open = True
                    

        # Run all entry functions
        for entry in self.entries:
            entry.on_hover(mouse_pos)
            if self.settings.mouse_function is None and entry.on_click(mouse_pos, mouse_state):
                self.settings.mouse_function = "entry"

    def run_keys(self, pressed_keys: list[bool]) -> None:
        """Runs keyboard functions of the interface"""
        # Run all entry functions
        for entry in self.entries:
            entry.get_input(pressed_keys)
