import tkinter as tk
import data
import math
from polycoin import PolyCoin
from circlecoin import CircleCoin
from rectcoin import RectCoin

S = data.DE

class MainScreen(tk.Frame):
    def __init__(self, screen):

        super().__init__(screen)

        # place to keep tk variables
        self.vars = {}
        self.widgets = {}
        self.coin = None
        self.alloy = {k: 0 for k in data.Metals.DATA}

        self.alloy_value = 0
        self.alloy_density = 0

        self.canvas = tk.Canvas(self)
        self.canvas.config(width=400, height=400)
        self.canvas.pack(side=tk.LEFT)

        self.center_frame = tk.Frame(self)
        self.shape_container = tk.LabelFrame(self.center_frame, text="Form festlegen")
        self.shape_selector = tk.Frame(self.shape_container)
        self.shape_selector.pack(side=tk.TOP, expand=1, fill=tk.X)
        self.shape_entry = tk.Frame(self.shape_container)
        self.shape_entry.pack(side=tk.BOTTOM)
        self.build_shape_selector()
        self.shape_container.pack(side=tk.TOP)
        self.result_frame = tk.LabelFrame(self.center_frame, text=S.RESULT)
        self.result_frame.pack(side=tk.BOTTOM)
        self.center_frame.pack(side=tk.LEFT)

        self.metallurgy = tk.Frame(self)
        self.smelting_pot = tk.LabelFrame(self.metallurgy, text=S.MELTING_POT)
        self.build_metallurgy_lab()
        self.metallurgy.pack(side=tk.LEFT)

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
            dim_unit = ["mm", "mm", "%", "mm"]

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

        self.update_coin_data()

    def update_coin_data(self):
        """ Update the result frame with information about the coin ... """

        # calculate data ...
        volume = 0
        if hasattr(self.coin, "volume"):
            volume = self.coin.volume / 1000
        weight = volume * self.alloy_density
        value = weight * self.alloy_value

        # format data ...
        volume = S.VOLUME + str(round(volume, 2)) + "cm³"
        weight = S.WEIGHT + str(round(weight, 2)) + "g"
        value = S.VALUE + str(round(value, 2)) + "$"

        # clear frame
        frame = self.result_frame
        for w in frame.winfo_children():
            w.destroy()

        # display data
        tk.Label(frame, text=volume).pack()
        tk.Label(frame, text=weight).pack()
        tk.Label(frame, text=value).pack()


    def build_metallurgy_lab(self):
        """ build the metallurgy lab frame """

        frame = self.metallurgy
        self.widgets["metal_absolute"] = {}
        self.widgets["metal_relative"] = {}
        self.widgets["metal_names"] = {}
        self.widgets["metal_filter"] = {}
        w_abs = self.widgets["metal_absolute"]
        w_rel = self.widgets["metal_relative"]
        w_name = self.widgets["metal_names"]

        selector = tk.LabelFrame(frame, text=S.METAL_GROUPS)
        for i in range(4):
            w = self.widgets["metal_filter"][i] = tk.Checkbutton(selector)
            var = tk.IntVar()
            var.set(1)
            var.trace("w", self.filter)
            w.config(text=S.METAL_SELECTION[i], variable=var)
            w.var = var
            w.pack(anchor=tk.W)
        selector.pack(fill=tk.X, expand=1)

        sorter = tk.LabelFrame(frame, text=S.METAL_SORT)
        criteria = ["name", "value", "amount", "density"]
        for c in criteria:
            button = tk.Button(
                sorter,
                text=S.METAL_SORTER[c],
                command=lambda e=c: self.filter(e)
            )
            button.pack(side=tk.LEFT)
        sorter.pack()

        for i, m in enumerate(data.Metals.DATA):

            w_name[m] = tk.Label(self.smelting_pot, text=S.METALS[m], anchor=tk.W)
            w_name[m].grid(row=i, column=0, sticky=tk.W)
            w_abs[m] = tk.Entry(self.smelting_pot,width=5)
            w_abs[m].bind("<Key>", lambda e, m=m: self.smelt(e, m))
            w_abs[m].insert(0, "0")
            w_abs[m].grid(row=i, column=1)
            w_rel[m] = tk.Label(self.smelting_pot, text="0.00%", width=7, anchor=tk.E)
            w_rel[m].grid(row=i, column=2)

        self.smelting_pot.pack(side=tk.TOP, fill=tk.X)

    def smelt(self, event, metal):
        """ smelt your metals to create an alloy
            args:
                metal(string): symbol of element changed
        """

        # check the value and update the alloy dict
        value = event.widget.get()
        if "," in value: value.replace(",", ".")
        try:
            value = float(value)
        except ValueError:
            event.widget.config(background="#f00")
            return

        # no negative values!
        if value < 0:
            event.widget.config(background="#f00")
            return

        event.widget.config(background="#fff")

        self.alloy[metal] = value

        # if a metal is used in an alloy, it's group must be displayed!
        for k, v in data.Metals.SELECTOR.items():
            if metal in v:
                total = sum([a for name, a in self.alloy.items() if name in v])
                selector = self.widgets["metal_filter"][k]
                if total: selector.config(state=tk.DISABLED)
                else: selector.config(state=tk.NORMAL)

        # calculating the absolute sum
        amount = sum(self.alloy.values())
        volume = 0
        price = 0

        # calculate mass percentage
        for name, value in self.alloy.items():
            try:
                percentage = 100 * value / amount
            except ZeroDivisionError:
                percentage = 0.0

            # updating the text
            percentage = str(round(percentage, 2)) + " %"
            self.widgets["metal_relative"][name].config(text=percentage)

            # adding to price
            price += value / 1000 * data.Metals.DATA[name][2]
            volume += value / data.Metals.DATA[name][1]

        try:
            density = amount / volume
            value = price / amount
        except ZeroDivisionError:
            density = 0
            value = 0

        self.alloy_density = density
        self.alloy_value = value

        self.update_coin_data()


    def filter(self, n=None, e=None, m=None):
        """ filter and sort the metals in the smelting pot """

        if n: print(n)

        # filter based on the selector
        selection = []
        for i in range(4):
            if self.widgets["metal_filter"][i].var.get() == 1:
                selection += data.Metals.SELECTOR[i]

        selection = [x for x in selection]
        metal_data = data.Metals.DATA.items()

        l = [(m, S.METALS[m]) for m in selection]
        l = sorted(l, key=lambda d: d[1])

        if n == "name":
            l = [(m, S.METALS[m]) for m in selection]
            l = sorted(l, key=lambda d: d[1])

        elif n == "density":
            l = [(s, d[1]) for s, d in metal_data if s in selection]
            l = sorted(l, key=lambda d: d[1], reverse=True)

        elif n == "amount":
            l = [(m, self.alloy[m]) for m in selection]
            l = sorted(l, key=lambda d: d[1], reverse=True)

        elif n == "value":
            l = [(s, d[2]) for s, d in metal_data if s in selection]
            l = sorted(l, key=lambda d: d[1], reverse=True)


        w_abs = self.widgets["metal_absolute"]
        w_rel = self.widgets["metal_relative"]
        w_name = self.widgets["metal_names"]

        # remove visibility for all entries
        for w in w_abs.values(): w.grid_forget()
        for w in w_rel.values(): w.grid_forget()
        for w in w_name.values(): w.grid_forget()

        for i, v in enumerate(l):
            w_name[v[0]].grid(row=i, column=0, sticky=tk.W)
            w_abs[v[0]].grid(row=i, column=1)
            w_rel[v[0]].grid(row=i, column=2)