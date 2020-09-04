import ctypes
import platform
import tkinter as tk

from PathFrame import PathFrame
from ImgFrame import ImgFrame
from SummaryFrame import SummaryFrame
from BtnFrame import BtnFrame


class MainFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # self.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.make_dpi_aware()
        self.path_frame = PathFrame(self)
        print(self.path_frame.folder_path)
        self.path_frame.place(relx=.05, rely=.015, relwidth=0.92, relheight=0.08)
        self.img_window = ImgFrame(self)
        self.img_window.place(relx=.25, rely=.14, relwidth=0.72, relheight=0.80)
        self.summary_window = SummaryFrame(self)
        self.summary_window.place(relx=.05, rely=.48, relwidth=0.15, relheight=0.46)
        self.btn_window = BtnFrame(self, self.path_frame, self.summary_window, self.img_window)
        self.btn_window.place(relx=.05, rely=.14, relwidth=0.15, relheight=0.3)

    @staticmethod
    def make_dpi_aware():
        if int(platform.release()) >= 8:
            ctypes.windll.shcore.SetProcessDpiAwareness(True)
