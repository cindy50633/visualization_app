import tkinter as tk
from tkinter import ttk
from tkinter import font


def error_window(title, content, size='350x150', shift='+1000+700'):
    error_window = tk.Tk()
    error_window.geometry(size+shift)
    error_window.wm_title(title)
    error_window.attributes('-toolwindow', 1)
    error_label = ttk.Label(error_window, text=content, font=('Arial', 19))
    error_label.place(relx=.5, rely=.3, anchor='c')
    error_btn = ttk.Button(error_window, text='OK', command=error_window.destroy)
    # error_btn.place(relx=0.28, rely=0.5)
    error_btn.place(relx=.5, rely=.7, anchor='c')
    error_window.mainloop()
