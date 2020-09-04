import pandas as pd
from collections import defaultdict


def get_column_name(filename):
    columns = pd.read_csv(filename, skiprows=1, header=0, index_col=False).columns
    ideal_x = columns[1]
    ideal_y = columns[2]
    reported_x = columns[5]
    reported_y = columns[6]
    offset = columns[7]
    return [ideal_x, ideal_y, reported_x, reported_y, offset]


def get_interval(xy_arr):
    previous_xy = 0
    for current_xy in sorted(set(xy_arr)):
        if abs(current_xy - previous_xy) >= 1:
            return abs(current_xy - previous_xy)


def get_xy_size(ideal_x_arr, ideal_y_arr):
    return min(ideal_x_arr), max(ideal_x_arr), min(ideal_y_arr), max(ideal_y_arr)


def get_ideal_tap_num(ideal_x_arr, ideal_y_arr):
    min_x, max_x, min_y, max_y = get_xy_size(ideal_x_arr, ideal_y_arr)
    x_interval = get_interval(ideal_x_arr)
    y_interval = get_interval(ideal_y_arr)
    x_num = (max_x-min_x)/x_interval + 1
    y_num = (max_y-min_y)/y_interval + 1
    return int(round(x_num * y_num))


def tap_data_process(filename):
    data_df = pd.read_csv(filename, skiprows=1, header=0, index_col=False).divide(1000)
    ideal_x, ideal_y, reported_x, reported_y, offset = get_column_name(filename)
    index_ideal_max_df = data_df.groupby([ideal_x, ideal_y], sort=False)
    index_ideal_max_df = index_ideal_max_df[offset].agg(['mean', 'max']).reset_index()
    x_interval = get_interval(index_ideal_max_df[ideal_x].to_numpy())
    y_interval = get_interval(index_ideal_max_df[ideal_y].to_numpy())
    index_ideal_max_df['x_index'] = index_ideal_max_df[ideal_x].div(x_interval).round(0).astype(int)
    index_ideal_max_df['y_index'] = index_ideal_max_df[ideal_y].div(y_interval).round(0).astype(int)
    ideal_reported_offset_df = data_df.groupby([ideal_x, ideal_y, reported_x, reported_y, offset], sort=False).size().reset_index(name='reported_count')
    dupli_bool = ideal_reported_offset_df.duplicated([ideal_x, ideal_y], keep=False)
    ideal_reported_offset_df['if_jitter'] = dupli_bool
    no_jitter_detail_df = pd.merge(ideal_reported_offset_df, index_ideal_max_df, on=[ideal_x, ideal_y], copy=False)
    # all.to_csv('all.csv', index=False)
    # index_ideal_max_df.to_csv('ideal.csv', index=False)
    # ideal_reported_offset_df.to_csv('reported.csv', index=False)
    return index_ideal_max_df, ideal_reported_offset_df, no_jitter_detail_df

# data_df = pd.read_csv('Tap10x10_20200319153700.csv', skiprows=1, header=0, index_col=False).divide(1000)


def dump_xy_array(filename):
    ideal_reported_offset_df = tap_data_process(filename)[1]
    ideal_x, ideal_y, reported_x, reported_y, offset = get_column_name(filename)
    ideal_x_arr = ideal_reported_offset_df[ideal_x].to_numpy()
    ideal_y_arr = ideal_reported_offset_df[ideal_y].to_numpy()
    reported_x_arr = ideal_reported_offset_df[reported_x].to_numpy()
    reported_y_arr = ideal_reported_offset_df[reported_y].to_numpy()
    offset_arr = ideal_reported_offset_df[offset].to_numpy()
    return ideal_x_arr, ideal_y_arr, reported_x_arr, reported_y_arr, offset_arr


def pair_tap_data(filename):
    ideal_reported_offset_df = tap_data_process(filename)[1]
    ideal_x_arr, ideal_y_arr, reported_x_arr, reported_y_arr, offset_arr = dump_xy_array(filename)
    ideal_reported_dict = defaultdict(list)
    reported_offset_dict = defaultdict(list)
    reported_max_offset_dict = defaultdict(float)
    for index, ideal_xy in enumerate(zip(ideal_x_arr, ideal_y_arr)):
        ideal_reported_dict[ideal_xy[0], ideal_xy[1]].append((reported_x_arr[index], reported_y_arr[index]))
    for index, reported_xy in enumerate(zip(reported_x_arr, reported_y_arr)):
        reported_offset_dict[reported_xy[0], reported_xy[1]].append(offset_arr[index])
    for reported_xy, offset_list in reported_offset_dict.items():
        reported_max_offset_dict[reported_xy] = max(offset_list)
    return ideal_reported_dict, reported_max_offset_dict


def calculate_max_jitter(filename):
    ideal_reported_dict = pair_tap_data(filename)[0]
    ideal_jitter_arr = []
    for ideal_xy, reported_list in ideal_reported_dict.items():
        ideal_x, ideal_y = ideal_xy
        if len(reported_list) == 1:
            ideal_jitter_tup = (ideal_x, ideal_y, 0, 0, 0)
        else:
            x_jitter_arr = [xy[0] for xy in reported_list]
            y_jitter_arr = [xy[1] for xy in reported_list]
            max_x_jitter = abs(max(x_jitter_arr) - min(x_jitter_arr))
            max_y_jitter = abs(max(y_jitter_arr) - min(y_jitter_arr))
            max_jitter = 0
            for i in range(len(reported_list)-1):
                for j in range(i+1, len(reported_list)):
                    cur_jitter = (abs(reported_list[i][0] - reported_list[j][0]) ** 2 + abs(reported_list[i][1] - reported_list[j][1]) ** 2) ** 0.5
                    max_jitter = cur_jitter if cur_jitter > max_jitter else max_jitter
            ideal_jitter_tup = (ideal_x, ideal_y, max_x_jitter, max_y_jitter, max_jitter)
        ideal_jitter_arr.append(ideal_jitter_tup)
    return ideal_jitter_arr


def include_jitter_result(filename):
    ideal_jitter_arr = calculate_max_jitter(filename)
    no_jitter_detail_df = tap_data_process(filename)[2]
    ideal_x, ideal_y, _, _, _ = get_column_name(filename)
    max_jitter_df = pd.DataFrame(ideal_jitter_arr, columns=[ideal_x, ideal_y,
                                                            'point_max_x_jitter', 'point_max_y_jitter', 'point_max_jitter'])
    detail_df = pd.merge(no_jitter_detail_df, max_jitter_df, on=[ideal_x, ideal_y], copy=False)
    return detail_df


def plt_color_mesh_process(filename):
    index_ideal_max_df = tap_data_process(filename)[0]
    ideal_x, ideal_y, _, _, _ = get_column_name(filename)
    ideal_x_arr = index_ideal_max_df[ideal_x].to_numpy()
    ideal_y_arr = index_ideal_max_df[ideal_y].to_numpy()
    x_index_arr = index_ideal_max_df['x_index'].to_numpy()
    y_index_arr = index_ideal_max_df['y_index'].to_numpy()
    max_offset_arr = index_ideal_max_df['max'].to_numpy()
    return ideal_x_arr, ideal_y_arr, x_index_arr, y_index_arr, max_offset_arr
