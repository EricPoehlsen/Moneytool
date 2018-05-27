import tkinter as tk
from rectcoin import RectCoin
from circlecoin import CircleCoin
from polycoin import PolyCoin

import data


S = data.DE

class CoinGenerator(tk.Frame):
    def __init__(self, screen):

        super().__init__(screen)

        self.widgets = {}
        new = tk.Button(self, text="Add Coin", command=self.add_coin)
        new.pack(fill=tk.X, expand=1)

    def add_coin(self):
        if not self.widgets.get("coins"):
            self.widgets["coins"] = []

        coins = self.widgets["coins"]
