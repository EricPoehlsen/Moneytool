import tkinter as tk
from metallurgy import Metallurgy
from app import MainScreen

if __name__ == '__main__':

    main = tk.Tk()
    main.title("Money Tool")
    main.geometry("800x600")
    screen = MainScreen(main)
    screen.pack(fill=tk.BOTH, expand=1)
    main.mainloop()
    
