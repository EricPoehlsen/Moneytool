import tkinter as tk
import random
from metallurgy import MetallurgyWindow
from coindesigner import CoinDesignerWindow

from rectcoin import RectCoin
from circlecoin import CircleCoin
from polycoin import PolyCoin

import data


S = data.DE

class CoinGenerator(tk.Frame):
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
        self.coins.append([])

        i = len(self.coins) - 1

        coin = tk.Frame(self)
        form = tk.Button(coin, text="Form", command=lambda i=i: self.select_shape(i))
        form.config(width=20)
        form.pack(side=tk.LEFT)

        value = tk.Entry(coin)
        value.pack(side=tk.LEFT)
        alloy = tk.Button(coin, text="Legierung", command=lambda i=i: self.select_alloy(i))
        alloy.pack(side=tk.LEFT)
        coin.pack(side=tk.TOP)
        widgets = (form, value, alloy)
        self.coins[i] = {"widgets": widgets}

    def generate(self):
        for coin in self.coins:
            widgets = coin.get("widgets")
            shape = coin.get("shape")
            alloy = coin.get("alloy")
            value = coin.get("value")

            if shape and alloy:
                self.calculate_value(shape, alloy)

            if shape and value:
                self.calculate_alloy(shape, value)

            if value and alloy:
                self.calculate_shape(value, alloy)

            if not coin.get("shape"):
                coin["shape"] = self.random_shape()

                shape_button = widgets[0]
                shape_button.config(text=str(coin["shape"]))

            if not coin.get("alloy"):
                coin["alloy"] = self.random_alloy()

    def calculate_value(self, shape, alloy):
        """ Calculate the value of a coin given shape and alloy
            shape (Coin): shape information for a coin

        """
        pass

    def calculate_shape(self, value, alloy):
        pass

    def calculate_alloy(self, shape, value):
        pass

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

        print(number)
        a = MetallurgyWindow(self)

    def select_shape(self, number):
        a = CoinDesignerWindow(self, number)

