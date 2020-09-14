from matplotlib import pyplot as plt
from collections import defaultdict

from data_process import get_xy_size, pair_tap_data, dump_xy_array
from plt_common_info import plt_common_info


def color_assign(filename):
    reported_max_offset_dict = pair_tap_data(filename)[1]
    color_dict = defaultdict(tuple)
    color_range_dict = {(float('-inf'), 0.5): (0.000, 0.000, 0.502), # Navy
                        (0.5, 1.0):           (0.000, 0.000, 1.000), # Blue
                        (1.0, 1.5):           (0.255, 0.412, 0.882), # Royal Blue
                        (1.5, 2.0):           (0.498, 1.000, 0.831), # Aquamarine
                        (2.0, 2.5):           (0.678, 1.000, 0.184), # Green Yellow
                        (2.5, 3.0):           (1.000, 1.000, 0.000), # Yellow
                        (3.0, 3.5):           (1.000, 0.647, 0.000), # Orange
                        (3.5, 4.0):           (1.000, 0.000, 0.000), # Red
                        (4.0, float('inf')):  (0.647, 0.165, 0.165)  # Brown
                        }
    for reported_xy, max_offset in reported_max_offset_dict.items():
        for offset_range, rgb_tuple in color_range_dict.items():
            if offset_range[0] < max_offset <= offset_range[1]:
                color_dict[reported_xy] = rgb_tuple
    return color_range_dict, color_dict


def plt_color_tap(filename, title='max_color_tap'):
    ideal_x_arr, ideal_y_arr, _, _, _ = dump_xy_array(filename)
    x_min, x_max, y_min, y_max = get_xy_size(ideal_x_arr, ideal_y_arr)
    fig, ax = plt_common_info(filename, title, x_min, x_max, y_min, y_max)
    ideal_reported_dict, reported_max_offset_dict = pair_tap_data(filename)
    color_range_dict, reported_color_dict = color_assign(filename)
    for ideal_xy, reported_xy_arr in ideal_reported_dict.items():
        ax.plot(ideal_xy[0], ideal_xy[1], 'x', markersize=6, color='r')
        for _, reported_xy in enumerate(reported_xy_arr):
            if reported_max_offset_dict.get(reported_xy) is not None:
                # print('QQQQQ')
                # print(reported_max_offset_dict)
                ax.plot(reported_xy[0], reported_xy[1], 'o', markersize=6, color=reported_color_dict[reported_xy])

    color_range_arr = ['0.0 - 0.5', '0.5 - 1.0', '1.0 - 1.5', '1.5 - 2.0',
                       '2.0 - 2.5', '2.5 - 3.0', '3.0 - 3.5', '3.5 - 4.0',
                       '>= 4.0']
    color_rgb_arr = color_range_dict.values()
    accuracy_markers = [plt.Line2D([0,0], [0,0], color=color_rgb, marker='o',
                      linestyle='', markersize=7) for color_rgb in color_rgb_arr]
    accuracy_legend = plt.legend(accuracy_markers, color_range_arr, numpoints=1,
                              loc='upper left', bbox_to_anchor=(1.013,0.6),
                              title='Accuracy(mm)', prop={'size': 7})
    ax.add_artist(accuracy_legend)
    fig.tight_layout()
    # fig.savefig(filename[:-18] + title + '.png')
    # plt.show()
    return fig, ax
