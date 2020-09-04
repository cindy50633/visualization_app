import os
import pathlib
import pickle
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import filedialog

from ExportSettingWindow import SettingsFrame
from error_window import error_window

class DBSettingsFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.script_path = self.parent.parent.script_path
        self.user_entry = self.db_info_entry(0.3, 0)
        self.password_entry = self.db_info_entry(0.3, 0.15)
        self.port_entry = self.db_info_entry(0.3, 0.3)
        self.host_entry = self.db_info_entry(0.3, 0.45)
        self.database_entry = self.db_info_entry(0.3, 0.6)
        ttk.Button(self, text='OK', command=self.save_db_settings).place(relx=0, rely=.9)
        ttk.Button(self, text='Cancel', command=self.parent.destroy).place(relx=.4, rely=.9)
        self.db_settings_dict = SettingsFrame.load_settings(self.script_path, 'db_settings.pickle')
        self.get_db_info_label()
        self.write_previous_db_settings()


    def get_db_info_label(self):
        self.db_info_label('User:', 0, 0)
        self.db_info_label('Password:', 0, 0.15)
        self.db_info_label('Port:', 0, 0.3)
        self.db_info_label('Host:', 0, 0.45)
        self.db_info_label('Database:', 0, 0.6)

    def db_info_label(self, info, x_ratio, y_ratio):
        label = ttk.Label(self, text=info, font=('Arial', 16, 'bold'), anchor='c')
        label.place(relx=x_ratio, rely=y_ratio)

    def db_info_entry(self, x_ratio, y_ratio):
        entry = ttk.Entry(self, font=('Arial', 16, 'bold'))
        entry.place(relx=x_ratio, rely=y_ratio, relwidth=0.35)
        return entry

    def save_db_settings(self):
        db_settings = {
                       'user': self.user_entry.get(),
                       'password': self.password_entry.get(),
                       'port': self.port_entry.get(),
                       'host': self.host_entry.get(),
                       'database': self.database_entry.get()
                      }
        if all(db_settings.values()):
            with open(os.path.join(self.script_path, 'db_settings.pickle'), 'wb') as handle:
                pickle.dump(db_settings, handle, protocol=pickle.HIGHEST_PROTOCOL)
                self.parent.destroy()
        else:
            error_window('Lack of DB Information', 'Please fill all the blanks!')

    def write_previous_db_settings(self):
        if self.db_settings_dict:
            self.user_entry.insert(0, self.db_settings_dict['user'])
            self.password_entry.insert(0, self.db_settings_dict['password'])
            self.port_entry.insert(0, self.db_settings_dict['port'])
            self.host_entry.insert(0, self.db_settings_dict['host'])
            self.database_entry.insert(0, self.db_settings_dict['database'])
        return self.db_settings_dict

class DBSettingWindow(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.title('DB Settings')
        self.geometry('500x600+700+400')
        self.setting_frame = DBSettingsFrame(self)
        self.setting_frame.place(relx=0.2, rely=0.2, relwidth=0.8, relheight=0.8)
        # self.main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        # self.protocol('WM_DELETE_WINDOW', self.close_btn_press)
