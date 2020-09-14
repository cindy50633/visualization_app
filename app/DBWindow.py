import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkinter import font
from tkinter import filedialog

from run.write_db import insert_db
from app_setting.error_window import error_window


class ResultDBFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.tap_label_arr = ['all_max(mm)', 'all_mean(mm)', 'without_edge_max(mm)', 'without_edge_mean(mm)', 'all_max_jitter(mm)', 'jitter_ratio(%)', 'detected_ratio(%)']
        self.drag_label_arr = ['max_linearity(mm)', 'mean_linearity(mm)', 'max_drag_ratio(%)', 'min_drag_ratio(%)', 'break_line_count']
        self.get_title_label()
        self.get_spec_label()

    def get_title_label(self):
        self.title_label('Test Data', 24, 0.4, 0)
        self.title_label('Tap', 21, 0.15, 0.12)
        x_ratio = 0.5
        for title in ['Horizontal', 'Vertical', 'Diagonal']:
            self.title_label(title, 21, x_ratio, 0.12)
            x_ratio += 0.2

    def get_spec_label(self):
        y_ratio=0.2
        for spec in self.tap_label_arr:
            self.spec_label(spec, 0.05,  y_ratio)
            y_ratio += 0.1
        y_ratio=0.2
        for spec in self.drag_label_arr:
            self.spec_label(spec, 0.37,  y_ratio)
            y_ratio += 0.1

    def title_label(self, title, font_size, x_ratio, y_ratio):
        label = ttk.Label(self, text=title, font=('Arial', font_size, 'bold'), anchor='c')
        label.place(relx=x_ratio, rely=y_ratio)

    def spec_label(self, spec, x_ratio, y_ratio):
        label = ttk.Label(self, text=spec)
        label.place(relx=x_ratio, rely=y_ratio)

    def value_label(self, value, x_ratio, y_ratio):
        label = ttk.Label(self, text=value)
        label.place(relx=x_ratio, rely=y_ratio)

    # currently not used
    def get_detail_result_db(self, file_summary_dict):
        detail_db_dict = {}
        def __get_each_db(type, label_arr, summary_dict, x_ratio, y_ratio_start=0.2):
            each_db_dict = {}
            for spec in label_arr:
                value = summary_dict[spec]
                each_db_dict[type+spec] = value
                # self.value_label(str(value), x_ratio, y_ratio_start)
                # y_ratio_start += 0.1
            return each_db_dict
        needed_file_key_arr = ['tap', 'hori100', 'hori200', 'vert100', 'vert200', 'diag100', 'diag200']
        x_ratio_arr = [0.14, 0.36, 0.46, 0.56, 0.66, 0.76, 0.86]
        for index, key in enumerate(needed_file_key_arr):
            if 'tap' in key:
                label_arr = self.tap_label_arr
            else:
                label_arr = self.drag_label_arr
            for filename, summary_dict in file_summary_dict.items():
                if key in filename.lower():
                    each_db_dict = __get_each_db(filename+'_', label_arr, summary_dict, x_ratio_arr[index])
                    detail_db_dict = {**detail_db_dict, **each_db_dict}
        print(detail_db_dict)
        return detail_db_dict

    def get_summary_result_db(self, file_summary_dict):
        summary_db_dict = {}
        def __get_each_db(type_key, label_arr, summary_dict, x_ratio, y_ratio_start=0.2):
            if 'tap' in type_key:
                for spec in label_arr:
                    value = summary_dict[spec]
                    summary_db_dict[spec] = value
                    self.value_label(str(value), x_ratio, y_ratio_start)
                    y_ratio_start += 0.1
            else:
                print('in')
                get_min_key_arr = 'min_drag_ratio'
                get_mean_key = 'mean_linearity'
                get_sum_key = 'break_line_count'
                for spec in label_arr:
                    value = summary_dict[spec]
                    if summary_db_dict.get(type_key+'_'+spec):
                        if spec == get_min_key_arr:
                            summary_db_dict[type_key+'_'+spec] = value if value < summary_db_dict[type_key+'_'+spec] else summary_db_dict[type_key+'_'+spec]
                        elif spec == get_mean_key:
                            print(summary_db_dict[type_key+'_'+spec])
                            value = float(value)
                            previous_value = float(summary_db_dict[type_key+'_'+spec])
                            summary_db_dict[type_key+'_'+spec] = round((value+previous_value)/2, 2)
                        elif spec == get_sum_key:
                            print(summary_db_dict[type_key+'_'+spec])
                            summary_db_dict[type_key+'_'+spec] = int(float(value) + float(summary_db_dict[type_key+'_'+spec]))
                            print(summary_db_dict[type_key+'_'+spec])
                        else:
                            summary_db_dict[type_key+'_'+spec] = value if value > summary_db_dict[type_key+'_'+spec] else summary_db_dict[type_key+'_'+spec]
                        self.value_label(str(value), x_ratio, y_ratio_start)
                        y_ratio_start += 0.1
                    else:
                        summary_db_dict[type_key+'_'+spec] = value
            return summary_db_dict

        needed_file_key_arr = ['tap', 'hori', 'vert', 'diag']
        x_ratio_arr = [0.22, 0.52, 0.72, 0.92]
        for index, key in enumerate(needed_file_key_arr):
            if 'tap' in key:
                label_arr = self.tap_label_arr
            else:
                label_arr = self.drag_label_arr
            for filename, summary_dict in file_summary_dict.items():
                if key in filename.lower():
                    __get_each_db(key, label_arr, summary_dict, x_ratio_arr[index])
        print(summary_db_dict)
        return summary_db_dict


class InfoDBFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.get_info_label()
        self.info_db_dict = {}
        self.test_date = datetime.now().strftime('%Y-%m-%d')
        self.testing = os.getlogin()
        self.project_name_entry = self.info_entry(0.3, 0.15)
        self.part_number_entry = self.info_entry(0.3, 0.23)
        self.dut_level_entry = self.info_entry(0.3, 0.31)
        self.ic_vendor_entry = self.info_entry(0.3, 0.39)
        self.ic_model_entry = self.info_entry(0.3, 0.47)
        self.config_file_entry = self.info_entry(0.3, 0.55)
        self.tuning_entry = self.info_entry(0.3, 0.63)
        self.testing_entry = self.info_entry(0.3, 0.71)
        self.test_date_entry = self.info_entry(0.3, 0.79)
        self.remark = tk.Text(self, font=('Arial', 19))
        self.remark.place(relx=0, rely=0.92, relwidth=0.7, relheight=0.08)
        self.info_db_dict = self.parent.info_db_dict
        self.get_default_info()

    def get_default_info(self):
        if self.info_db_dict:
            self.project_name_entry.insert(0, self.info_db_dict['project']),
            self.part_number_entry.insert(0, self.info_db_dict['part_no']),
            self.dut_level_entry.insert(0, self.info_db_dict['dut_lv']),
            self.ic_vendor_entry.insert(0, self.info_db_dict['ic_vender']),
            self.ic_model_entry.insert(0, self.info_db_dict['ic_model']),
            self.config_file_entry.insert(0, self.info_db_dict['config_file']),
            self.tuning_entry.insert(0, self.info_db_dict['tuning']),
            self.testing_entry.insert(0, self.info_db_dict['testing']),
            self.test_date_entry.insert(0, self.info_db_dict['test_date'])
        else:
            self.testing_entry.insert(0, self.testing)
            self.test_date_entry.insert(0, self.test_date)
        self.testing_entry.config(state='disabled')
        self.test_date_entry.config(state='disabled')

    def get_info_db_dict(self):
        self.info_db_dict = {
                         'project': self.project_name_entry.get(),
                         'part_no': self.part_number_entry.get(),
                         'dut_lv': self.dut_level_entry.get(),
                         'ic_vender': self.ic_vendor_entry.get(),
                         'ic_model': self.ic_model_entry.get(),
                         'config_file': self.config_file_entry.get(),
                         'tuning': self.tuning_entry.get(),
                         'testing': self.testing,
                         'test_date': self.test_date,
                         'remark': self.remark.get('1.0', tk.END)
                         }
        # set button frame's info_db_dict
        self.parent.parent.parent.info_db_dict = self.info_db_dict
        return self.info_db_dict

    def get_info_label(self):
        self.title_label('Test Information', 24, 0.15, 0)
        self.info_label('Project Name:', 0, 0.15)
        self.info_label('Part Number:', 0, 0.23)
        self.info_label('DUT Level:', 0, 0.31)
        self.info_label('IC Vendor:', 0, 0.39)
        self.info_label('IC Model:', 0, 0.47)
        self.info_label('Config File:', 0, 0.55)
        self.info_label('Tuning:', 0, 0.63)
        self.info_label('Testing:', 0, 0.71)
        self.info_label('Date:', 0, 0.79)
        self.info_label('Remark:', 0, 0.87)

    def title_label(self, title, font_size, x_ratio, y_ratio):
        label = ttk.Label(self, text=title, font=('Arial', font_size, 'bold'), anchor='c')
        label.place(relx=x_ratio, rely=y_ratio)

    def info_label(self, table_title, x_ratio, y_ratio):
        label = ttk.Label(self, text=table_title, font=('Arial', 16, 'bold'))
        label.place(relx=x_ratio, rely=y_ratio)

    def info_entry(self, x_ratio, y_ratio):
        entry = ttk.Entry(self, font=('Arial', 19))
        entry.place(relx=x_ratio, rely=y_ratio, relwidth=0.4)
        return entry


class ExportDBFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args, **kwargs)
        self.red_entry_style = ttk.Style()
        self.red_entry_style.configure('red.TEntry',fieldbackground='red')
        self.parent = parent
        self.file_summary_dict = self.parent.file_summary_dict
        self.db_dict = {}
        self.info_db_dict = self.parent.info_db_dict
        self.info_db_frame = InfoDBFrame(self)
        self.info_db_frame.place(relx=0.05, rely=0.05, relwidth=0.25, relheight=0.85)
        self.result_db_frame = ResultDBFrame(self)
        self.result_db_frame.place(relx=0.25, rely=0.05, relwidth=0.7, relheight=0.85)
        ttk.Button(self, text='Save to DB', command=self.save_to_db).place(relx=.35, rely=.9, anchor='c')
        ttk.Button(self, text='Cancel', command=self.delete_wondow).place(relx=.65, rely=.9, anchor='c')
        self.get_result_db_dict()
        # self.format_db_dict()

    def get_result_db_dict(self):
        print(self.file_summary_dict)
        result_db_dict = self.result_db_frame.get_summary_result_db(self.file_summary_dict)
        self.db_dict = {**self.db_dict, **result_db_dict}
        print(self.db_dict)
        return self.db_dict

    def format_db_dict(self):
        all_filename_str = '_'.join(self.file_summary_dict.keys()).lower()
        if 'tap' in all_filename_str:
            self.db_dict['all_max'] = self.db_dict.pop('all_max(mm)')
            self.db_dict['all_mean'] = self.db_dict.pop('all_mean(mm)')
            self.db_dict['withoutedge_max'] = self.db_dict.pop('without_edge_max(mm)')
            self.db_dict['withoutedge_mean'] = self.db_dict.pop('without_edge_mean(mm)')
            self.db_dict['allmax_jitter'] = self.db_dict.pop('all_max_jitter(mm)')
            self.db_dict['jitter_ratio'] = self.db_dict.pop('jitter_ratio(%)')
            self.db_dict['detected_ratio'] = self.db_dict.pop('detected_ratio(%)')

        if 'hori' in all_filename_str:
            self.db_dict['hori_max_lin'] = self.db_dict.pop('hori_max_linearity(mm)')
            self.db_dict['hori_mean_lin'] = self.db_dict.pop('hori_mean_linearity(mm)')
            self.db_dict['hori_max_drag_ratio'] = self.db_dict.pop('hori_max_drag_ratio(%)')
            self.db_dict['hori_min_drag_ratio'] = self.db_dict.pop('hori_min_drag_ratio(%)')
            self.db_dict['hori_break_count'] = self.db_dict.pop('hori_break_line_count')

        if 'vert' in all_filename_str:
            self.db_dict['vert_max_lin'] = self.db_dict.pop('vert_max_linearity(mm)')
            self.db_dict['vert_mean_lin'] = self.db_dict.pop('vert_mean_linearity(mm)')
            self.db_dict['vert_max_drag_ratio'] = self.db_dict.pop('vert_max_drag_ratio(%)')
            self.db_dict['vert_min_drag_ratio'] = self.db_dict.pop('vert_min_drag_ratio(%)')
            self.db_dict['vert_break_count'] = self.db_dict.pop('vert_break_line_count')

        if 'diag' in all_filename_str:
            self.db_dict['diag_max_lin'] = self.db_dict.pop('diag_max_linearity(mm)')
            self.db_dict['diag_mean_lin'] = self.db_dict.pop('diag_mean_linearity(mm)')
            self.db_dict['diag_max_drag_ratio'] = self.db_dict.pop('diag_max_drag_ratio(%)')
            self.db_dict['diag_min_drag_ratio'] = self.db_dict.pop('diag_min_drag_ratio(%)')
            self.db_dict['diag_break_count'] = self.db_dict.pop('diag_break_line_count')
        return self.db_dict

    def check_duplicate_files(self):
        files_arr = self.file_summary_dict.keys()
        files_arr = [filename.lower() for filename in files_arr]

    def save_to_db(self):
        print(self.db_dict)
        if self.db_dict:
            info_db_dict = self.info_db_frame.get_info_db_dict()
            print(info_db_dict)
            self.db_dict = {**self.db_dict, **info_db_dict}
            print('in save to db')
            try:
                self.db_dict = self.format_db_dict()
            except KeyError:
                print('key error')
            finally:
                if self.check_db_dict():
                    if insert_db(self.parent.db_settings_dict, self.db_dict):
                        print('finished inserting to DB')
                        self.parent.destroy()
                        # print('hereeeeee')
                        self.db_dict = {}
                        error_window('Update Finished', 'Finish DB updating!', size='400x150', shift='+1000+700')
                        return True
                    else:
                        error_window('Error During Update', 'Error code:', size='700x200', shift='+1000+700')
                        return False
                else:
                    print('check error')
                    return False
        else:
            error_window('Already Saved', 'Do not Save again!', size='400x150', shift='+1000+700')

    def check_db_dict(self):
        need_dict_key_arr = ['project', 'part_no', 'dut_lv', 'config_file', 'tuning']
        alert_dict_key = []
        def __check_db_dict_each(need_dict_key):
            if not self.db_dict[need_dict_key]:
                print('in check')
                alert_dict_key.append(need_dict_key)
        for _, need_dict_key in enumerate(need_dict_key_arr):
            __check_db_dict_each(need_dict_key)
        if alert_dict_key:
            alert_msg = ', '.join(alert_dict_key)
            error_window('Required Field Not Filled', 'Please fill the blanks:\n'+alert_msg, size='700x200', shift='+1000+700')
            return False
        if not self.db_dict['all_max']:
            error_window('No Tap Result', 'Please add tap result!', size='350x150', shift='+1000+700')
            return False
        return True

    def delete_wondow(self):
        info_db_dict = self.info_db_frame.get_info_db_dict()
        self.parent.parent.info_db_dict = info_db_dict
        self.parent.destroy()

class DBWindow(tk.Toplevel):
    def __init__(self, parent, file_summary_dict, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.file_summary_dict = file_summary_dict
        # print('file_summary_dict' + str(file_summary_dict))
        self.parent = parent
        self.info_db_dict = self.parent.info_db_dict
        self.db_settings_dict = parent.db_settings_dict
        self.db_style = ttk.Style(self)
        # print(self.btn_style.theme_use())
        # self.db_style.configure('.', font=('Arial', 14))
        self.title('Input Data Details')
        self.geometry('2300x900+400+200')
        self.export_db_frame = ExportDBFrame(self)
        self.export_db_frame.place(relx=0, rely=0, relwidth=1, relheight=1)


class AlertDBWindow(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.geometry('700x200+500+400')
        self.title('File Number Alert')
        self.attributes('-toolwindow', 1)
        ttk.Label(self, text='Current tab numbers do not match the standard amount!', font=('Arial', 19)).place(relx=.5, rely=.3, anchor='c')
        ttk.Button(self, text='Continue', command=self.ignore_alert).place(relx=.35, rely=.8, anchor='c')
        ttk.Button(self, text='Add Data', command=self.destroy).place(relx=.65, rely=.8, anchor='c')

    def ignore_alert(self):
        print('ignore')
        DBWindow(self.parent, self.parent.file_summary_dict)
        self.destroy()
