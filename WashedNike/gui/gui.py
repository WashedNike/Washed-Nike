from tkinter import *
from tkinter import ttk
from tkinter.ttk import *

class Bot(Frame):
    def __init__(self, main):
        Frame.__init__(self, main)
        self.main = main
        f = GradientFrame(window)
        f.pack(fill=BOTH, expand=True)


class GradientFrame(Canvas):
    def __init__(self, main, borderwidth=1, relief="sunken"):
        Canvas.__init__(self, main, borderwidth=1, relief="sunken")
        self.main = main
        main.title("Washed Nike")
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()
        window.geometry("%dx%d" % (width, height))
        window.resizable(True, True)
        self._color1 = "#36393E"
        self._color2 = "#36393E"
        self.bind("<Configure>", self._draw_gradient)


    def _draw_gradient(self, main, event=None):
        self.delete("gradient")
        self.main = main
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        limit = width
        (r1,g1,b1) = self.winfo_rgb(self._color1)
        (r2,g2,b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
            self.create_line(i,0,i,height, tags=("gradient",), fill=color)
        self.lower("gradient")

if __name__ == "__main__":
    window = Tk()
    window.title("Washed Nike")
    Bot(window)
    window.mainloop()