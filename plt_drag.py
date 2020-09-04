from matplotlib import pyplot as plt

from plt_common_info import plt_common_info
from data_process_drag import get_column_name, get_xy_size, dump_drag_xy_array


def get_regression_pair(ideal_pair, coeff_a, coeff_b):
    def __get_regression_value(ideal, coeff_a=coeff_a, coeff_b=coeff_b):
        return coeff_a + coeff_b*ideal
    return [__get_regression_value(ideal_pair[0]), __get_regression_value(ideal_pair[1])]


def plt_drag(filename):
    if 'vert' in filename.lower():
        title = 'Vertical'
    elif 'diag' in filename.lower():
        title = 'Diagonal'
    else:
        title = 'Horizontal'
    title = title + '_' + filename[4:7] + 'mm_s'
    reported_x_arr, reported_y_arr, regression_plt_dict = dump_drag_xy_array(filename)
    ideal_x_start, ideal_y_start, ideal_y_end, ideal_y_end, reported_x, reported_y, _, if_break_line = get_column_name(filename)
    x_min, x_max, y_min, y_max = get_xy_size(reported_x_arr, reported_y_arr)
    fig, ax = plt_common_info(filename, title, x_min, x_max, y_min, y_max)
    for key, regression_plt_df in regression_plt_dict.items():
        regression_plt_df.to_csv('test.csv')
        # plot ideal by regression coefficient
        if 'Vertical' not in title:
            ideal_x_pair = [key[0], key[2]]
            coeff_a = regression_plt_df.iloc[0]['coeff_a']
            coeff_b = regression_plt_df.iloc[0]['coeff_b']
            ax.plot(ideal_x_pair, get_regression_pair(ideal_x_pair, coeff_a, coeff_b), 'b', markersize=4, linewidth=3)
        else:
            ideal_y_pair = [key[1], key[3]]
            coeff_a = regression_plt_df.iloc[0]['ver_coeff_a']
            coeff_b = regression_plt_df.iloc[0]['ver_coeff_b']
            ax.plot(get_regression_pair(ideal_y_pair, coeff_a, coeff_b), ideal_y_pair, 'b', markersize=4, linewidth=3)
        # plot reported
        # ax.plot(regression_plt_df[reported_x], regression_plt_df[reported_y], 'r.', markersize=4)

        # plot reported
        all_reported_x_arr = []
        all_reported_y_arr = []
        reported_x_arr = []
        reported_y_arr = []
        for i, _ in enumerate(regression_plt_df[reported_x]):
            current_x = regression_plt_df[reported_x].iloc[i]
            current_y = regression_plt_df[reported_y].iloc[i]
            reported_x_arr.append(current_x)
            reported_y_arr.append(current_y)
            if regression_plt_df[if_break_line].iloc[i] == 1:
                highlight_circle = plt.Circle((current_x, current_y), x_max/55, color='y', fill=False)
                ax.add_artist(highlight_circle)
                all_reported_x_arr.append(reported_x_arr)
                all_reported_y_arr.append(reported_y_arr)
                reported_x_arr = []
                reported_y_arr = []
        all_reported_x_arr.append(reported_x_arr)
        all_reported_y_arr.append(reported_y_arr)
        for i, _ in enumerate(all_reported_x_arr):
            ax.plot(all_reported_x_arr[i], all_reported_y_arr[i], 'r.', markersize=4)
            ax.plot(all_reported_x_arr[i], all_reported_y_arr[i], 'r', markersize=4, linewidth=3)
        print(all_reported_x_arr)
            # if regression_plt_df[if_break_line]
            # ax.plot(regression_plt_df[reported_x], regression_plt_df[reported_y], 'r.', markersize=4)
    fig.tight_layout()
    #fig.savefig(filename[:-18] + title + '.png')
    # plt.show()
    return {fig: ax}

# plt_drag('Hori100_break.csv')
# plt_drag('Hori100_20200409151316.csv')
# plt_drag('Hori100_20200409151316.csv')
