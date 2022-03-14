class Colour:
    """Handles hsv colours"""
    def __init__(self, hue: int, saturation: float, value: float) -> None:
        """Initialising function for colour class"""
        # Create instance variables
        self._h = hue
        self._s = saturation
        self._v = value

    @property
    def v(self) -> float:
        return self._v

    @v.setter
    def v(self, val: float) -> None:
        # Check that the 0 <= val <= 1
        if val > 1:
            self._v = 1
        elif val < 0:
            self._v = 0
        else:
            self._v = val

    @property
    def h(self) -> int:
        return self._h

    @h.setter
    def h(self, val: int) -> None:
        # Enforce that 0 <= val <= 360
        self._h = val % 360
    
    @property
    def rgb(self) -> tuple[int, int, int]:
        # Use hsv to rgb algorithm to convert
        c = self._s * self._v
        x = c * (1 - abs((self._h//6)%2 - 1))
        m = self._v - c

        # Colour list to get r, g and b values
        colour = [0, 0, 0]

        # Get x position and set to x
        x_pos = (10 - self._h // 60)%3
        colour[x_pos] = x

        # Get c position and set to c
        c_pos = ((self._h+60)//120)%3
        colour[c_pos] = c

        # Get r, g and b values
        r, g, b = [int((col+m)*255) for col in colour]

        return (r, g, b) 

    @property
    def hsv(self) -> tuple[int, float, float]:
        return (self._h, self._s, self._v)
