import tkinter as tk
from tkinter import ttk


class CustomEntry(ttk.Entry):
    '''A ttk entry with red background'''
    def __init__(self, parent, *args, **kwargs):
        # kwargs['style'] = 'CustomEntry'
        # self.__initialize_custom_style()
        ttk.Entry.__init__(self, parent, *args, **kwargs)

    def initialize_custom_style(self, background_color):
        style = ttk.Style()
        style.configure('CustomEntry', foreground='white', fieldbackground=background_color)
        style.layout('CustomEntry',
            [('Entry.plain.field',
                {'children': [('Entry.background',
                    {'children': [('Entry.padding',
                        {'children': [('Entry.textarea', {'sticky': 'nswe'})],
                         'sticky': 'nswe'})],
                     'sticky': 'nswe'})],
                 'border': '2',
                 'sticky': 'nswe'})])

    def red_background(self, background_color='red'):
        self.initialize_custom_style(background_color)
        self['style'] = 'CustomEntry'
        # style = ttk.Style()
        # style.configure('CustomEntry', foreground='white', fieldbackground='black')

    def white_background(self, background_color='white'):
        self.initialize_custom_style(background_color)
        self['style'] = 'CustomEntry'
root_window = tk.Tk()

entry_v = tk.StringVar()
entry = CustomEntry(root_window, textvariable=entry_v)
entry.red_background()
entry2 = CustomEntry(root_window, textvariable=entry_v)
entry3 = ttk.Entry(root_window, textvariable=entry_v, background='red', highlightcolor='red')
entry2.white_background()

entry.pack(padx=10, pady=10)
entry2.pack(padx=20, pady=20)
entry3.pack(padx=30, pady=30)
root_window.mainloop()
