import tkinter as tk
import data

from polycoin import PolyCoin
from circlecoin import CircleCoin
from rectcoin import RectCoin
from metallurgy import Metallurgy
from coingenerator import CoinGenerator

S = data.DE

class CoinDesigner(tk.Frame):
    def __init__(self, screen):
        super().__init__(screen)

        # place to keep tk variables
        self.vars = {}
        self.widgets = {}
        self.coin = None

        self.canvas = tk.Canvas(self)
        self.canvas.config(width=400, height=400)
        self.canvas.pack(side=tk.LEFT)

        self.shape_container = tk.LabelFrame(self, text="Form festlegen")
        self.shape_selector = tk.Frame(self.shape_container)
        self.shape_selector.pack(side=tk.TOP, expand=1, fill=tk.X)
        self.shape_entry = tk.Frame(self.shape_container)
        self.shape_entry.pack(side=tk.BOTTOM)
        self.build_shape_selector()
        self.shape_container.pack(side=tk.LEFT)

    def build_shape_selector(self):
        """ add the selector for the basic coin shape """

        frame = self.shape_selector

        shapes = [f for f in S.SHAPES.values()]
        shape = self.vars["shape"] = tk.StringVar()
        shape.trace("w", self.update_shape_entry)

        shape.set(shapes[0])
        selector = tk.OptionMenu(frame, shape, *shapes)
        selector.pack(expand=1)

    def update_shape_entry(self, n=None, e=None, m=None):
        """ construct the coin entry fields, when the primary shape is selected """

        container = self.shape_entry
        selected = self.vars["shape"].get()

        # clear the current entry area ...
        widgets = container.winfo_children()
        for widget in widgets:
            widget.destroy()
        vars = self.vars["shape_data"] = {}
        names = self.vars["var_names"] = {}

        # remove the drawing of the last coin ...
        self.canvas.delete("all")

        dimensions = []
        dim_unit = []

        # defining the dimensions for the shapes ...
        # ... rectangle ...
        if selected == S.SHAPES["rect"]:
            dimensions = [
                "length",
                "width",
                "thickness",
                "corners"
            ]
            dim_unit = ["mm", "mm", "mm", "mm"]

        # ... circle ...
        if selected == S.SHAPES["circle"]:
            dimensions = [
                "radius",
                "inner_radius",
                "thickness"
            ]
            dim_unit = ["mm", "mm", "mm"]

        # ... polygon ...
        if selected == S.SHAPES["poly"]:
            dimensions = [
                "sides",
                "radius",
                "chamfer",
                "thickness"
            ]
            dim_unit = ["", "mm", "%", "mm"]

        # creating the tk.StringVars to store and trace the data
        labels = []
        variables = []
        for dim in dimensions:
            vars[dim] = tk.StringVar()
            names[str(vars[dim])] = dim
            labels.append(S.SHAPE_DATA[dim])
            variables.append(vars[dim])

        # packing - unpacking and constructing the entry fields ...
        for i, l, v, u in zip(range(len(labels)), labels, variables, dim_unit):

            label = tk.Label(container, text=l, anchor=tk.W)
            label.grid(row=i, column=0)
            v.set(0)
            v.trace("w", self.update_shape)
            entry = tk.Entry(container, width=4, textvariable=v)
            entry.grid(row=i, column=1)
            unit = tk.Label(container, text=u, anchor=tk.W)
            unit.grid(row=i, column=2)

    def update_shape(self, varname, e=None, m=None):
        """ recalculate the shape after it was changed

        this is realized as 'trace' callback on the entry variables ...
        """

        # replace commas with decimal in the entry
        changed = self.vars["shape_data"][self.vars["var_names"][varname]]
        if "," in changed.get():
            changed.set(changed.get().replace(",", "."))

        # tk.StringVar() => float (but be careful it is user input!)
        try:
            data = {k: float(v.get()) for k, v in self.vars["shape_data"].items()}
        except ValueError:
            return

        # create the coin  ...
        shapes = {v: k for k, v in S.SHAPES.items()}
        shape = self.vars["shape"].get()
        selected = shapes[shape]

        if selected == "circle":
            radius = data["radius"]
            inner_radius = data["inner_radius"]
            thickness = data["thickness"]
            self.coin = CircleCoin(radius, thickness, inner_radius)

        elif selected == "rect":
            length = data["length"]
            width = data["width"]
            thickness = data["thickness"]
            corners = data["corners"]
            self.coin = RectCoin(length, width, thickness, corners)

        elif selected == "poly":
            radius = data["radius"]
            sides = int(data["sides"])
            chamfer = data["chamfer"]
            thickness = data["thickness"]
            self.coin = PolyCoin(sides, radius, thickness, chamfer)

        try:
            self.coin.calculate_shape()
        except ValueError as e: print("Not updated: ", e)

        if self.coin.area and self.coin.volume:
            self.coin.draw(self.canvas)
            print("Area: ", self.coin.area, " | Volume: ", self.coin.volume)

