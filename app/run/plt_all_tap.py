import matplotlib.pyplot as plt

from data_process import get_xy_size, dump_xy_array
from plt_common_info import plt_common_info

def plt_all_tap(filename, title='all_plot'):
    ideal_x_arr, ideal_y_arr, reported_x_arr, reported_y_arr, _ = dump_xy_array(filename)
    x_min, x_max, y_min, y_max = get_xy_size(ideal_x_arr, ideal_y_arr)
    fig, ax = plt_common_info(filename, title, x_min, x_max, y_min, y_max)
    ax.plot(ideal_x_arr, ideal_y_arr, 'bx', markersize=6)
    ax.plot(reported_x_arr, reported_y_arr, 'r.', markersize=6)
    fig.tight_layout()
    #fig.savefig(filename[:-18] + title + '.png')
    # plt.show()
    return fig, ax

# plt_all_tap('Tap5x10_test_jitter.csv')
