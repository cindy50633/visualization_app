import pandas as pd
import numpy as np
from collections import defaultdict
from matplotlib import pyplot as plt


def get_column_name(filename):
    columns = pd.read_csv(filename, skiprows=1, header=0, index_col=False).columns
    ideal_x_start = columns[1]
    ideal_y_start = columns[2]
    ideal_x_end = columns[3]
    ideal_y_end = columns[4]
    reported_x = columns[5]
    reported_y = columns[6]
    offset = columns[7]
    if_break_line = columns[8]
    return [ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end,
            reported_x, reported_y, offset, if_break_line]


def get_interval(xy_arr):
    previous_xy = 0
    for current_xy in sorted(set(xy_arr)):
        if abs(current_xy - previous_xy) >= 1:
            return abs(current_xy - previous_xy)


def get_xy_size(ideal_x_arr, ideal_y_arr):
    return min(ideal_x_arr), max(ideal_x_arr), min(ideal_y_arr), max(ideal_y_arr)


def drag_ratio_process(filename):
    data_df = pd.read_csv(filename, skiprows=1, header=0, index_col=False).divide(1000)
    ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end, reported_x, reported_y, _, if_break_line = get_column_name(filename)
    drag_ratio_df = data_df.iloc[:,1:9]
    drag_ratio_df[if_break_line] = np.where(drag_ratio_df[if_break_line]==0.001, 1, 0)
    drag_ratio_df['ideal_length'] = ((drag_ratio_df[ideal_x_end]-drag_ratio_df[ideal_x_start])**2 + (drag_ratio_df[ideal_y_end]-drag_ratio_df[ideal_y_start])**2) ** 0.5
    drag_ratio_df['xy_diff'] = (drag_ratio_df[reported_x].diff()**2 + drag_ratio_df[reported_y].diff()**2) ** 0.5
    drag_ratio_df['xy_diff'] = np.where(drag_ratio_df[if_break_line].shift()==False, drag_ratio_df['xy_diff'], np.NaN)
    drag_ratio_df.loc[drag_ratio_df.groupby([ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end], sort=False).head(1).index, 'xy_diff'] = np.NaN
    temp_ratio_df1 = pd.pivot_table(drag_ratio_df, index=[ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end, 'ideal_length'], values=['xy_diff'], aggfunc=np.sum).rename(columns={'xy_diff': 'reported_length'})
    temp_ratio_df2 = pd.pivot_table(drag_ratio_df, index=[ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end, 'ideal_length'], values=[if_break_line], aggfunc=np.sum).rename(columns={if_break_line: 'break_line_count'})
    drag_ratio_df = pd.concat([temp_ratio_df1, temp_ratio_df2], axis=1)  # meaning of axis=1?
    drag_ratio_df.reset_index(inplace=True)
    print(drag_ratio_df.columns)
    drag_ratio_df['drag_ratio'] = drag_ratio_df['reported_length'] / drag_ratio_df['ideal_length'] * 100
    # drag_ratio_df.to_csv('test.csv')
    return drag_ratio_df


def drag_regression_coeff_process(filename, data_df):
    # data_df = pd.read_csv(filename, skiprows=1, header=0, index_col=False).divide(1000)
    ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end, reported_x, reported_y, _, _ = get_column_name(filename)
    # ideal_reported_df1= ideal_reported_df[reported_x].agg(['sum'])
    data_df['reported_x_sqrt'] = data_df[reported_x] ** 2
    data_df['reported_y_sqrt'] = data_df[reported_y] ** 2
    data_df['reported_x*y'] = data_df[reported_x] * data_df[reported_y]
    ideal_reported_df = data_df.groupby([ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end], sort=False)
    temp_data_df1 = pd.pivot_table(data_df, index=[ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end], values=[reported_x, reported_y, 'reported_x_sqrt', 'reported_y_sqrt', 'reported_x*y'], aggfunc=np.sum)
    temp_data_df2 = pd.pivot_table(data_df, index=[ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end], values=[reported_x, reported_y], aggfunc='size').rename('reported_count')
    ideal_reported_df = pd.concat([temp_data_df1, temp_data_df2], axis=1)
    x_sum = ideal_reported_df[reported_x]
    y_sum = ideal_reported_df[reported_y]
    xy_sum = ideal_reported_df['reported_x*y']
    x_sum_sqrt = ideal_reported_df[reported_x] ** 2
    y_sum_sqrt = ideal_reported_df[reported_y] ** 2
    x_sqrt_sum = ideal_reported_df['reported_x_sqrt']
    y_sqrt_sum = ideal_reported_df['reported_y_sqrt']
    n = ideal_reported_df['reported_count']
    denominator = n*x_sqrt_sum - x_sum**2
    ver_denominator = n*y_sqrt_sum - y_sum**2
    ideal_reported_df['coeff_a'] = (y_sum*x_sqrt_sum - x_sum*xy_sum) / denominator
    ideal_reported_df['coeff_b'] = (n*xy_sum - x_sum*y_sum) / denominator
    ideal_reported_df['ver_coeff_a'] = (x_sum*y_sqrt_sum - y_sum*xy_sum) / ver_denominator
    ideal_reported_df['ver_coeff_b'] = (n*xy_sum - x_sum*y_sum) / ver_denominator
    regression_coeff_df = pd.merge(data_df.iloc[:,1:9], ideal_reported_df[['coeff_a', 'coeff_b', 'ver_coeff_a', 'ver_coeff_b', 'reported_count']], on=[ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end], copy=False)
    return regression_coeff_df


def drag_regression_process(filename):
    data_df = pd.read_csv(filename, skiprows=1, header=0, index_col=False).divide(1000)
    _, _, _, _, reported_x, reported_y, _, if_break_line = get_column_name(filename)
    regression_process_df = drag_regression_coeff_process(filename, data_df)
    regression_process_df[if_break_line] = np.where(regression_process_df[if_break_line]==0.001, 1, 0)
    if 'ver' not in filename.lower():
        regression_process_df['regression_y'] = regression_process_df['coeff_a'] + regression_process_df['coeff_b'] * regression_process_df[reported_x]
        regression_process_df['regression_offset'] = abs(regression_process_df['regression_y'] - regression_process_df[reported_y])
        # regression_process_df.to_csv('test.csv')
    else:
        regression_process_df['regression_x'] = regression_process_df['ver_coeff_a'] + regression_process_df['ver_coeff_b'] * regression_process_df[reported_y]
        regression_process_df['regression_offset'] = abs(regression_process_df['regression_x'] - regression_process_df[reported_x])
    return regression_process_df


def dump_drag_xy_array(filename):
    regression_process_df = drag_regression_process(filename)
    ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end, reported_x, reported_y, _, if_break_line = get_column_name(filename)
    print(regression_process_df.columns)
    reported_x_arr = regression_process_df[reported_x].to_numpy()
    reported_y_arr = regression_process_df[reported_y].to_numpy()
    regression_plt_df = regression_process_df[[ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end, reported_x, reported_y, if_break_line, 'coeff_a', 'coeff_b', 'ver_coeff_a', 'ver_coeff_b']]
    regression_plt_dict = dict(list(regression_plt_df.groupby([ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end])))
    print(regression_plt_dict)
    # print(regression_plt_dict)
    # regression_process_df.to_csv('test2.csv')
    return reported_x_arr, reported_y_arr, regression_plt_dict


def get_distance(previous_x, previous_y, current_x, current_y):
    return ((current_x-previous_x)**2 + (current_y-previous_y)**2) ** 0.5



# drag_ratio_process('Hori100_20200409151316.csv')
# drag_ratio_process('Vert100_break.csv')
# drag_ratio_process('Vert100_20200218093113.csv')
