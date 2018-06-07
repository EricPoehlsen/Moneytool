import tkinter as tk
import data

from coin import Coin
from polycoin import PolyCoin
from circlecoin import CircleCoin
from rectcoin import RectCoin
from metallurgy import Metallurgy
from PIL import Image, ImageTk

S = data.DE

class CoinDesigner(tk.Frame):
    def __init__(self, screen, coin=None):
        super().__init__(screen)

        # place to keep tk variables
        self.vars = {}
        self.widgets = {}
        self.coin = coin
        self.canvas = tk.Canvas(self)
        self.canvas.config(width=400, height=400)

        self.shape_container = tk.LabelFrame(self, text="Form festlegen")
        self.shape_selector = tk.Frame(self.shape_container)
        self.shape_selector.pack(side=tk.TOP, fill=tk.X)
        self.shape_entry = tk.Frame(self.shape_container)
        self.shape_entry.pack(side=tk.TOP)
        self.build_shape_selector()
        self.shape_container.pack(side=tk.LEFT, fill=tk.Y, expand=1)

        self.canvas.pack(side=tk.LEFT)

    def build_shape_selector(self):
        """ add the selector for the basic coin shape """

        frame = self.shape_selector

        shapes = [f for f in S.SHAPES.values()]
        shape = self.vars["shape"] = tk.StringVar()
        shape.trace("w", self.update_shape_entry)

        # set to shape of current coin
        if self.coin:
            current = S.SHAPES[self.coin.NAME]
        else:
            current = shapes[0]
        shape.set(current)
        selector = tk.OptionMenu(frame, shape, *shapes)
        selector.config(width=20)
        selector.pack(fill=tk.X, expand=1)

    def update_shape_entry(self, n=None, e=None, m=None):
        """ construct the coin entry fields, when the primary shape is selected """

        container = self.shape_entry
        selected = self.vars["shape"].get()
        self.widgets = {}

        # clear the current entry area ...
        widgets = container.winfo_children()
        for widget in widgets:
            widget.destroy()

        # remove the drawing of the last coin ...
        self.canvas.delete("all")

        # creating the coin ...
        # ... rectangle ...
        if selected == S.SHAPES["rect"]:
            new_coin = RectCoin()
        # ... polygon ...
        elif selected == S.SHAPES["poly"]:
            new_coin = PolyCoin()
        # ... circle ...
        elif selected == S.SHAPES["circle"]:
            new_coin = CircleCoin()
        # ... generic ...
        else:
            new_coin = Coin()

        if type(new_coin) != type(self.coin):
            self.coin = new_coin

        dimensions = self.coin.DIMS
        units = self.coin.UNITS
        labels = [S.SHAPE_DIMENSIONS[dim] for dim in dimensions]

        # packing - unpacking and constructing the entry fields ...
        for i, l, u, d in zip(range(len(labels)), labels, units, dimensions):

            label = tk.Label(container, text=l, anchor=tk.W)
            label.grid(row=i, column=0)
            var = tk.StringVar()
            var.set(getattr(self.coin, d, 0))
            var.trace("w", self.update_shape)
            self.widgets[d] = entry = tk.Entry(container, width=4, textvariable=var)
            entry.var = var
            entry.grid(row=i, column=1)
            unit = tk.Label(container, text=u, anchor=tk.W)
            unit.grid(row=i, column=2)

    def update_shape(self, n=None, e=None, m=None):
        """ recalculate the shape after it was changed

        this is realized as 'trace' callback on the entry variables ...
        """

        # create the coin  ...
        shapes = {v: k for k, v in S.SHAPES.items()}
        shape = self.vars["shape"].get()
        selected = shapes[shape]

        def to_number(v):
            """ number conversion for dict comprehension below ... """
            value = v.var.get()
            if "," in value: value = value.replace(",", ".")
            try:
                value = float(value)
                v.config(bg="#fff")
            except ValueError:
                value = 0
                v.config(bg="#f00")
            return value

        data = {k: to_number(v) for k, v in self.widgets.items()}

        if selected == "circle":
            self.coin.radius = data["radius"]
            self.coin.inner_radius = data["inner_radius"]
            self.coin.thickness = data["thickness"]

        elif selected == "rect":
            self.coin.length = data["length"]
            self.coin.width = data["width"]
            self.coin.thickness = data["thickness"]
            self.coin.corner_radius = data["corner_radius"]

        elif selected == "poly":
            self.coin.radius = data["radius"]
            self.coin.sides = int(data["sides"])
            self.coin.chamfer = data["chamfer"]
            self.coin.thickness = data["thickness"]

        try:
            self.coin.calculate_shape()
        except ValueError as e: print("Not updated: ", e)

        if self.coin.area and self.coin.volume:
            self.coin.draw(self.canvas)

class CoinDesignerWindow(tk.Toplevel):
    def __init__(self, master, number):
        """ Creates a top level window for the coin designer
        Args:
            master (CoinGenerator): the parent widget
            number (int): index of coin to modify
        """

        super().__init__(master)

        coin = self.master.coins[number].get("shape")

        # set up CoinDesigner
        self.shape_selector = CoinDesigner(self, coin)
        if coin: self.shape_selector.update_shape()
        self.shape_selector.pack()

        # add buttons
        delete = tk.Button(self, text=S.DELETE, command=self.remove_coin)
        delete.pack(fill=tk.X)
        cancel = tk.Button(self, text=S.CANCEL, command=self.destroy)
        # cancel.pack(fill=tk.X)
        ok = tk.Button(self, text=S.ACCEPT, command=self.destroy)
        ok.pack(fill=tk.X)

        self.number = number

    def remove_coin(self):
        self.shape_selector.coin = Coin()
        self.destroy()

    def destroy(self):
        """ Destroy window, write data back before closing """

        coin = self.shape_selector.coin

        if coin:
            coins = self.master.coins
            coins[self.number]["shape"] = coin
            button = coins[self.number]["widgets"][0]
            image = coin.image()
            scale = 32 / image.height
            x = int(scale * image.width)
            y = int(scale * image.height)
            image = image.resize((x, y), Image.BICUBIC)
            image = ImageTk.PhotoImage(image)
            button.config(
                anchor=tk.W,
                text=str(coin),
                image=image,
                compound=tk.LEFT
            )
            button.img = image

        super().destroy()