import os
import pathlib
import pickle
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import filedialog

from PathFrame import PathFrame

class SettingsFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.setting_style = ttk.Style(self)
        self.setting_style.configure('custom.TCheckbutton', font=('Arial', 16))
        self.setting_style.configure('custom.TButton', font=('Arial', 17))
        ttk.Label(self, text='Export Folder Path:', font=('Arial', 19, 'bold')).place(relx=0.04, rely=0.2)
        ttk.Label(self, text='Select export files:', font=('Arial', 19, 'bold')).place(relx=0.1, rely=0.49)
        self.export_btn = ttk.Button(self, text='...', command=self.set_export_path, style='custom.TButton')
        self.export_btn.place(relx=0.9, rely=0.2, relwidth=0.03, relheight=0.1)
        self.export_folder_entry = ttk.Entry(self, font=('Arial', 21))
        self.export_folder_entry.place(relx=0.25, rely=0.2, relwidth=0.65, relheight=0.1)
        self.if_all_tabs =  tk.IntVar()
        self.if_summary =  tk.IntVar()
        self.if_detail = tk.IntVar()
        self.if_fig = tk.IntVar()
        self.if_all_tabs_btn = self.check_button(self.if_all_tabs, 'export all tabs: only export current tab result if not checked', 0.48, 0.55)
        self.summary_check_btn = self.check_button(self.if_summary, 'summary csv file', 0.38)
        self.detail_check_btn = self.check_button(self.if_detail, 'detail csv file', 0.51)
        self.fig_check_btn = self.check_button(self.if_fig, 'figure file',  0.61)
        ttk.Button(self, text='OK', command=self.save_export_settings).place(relx=.35, rely=.85, anchor='c')
        ttk.Button(self, text='Cancel', command=self.parent.destroy).place(relx=.65, rely=.85, anchor='c')
        self.script_path = self.parent.parent.script_path
        self.export_settings_dict = self.load_settings(self.script_path)
        self.write_previous_settings()

    def check_button(self, if_check, item, x_ratio, y_ratio=0.65):
        print(if_check)
        check_button = ttk.Checkbutton(self, variable=if_check, text=item, style='custom.TCheckbutton')
        check_button.place(relx=x_ratio, rely=y_ratio, anchor='c')
        return check_button

    def clear_export_path(self):
        self.export_folder_entry.delete(0, tk.END)

    def set_export_path(self):
        self.clear_export_path()
        export_path = filedialog.askdirectory()
        self.export_folder_entry.insert(0, export_path)
        self.parent.lift()
        # return self.export_folder_entry.get()

    @staticmethod
    def load_settings(folder, file='export_settings.pickle'):
        pickle_path = os.path.join(folder, file)
        if os.path.isfile(pickle_path):
            with open(pickle_path, 'rb') as handle:
                settings_dict = pickle.load(handle)
                return settings_dict

    def save_export_settings(self):
        with open(os.path.join(self.script_path, 'export_settings.pickle'), 'wb') as handle:
            export_settings = {
                               'export_path': self.export_folder_entry.get(),
                               'if_all_tabs': self.if_all_tabs.get(),
                               'if_summary': self.if_summary.get(),
                               'if_detail': self.if_detail.get(),
                               'if_fig': self.if_fig.get()
                               }
            pickle.dump(export_settings, handle, protocol=pickle.HIGHEST_PROTOCOL)
            self.parent.destroy()

    def write_previous_settings(self):
        if self.export_settings_dict:
            self.clear_export_path()
            self.export_folder_entry.insert(0, self.export_settings_dict['export_path'])
            self.if_all_tabs.set(self.export_settings_dict['if_all_tabs'])
            self.if_summary.set(self.export_settings_dict['if_summary'])
            self.if_detail.set(self.export_settings_dict['if_detail'])
            self.if_fig.set(self.export_settings_dict['if_fig'])

class ExportSettingWindow(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.title('Export Settings')
        self.geometry('1400x350+700+400')
        self.setting_frame = SettingsFrame(self)
        self.setting_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        # self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        # self.protocol('WM_DELETE_WINDOW', self.close_btn_press)
