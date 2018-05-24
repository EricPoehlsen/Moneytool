from math import pi, sin, cos, sqrt

class RectCoin(object):
    def __init__(self, length, width, thickness, corner_radius=0.0):
        self.length = length
        self.width = width
        self.thickness = thickness
        self.corner_radius = corner_radius
        self.points = []
        self.area = 0
        self.volume = 0
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


    def draw(self, canvas):

        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        x_scale = (width * 0.8) / self.length
        y_scale = (height * 0.8) / self.width
        scale = min(x_scale, y_scale)

        coin_width = self.length * scale
        coin_height = self.width * scale
        corners = self.corner_radius * scale

        x0 = (width - coin_width) / 2
        y0 = (height - coin_height) / 2

        if not corners:
            canvas.create_rectangle(
                x0,
                y0,
                x0+coin_width,
                y0+coin_height,
                fill=self.color
            )
        else:
            canvas.create_rectangle(
                x0,
                y0+corners,
                x0+coin_width,
                y0+coin_height-corners,
                fill=self.color
            )
            canvas.create_rectangle(
                x0+corners,
                y0,
                x0+coin_width-corners,
                y0+coin_height,
                fill=self.color
            )
            canvas.create_oval(
                x0,
                y0,
                x0+2*corners,
                y0+2*corners,
                fill=self.color
            )
            canvas.create_oval(
                x0+coin_width-2*corners,
                y0,
                x0+coin_width,
                y0+2*corners,
                fill=self.color
            )
            canvas.create_oval(
                x0,
                y0+coin_height-2*corners,
                x0+2*corners,
                y0+coin_height,
                fill=self.color
            )
            canvas.create_oval(
                x0+coin_width-2*corners,
                y0+coin_height-2*corners,
                x0+coin_width,
                y0+coin_height,
                fill=self.color
            )