import pandas as pd
import numpy as np

from data_process import get_ideal_tap_num
from write_tap_detail import write_tap_detail

def get_edge_max(detail_df):
    min_x_index = min(detail_df['x_index'])
    max_x_index = max(detail_df['x_index'])
    min_y_index = min(detail_df['y_index'])
    max_y_index = max(detail_df['y_index'])
    x_index_bool = detail_df['x_index'].isin([min_x_index, max_x_index])
    y_index_bool = detail_df['y_index'].isin([min_y_index, max_y_index])
    edge_detail_df = detail_df.loc[x_index_bool | y_index_bool]
    without_edge_detail_df =  detail_df.loc[~(x_index_bool | y_index_bool)]
    edge_max = max(edge_detail_df['point_max(mm)'])
    without_edge_max = max(without_edge_detail_df['point_max(mm)'])
    edge_mean = np.mean(edge_detail_df['point_mean(mm)'])
    without_edge_mean = np.mean(without_edge_detail_df['point_mean(mm)'])
    # print(without_edge_detail_df)
    return edge_max, without_edge_max, edge_mean, without_edge_mean


def write_tap_summary(filename):
    detail_df = write_tap_detail(filename)
    detail_df = detail_df.astype(float)  # convert items in drag_detail_df back to numeric
    edge_max, without_edge_max, edge_mean, without_edge_mean = get_edge_max(detail_df)
    summary_dict = {}
    summary_dict['all_max(mm)'] = max(detail_df['point_max(mm)'])
    summary_dict['edge_max(mm)'] = edge_max
    summary_dict['without_edge_max(mm)'] = without_edge_max
    summary_dict['all_mean(mm)'] = np.mean(detail_df['point_mean(mm)'])
    summary_dict['edge_mean(mm)'] = edge_mean
    summary_dict['without_edge_mean(mm)'] = without_edge_mean
    summary_dict['all_max_x_jitter(mm)'] = max(detail_df['point_max_x_jitter(mm)'])
    summary_dict['all_max_y_jitter(mm)'] = max(detail_df['point_max_y_jitter(mm)'])
    summary_dict['all_max_jitter(mm)'] = max(detail_df['point_max_jitter(mm)'])
    is_jitter_bool = detail_df['if_jitter']==True
    jitter_num = len(set(detail_df[is_jitter_bool].index))
    detected_num = len(set(detail_df.index))
    ideal_num = get_ideal_tap_num(detail_df['ideal_x(mm)'], detail_df['ideal_y(mm)'])
    summary_dict['jitter_ratio(%)'] = jitter_num / ideal_num * 100
    summary_dict['detected_ratio(%)'] = detected_num / ideal_num * 100
    summary_dict = {key: '{:.2f}'.format(value) for key, value in summary_dict.items()}
    # print(summary_dict)
    summary_df = pd.DataFrame([summary_dict])
    # summary_df.to_csv('summary_df.csv', index=False)
    return summary_df, summary_dict

# write_tap_summary('Tap5x10_20200326135225.csv')
# get_edge_max(df)
