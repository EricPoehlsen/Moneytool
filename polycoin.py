from coin import Coin
from math import pi, sin, cos, sqrt
from PIL import Image, ImageDraw, ImageTk
import data
import random
S = data.DE


class PolyCoin(Coin):
    DIMS = ("sides", "radius", "thickness", "chamfer")
    UNITS = ("", "mm", "mm", "%")
    NAME = "poly"

    def __init__(self, sides=3, radius=1.0, thickness=1.0, chamfer=0.0):
        """ manages a polygonal coin
        Args:
            sides (int): number of sides [>= 3]
            radius(float): circumcircle radius in mm [> 0.0]
            thickness(float): coin thickness in mm [> 0.0]
            chamfer(float): corner chamfering [0.0 < 100.0]
        """

        super().__init__()
        self.radius = radius
        self.sides = sides
        self.chamfer = chamfer / 100
        self.thickness = thickness
        self.points = [(0,0)]

    def calculate_shape(self):
        """ Calculate points of a (chamfered) regular n-gon """

        # error handling
        if self.sides < 3: raise ValueError("Polygon needs at least three sides.")
        if self.radius <= 0: raise ValueError("Radius must be positive.")
        if not 0.0 <= self.chamfer <= 100.0: raise ValueError("Valid range 0 <= c < 100")
        if self.thickness <= 0: raise ValueError("Thickness must be positive")

        # initial trigonometry ...
        chamfer = self.chamfer / 200
        angle = 360 / self.sides
        side = 2 * self.radius * sin((pi/self.sides))
        radius_inner = sqrt(self.radius**2 - (0.5 * side)**2)

        # primary polygon area
        self.area = 0.5 * side * radius_inner * self.sides

        # chamfer areas
        cut = side * chamfer

        try:
            chamfer_length = sqrt(2 * cut**2 - 2 * cut * cos(angle * pi/180))
            chamfer_depth = sqrt(cut**2 - (0.5 * chamfer_length)**2)
            chamfer_area = 0.5 * chamfer_length * chamfer_depth * self.sides
        except ValueError:
            chamfer_area = 0

        self.area -= chamfer_area
        self.volume = self.area * self.thickness

        # resetting the points with starting point
        self.points = [(0,0)]

        cur_angle = 0
        for i in range(self.sides):
            x, y = self.points[-1]

            # vector to next corner
            x_factor = cos(cur_angle * pi / 180)
            y_factor = sin(cur_angle * pi / 180)

            # adding chamfered midpoints
            if chamfer:
                x_sub1 = x + x_factor * side * chamfer
                y_sub1 = y + y_factor * side * chamfer
                x_sub2 = x + x_factor * side * (1 - chamfer)
                y_sub2 = y + y_factor * side * (1 - chamfer)
                self.points.append((x_sub1, y_sub1))
                self.points.append((x_sub2, y_sub2))

            # adding next corner
            x1 = x + x_factor * side
            y1 = y + y_factor * side
            self.points.append((x1, y1))

            cur_angle += angle

        # removing original n-gon corners of chamfered n-gon
        if self.chamfer:
            self.points = [p for i, p in enumerate(self.points) if i % 3]

    def generate_shape(self, volume):
        """ Generate a shape given a specific volume
        Args:
            volume (float): volume in cm³
        """

        # assuming minimum thickness of 1/10 mm
        max_area = volume * 1000 * 10

        # target area
        area = min([random.random() * (max_area / i) for i in range(1, 5)])

        radius = sqrt(area / pi)
        chamfer = max(.5 * random.random() - random.random(), 0)
        sides = random.choice([3,3,4,5,6,6,6,6,7,8,8])

        # initial trigonometry ...
        chamfer = chamfer / 2
        angle = 360 / sides
        side = 2 * radius * sin((pi/sides))
        radius_inner = sqrt(radius**2 - (0.5 * side)**2)

        # primary polygon area
        area = 0.5 * side * radius_inner * self.sides

        # chamfer areas
        cut = side * chamfer
        try:
            chamfer_length = sqrt(2 * cut**2 - 2 * cut * cos(angle * pi/180))
            chamfer_depth = sqrt(cut**2 - (0.5 * chamfer_length)**2)
            chamfer_area = 0.5 * chamfer_length * chamfer_depth * self.sides
        except ValueError:
            chamfer_area = 0
            chamfer = 0

        area -= chamfer_area

        thickness = volume * 1000 / area

        # update the coin
        self.sides = sides
        self.radius = radius
        self.chamfer = chamfer
        self.thickness = thickness

        # needed to calculate the points ...
        self.calculate_shape()

    def image(self):
        """ Create an Image of the coin """

        # image dimension ...
        # margin + DPI * double radius * mm to cm to inch
        size = int(data.Export.MARGIN + data.Export.DPI * 2 * self.radius * 0.1 / 2.54)

        # transforming the points ...
        x_values = [x for x,y in self.points]
        y_values = [y for x,y in self.points]

        min_x = min(x_values)
        min_y = min(y_values)

        scale = data.Export.DPI * 0.1 / 2.54
        d = data.Export.MARGIN * 0.5
        points = [(int(d + (x - min_x) * scale), int(d + (y - min_y) * scale)) for x, y in self.points]

        image = Image.new("RGBA", (size,size))

        draw = ImageDraw.Draw(image)
        draw.polygon(points, fill=(0,0,0,255))
        return image

    def draw(self, canvas):
        """ draw PIL image to canvas ... """

        canvas.delete("all")

        width = canvas.winfo_reqwidth()
        height = canvas.winfo_reqheight()
        image = ImageTk.PhotoImage(self.image())
        canvas.create_image(width/2 ,height/2 ,image=image)
        canvas.img = image

    def __str__(self):
        return S.SHAPES["poly"] + " V: " + str(round(self.volume / 1000, 2)) + "cm³"
