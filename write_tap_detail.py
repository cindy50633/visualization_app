import pandas as pd

from data_process import get_column_name, include_jitter_result


def set_csv_column_name():
    new_column_names = ['tap_id', 'x_index', 'y_index', 'ideal_x(mm)', 'ideal_y(mm)', 'reported_x(mm)', 'reported_y(mm)',
                        'each_offset(mm)', 'reported_count(times)', 'if_jitter',
                        'point_max_x_jitter(mm)', 'point_max_y_jitter(mm)', 'point_max_jitter(mm)',
                        'point_mean(mm)', 'point_max(mm)']
    return new_column_names


def write_index(filename):
    unorder_detail_df = include_jitter_result(filename)
    id_list = [0]
    x_index_ds = unorder_detail_df['x_index']
    y_index_ds = unorder_detail_df['y_index']

    for i in range(1, len(x_index_ds)):
        if x_index_ds[i] == x_index_ds[i-1] and y_index_ds[i] == y_index_ds[i-1]:
            id_list.append(id_list[i-1])
        else:
            id_list.append(id_list[i-1]+1)

    id_detail_df = unorder_detail_df.assign(tap_id=id_list)
    # id_detail_df = id_detail_df.set_index('id')
    return id_detail_df


def write_tap_detail(filename):
    id_detail_df = write_index(filename)
    ideal_x, ideal_y, reported_x, reported_y, each_offset = get_column_name(filename)
    new_column_order = ['tap_id', 'x_index', 'y_index', ideal_x, ideal_y, reported_x, reported_y,
                        each_offset, 'reported_count', 'if_jitter',
                        'point_max_x_jitter', 'point_max_y_jitter', 'point_max_jitter',
                        'mean', 'max']
    detail_df = id_detail_df[new_column_order]
    column_names = detail_df.columns.values
    column_names[:] = set_csv_column_name()
    float_columns = ['ideal_x(mm)', 'ideal_y(mm)', 'reported_x(mm)', 'reported_y(mm)',
                     'each_offset(mm)', 'point_max_x_jitter(mm)', 'point_max_y_jitter(mm)',
                     'point_max_jitter(mm)', 'point_mean(mm)', 'point_max(mm)']
    detail_df[float_columns] = detail_df[float_columns].applymap('{:.2f}'.format)
    print(detail_df.columns)
    detail_df.set_index('tap_id', inplace=True)
    # print(detail_df)
    # detail_df.to_csv('detail_df.csv')
    return detail_df

# write_tap_detail('Tap5x10_test_jitter.csv').to_csv('test.csv')
