import ctypes
import platform
import tkinter as tk
from tkinter import ttk
from tkinter import font

from ImgFrame import ImgFrame
from SummaryFrame import SummaryFrame
from CustomNotebook import CustomNotebook


class ResultFrame(tk.Frame):
    def __init__(self, parent, summary_dict, fig_dict, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        # self.file = file
        self.summary_frame = SummaryFrame(self, summary_dict)
        self.summary_frame.place(relx=.03, rely=.35, relwidth=0.17, relheight=0.55)
        self.img_window = ImgFrame(self, fig_dict)
        self.img_window.place(relx=.25, rely=.10, relwidth=0.72, relheight=0.85)
        self.get_result()
        print('in result frame init')

    def get_result(self):
        self.summary_frame.get_result_summary()
        self.img_window.get_result_fig()

# class ResultTab(CustomNotebook):
class ResultTab(CustomNotebook):
    def __init__(self, parent, *args, **kwargs):
        # ttk.Notebook.__init__(self, parent, *args, **kwargs)
        super().__init__(parent, *args, **kwargs)
        self.place(relx=0.02, rely=0.15, relwidth=0.96, relheight=0.83)
        print('in result tab init')
        self.file_summary_dict = {}
        self.file_summary_df = {}
        self.file_detail_df = {}
        self.file_fig_dict = {}
        self.bind('<ButtonPress-1>', super().close_btn_press, True)
        self.bind('<ButtonRelease-1>', super().close_btn_release)

        # print(self.tab(self.select(), 'text'))
        #tabs.tab('current', text=['Options'])
    def add_result(self, tabname, summary_dict, fig_dict):
        result_frame = ResultFrame(self, summary_dict, fig_dict)
        self.add(result_frame, text=tabname)

    def get_current_tab_name(self):
        current_tab_name = self.tab(self.select(), 'text')
        return current_tab_name

    def get_all_tab_names(self):
        return [self.tab(name, option='text') for name in self.tabs()]

    def set_result(self, new_file_summary_dict, new_file_summary_df, new_file_detail_df, new_file_fig_dict):
        self.file_summary_dict = {**self.file_summary_dict, **new_file_summary_dict}
        self.file_summary_df = {**self.file_summary_df, **new_file_summary_df}
        self.file_detail_df = {**self.file_detail_df, **new_file_detail_df}
        self.file_fig_dict = {**self.file_fig_dict, **new_file_fig_dict}

    def get_file_summary_dict(self):
        return self.file_summary_dict

    def get_file_summary_df(self):
        return self.file_summary_df

    def get_file_detail_df(self):
        return self.file_detail_df

    def get_file_fig_dict(self):
        return self.file_fig_dict

    def close_btn_press(self, event):
        print('press!!')

    def close_btn_release(self, event):
        print('release!!')
