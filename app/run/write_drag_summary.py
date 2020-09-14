import pandas as pd
import numpy as np

from write_drag_detail import write_drag_detail

def write_drag_summary(found_filename):
    drag_detail_df = write_drag_detail(found_filename)
    drag_detail_df = drag_detail_df.astype(float)  # convert items in drag_detail_df back to numeric
    drag_summary_dict = {}
    drag_summary_dict['max_linearity(mm)'] = max(drag_detail_df['max_linearity(mm)'])
    drag_summary_dict['mean_linearity(mm)'] = np.mean(drag_detail_df['mean_linearity(mm)'])
    drag_summary_dict['max_reported_count'] = max(drag_detail_df['reported_count(times)'])
    drag_summary_dict['min_reported_count'] = min(drag_detail_df['reported_count(times)'])
    drag_summary_dict['mean_reported_count'] = np.mean(drag_detail_df['reported_count(times)'])
    drag_summary_dict['max_drag_ratio(%)'] = max(drag_detail_df['drag_ratio(%)'])
    drag_summary_dict['min_drag_ratio(%)'] = min(drag_detail_df['drag_ratio(%)'])
    drag_summary_dict['break_line_count'] = sum(drag_detail_df['break_line_count(times)'])
    drag_float_summary_dict = {key: '{:.2f}'.format(drag_summary_dict[key]) for key in ['mean_linearity(mm)', 'mean_reported_count']}
    drag_int_summary_dict = {key: '{:d}'.format(round(drag_summary_dict[key])) for key in ['max_reported_count', 'min_reported_count', 'break_line_count']}
    drag_summary_dict = {**drag_summary_dict, **drag_float_summary_dict}
    drag_summary_dict = {**drag_summary_dict, **drag_int_summary_dict}
    # print(drag_summary_dict)
    drag_summary_df = pd.DataFrame([drag_summary_dict])
    # drag_summary_df.to_csv('test.csv', index=False)
    return drag_summary_df, drag_summary_dict

# write_drag_summary('Vert100_20200218093113.csv')
