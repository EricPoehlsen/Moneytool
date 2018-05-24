from math import pi, sin, cos, sqrt

class PolyCoin(object):
    def __init__(self, sides, radius, thickness, chamfer=0.0):
        self.radius = radius
        self.sides = sides
        self.chamfer = chamfer / 100
        self.thickness = thickness
        self.points = [(0,0)]

        self.area = 0
        self.volume = 0

    def calculate_shape(self):
        """ Calculate points of a (chamfered) regular n-gon """

        # error handling
        print(self.thickness)
        if self.sides < 3: raise ValueError("Polygon needs at least three sides.")
        if self.radius <= 0: raise ValueError("Radius must be positive.")
        if not 0.0 <= self.chamfer <= 1.0: raise ValueError("Valid range 0 <= c < 1")
        if self.thickness <= 0: raise ValueError("Thickness must be positive")

        # initial trigonometry ...
        chamfer = self.chamfer / 2
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

    def draw(self, canvas):
        canvas.delete("all")

        width = canvas.winfo_width()
        height = canvas.winfo_height()

        x_values = [x for x,y in self.points]
        y_values = [y for x,y in self.points]

        min_x = min(x_values)
        max_x = max(x_values)
        min_y = min(y_values)
        max_y = max(y_values)

        d = .1 * min(width, height)
        x_range = max_x - min_x
        y_range = max_y - min_y
        x_scale_factor = width / x_range
        y_scale_factor = height / y_range
        scale = min(x_scale_factor, y_scale_factor) * .75
        points = [(d + (x - min_x) * scale, d + (y - min_y) * scale) for x, y in self.points]
        print(points)
        size = min(width, height)

        if min_x > 0: min_x = 0
        if min_y > 0: min_y = 0

        canvas.create_polygon(*points, fill="#000")
