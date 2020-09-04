import pandas as pd

from data_process_drag import get_column_name, drag_ratio_process, drag_regression_process

def write_drag_detail(filename):
    ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end, _, _, _, _ = get_column_name(filename)
    regression_process_df = drag_regression_process(filename)
    temp_regression_df1 = pd.pivot_table(regression_process_df, index=[ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end], values=['reported_count'])
    temp_regression_df2 = pd.pivot_table(regression_process_df, index=[ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end], values=['regression_offset'], aggfunc=['max', 'mean'])
    regression_detail_df = pd.concat([temp_regression_df1, temp_regression_df2], axis=1)  # meaning of axis=1?
    drag_ratio_df = drag_ratio_process(filename)
    drag_detail_df = pd.merge(regression_detail_df, drag_ratio_df, on=[ideal_x_start, ideal_y_start, ideal_x_end, ideal_y_end], copy=False)
    drag_detail_df.reset_index(inplace=True, drop=True)
    drag_detail_df.columns = ['x_start(mm)', 'y_start(mm)', 'x_end(mm)', 'y_end(mm)', 'reported_count(times)', 'max_linearity(mm)', 'mean_linearity(mm)', 'ideal_length(mm)', 'reported_length(mm)', 'break_line_count(times)', 'drag_ratio(%)']
    float_columns = ['x_start(mm)', 'y_start(mm)', 'x_end(mm)', 'y_end(mm)', 'max_linearity(mm)', 'mean_linearity(mm)', 'ideal_length(mm)', 'reported_length(mm)', 'drag_ratio(%)']
    drag_detail_df[float_columns] = drag_detail_df[float_columns].applymap('{:,.2f}'.format)
    # drag_detail_df = drag_detail_df.astype(float).round(2)
    drag_detail_df.index.name = 'line_id'
    # drag_detail_df.to_csv('test.csv')
    # drag_detail_df.to_csv('test.csv')
    return drag_detail_df

# write_drag_detail('Hori100_20200409151316.csv')
