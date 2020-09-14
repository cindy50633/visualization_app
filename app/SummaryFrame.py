import tkinter as tk
from tkinter import ttk
from tkinter import font


class SummaryFrame(tk.Frame):
    def __init__(self, parent, summary_dict={}, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.summary_dict = summary_dict
        self.summary_style = ttk.Style()
        self.summary_style.configure('.', font=('Arial', 14))

    def summary_label(self, summary_label, x_ratio, y_ratio):
        label = ttk.Label(self, text=summary_label)
        label.place(relx=x_ratio, rely=y_ratio)

    def get_result_summary(self):
        y_ratio = 0
        for label, value in self.summary_dict.items():
            self.summary_label(label+':', 0, y_ratio)
            self.summary_label(str(value), 0.75, y_ratio)
            y_ratio += 0.08
