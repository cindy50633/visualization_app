import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


class ImgFrame(tk.Frame):
    def __init__(self, parent, fig_dict={}, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.fig_dict = fig_dict
        self.var = tk.StringVar()

    def get_result_fig(self):
        radio_style = ttk.Style()
        radio_style.configure('img.TRadiobutton')
        x_ratio = 0
        default_fig_bool = False
        for fig, ax in self.fig_dict.items():
            title = ax.get_title()
            self.var.set(title) if default_fig_bool is False else ''
            default_fig_bool = self.update_fig(fig) if default_fig_bool is False else True
            ttk.Radiobutton(self, value=title, variable=self.var, command=lambda fig = fig: self.update_fig(fig)).place(relx=x_ratio, rely=0.97)
            x_ratio += 0.1

    def update_fig(self, fig):
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        canvas.get_tk_widget().place(relx=0, rely=0, relwidth=1, relheight=0.95)
        return True
