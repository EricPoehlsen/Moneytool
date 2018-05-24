from math import pi, sin, cos, sqrt

class CircleCoin(object):
    def __init__(self, radius, thickness, inner_radius=0):
        self.radius = radius
        self.inner_radius = inner_radius
        self.thickness = thickness
        self.area = 0
        self.volume = 0

    def calculate_shape(self):
        """ calculate the shape of a circular (cylindrical) coin
            returns: [(x,y),...], area
        """

        # error handling
        if self.radius <= 0: raise ValueError("Radius must be positive.")
        if self.inner_radius < 0: raise ValueError("Inner radius must not be negative")
        if self.inner_radius > self.radius: raise ValueError("Inner radius must be smaller than radius")
        if self.thickness <= 0: raise ValueError("Thickness must be positive")

        self.area = pi * self.radius ** 2
        self.area -= pi * self.inner_radius ** 2

        self.volume = self.area * self.thickness

    def draw(self, canvas):
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        r = min(width, height) * .4
        x = width / 2
        y = height / 2
        canvas.create_oval(
            x - r,
            y - r,
            x + r,
            y + r,
            fill="#000"
        )

        if self.inner_radius:
            i_r = (self.inner_radius / self.radius) * r
            canvas.create_oval(
                x - i_r,
                y - i_r,
                x + i_r,
                y + i_r,
                fill = "#eee"
            )

        pass