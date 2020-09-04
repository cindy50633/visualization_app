import os
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import filedialog

class TestSettingsFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.setting_style = ttk.Style(self)
        self.setting_style.configure('custom.TCheckbutton', font=('Arial', 22))
        self.setting_style.configure('custom.TButton', font=('Arial', 17))
        ttk.Label(self, text='Test files type:', font=('Arial', 22, 'bold')).place(relx=0.1, rely=0.3)
        ttk.Label(self, text='Test files amount:', font=('Arial', 22, 'bold')).place(relx=0.1, rely=0.49)
        self.tap_check_btn = self.check_button(self.parent.parent.if_tap, 'tap', 0.33, 0.35)
        self.drag_check_btn = self.check_button(self.parent.parent.if_drag, 'drag', 0.4, 0.35)
        self.all_files_check_btn = self.check_button(self.parent.parent.if_all_files, 'all files in folder', 0.39, 0.55)
        self.customize_files_check_btn = self.check_button(self.parent.parent.if_customize_files, 'customize files amounts:', 0.7, 0.55)
        self.customize_files_entry = ttk.Entry(self, textvariable=self.parent.parent.customize_files_num, font=('Arial', 15), justify='c')
        self.customize_files_entry.place(relx=0.84, rely=0.55, relwidth=0.03, relheight=0.09, anchor='c')
        ttk.Button(self, text='OK', command=self.parent.destroy).place(relx=.35, rely=.82, anchor='c')
        ttk.Button(self, text='Cancel', command=self.parent.reset_test_settings).place(relx=.65, rely=.82, anchor='c')

    def check_button(self, if_check, item, x_ratio, y_ratio):
        check_button = ttk.Checkbutton(self, variable=if_check, text=item, style='custom.TCheckbutton')
        check_button.place(relx=x_ratio, rely=y_ratio, anchor='c')
        return check_button


class TestSettingWindow(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.title('Test Settings')
        self.geometry('1400x350+700+400')
        self.setting_frame = TestSettingsFrame(self)
        self.setting_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        # self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.protocol('WM_DELETE_WINDOW', self.reset_test_settings)

    def reset_test_settings(self):
        self.parent.if_tap.set(1)
        self.parent.if_drag.set(1)
        self.parent.if_all_files.set(0)
        self.parent.if_customize_files.set(1)
        self.parent.customize_files_num.set(7)
        self.destroy()
