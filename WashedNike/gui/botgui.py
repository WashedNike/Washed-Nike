from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

from gui.settings import Settings
from gui.productman import ProductMan
from gui.profileman import ProfileMan


class Bot(Frame):
    def __init__(self, main):
        self.main = main
        width = main.winfo_screenwidth()
        height = main.winfo_screenheight()
        main.geometry("%dx%d" % (width, height))
        main.configure(background='#36393e')
        main.resizable(True, True)


    


if __name__ == "__main__":
    window = Tk()
    window.title("Washed Nike")
    Bot(window)
    window.mainloop()