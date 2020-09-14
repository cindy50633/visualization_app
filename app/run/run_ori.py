import os
from datetime import datetime

from write_tap_detail import write_tap_detail
from write_tap_summary import write_tap_summary
from plt_all_tap import plt_all_tap
from plt_color_tap import plt_color_tap
from plt_color_mesh import plt_color_mesh
from data_process_drag import plt_drag


def plt_tap(found_filename):
    all_tap, all_tap_ax = plt_all_tap(found_filename)
    color_tap, color_tap_ax = plt_color_tap(found_filename)
    color_mesh, color_mesh_ax = plt_color_mesh(found_filename)
    # print('plt result finished')
    return {all_tap: all_tap_ax, color_tap: color_tap_ax, color_mesh: color_mesh_ax}


def write_result(found_filename_arr, if_check_name=True):
    file_summary_dict = {}
    file_summary_df = {}
    file_detail_df = {}
    file_fig_dict = {}
    def write_result_process(found_filename, name, file_summary_dict, file_summary_df, file_detail_df):
        # print('in write_result_process')
        summary_df, summary_dict = write_tap_summary(found_filename)
        detail_df = write_tap_detail(found_filename)
        file_summary_dict[name] = summary_dict
        file_summary_df[name] = summary_df
        file_detail_df[name] = detail_df
    # try:
    for found_filename in found_filename_arr:
        name, _ = os.path.basename(found_filename).split('.')
        # print(found_filename_arr)
        if if_check_name:
            if str.isdigit(name[-14:]):
                # print(name)
                write_result_process(found_filename, name, file_summary_dict, file_summary_df, file_detail_df)
                file_fig_dict[name] = plt_tap(found_filename)
            else:
                file_summary_dict[name] = None
                file_summary_df[name] = None
                file_detail_df[name] = None
                file_fig_dict[name] = None
        else:
            # print(found_filename)
            write_result_process(found_filename, name, file_summary_dict, file_summary_df, file_detail_df)
            file_fig_dict[name] = plt_tap(found_filename)
    # except Exception as error:
        # return type(error).__name__
    # finally:
    print('output result finished')
    # print(file_summary_dict)
    return file_summary_dict, file_summary_df, file_detail_df, file_fig_dict
