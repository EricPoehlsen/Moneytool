import data
from coin import Coin
from math import pi, sin, cos, sqrt
import random
from PIL import Image, ImageDraw, ImageTk
S = data.DE


class RectCoin(Coin):
    DIMS = ("length", "width", "thickness", "corner_radius")
    UNITS = ("mm", "mm", "mm", "mm")
    NAME = "rect"

    def __init__(self, length=1, width=1, thickness=1, corner_radius=0.0):
        """ manages a rectangular coin
        Args:
            length (float): length of rectangle in mm [> 0.0]
            width (float): width of rectangle in mm [> 0.0]
            thickness(float): coin thickness in mm [> 0.0]
            corner_radius(float): rounded corners radius in mm [>= 0.0]
        """

        super().__init__()
        self.length = length
        self.width = width
        self.thickness = thickness
        self.corner_radius = corner_radius
        self.points = []
        self.color = "#000"

    def calculate_shape(self):
        """ calculate the shape of a rectangular coin """

        # error handling
        for dim in [self.length, self.width, self.thickness]:
            if dim <= 0:
                raise ValueError("Coin dimensions need to be positive")
        if self.corner_radius < 0:
            raise ValueError("Corner radius can't be negative")
        if self.corner_radius >= (min(self.length, self.width) / 2):
            raise ValueError("Corner radius too big")

        self.area = self.length * self.width

        if self.corner_radius:
            self.area -= (2 * self.corner_radius) ** 2 + pi * self.corner_radius ** 2

        self.volume = self.area * self.thickness

    def generate_shape(self, volume):
        """ Generate a shape given a specific volume
        Args:
            volume (float): volume in cm³
        """

        # assuming minimum thickness of 1/10 mm
        max_area = volume * 1000 * 10

        # target area
        area = min([random.random() * (max_area / i) for i in range(1, 5)])

        # calculating sides
        length = random.random() * area
        width = area / length

        # generating border radius
        max_corner_radius = min(length, width) / 2
        corner_radius = max((random.random() - 0.5) * max_corner_radius, 0)
        area -= (2 * corner_radius) ** 2 + pi * corner_radius ** 2

        # calculating thicnkness
        thickness = volume * 1000 / area

        # updating data ...
        self.width = width
        self.length = length
        self.thickness = thickness
        self.area = area
        self.volume = volume * 1000
        self.corner_radius = corner_radius

    def image(self):
        """ Create an Image of the coin """

        # image dimension ...
        x_dim = int(data.Export.DPI * self.length * 0.1 / 2.54)
        y_dim = int(data.Export.DPI * self.width * 0.1 / 2.54)
        margin = data.Export.MARGIN
        c_rad = self.corner_radius * data.Export.DPI * 0.1 / 2.54
        img_x = x_dim + data.Export.MARGIN
        img_y = y_dim + data.Export.MARGIN

        image = Image.new("RGBA", (img_x, img_y))

        draw = ImageDraw.Draw(image)
        draw.rectangle(
            (margin, margin+c_rad, margin+x_dim, margin+y_dim-c_rad),
            fill=(0, 0, 0, 255)
        )
        if c_rad:
            draw.rectangle(
                (margin+c_rad, margin, margin + x_dim-c_rad, margin + y_dim),
                fill=(0, 0, 0, 255)
            )
            xy_0 = [
                (margin, margin),
                (margin + x_dim - 2*c_rad, margin),
                (margin, margin + y_dim - 2*c_rad),
                (margin + x_dim - 2*c_rad, margin + y_dim - 2*c_rad)
            ]
            for entry in xy_0:
                x, y = entry
                draw.ellipse((x, y, x+2*c_rad, y+2*c_rad), fill=(0,0,0,255))

        return image

    def draw(self, canvas):
        """ draw PIL image to canvas ... """

        canvas.delete("all")
        width = canvas.winfo_reqwidth()
        height = canvas.winfo_reqheight()

        image = ImageTk.PhotoImage(self.image())
        canvas.create_image(width/2, height/2, image=image)
        canvas.img = image

    def __str__(self):
        return S.SHAPES["rect"] + " V: " + str(round(self.volume / 1000, 2)) + "cm³"
        pass
