import tkinter as tk
from PIL import ImageTk, Image
import random
from metallurgy import MetallurgyWindow
from coindesigner import CoinDesignerWindow

from rectcoin import RectCoin
from circlecoin import CircleCoin
from polycoin import PolyCoin
from alloy import Alloy
import data




S = data.DE

class CoinGenerator(tk.Frame):
    """ Generate multiple coins by input or pseudo-randomly """

    def __init__(self, screen):
        super().__init__(screen)
        self.coins = []
        self.widgets = {}
        self.windows = None
        frame = tk.Frame(self)
        subframe = tk.Frame(frame)
        calc_forms = tk.Button(
            subframe,
            text=S.GENERATE_SHAPES,
            command=self.generate_shape
        )
        calc_forms.grid(row=0, column=0, sticky=tk.NSEW)
        calc_values = tk.Button(
            subframe,
            text=S.GENERATE_VALUES,
            command=self.generate_value
        )
        calc_values.grid(row=0, column=1, sticky=tk.NSEW)
        calc_alloys = tk.Button(
            subframe,
            text=S.GENERATE_ALLOYS,
            command=self.generate_alloy
        )
        calc_alloys.grid(row=0, column=2, sticky=tk.NSEW)
        subframe.columnconfigure(0, weight=1)
        subframe.columnconfigure(1, weight=1)
        subframe.columnconfigure(2, weight=1)

        subframe.pack(fill=tk.X, expand=1)

        generate = tk.Button(frame, text=S.GENERATE_COINS, command=self.generate)
        generate.pack(fill=tk.X, expand=1)
        new = tk.Button(frame, text=S.ADD_COIN, command=self.add_coin)
        new.pack(fill=tk.X, expand=1)
        frame.pack(fill=tk.X, expand=1, anchor=tk.N)
        self.coin_frame = tk.Frame(self)
        self.coin_frame.pack(fill=tk.X, expand=1)

        self.coin_frame.columnconfigure(0, weight=45)
        self.coin_frame.columnconfigure(1, weight=10)
        self.coin_frame.columnconfigure(2, weight=45)
        self.coin_frame.columnconfigure(3, weight=1)

    def add_coin(self):
        """ add a new coin to the set """

        self.coins.append([])

        i = len(self.coins) - 1

        form = tk.Button(self.coin_frame, text=S.SELECT_SHAPE, command=lambda i=i: self.select_shape(i))
        form.grid(row=i, column=0, sticky=tk.NSEW)
        value = tk.Entry(self.coin_frame)
        value.var = tk.StringVar()
        value.var.trace("w", lambda n, e, m, i=i: self.update_value(i))
        value.config(textvariable=value.var)
        value.grid(row=i, column=1, sticky=tk.NSEW)
        alloy = tk.Button(self.coin_frame, text="Legierung", command=lambda i=i: self.select_alloy(i))
        alloy.grid(row=i, column=2, sticky=tk.NSEW)
        delete = tk.Button(self.coin_frame, text="X", command=lambda i=i: self.delete_coin(i))
        delete.grid(row=i, column=3, sticky=tk.NSEW)
        widgets = (form, value, alloy, delete)
        self.coins[i] = {"widgets": widgets}

    def delete_coin(self, i):
        """ removes a coin """

        # destroy widgets
        widgets=self.coins[i]["widgets"]
        for widget in widgets:
            widget.destroy()

        # remove from list
        self.coins.pop(i)

        # rewrite commands and update placement ...
        for i, coin in enumerate(self.coins):
            coin["widgets"][0].config(command=lambda i=i: self.select_shape(i))
            coin["widgets"][0].grid(row=i, column=0, sticky=tk.NSEW)

            coin["widgets"][1].var.trace("w", lambda n, e, m, i=i: self.update_value(i))
            coin["widgets"][1].grid(row=i, column=1, sticky=tk.NSEW)

            coin["widgets"][2].config(command=lambda i=i: self.select_alloy(i))
            coin["widgets"][2].grid(row=i, column=2, sticky=tk.NSEW)

            coin["widgets"][3].config(command=lambda i=i: self.delete_coin(i))
            coin["widgets"][3].grid(row=i, column=3, sticky=tk.NSEW)

    def generate_shape(self, index=-1):
        coins = self.coins
        if 0 <= index < len(self.coins):
            coins = [self.coins[index]]

        for coin in self.coins:
            widgets = coin.get("widgets")
            shape = coin.get("shape")
            alloy = coin.get("alloy")
            value = coin.get("value")

            # in case no shape is defined - calculate one
            if value and alloy:
                shape = coin["shape"] = self.calculate_shape(value, alloy)

            # ...obviously we are on a total random run ...
            if not shape or shape.volume == 0:
                shape = coin["shape"] = self.random_shape()

            # update the shape button in any case ...
            shape_button = widgets[0]
            image = shape.image()
            scale = 32 / image.height
            x = int(scale * image.width)
            y = int(scale * image.height)
            image = image.resize((x, y), Image.BICUBIC)
            image = ImageTk.PhotoImage(image)
            shape_button.config(
                anchor=tk.W,
                width=300,
                text=str(shape),
                image=image,
                compound=tk.LEFT
            )
            shape_button.img = image

    def generate_value(self, index=-1):
        coins = self.coins
        if 0 <= index < len(self.coins):
            coins = [self.coins[index]]

        for coin in self.coins:
            widgets = coin.get("widgets")
            shape = coin.get("shape")
            alloy = coin.get("alloy")
            value = coin.get("value")

            # first just try to update the value ...
            if shape and alloy:
                if value:
                    if type(value) == str: value = value.replace("€", "")
                    try: value = float(value)
                    except ValueError: value = 0.0
                    new_value = self.calculate_value(shape, alloy)

                value = self.calculate_value(shape, alloy)
                text = str(round(value, 2)) + "€"
                entry = widgets[1]
                entry.delete(0, tk.END)
                entry.insert(0, text)
                continue

    def generate_alloy(self, index=-1):
        coins = self.coins
        if 0 <= index < len(self.coins):
            coins = [self.coins[index]]

        for coin in self.coins:
            widgets = coin.get("widgets")
            shape = coin.get("shape")
            alloy = coin.get("alloy")
            value = coin.get("value")

            # try to create an appropriate alloy
            if shape and value and not alloy:
                alloy = coin["alloy"] = self.calculate_alloy(shape, value)

            # should we end up here, it is the random run ... just make some alloy
            if not alloy:
                # generate random alloy
                alloy = Alloy()
                alloy.random_generation()
                alloy = coin["alloy"] = alloy

            # update text ...
            text = ""
            alloy_list = [(v, k) for k, v in alloy.alloy.items()]
            alloy_list = sorted(alloy_list, reverse=True)
            for entry in alloy_list:
                v, k = entry
                text += k + ": " + str(round(v * 100, 2)) + "% - "

            if text: text = text[:-3]
            button = widgets[2]
            button.config(text=text)

    def generate(self):
        """ calculate missing values for all coins """

        self.generate_shape()
        self.generate_alloy()
        self.generate_value()

    def calculate_value(self, shape, alloy):
        """ Calculate the value of a coin given shape and alloy
            shape (Coin): shape information for a coin
            alloy (dict): an alloy dictionary

        """

        volume = 0
        price = 0

        # calculate mass percentage
        for name, value in alloy.alloy.items():

            # adding to price
            price += value / 1000 * data.Metals.DATA[name][2]
            volume += value / data.Metals.DATA[name][1]

        try:
            density = 1 / volume
            value = price
        except ZeroDivisionError:
            density = 0
            value = 0

        coin_volume = shape.volume / 1000
        coin_mass = coin_volume * density
        coin_value = coin_mass * value

        return coin_value

    def calculate_shape(self, value, alloy):
        """ Calculate a shape that creates a coin with a given value and alloy
        Args:
            value (float): the monetary value of the coin
            alloy (Alloy): an alloy object
        Returns:
            Coin: a coin object with corresponding volume

        """

        density = 0
        metal_value = 0
        for metal, percentage in alloy.alloy.items():
            density += percentage * data.Metals.DATA[metal][1]
            metal_value += percentage * data.Metals.DATA[metal][2] / 1000

        weight = value / metal_value
        volume = weight / density
        C = CircleCoin
        R = RectCoin
        P = PolyCoin
        selection = [C(), C(), C(), R(), P()]
        coin = random.choice(selection)
        coin.generate_shape(volume)
        return coin

    def calculate_alloy(self, shape, value):
        """ create an alloy which completes a coin with given shape and value
        Args:
            shape (Coin): a coin shape object
            value (float): monetary value of the given coin
        Returns:
            Alloy: an alloy that complements shape and value of the given coin
        """

        volume = shape.volume / 1000

        alloy_value = value / volume
        alloy = Alloy()

        selection = list(set([random.randint(0, 3) for i in range(3)]))
        for i in selection: alloy.selector_add(i)
        elements = random.randint(2, 4)
        try:
            alloy.generate_from_value_cm3(alloy_value, elements)
        except ValueError as e:
            print(e)
        return alloy

    def random_shape(self):
        """ generate a random coin based on some constraints ... """

        # coin volume 0.1 - 6.1 cm³
        volume = random.choice([
            random.random() * 6,
            random.random() * 3,
            random.random() * 2,
        ]) + .1

        # shape 60% circle. 20% rect, 20% poly
        C = CircleCoin
        R = RectCoin
        P = PolyCoin
        c = random.choice([C, C, C, R, P])

        # build and return coin
        coin = c()
        coin.generate_shape(volume)
        coin.calculate_shape()
        return coin

    def select_alloy(self, number):
        """ Display the metallurgy window for a given coin
        Args:
            number (int): numeric list entry from the current coin list ...
        """

        if self.windows: self.windows.destroy()
        self.windows = MetallurgyWindow(self, number)

    def select_shape(self, number):
        """ Display the shape selection window for a given coin
        Args:
            number (int): numeric list entry from the current coin list ...
        """
        if self.windows: self.windows.destroy()
        self.windows = CoinDesignerWindow(self, number)

    def update_value(self, number):
        widget = self.coins[number]["widgets"][1]
        var = widget.var
        value = var.get()

        try:
            value = float(value)
        except ValueError:
            return

        self.coins[number]["value"] = value
