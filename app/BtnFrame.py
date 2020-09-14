import os
import pathlib
import tkinter as tk
from tkinter import ttk
from tkinter import font

from ResultFrame import ResultTab
from SummaryFrame import SummaryFrame
from ExportSettingWindow import SettingsFrame, ExportSettingWindow
from TestSettingWindow import TestSettingsFrame, TestSettingWindow
from DBSettingWindow import DBSettingWindow
from DBWindow import DBWindow, AlertDBWindow
import run

class BtnFrame(tk.Frame):
    def __init__(self, parent, path_frame, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.info_db_dict = {}
        self.script_path = self.parent.script_path
        self.btn_style = ttk.Style(self)
        # print(self.btn_style.theme_use())
        self.btn_style.configure('.', font=('Arial', 16))
        self.path_frame = path_frame
        self.result_tabs = ResultTab(self.parent)
        self.result_tabs.lower(self)
        self.test_btn = self.control_btn('Calculate Result', 0, 0, self.get_result)
        self.test_setting_btn = self.control_btn('...', 0.85, 0, self.test_setting_window, 0.15)
        self.detail_btn = self.control_btn('Show Details', 0, 0.25, self.get_detail)
        self.result_btn = self.control_btn('Export Result', 0, 0.5, self.export_result)
        self.result_setting_btn = self.control_btn('...', 0.85, 0.5, self.export_setting_window, 0.15)
        self.save_db_btn = self.control_btn('Save to DB', 0, 0.75, self.export_db)
        self.db_setting_btn = self.control_btn('...', 0.85, 0.75, self.db_setting_window, 0.15)
        self.initial_btn_state()
        self.export_settings_dict = SettingsFrame.load_settings(self.script_path)
        self.if_tap = tk.IntVar()
        self.if_drag = tk.IntVar()
        self.if_all_files =  tk.IntVar()
        self.if_customize_files = tk.IntVar()
        self.customize_files_num = tk.IntVar()
        self.set_default_test_settings()
        self.file_summary_dict = {}
        # self.test = TestSettingWindow(self)

    def export_setting_window(self):
        return ExportSettingWindow(self)

    def test_setting_window(self):
        return TestSettingWindow(self)

    def db_setting_window(self):
        return DBSettingWindow(self)

    def control_btn(self, btn_label, x_ratio, y_ratio, command_function, x_width=1):
        btn = ttk.Button(self, text=btn_label, command=command_function)
        btn.place(relx=x_ratio, rely=y_ratio, relwidth=x_width, relheight=0.2)
        return btn

    def initial_btn_state(self):
        self.test_btn['state'] = 'active'
        self.detail_btn['state'] = 'disabled'
        self.result_btn['state'] = 'disabled'
        self.result_setting_btn['state'] = 'normal'
        self.save_db_btn['state'] = 'normal'

    def normal_btn_state(self):
        self.detail_btn['state'] = 'normal'
        self.result_btn['state'] = 'normal'
        self.result_setting_btn['state'] = 'normal'
        self.save_db_btn['state'] = 'normal'

    def set_default_test_settings(self):
        self.if_tap.set(1)
        self.if_drag.set(1)
        self.if_all_files.set(0)
        self.if_customize_files.set(1)
        self.customize_files_num.set(7)

    def get_result(self):
        self.info_db_dict = {}
        file_type = '.csv'
        tap_filename = '?'
        horizontal_filename = '?'
        diagonal_filename = '?'
        vertical_filename = '?'
        if self.if_tap.get() == 1:
            tap_filename = 'tap'
        if self.if_drag.get() == 1:
            horizontal_filename = 'hori'
            diagonal_filename = 'diag'
            vertical_filename = 'vert'
        if self.if_all_files.get() == 1:
            self.customize_files_num.set(21)
        found_filename_arr = self.path_frame.check_path_valid(file_type, tap_filename, horizontal_filename, diagonal_filename, vertical_filename, self.customize_files_num.get())
        self.normal_btn_state()
        file_summary_dict, file_summary_df, file_detail_df, file_fig_dict = run.write_result(found_filename_arr)
        self.file_summary_dict = file_summary_dict
        self.result_tabs.set_result(file_summary_dict, file_summary_df, file_detail_df, file_fig_dict)
            # add test result to result_tab in case re-excute the test result
            # BtnFrame's instance variable will be reset if push 'ex'
            # self.result_tabs.set_result(self.file_summary_dict, self.file_summary_df, self.file_detail_df, self.file_fig_dict)
        for filename in file_summary_dict.keys():
            if file_summary_dict[filename]:
                self.result_tabs.add_result(filename, file_summary_dict[filename], file_fig_dict[filename])

    def get_detail(self):
        current_tab = self.result_tabs.get_current_tab_name()
        # print(current_tab)
        file_detail_df = self.result_tabs.get_file_detail_df()
        detail_window = tk.Tk()
        detail_window.geometry('2380x1300')
        ttk.Style(detail_window).configure('Treeview', rowheight=50)
        detail_df = file_detail_df[current_tab]
        columns_arr = [detail_df.index.name] + list(detail_df.columns)
        # id_list = detail_df.index.to_list()
        detail_tree = ttk.Treeview(detail_window, style='Detail.Treeview')
        detail_scroll = ttk.Scrollbar(detail_window, orient=tk.HORIZONTAL, command=detail_tree.xview)
        detail_scroll.place(relx=0, rely=0.95, relwidth=1, relheight=0.02)
        detail_vertical_scroll = ttk.Scrollbar(detail_window, orient=tk.VERTICAL, command=detail_tree.yview)
        detail_vertical_scroll.place(relx=0.98, rely=0, relwidth=0.02, relheight=1)
        detail_tree.place(relx=0, rely=0, relwidth=1, relheight=1)
        detail_tree['columns'] = columns_arr
        for _, column_name in enumerate(columns_arr):
            detail_tree.heading(column_name, text=column_name, anchor='c')
            detail_tree.column(column_name, minwidth=10, width=len(column_name)*17, stretch=False, anchor='c')
        # how to move children?
        # for index in range(len(detail_df.index)-1, -1, -1):
        for index in range(max(detail_df.index), -1, -1):
            # detail_tree.insert('', 0, iid=id_list[index], text=index, values=[id_list[index]]+detail_df.loc[index, :].values.tolist())
            # print(id_list[index])
            # detail_df.to_csv('test.csv')
            values_list = detail_df.loc[index, :].values.tolist()
            if type(values_list[0]) == list:
                n = 0
                # current_values_list = values_list[id_list[index]]
                for _, each_values_list in enumerate(values_list):
                    current_iid = str(index)+'_'+str(n)
                    detail_tree.insert('', 0, iid=current_iid, text=index, values=[index]+each_values_list)
                    # detail_tree.item(current_iid, tags=('red', 'bold'))
                    # print(detail_tree.item(current_iid))
                    n += 1
            else:
                detail_tree.insert('', 0, iid=str(index), text=index, values=[index]+values_list)

        detail_tree['show'] = 'headings'  # supress the identifier
        detail_window.mainloop()

    def export_result(self):
        self.export_settings_dict = SettingsFrame.load_settings(self.script_path)
        tab_arr = self.result_tabs.get_all_tab_names() if self.export_settings_dict['if_all_tabs'] else [self.result_tabs.get_current_tab_name()]
        # print(tab_arr)
        export_path = self.export_settings_dict['export_path']
        for _, tab_name in enumerate(tab_arr):
            if self.export_settings_dict['if_summary']:
                file_summary_df = self.result_tabs.get_file_summary_df()
                summary_df = file_summary_df[tab_name]
                summary_df.to_csv(os.path.join(export_path, tab_name+'_summary.csv'))
            if self.export_settings_dict['if_detail']:
                file_detail_df = self.result_tabs.get_file_detail_df()
                detail_df = file_detail_df[tab_name]
                # print(os.path.join(export_path, tab_name+'_detail.csv'))
                detail_df.to_csv(os.path.join(export_path, tab_name+'_detail.csv'))
            if self.export_settings_dict['if_fig']:
                # print(self.export_settings_dict['if_fig'])
                file_fig_dict = self.result_tabs.get_file_fig_dict()
                fig_dict = file_fig_dict[tab_name]
                # print(file_fig_dict)
                # print(fig_dict)
                for fig, ax in fig_dict.items():
                    print(os.path.join(export_path, tab_name + '_' + ax.get_title() + '.png'))
                    fig.savefig(os.path.join(export_path, tab_name + '_' + ax.get_title() + '.png'))

    def export_db(self):
        self.db_settings_dict = SettingsFrame.load_settings(self.script_path, 'db_settings.pickle')
        if self.db_settings_dict:
            if all(self.db_settings_dict.values()):
                all_tab_names = self.result_tabs.get_all_tab_names()
                self.file_summary_dict = {file:self.file_summary_dict[file] for file in all_tab_names}
                if len(all_tab_names) != 7:
                    AlertDBWindow(self)
                else:
                    DBWindow(self, self.file_summary_dict)
            else:
                DBSettingWindow(self)
        else:
            DBSettingWindow(self)
