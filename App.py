print('Start App')
import os
import base64
import ctypes
import pathlib
import platform
import pickle
import tkinter as tk
from tkinter import ttk

from PathFrame import PathFrame
from BtnFrame import BtnFrame
from get_logo import get_logo

class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.script_path = self.parent.script_path
        # self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.make_dpi_aware()
        self.path_frame = PathFrame(self)
        self.path_frame.place(relx=.05, rely=.012, relwidth=0.92, relheight=0.08)
        self.btn_frame = BtnFrame(self, self.path_frame)
        self.btn_frame.place(relx=.05, rely=0.20, relwidth=0.15, relheight=0.2)
        self.user = ttk.Label(text=('User: '+os.getlogin()), anchor='c').place(relx=0.05, rely=0.9, relwidth=0.15, relheight=0.04)

    def save_folder_settings(self):
        folder_path = self.path_frame.get_folder_path()
        with open(os.path.join(self.script_path, 'path.pickle'), 'wb') as handle:
            pickle.dump(folder_path, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load_settings(self, file='path.pickle'):
        pickle_path = os.path.join(self.script_path, file)
        if os.path.isfile(pickle_path):
            with open(pickle_path, 'rb') as handle:
                folder_path = pickle.load(handle)
                self.path_frame.set_default_folder_path(folder_path)

    @staticmethod
    def make_dpi_aware():
        if int(platform.release()) >= 8:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self)
        self.geometry('1920x1440')
        self.script_path = pathlib.Path(__file__).parent.absolute()
        self.main_frame = MainFrame(self)
        self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.main_frame.load_settings()
        self.protocol('WM_DELETE_WINDOW', self.close_btn_press)
        self.get_window_logo(self)

    @staticmethod
    def get_window_logo(parent):
        icon_data = base64.b64decode(get_logo())
        temp_file = 'icon.ico'
        with open(temp_file, 'wb') as icon_file:
            icon_file.write(icon_data)
        parent.wm_iconbitmap(temp_file)
        os.remove(temp_file)

    def close_btn_press(self):
        # print('press')
        self.main_frame.save_folder_settings()
        self.destroy()

if __name__ == "__main__":
    main = MainWindow()
    main.title('Test Tool Trial')
    main.mainloop()
