from matplotlib import pyplot as plt

def plt_common_info(filename, title, x_min, x_max, y_min, y_max):
    fig, ax = plt.subplots(figsize=(8,6))
    # fig = Figure()
    # ax = fig.add_subplot(111)
    # plt.gcf().set_size_inches(20, 12)
    fig.canvas.set_window_title(title)
    ax.set_title(title)
    ax.set_xlabel('Width(mm)')
    ax.set_ylabel('Length(mm)')
    ax.set_xlim(x_min-20, x_max+20)
    ax.set_ylim(y_min-20, y_max+20)
    ax.invert_yaxis()
    ideal_cross, = ax.plot([], [], color='b', label='ideal',
                            marker='x', linewidth='0', markersize=7)
    reported_circle, = ax.plot([], [], color='r', label='reported',
                       marker='.', linewidth='0', markersize=7)
    common_legend = plt.legend(handles=[ideal_cross, reported_circle],
               loc=4, bbox_to_anchor=(1.15,0.1), prop={'size': 7})
    ax.add_artist(common_legend)
    # plt.savefig(filename[:-18] + title + '.png')
    # plt.close()
    return fig, ax
