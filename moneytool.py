import tkinter as tk
from app import MainScreen

if __name__ == '__main__':

    main = tk.Tk()
    main.geometry("800x600")
    screen = MainScreen(main)
    screen.pack()
    main.mainloop()

