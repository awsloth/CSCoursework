from guiElements import Label

class Settings:
    def __init__(self, width, height) -> None:
        """Initialisation function of settings class"""
        # Create instance variables:
        self.width = width
        self.height = height
        self.start_node = None
        self.start_algorithm = None
        self.cur_algorithm = None
        self.mouse_function = None
        with open("config.txt", "r") as f:
            content = [l.rstrip() for l in f.readlines()]
        self.font = content[0].split(":")[-1]
        self.show_names = [True, False][content[1].split(":")[-1].lower() != "true"]
        self.show_weight = [True, False][content[2].split(":")[-1].lower() != "true"]
        self.help_label = Label(5, 5, "", 20, self)
