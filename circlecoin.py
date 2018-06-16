from coin import Coin
from math import pi, sin, cos, sqrt
import data
import random
from PIL import Image, ImageDraw, ImageTk
S = data.DE


class CircleCoin(Coin):
    DIMS = ("radius", "inner_radius", "thickness")
    UNITS = ("mm", "mm", "mm")
    NAME = "circle"

    def __init__(self, radius=1, thickness=1, inner_radius=0):
        """ manages a circular (cylindrical) coin
        Args:
            radius(float): coin radius in mm [> 0.0]
            thickness(float): coin thickness in mm [> 0.0]
            inner_radius(float): hole radius in mm [>= 0.0]
        """

        super().__init__()
        self.radius = radius
        self.inner_radius = inner_radius
        self.thickness = thickness

    def calculate_shape(self):
        """ calculate the shape of a circular (cylindrical) coin """

        # error handling
        if self.radius <= 0: raise ValueError("Radius must be positive.")
        if self.inner_radius < 0: raise ValueError("Inner radius must not be negative")
        if self.inner_radius > self.radius: raise ValueError("Inner radius must be smaller than radius")
        if self.thickness <= 0: raise ValueError("Thickness must be positive")

        self.area = pi * self.radius ** 2
        self.area -= pi * self.inner_radius ** 2

        self.volume = self.area * self.thickness

    def generate_shape(self, volume):
        """ Generate a shape given a specific volume
        Args:
            volume (float): volume in cm³
        """

        # assuming minimum thickness of 1/10 mm
        max_area = volume * 1000 * 10

        area = min([random.random() * (max_area / i) for i in range(1,5)])

        radius = sqrt(area / pi)
        inner_radius = max((random.random() - random.random()) * radius, 0)
        inner_area = inner_radius ** 2 * pi
        area -= inner_area
        thickness = (volume * 1000) / area

        self.radius = radius
        self.inner_radius = inner_radius
        self.thickness = thickness
        self.volume = volume * 1000
        self.area = area

    def image(self):
        """ Create an Image of the coin """

        # image dimension ...
        # margin + DPI * double radius * mm to cm to inch
        size = int(data.Export.MARGIN + data.Export.DPI * 2 * self.radius * 0.1 / 2.54)

        x = size / 2
        y = size / 2

        # scaling to the DPI
        r = data.Export.DPI * self.radius * .1 / 2.54
        i = data.Export.DPI * self.inner_radius * .1 / 2.54

        image = Image.new("RGBA", (size, size))

        draw = ImageDraw.Draw(image)
        draw.ellipse((x-r, y-r, x+r, y+r), fill=(0,0,0,255))
        draw.ellipse((x-i, y-i, x+i, y+i), fill=(0,0,0,0))
        return image

    def draw(self, canvas):
        """ Draw PIL image to canvas """
        canvas.delete("all")
        width = canvas.winfo_reqwidth()
        height = canvas.winfo_reqheight()

        image = ImageTk.PhotoImage(self.image())
        canvas.create_image(width/2, height/2, image=image)
        canvas.img = image

    def __str__(self):
        return S.SHAPES["circle"] + " V: " + str(round(self.volume / 1000, 2)) + "cm³"
