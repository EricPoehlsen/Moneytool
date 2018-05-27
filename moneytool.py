import tkinter as tk
from metallurgy import Metallurgy
from app import MainScreen

if __name__ == '__main__':

    main = tk.Tk()
    main.geometry("1024x768")
    main.title("Money Tool")
    screen = MainScreen(main)
    screen.pack()
    main.mainloop()
    
