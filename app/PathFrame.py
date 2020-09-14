import os
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import filedialog

from app_setting.error_window import error_window


class PathFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.path_style = ttk.Style()
        self.folder_label = self.path_label('Project Folder:', 0, 0.05)
        self.folder_entry = self.path_entry(0.13, 0)
        self.folder_btn = self.path_btn(0.97, 0, self.set_folder_path)
        self.files_label = self.path_label('Raw Data Files:', 0, 0.65)
        self.files_entry = self.path_entry(0.13, 0.6)
        self.files_btn = self.path_btn(0.97, 0.6, self.set_files_path)
        # self.export_label = self.path_label('Raw Data Files:', 0, 0.85)
        # self.export_entry = self.path_entry(0.13, 0.8)
        # self.folder_path = self.folder_entry.get()
        # self.files_path = self.files_entry.get()

    def path_label(self, path_type, x_ratio, y_ratio):
        label = ttk.Label(self, text=path_type, font=('Arial', 22, 'bold'))
        label.place(relx=x_ratio, rely=y_ratio)

    def path_entry(self, x_ratio, y_ratio):
        entry = ttk.Entry(self, font=('Arial', 21))
        entry.place(relx=x_ratio, rely=y_ratio, relwidth=0.84, relheight=0.4)
        return entry

    def path_btn(self, x_ratio, y_ratio, command_function):
        self.path_style.configure('path.TButton', font=('Arial', 18))
        btn = ttk.Button(self, text='...', style='path.TButton', command=command_function)
        btn.place(relx=x_ratio, rely=y_ratio, relwidth=0.03, relheight=0.4)

    def clear_folder_path(self):
        self.folder_entry.delete(0, tk.END)
        # self.folder_path = ''

    def clear_files_path(self):
        self.files_entry.delete(0, tk.END)

    def set_folder_path(self):
        self.clear_folder_path()
        self.folder_entry.insert(0, filedialog.askdirectory())
        return self.folder_entry.get()

    def set_default_folder_path(self, default_folder_path):
        self.clear_folder_path()
        self.folder_entry.insert(0, default_folder_path)
        return self.folder_entry.get()

    def get_folder_path(self):
        return self.folder_entry.get()

    def set_files_path(self):
        self.clear_files_path()
        files_path_tuple = filedialog.askopenfilenames()
        if files_path_tuple:
            all_file_path = ''
            filename = ''
            for file_path in files_path_tuple:
                if os.path.basename(file_path)[-4:] != '.csv':
                    self.clear_files_path()
                    error_window('File Type Error', 'Please select .csv files!')
                    raise
                all_file_path += file_path + ', '
                filename += os.path.basename(file_path) + ', '
            self.files_entry.insert(0, all_file_path[:-2])  # remove the last space
        return self.get_files_path()

    def get_files_path(self):
        return self.files_entry.get()

    def check_path_valid(self, file_type, tap_filename, horizontal_filename, diagonal_filename, vertical_filename, customize_files_num):
        def __find_raw_data(file_type, path, files):
            # case of file path
            if files:
                found_filename_arr = files.split(', ')
                for _, found_filename in enumerate(found_filename_arr):
                    if not os.path.exists(found_filename):
                        error_window('File Not Found', 'The path selected is not valid!\nPlease check the input path again!', size='600x150', shift='+1000+700')
                        raise FileNotFoundError
                return found_filename_arr
            # case of folder path
            else:
                try:
                    raw_files_arr = [basename for basename in os.listdir(path) if str.isdigit(basename[-18:-4])]
                except FileNotFoundError:
                    error_window('File Not Found', 'The path selected is not valid!\nPlease check the input path again!', size='600x150', shift='+1000+700')
                    raise FileNotFoundError
                valid_file_type_arr = [file.endswith(file_type) for file in raw_files_arr]
                # valid_filename_arr = [file if keyword in file.lower() else False for file in raw_files_arr]
                valid_tap_arr = [file if tap_filename in file.lower() else False for file in raw_files_arr]
                valid_horizontal_arr = [file if horizontal_filename in file.lower() else False for file in raw_files_arr]
                valid_diagonal_arr = [file if diagonal_filename in file.lower() else False for file in raw_files_arr]
                valid_vertical_arr = [file if vertical_filename in file.lower() else False for file in raw_files_arr]
                valid_filename_arr = [files[0] or files[1] or files[2] or files[3] if any(files) else False for files in zip(valid_tap_arr, valid_horizontal_arr, valid_diagonal_arr, valid_vertical_arr)]
                valid_file_arr = [type and name for type, name in zip(valid_file_type_arr, valid_filename_arr)]
                all_found_filename_arr = [file for file in valid_file_arr if file != False]
                all_found_filename_arr = [os.path.join(path, file) for file in all_found_filename_arr]
                # filename_arr = [file for file in valid_file_arr if file != False]
                # use getmtime instead of getctime because copy files will change created time on windows
                all_found_filename_arr.sort(key=os.path.getmtime, reverse=True)
                found_filename_arr = all_found_filename_arr[0:customize_files_num]
                print('found_filename_arr = ' + str(found_filename_arr))
                return found_filename_arr

        folder_path = self.get_folder_path()
        files_path = self.get_files_path()
        if folder_path == '' and files_path == '':
            error_window('File Number Error', 'Please select at least one file or folder!', size='570x150')
            raise FileNotFoundError
        found_filename_arr = __find_raw_data(file_type=file_type, path=folder_path, files=files_path)
        return found_filename_arr
