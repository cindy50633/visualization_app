import os
from datetime import datetime

from write_tap_detail import write_tap_detail
from write_tap_summary import write_tap_summary
from write_drag_detail import write_drag_detail
from write_drag_summary import write_drag_summary
from plt_all_tap import plt_all_tap
from plt_color_tap import plt_color_tap
from plt_color_mesh import plt_color_mesh
from plt_drag import plt_drag


def plt_tap(found_filename):
    all_tap, all_tap_ax = plt_all_tap(found_filename)
    color_tap, color_tap_ax = plt_color_tap(found_filename)
    color_mesh, color_mesh_ax = plt_color_mesh(found_filename)
    # print('plt result finished')
    return {all_tap: all_tap_ax, color_tap: color_tap_ax, color_mesh: color_mesh_ax}


def write_result(found_filename_arr):
    file_summary_dict = {}
    file_summary_df = {}
    file_detail_df = {}
    file_fig_dict = {}
    def __write_result_process(found_filename, basename):
        if 'tap' in basename.lower():
            # print('in __write_result_process')
            summary_df, summary_dict = write_tap_summary(found_filename)
            detail_df = write_tap_detail(found_filename)
            file_fig_dict[basename] = plt_tap(found_filename)
        else:
            summary_df, summary_dict = write_drag_summary(found_filename)
            detail_df = write_drag_detail(found_filename)
            file_fig_dict[basename] = plt_drag(found_filename)
        file_summary_dict[basename] = summary_dict
        file_summary_df[basename] = summary_df
        file_detail_df[basename] = detail_df
    # try:
    for found_filename in found_filename_arr:
        basename, _ = os.path.basename(found_filename).split('.')
        __write_result_process(found_filename, basename)
# except Exception as error:
        # return type(error).__name__
    # finally:
    print('output result finished')
    # print(file_summary_dict)
    return file_summary_dict, file_summary_df, file_detail_df, file_fig_dict
