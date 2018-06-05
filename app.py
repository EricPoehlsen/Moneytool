import tkinter as tk
import data

from metallurgy import Metallurgy
from coingenerator import CoinGenerator
from coindesigner import CoinDesigner

S = data.DE

class MainScreen(tk.Frame):
    """ The primary program class - holding some global stuff """

    def __init__(self, screen):
        super().__init__(screen)

        self.menu = tk.Menu(screen)
        screen.config(menu=self.menu)
        self.build_menu()
        current = CoinGenerator(self)
        current.pack(fill=tk.BOTH, expand=1)
        self.loaded_alloys = {}

    def build_menu(self):
        """ construction the menu ... """

        # file menu
        filemenu = tk.Menu(self.menu, tearoff=0)
        filemenu.add_command(label=S.MENU_OPEN, command=lambda: print("Open"))
        filemenu.add_command(label=S.MENU_SAVE, command=lambda: print("Save"))
        filemenu.add_separator()
        filemenu.add_command(label=S.MENU_EXIT, command=self.master.quit)
        self.menu.add_cascade(label=S.MENU_FILE, menu=filemenu)

        self.menu.add_command(label=S.MENU_ABOUT, command=lambda: print("Eric Pöhlsen"))
