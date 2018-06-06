import tkinter as tk
from PIL import ImageTk, Image
import random
from metallurgy import MetallurgyWindow
from coindesigner import CoinDesignerWindow

from rectcoin import RectCoin
from circlecoin import CircleCoin
from polycoin import PolyCoin

import data


S = data.DE

class CoinGenerator(tk.Frame):
    """ Generate multiple coins by input or pseudo-randomly """

    def __init__(self, screen):
        super().__init__(screen)
        self.coins = []
        self.widgets = {}
        frame = tk.Frame(self)
        generate = tk.Button(frame, text=S.GENERATE_COINS, command=self.generate)
        generate.pack(fill=tk.X, expand=1)
        new = tk.Button(frame, text="Add Coin", command=self.add_coin)
        new.pack(fill=tk.X, expand=1)
        frame.pack(fill=tk.X, expand=1, anchor=tk.N)

    def add_coin(self):
        """ add a new coin to the set """

        self.coins.append([])

        i = len(self.coins) - 1

        coin = tk.Frame(self)
        form = tk.Button(coin, text=S.SELECT_SHAPE, command=lambda i=i: self.select_shape(i))
        form.config(width=20)
        form.pack(side=tk.LEFT)

        value = tk.Entry(coin)
        value.var = tk.StringVar()
        value.var.trace("w", lambda n, e, m, i=i: self.update_value(i))
        value.config(textvariable=value.var)
        value.pack(side=tk.LEFT)
        alloy = tk.Button(coin, text="Legierung", command=lambda i=i: self.select_alloy(i))
        alloy.pack(side=tk.LEFT)
        delete = tk.Button(coin, text="X", command=lambda i=i: self.delete_coin(i))
        delete.pack(side=tk.LEFT)
        coin.pack(side=tk.TOP)
        widgets = (form, value, alloy, delete)
        self.coins[i] = {"widgets": widgets}

    def delete_coin(self, i):
        """ remove a coin """

        # destroy widgets
        widgets=self.coins[i]["widgets"]
        parent_frame = widgets[0].master
        parent_frame.destroy()

        # remove from list
        self.coins.pop(i)

        # rewrite commands
        for i, coin in enumerate(self.coins):
            coin["widgets"][0].config(command=lambda i=i: self.select_shape(i))
            coin["widgets"][1].var.trace("w", lambda n, e, m, i=i: self.update_value(i))
            coin["widgets"][2].config(command=lambda i=i: self.select_alloy(i))
            coin["widgets"][3].config(command=lambda i=i: self.delete_coin(i))

    def generate(self):
        """ calculate missing values for all coins """

        for coin in self.coins:
            widgets = coin.get("widgets")
            shape = coin.get("shape")
            alloy = coin.get("alloy")
            value = coin.get("value")

            if value and alloy:
                self.calculate_shape(value, alloy)
                continue

            if not shape:
                # generate random shape
                shape = coin["shape"] = self.random_shape()

                # update text ...
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

            if shape and value:
                alloy = coin["alloy"] = self.calculate_alloy(shape, value)

                # update text ...
                text = ""
                alloy_list = [(v, k) for k, v in alloy.items()]
                alloy_list = sorted(alloy_list, reverse=True)
                for entry in alloy_list:
                    v, k = entry
                    text += k + ": " + str(round(v * 100, 2)) + "% - "

                if text: text = text[:-3]
                button = widgets[2]
                button.config(text=text)

                continue

            if not alloy:
                # generate random alloy
                alloy = coin["alloy"] = self.random_alloy()

                # update text ...
                text = ""
                alloy_list = [(v, k) for k, v in alloy.items()]
                alloy_list = sorted(alloy_list, reverse=True)
                for entry in alloy_list:
                    v, k = entry
                    text += k + ": " + str(round(v * 100, 2)) + "% - "

                if text: text = text[:-3]
                button = widgets[2]
                button.config(text=text)

            if shape and alloy:
                value = self.calculate_value(shape, alloy)
                text = str(round(value, 2)) + "$"
                entry = widgets[1]
                entry.delete(0, tk.END)
                entry.insert(0, text)

            try: coin["shape"].image()
            except: pass

    def calculate_value(self, shape, alloy):
        """ Calculate the value of a coin given shape and alloy
            shape (Coin): shape information for a coin
            alloy (dict): an alloy dictionary

        """

        volume = 0
        price = 0

        # calculate mass percentage
        for name, value in alloy.items():

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
        density = 0
        metal_value = 0
        for metal, percentage in alloy.items():
            density += percentage * data.Metals.DATA[metal][1]
            metal_value += percentage * data.Metals.DATA[metal][2] / 1000

        weight = value / metal_value
        volume = weight / density
        C = CircleCoin
        R = RectCoin
        P = PolyCoin
        selection = [C(1,1), C(1,1), C(1,1), R(1,1,1), P(1,1,1)]
        coin = random.choice(selection)
        coin.generate_shape(volume)

    @staticmethod
    def partial_alloy(metal, volume, percentage, target_value):
        """ iteration to find the volume percentage of a metal closest to the price
        Args:
            metal (str): Element Symbol of metal
            volume (float): total volume of of coin in cm³
            percentage (float): starting volume percentage 0.0 => 1.0
            target_value(float): monetary value this percentage should yield

        Returns: (price (int), metal (str), price (float))
        """

        metal_value = data.Metals.DATA[metal][2] / 1000
        density = data.Metals.DATA[metal][1]
        within_price_range = False
        price = 0
        while not within_price_range:
            percentage -= .01
            mass = percentage * volume * density
            price = mass * metal_value
            if price < target_value: within_price_range = True
            if percentage <= 0: break

        return [price, metal, percentage]

    def calculate_alloy(self, shape, value):
        """ create an alloy based on a target coin value and shape """

        # primary metal selection ...
        precious = ["Au", "Au", "Au", "Pd", "Pt"]
        medium = ["Ag", "Ag", "Ag", "Ti"]
        low = ["Cu","Cu","Cu","Cu", "Ni", "Sn"]
        filler = ["Fe", "Al"]

        main_metals = [
            random.choice(precious),
            random.choice(medium),
            random.choice(low)
        ]

        volume = shape.volume / 1000
        alloy = []

        vol = volume
        val = value
        for i in range(3):
            selection = []

            # approximate main metal and volume
            for metal in main_metals:
                selection.append(self.partial_alloy(metal, vol, 1, val))

            selection = sorted(selection)
            alloy.append(selection[-1])
            vol *= (1 - alloy[i][2])
            val -= alloy[i][0]

        # to absolute percentages
        alloy[1][2] = (1 - alloy[0][2]) * alloy[1][2]
        alloy[2][2] = (1 - alloy[0][2] - alloy[1][2]) * alloy[2][2]

        # volumetric alloy ...
        volume_alloy = {
            alloy[0][1]: round(alloy[0][2], 2),
            alloy[1][1]: round(alloy[1][2], 2),
            alloy[2][1]: round(alloy[2][2], 2),
        }
        residual = 1
        for v in volume_alloy.values(): residual -= v
        volume_alloy[random.choice(filler)] = residual

        # ... needs to be converted into a mass based alloy ...
        total_mass = 0
        for metal, percentage in volume_alloy.items():
            density = data.Metals.DATA[metal][1]
            total_mass += percentage * volume * density

        alloy = {}
        for metal, percentage in volume_alloy.items():
            density = data.Metals.DATA[metal][1]
            mass = percentage * volume * density
            percentage = round(mass/total_mass, 2)
            alloy[metal] = percentage

        return alloy

    def random_shape(self):
        """ generate a random coin based on some constraints ... """

        shape_select = random.randint(0, 100)
        if 0 <= shape_select <= 60: shape = "round"
        elif shape_select <= 80: shape = "rect"
        else: shape = "poly"

        # creating random data for the shape ...
        radius = round(5 + random.random() * 15, 2)
        inner_radius = max(0, round((random.random() - 0.3) * radius, 2))
        sides = random.choice([3,4,4,5,5,5,6,6,6,6,7,8,8])
        thickness = round(sum([random.random() for i in range(4)]), 2)
        chamfer = max(0, round(random.random() * 0.66 - 0.33, 2))

        if shape == "round":
            coin = CircleCoin(
                radius,
                thickness,
                inner_radius
            )
        elif shape == "rect":
            length = round(radius * (1 + random.random()), 2)
            width = round(radius * (1 + random.random()), 2)
            corner_radius = min([length/2-1, width/2-1, inner_radius])

            coin = RectCoin(
                length=length,
                width=width,
                thickness=thickness,
                corner_radius=corner_radius
            )
        else:
            coin = PolyCoin(
                sides,
                radius,
                thickness,
                chamfer
            )

        coin.calculate_shape()
        return coin

    def random_alloy(self):
        """ generating a mostly random alloy using some constraints"""

        # this will be the resulting alloy dict
        alloy = {}

        # selection lists for common metals, roughly sorted into three value groups
        high = ["Au", "Au", "Au", "Au", "Au", "Pt", "Pt", "Pd"]
        medium =["Ag", "Ag", "Ag", "Ag", "Ti"]
        low = ["Cu", "Cu", "Cu", "Fe", "Fe", "Al", "Sn", "Zn"]

        # creating the percentages for (up to three) metals in the alloy
        primary = min(random.randint(50, 105), 100)
        secondary = min(random.randint(0, 40), 100-primary)
        tertiary = max(0, 100-primary-secondary)
        parts = [primary, secondary, tertiary]
        parts = sorted([x for x in parts], reverse=True)

        # selecting three metal groups to smelt the alloy
        variants = [
            (high, high, high),
            (high, high, medium),
            (high, medium, medium),
            (medium, medium, high),
            (medium, medium, low),
            (medium, low, low),
            (low, low, medium),
            (low, low, low),
            (medium, low, low),
            (low, low, medium),
            (low, low, low)
        ]
        variant = random.choice(variants)

        # creating the alloy ...
        for amount, metals in zip(parts, variant):
            metal = random.choice(metals)
            amount = round(amount / 100, 2)
            if not amount: continue
            if alloy.get(metal): alloy[metal] += amount
            else: alloy[metal] = amount

        return alloy

    def select_alloy(self, number):
        """ Display the metallurgy window for a given coin
        Args:
            number (int): numeric list entry from the current coin list ...
        """

        a = MetallurgyWindow(self, number)

    def select_shape(self, number):
        a = CoinDesignerWindow(self, number)

    def update_value(self, number):
        widget = self.coins[number]["widgets"][1]
        var = widget.var
        value = var.get()

        try:
            value = float(value)
        except ValueError:
            return

        self.coins[number]["value"] = value

